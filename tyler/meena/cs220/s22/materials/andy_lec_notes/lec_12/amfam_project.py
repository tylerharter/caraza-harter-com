__students__ = []


def __init__():
    import csv
    """This function will read in the csv_file and store it in a list of dictionaries"""
    __students__.clear()
    with open('amfam_survey_data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            __students__.append(row)


def count():
    """This function will return the number of records in the dataset"""
    return len(__students__)


def get_state(idx):
    """get_state(idx) returns the state of the students in row idx"""
    return __students__[int(idx)]['state']


def get_early(idx):
    """get_early(idx) returns the early bird/night owl of the students in row idx"""
    return __students__[int(idx)]['early']


def get_pet(idx):
    """get_pet(idx) returns the favorite pet of the students in row idx"""
    return __students__[int(idx)]['pet']


def get_season(idx):
    """get_season(idx) returns the favorite season of the students in row idx"""
    return int(__students__[int(idx)]['season'])


def get_years(idx):
    """get_years(idx) returns the years of the students in row idx"""
    return __students__[int(idx)]['years']


def get_pizza(idx):
    """get_pizza(idx) returns the pizza topping of the students in row idx"""
    return int(__students__[int(idx)]['pizza'])


__init__()
