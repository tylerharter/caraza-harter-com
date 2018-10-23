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


def main():
    dataset = read_csv('data.csv')
    print('dataset:', dataset)
    header = dataset[0]
    print('header:', header)
    data = dataset[1:]
    print('data:', data)
    data_dict = transform(header, data)
    print(data_dict)


main()
