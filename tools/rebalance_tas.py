import os, sys, json
from project_summary import Snapshot
from collections import defaultdict


def get_work(buckets, weights, key):
    return len(buckets[key]) / weights.get(key, 1e-9)


def rebalance(buckets, weights):
    keys = set(buckets.keys()) | set(weights.keys())
    most = None
    least = None
    while True:
        for k in keys:
            work = get_work(buckets, weights, k)
            if most == None or work > get_work(buckets, weights, most):
                most = k
            if least == None or work < get_work(buckets, weights, least):
                least = k
        buckets[least].add(buckets[most].pop())
        if get_work(buckets, weights, least) > get_work(buckets, weights, most):
            break
    for k in keys:
        print(k, len(buckets[k]))


def main():
    if len(sys.argv) < 3:
        print('Usage: python project_summary.py <snap-dir> <project_id>')
        sys.exit(1)
    snap_dir = sys.argv[1]
    proj_id = sys.argv[2]
    snap = Snapshot(snap_dir)

    ta_to_submitters = defaultdict(set)
    ta_to_others = defaultdict(set)

    # see who has submitted
    print("Students:", len(snap.roster))
    for row in snap.roster:
        if not row.get("enrolled", False) or not "net_id" in row:
            continue
        net_id = row["net_id"]
        submission = snap.project_submission(proj_id, net_id)
        if submission != None:
            ta_to_submitters[row.get("ta", "none")].add(net_id)
        else:
            ta_to_others[row.get("ta", "none")].add(net_id)

    weights = {"Bob":3, "Mitali":3, "Om":3, "Shruthi":3, "Ushmal":2,
               "Ashay":3, "Chakshu":3, "Deepan":3, "Hugh":3, "Zhanpeng":3}

    # decide who is doing what, according to their weight
    # (try to keep ta->student pairings)
    rebalance(ta_to_submitters, weights)
    rebalance(ta_to_others, weights)

    # read and index old roster
    with open(snap_dir + '/users/roster.json') as f:
        roster = json.loads(f.read())
    rosterd = {}
    for row in roster:
        assert('net_id' in row)
        rosterd[row['net_id']] = row

    # update roster
    for mapping in [ta_to_submitters, ta_to_others]:
        for ta in mapping:
            for net_id in mapping[ta]:
                rosterd[net_id]["ta"] = ta

    with open('roster-balanced.json', 'w') as f:
        json.dump(roster, f, indent=2, sort_keys=True)
                
if __name__ == '__main__':
     main()
