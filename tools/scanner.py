import os, sys, json, getpass, re, datetime, time, subprocess
from collections import defaultdict

BUCKET = 'tharter-exams'
SCANNER_DIR = "scanner_batch"
EXAMS = ['exam1', 'exam2', 'final']

def yell(line):
    line2 = "!!  " + " " * len(line) + "  !!"
    line = "!!  " + line.upper() + "  !!"
    print("\n")
    print("!" * len(line))
    print("!" * len(line))
    print(line2)
    print(line)
    print(line2)
    print("!" * len(line))
    print("!" * len(line))
    print()

def read_json(path):
    with open(path) as f:
        return json.load(f)

def upload():
    # import here so that app works even if boto3 isn't installed
    import boto3
    from botocore.exceptions import EndpointConnectionError
    s3 = boto3.Session(**read_json("scanner.cred")).client("s3")

    def upload_batch():
        while True:
            paths = [os.path.join(SCANNER_DIR, p)
                     for p in os.listdir(SCANNER_DIR)
                     if p.endswith(".json")]
            if len(paths) == 0:
                return

            if len(paths):
                paths.sort()
                row = read_json(paths[0])
                path = [str(row.get(k, "unknown")) for k in ["session", "location", "timestamp"]]
                path = "/".join(path) + ".json"
                s3.put_object(Bucket=BUCKET,
                                  Key=path,
                                  Body=bytes(json.dumps(row), 'utf-8'),
                                  ContentType='text/json')
                os.remove(paths[0])

    try:
        while True:
            try:
                upload_batch()
                time.sleep(3)
            except EndpointConnectionError:
                print("\nnetwork issue, cannot upload logs now\n")
                sys.stdout.flush()
                time.sleep(3)
    except (KeyboardInterrupt, SystemExit):
        print("\ntry uploading last batch\n")
        try:
            upload_batch()
        except EndpointConnectionError:
            # TODO: why doesn't this always print?
            yell("network issue, cannot upload logs now")
            print("Please re-open scanner.py when you have network access to upload local records.")
        sys.stdout.flush()


def scanner(exam, direction):
    session = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    ta = getpass.getuser()

    # parse roster
    if not os.path.exists("roster.json"):
        print("Need a roster.json in this directory")
        return

    with open("roster.json", encoding="utf-8") as f:
        roster = json.load(f)

    # KEY: net IDs and campus IDs, VAL: venue
    student_lookup = {row["campus_id"]: row.get(exam, None)
                      for row in roster
                      if "campus_id" in row and row.get("enrolled", False)}
    student_lookup.update({row["net_id"]: row.get(exam, None)
                           for row in roster
                           if "campus_id" in row and row.get("enrolled", False)})

    # we'll flag it if a student is not at same location as most others being checked in here
    counts = defaultdict(int)
    while True:
        who = input("Swipe (or type Campus ID or NetID): ").strip()
        m = re.match('s(\d{10})\dZ', who)
        if m == None:
            m = re.match('\;(\d{10})\d\?', who)
        if m:
            who = m.group(1)
        if who in student_lookup:
            location = student_lookup[who]
            if location != None:
                # set of where most students have signed in
                # (will be length 1 unless there is a tie)
                if len(counts) > 0:
                    most_common = {k for k in counts if counts[k] == max(counts.values())}
                    if not location in most_common:
                        yell("student should be at " + location + " (are they?)")
                counts[location] += 1
            else:
                yell("student on roster, but at unspecified location")
                location = "unknown"
        else:
            yell("student not on roster")
            location = "unknown"

        print("<{}> scans <{}> <{}> at exam <{}>".format(ta, who, direction, location))
        timestamp = time.time()
        record = {
            "session": session,
            "ta": ta, "who": who, "direction": direction,
            "location": location, "timestamp": timestamp
        }
        with open(os.path.join(SCANNER_DIR, str(time.time())+".json"), "w") as f:
            json.dump(record, f)


def main():
    # PROCESS 1: uploader
    if len(sys.argv) > 1 and sys.argv[1] == "upload":
        upload()
        return

    # PROCESS 2: scanner
    if len(sys.argv) != 3 or sys.argv[1] not in EXAMS or sys.argv[2] not in ("in", "out"):
        print("Usage: python3 scanner.py [%s] [in|out]" % "|".join(EXAMS))
        return

    exam, direction = sys.argv[1:]

    # attempt to spin up uploader as separate process
    if not os.path.exists(SCANNER_DIR):
        os.mkdir(SCANNER_DIR)
    argv = [sys.executable, sys.argv[0], "upload"]
    print(" ".join(argv))
    uploader_proc = subprocess.Popen(argv, stdout=sys.stdout)
    try:
        print("exit with ctrl-c")
        scanner(exam, direction)
    except KeyboardInterrupt:
        uploader_proc.kill()
        uploader_proc.wait()
        print("exiting...")


if __name__ == '__main__':
    main()
