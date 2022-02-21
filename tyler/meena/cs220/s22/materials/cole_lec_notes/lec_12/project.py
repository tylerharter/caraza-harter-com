__student__ = []


def __init__():
    import csv
    """This function will read in the csv_file and store it in a list of dictionaries"""
    __student__.clear()
    with open('cs220_survey_data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            __student__.append(row)

def reload():
    """This function reloads the CSV file, you must run it if you make any changes."""
    __init__()

def count():
    """This function will return the number of records in the dataset"""
    return len(__student__)


def get_lecture(idx):
    """get_lecture(idx) returns the lecture of the student in row idx"""
    return __student__[int(idx)]['Lecture']


def get_age(idx):
    """get_age(idx) returns the age of the student in row idx as a string"""
    return __student__[int(idx)]['Age']


def get_primary_major(idx):
    """get_primary_major(idx) returns the primary major of the student in row idx"""
    return __student__[int(idx)]['Primary major']


def get_other_majors(idx):
    """get_other_majors(idx) returns the secondary major of the student in row idx"""
    return __student__[int(idx)]['Other majors']


def get_zip_code(idx):
    """get_zip_code(idx) returns the residential zip code of the student in row idx"""
    return __student__[int(idx)]['Zip Code']


def get_piazza_topping(idx):
    """get_piazza_topping(idx) returns the preferred pizza toppings of the student in row idx"""
    return __student__[int(idx)]['Pizza topping']

def get_pet_owner(idx):
    """get_pet_owner(idx) returns whether student in row idx is a pet owner"""
    return __student__[int(idx)]['Pet owner']

def get_runner(idx):
    """get_runner(idx) returns whether student in row idx is a runner"""
    return __student__[int(idx)]['Runner']

def get_sleep_habit(idx):
    """get_sleep_habit(idx) returns the sleep habit of the student in row idx"""
    return __student__[int(idx)]['Sleep habit']

def get_procrastinator(idx):
    """get_procrastinator(idx) returns whether student in row idx is a procrastinator"""
    return __student__[int(idx)]['Procrastinator']


__init__()
