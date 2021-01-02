import csv
from pathlib import Path


FIRST_NAME_LIST = []
LAST_NAME_LIST = []
PRONOUNS_LIST = []
NATIONALITY = []
ETHNICITITY = []
WORDS = []
DEPARTMENTS = {}
SPECIAL_ROLES = [
    {'role':'CEO', 'department': 'Other', 'level': 'S'},
    {'role':'Chief Technology Officer', 'department': 'Engineering', 'level': 'A'},
    {'role':'Chief Revenue Officier', 'department': 'Sales', 'level': 'A'},
    {'role':'Head of Sales EMEA', 'department': 'Sales', 'level': 'B'},
    {'role':'Head of Sales Americas', 'department': 'Sales', 'level': 'B'},
    {'role':'Head of Client Services', 'department': 'Client Services','level': 'A'},
    {'role':'Head of Marketing', 'department': 'Marketing','level': 'A'},
    {'role':'Chief People Director', 'department': 'People','level': 'A'},
    {'role':'Head of People Americas', 'department': 'People','level': 'B'},
    {'role':'Head of People EMEA', 'department': 'People','level': 'B'},
    {'role':'PA to CEO', 'department': 'Administration','level': 'S'}
]


def _load_lists():
    # check to see if the list has already been loaded
    if len(FIRST_NAME_LIST) > 0:
        return

    list_paths = 'tests/fixtures/gendata_input/'
    with open(Path(list_paths + 'words.txt').absolute(), encoding="cp1252") as f:
        for line in f:
            WORDS.append(str(line.strip()))
    with open(Path(list_paths + 'first_names.txt').absolute()) as f:
        for line in f:
            FIRST_NAME_LIST.append(line.strip())
    with open(Path(list_paths + 'last_names.txt').absolute()) as f:
        for line in f:
            LAST_NAME_LIST.append(line.strip())
    with open(Path(list_paths + 'role_level.csv').absolute()) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if row["department"] in DEPARTMENTS:
                    DEPARTMENTS[row["department"]].append({
                        "role": row["role"],
                        "level": row["level"],
                        "role_relation": row["role_relation"]
                    })
                else:
                    DEPARTMENTS[row["department"]] = []
                    DEPARTMENTS[row["department"]].append({
                        "role": row["role"],
                        "level": row["level"],
                        "role_relation": row["role_relation"]
                    })
            except KeyError as e:
                print(e)
                sys.exit(-1)
                break
    with open(Path(list_paths + 'nationality.txt').absolute()) as f:
        for line in f:
            NATIONALITY.append(line.strip())
    with open(Path(list_paths + "ethnicity.txt").absolute()) as f:
        for line in f:
            ETHNICITITY.append(line.strip())
    with open(Path(list_paths + "pronouns.txt").absolute()) as f:
        for line in f:
            PRONOUNS_LIST.append(line.strip())