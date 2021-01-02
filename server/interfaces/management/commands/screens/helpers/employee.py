import random
from datetime import date

from . import lists

random.seed()
lists._load_lists()


# Creates a random employee and returns a dictionary object
def create_default_employee():
    first_name = random.choice(lists.FIRST_NAME_LIST)
    last_name = random.choice(lists.LAST_NAME_LIST)
    gender =  random.choice(["Male", "Female", "Other"])
    pronouns = random.choice(lists.PRONOUNS_LIST)
    nationality = random.choice(lists.NATIONALITY)
    ethnicity = random.choice(lists.ETHNICITITY)
    location = "London"
    start_date = None
    end_date = None
    salary = random.randrange(10000, 100000, 1000)
    department_key = random.choice(list(lists.DEPARTMENTS.keys()))
    department_ = random.choice(lists.DEPARTMENTS[department_key])
    role = department_['role']
    level = department_['level']

    start_date_obj = generate_date_between()
    end_date_obj = generate_date_between()

    if start_date_obj < end_date_obj:
        start_date = start_date_obj
        end_date = end_date_obj
    else:
        start_date = end_date_obj
        end_date = start_date_obj

    return dict({
        "name": "{} {}".format(first_name, last_name),
        "gender": gender,
        "pronouns": pronouns,
        "nationality": nationality,
        "ethnicity": ethnicity,
        "role": role,
        "department": department_key,
        "start_date": start_date,
        "end_date": end_date,
        "salary": salary,
        "location": "London",
        "level": level,
    })

# CSV output employee
def create_default_employee_csv():
    employee = create_default_employee()
    name = employee.pop('name').split(sep=' ')
    first_name = name[0]
    last_name = name[1]

    start_date = employee.pop('start_date')
    end_date = employee.pop('end_date')
    location = employee.pop('location')

    employee['first name'] = first_name
    employee['last name'] = last_name
    employee['line manager'] = ''
    employee['Line Manager Role Title'] = ''
    employee['FTE'] = 1
    employee['start date'] = start_date
    employee['end date'] = end_date
    employee['Location'] = location

    return employee

# This method with generate a date between min and max date from the constructor
def generate_date_between():
    min_date = date(1970,1,1).toordinal()
    max_date = date.today().toordinal()

    return date.fromordinal(random.randint(min_date, max_date))