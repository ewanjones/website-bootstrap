import csv
import random

from itertools import groupby
from pathlib import Path

from .base_screen import BaseScreen
from .helpers import lists
from .helpers.employee import create_default_employee_csv

class CSVScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.headers = [
            "first name",
            "last name", 
            "gender",
            "pronouns", 
            "nationality", 
            "ethnicity",
            "role",
            "department", 
            "start date", 
            "end date",
            "salary",
            "FTE",
            "Location",
            "line manager",
            "Line Manager Role Title",
            "level"
        ]

    def handle_choice(self):
        self.filename = input("Please enter the output filename: ")
        self.max = int(input("Enter total amount of employees: in business: "))
        self.rentention_percentage = int(input("Enter percentage of active employees (number 0-100): "))
        print("creating random data for csv....")
        self._create_data()
        print("finished! press enter to exit program")
        input()

    def _create_data(self):
        with open(Path("tests/fixtures/" + self.filename + ".csv").absolute(), "w", newline="") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            csv_writer.writeheader()
            csv_writer.writerows(self._create_random_employees())

    def _create_employee(self, department_name, role_name, level_name):
        employee = create_default_employee_csv()
        employee['department'] =  department_name
        employee['role'] = role_name
        employee['end date'] = '' # These special roles are always with us 
        employee['level'] = level_name
        return employee

    def _create_random_employees(self):
        result = self._create_special_roles()
        for i in range(0, self.max):
            employee = create_default_employee_csv()
            
            # we're basically flipping a biased coin to determine whether the employee is still with us
            true_rentention_weight = self.rentention_percentage / 100
            false_rentention_weight = 1 - true_rentention_weight
            employee_stayed = random.choices(population=[True, False], weights=[true_rentention_weight, false_rentention_weight], k=1)
            if employee_stayed[0]:
                employee['end date'] = ''

            result.append(employee)
        result = self._add_line_managers(result)
        return result

    def _add_line_managers(self, data):
        result = []
        cpd = [employee for employee in data if employee['role'] == 'Chief People Director'][0]
        department_keyfunc = lambda department: department['department']
        level_keyfunc = lambda level: level['level']
        sorted_result = sorted(data, key=department_keyfunc)
        for k, g in groupby(sorted_result, department_keyfunc):
            if k == "Administration":
                for employee in list(g):
                    tmp_employee = employee
                    tmp_employee['line manager'] = '{} {}'.format(cpd['first name'], cpd['last name'])
                    tmp_employee['Line Manager Role Title'] = cpd['role']
                    result.append(tmp_employee)
                continue

            department_employees = sorted(list(g), key=level_keyfunc)
            employees_by_level = []
            for level, employee in groupby(department_employees , level_keyfunc):
                employees_by_level.append(dict({
                    level: list(employee)
                }))
            employees_by_level.reverse()

            for i in range( len(employees_by_level) - 1):
                low_level = employees_by_level[i]
                high_level = employees_by_level[i+1]                
                for level, employees in low_level.items():
                    for employee in employees:
                        if employee['line manager'] == '':
                            hle = None
                            if level == "D":
                                hle = high_level["C"]
                            elif level == "C":
                                hle = high_level["B"]
                            elif level == "B":
                                hle = high_level["A"]

                            tmp_employee = employee
                            line_manager = random.choice(hle)
                            tmp_employee['line manager'] =  '{} {}'.format(line_manager['first name'], line_manager['last name'])
                            tmp_employee['Line Manager Role Title'] = line_manager['role']
                            result.append(tmp_employee)
                        else:
                            result.append(employee)

            high_level_employees = employees_by_level[len(employees_by_level) - 1]
            for value in high_level_employees.values():
                for employee in value:
                    result.append(employee)

        return result
            
    def _create_special_roles(self):
        result = []
        roles_index = {}
        index = 0
        for role in lists.SPECIAL_ROLES:
            department_ = role['department']
            role_ = role['role']
            level = role['level']
            result.append(self._create_employee(department_, role_, level))
            
            roles_index[role_] = index
            index += 1

        ceo = result[roles_index['CEO']]

        cto = result[roles_index['Chief Technology Officer']]
        cto['line manager'] = "{} {}".format(ceo['first name'], ceo['last name'])
        cto['Line Manager Role Title'] = ceo['role']
        
        cro = result[roles_index['Chief Revenue Officier']]
        cro['line manager'] = "{} {}".format(ceo['first name'], ceo['last name'])
        cro['Line Manager Role Title'] = ceo['role']

        hos_emea = result[roles_index['Head of Sales EMEA']]
        hos_emea['line manager'] = "{} {}".format(cro['first name'], cro['last name'])
        hos_emea['Line Manager Role Title'] = cro['role']
        
        hos_a = result[roles_index["Head of Sales Americas"]]
        hos_a['line manager'] = "{} {}".format(cro['first name'], cro['last name'])
        hos_a['Line Manager Role Title'] = cro['role']
        
        hocs = result[roles_index["Head of Client Services"]]
        hocs['line manager'] = "{} {}".format(ceo['first name'], ceo['last name'])
        hocs['Line Manager Role Title'] = ceo['role']

        hom = result[roles_index["Head of Marketing"]]
        hom['line manager'] = "{} {}".format(cro['first name'], cro['last name'])
        hom['Line Manager Role Title'] = cro['role']
        
        cpd = result[roles_index["Chief People Director"]]
        cpd['line manager'] = "{} {}".format(ceo['first name'], ceo['last name'])
        cpd['Line Manager Role Title'] = ceo['role']

        hop_a = result[roles_index["Head of People Americas"]]
        hop_a['line manager'] = "{} {}".format(cpd['first name'], cpd['last name'])
        hop_a['Line Manager Role Title'] = cpd['role']
        
        hop_emea = result[roles_index["Head of People EMEA"]]
        hop_emea['line manager'] = "{} {}".format(cpd['first name'], cpd['last name'])
        hop_emea['Line Manager Role Title'] = cpd['role']

        pa_ceo = result[roles_index["PA to CEO"]]
        pa_ceo['line manager'] = "{} {}".format(ceo['first name'], ceo['last name'])
        pa_ceo['Line Manager Role Title'] = ceo['role']

        result.clear()
        result.append(ceo)
        result.append(cto)
        result.append(cro)
        result.append(hos_a)
        result.append(hos_emea)
        result.append(hocs)
        result.append(hom)
        result.append(cpd)
        result.append(hop_a)
        result.append(hop_emea)
        result.append(pa_ceo)

        return result
