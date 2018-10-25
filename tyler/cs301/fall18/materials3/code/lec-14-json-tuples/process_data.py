import csv


def read_csv(csv_file):
    # Copied from http://automatetheboringstuff.com/chapter14/
    exampleFile = open(csv_file)
    exampleReader = csv.reader(exampleFile)
    exampleData = list(exampleReader)
    return exampleData


def transform(head, dat):
    list_dict = list()
    for item in dat:
        d = {}
        for i in range(len(head)):
            d[head[i]] = item[i]
        list_dict.append(d)
    return list_dict


def group_data(data_dict):
    d = dict()
    for item in data_dict:
        if item["Group"] not in d:
            d[item["Group"]] = [item["Student"]]
        else:
            d[item["Group"]].append(item["Student"])
    return d


def convert_group_to_int(group_dict):
    d = {}
    for key in group_dict:
        d[int(key)] = group_dict[key]
    return d


def main():
    dataset = read_csv('data.csv')
    print('dataset:', dataset)
    header = dataset[0]
    print('header:', header)
    data = dataset[1:]
    print('data:', data)
    data_dict = transform(header, data)
    print('data_dict:', data_dict)
    print('name =', data_dict[0]["Name"])

    dataset = read_csv('group.csv')
    print('dataset:', dataset)
    header = dataset[0]
    print('header:', header)
    data = dataset[1:]
    print('data:', data)
    data_dict = transform(header, data)
    print('data_dict:', data_dict)
    group_dict = group_data(data_dict)
    print('group_dict:', group_dict)
    group_dict = convert_group_to_int(group_dict)
    print('group_dict:', group_dict)

main()
