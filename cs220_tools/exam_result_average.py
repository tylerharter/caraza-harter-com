import os
import sys
import csv

################################################################################
# Copy-paste wisc email, section, exam score columns from canvas into a new file
# called "only_exam_score.csv"
# "only_exam_score.csv" should not have any header
################################################################################

# copied from https://automatetheboringstuff.com/2e/chapter16/
def process_csv(filename):
    exampleFile = open(filename, encoding="utf-8")
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    exampleFile.close()
    return exampleData

def median(some_items):
    """
    Returns median of a list passed as argument
    """
    some_items.sort()
    n = len(some_items)

    if n % 2 == 1:
        return some_items[n // 2]
    else:
        first_middle = some_items[n//2 - 1]
        second_middle = some_items[n // 2]
        median = (first_middle + second_middle) / 2
        return median

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 {} <canvas csv file, ex: only_exam_scores.csv>".format(sys.argv[0]))
        sys.exit(0)

    averages = {
                "LEC001": {},
                "LEC002": {},
                "LEC003": {},
                "LEC004": {},
                #"LEC005": {}
                }

    canvas_data = process_csv(sys.argv[1])

    for row in canvas_data:
        lecture = row[1]
        if row[2].strip() == '':
            row[2] = '0'
        score = int(row[2])
        if score == 0:
            print(row)
        if "LEC001" in lecture:
            if "count" not in averages["LEC001"]:    
                averages["LEC001"]["count"] = 1
                averages["LEC001"]["total"] = score
                averages["LEC001"]["scores"] = [score]
            else:
                averages["LEC001"]["count"] += 1
                averages["LEC001"]["total"] += score
                averages["LEC001"]["scores"].append(score)
        if "LEC002" in lecture:
            if "count" not in averages["LEC002"]:    
                averages["LEC002"]["count"] = 1
                averages["LEC002"]["total"] = score
                averages["LEC002"]["scores"] = [score]
            else:
                averages["LEC002"]["count"] += 1
                averages["LEC002"]["total"] += score
                averages["LEC002"]["scores"].append(score)
        if "LEC003" in lecture:
            if "count" not in averages["LEC003"]:    
                averages["LEC003"]["count"] = 1
                averages["LEC003"]["total"] = score
                averages["LEC003"]["scores"] = [score]
            else:
                averages["LEC003"]["count"] += 1
                averages["LEC003"]["total"] += score
                averages["LEC003"]["scores"].append(score)
        if "LEC004" in lecture:
            if "count" not in averages["LEC004"]:    
                averages["LEC004"]["count"] = 1
                averages["LEC004"]["total"] = score
                averages["LEC004"]["scores"] = [score]
            else:
                averages["LEC004"]["count"] += 1
                averages["LEC004"]["total"] += score
                averages["LEC004"]["scores"].append(score)
        if "LEC005" in lecture:
            if "count" not in averages["LEC005"]:    
                averages["LEC005"]["count"] = 1
                averages["LEC005"]["total"] = score
                averages["LEC005"]["scores"] = [score]
            else:
                averages["LEC005"]["count"] += 1
                averages["LEC005"]["total"] += score
                averages["LEC005"]["scores"].append(score)

    total = 0
    count = 0
    all_scores = []

    for section in averages:
        section_avg = averages[section]["total"] / averages[section]["count"]
        total += averages[section]["total"]
        count += averages[section]["count"]
        print("Average for {}: {} ({}%)".format(section, str(round(section_avg, 2)), str(round(section_avg / 35 * 100, 2))))
        print("Median for {}: {}".format(section, str(median(averages[section]["scores"]))))

        all_scores += averages[section]["scores"]

    avg_overall = total / count
    print("Overall average is: {} ({}%)".format(str(round(avg_overall, 2)), str(round(avg_overall / 35 * 100, 2))))
    print("Overall median is: {}".format(str(median(all_scores))))

if __name__ == "__main__":
    main()
