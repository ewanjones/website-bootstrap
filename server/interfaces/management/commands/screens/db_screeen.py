from .base_screen import BaseScreen

import sys
import uuid
import random
import string

from tqdm import tqdm

from datetime import datetime

from data.accounts import models as account_models
from data.organisation import models as org_models

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from .helpers import lists
from .helpers.employee import create_default_employee

# These roles only have 1 per business


class DBScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.text = " "
    
    def handle_choice(self):
        self.max = int(input("Enter total amount of employees in business: "))
        self.rentention_percentage = int(input("Enter percentage of active employees (number 0-100): "))
        print()
        self.insert_db()
        print("finished! press enter to exit program")
        input()
        
    def insert_db(self):
        business, password = self._create_random_account()

        # creating special roles
        print("Creating special roles...")
        for role in tqdm(lists.SPECIAL_ROLES):
            result = self._create_employee(business, role['department'], role['role'], role['level'])
            if not result:
                print("something has gone wrong, exiting script")
                sys.exit(-1)

        self._assign_special_role_relations(business)

        print("Creating random employees...")
        for i in tqdm(range(self.max)):
            result = self._create_random_employee(business)
            if not result:
                print("Something has gone wrong with the import....Stopping process")
                break
        
        print("Sorting relations between the employees...")
        employees = org_models.Employee.objects.filter(role__department__business=business,line_manager=None)
        for employee in tqdm(employees):
            line_manager = self._get_line_manager(business, employee.role.level.name, employee.role.department.name, employee.role.name)
            if line_manager is not None:
                employee.add_line_manager(line_manager)

        print('\nUser account: {}\nPassword: {}\n\n'.format(business.user.email, password))

    # creates a random user account associated with a random business
    def _create_random_account(self):
        user_first_name = random.choice(lists.FIRST_NAME_LIST)
        user_last_name = random.choice(lists.LAST_NAME_LIST)
        activation_code = uuid.uuid4().hex
        business_name = random.choice(lists.WORDS)
        email = business_name + "@" + business_name + ".com"
        password = ''.join(random.choice(string.ascii_letters) for i in range(10))

        try:
            user = account_models.User.objects.create_user(
                email=email,
                password=password,
                full_name=user_first_name + " " + user_last_name,
                nickname=user_first_name,
                phone='00000000000',
                activation_code=activation_code,
            )
            user.is_active = True
            user.save()
        except IntegrityError:
            raise UnableToRegister("Couldn't create an account with this email")

        try:
            business = org_models.Business.objects.create(
                user=user, name=business_name, description=""
            )
            return business, password
        except IntegrityError:
            raise UnableToRegister("Couldn't create an business")
        return None

    def _create_employee(self, business, department_name, role_name, level_name):
        employee_dict =  create_default_employee()
        
        #removing unneeded key/values
        employee_dict.pop('role')
        employee_dict.pop('department')
        employee_dict.pop('level')
        
        # creating department in db
        department, _ = org_models.Department.objects.get_or_create(
            name=department_name, business=business
        )

        # creating level in db
        level, _ = org_models.Level.objects.get_or_create(name=level_name, business=business)

        # creating role in db
        role, _ = org_models.Role.objects.get_or_create(
            name=role_name, department=department, level=level
        )

        employee_dict['role'] = role

        employee = org_models.Employee.objects.create(**employee_dict)

        employee.start_date = employee_dict['start_date']
        employee.end_date = employee_dict['end_date']
        employee.save()

        if employee is not None:
            return True
        return False

    def _create_random_employee(self, business):
        random_employee = create_default_employee()

        # we're basically flipping a biased coin to determine whether the employee is still with us
        true_rentention_weight = self.rentention_percentage / 100
        false_rentention_weight = 1 - true_rentention_weight
        employee_stayed = random.choices(population=[True, False], weights=[true_rentention_weight, false_rentention_weight], k=1)
        if employee_stayed[0]:
            random_employee['end_date'] = None

        # creating department in db
        department, _ = org_models.Department.objects.get_or_create(
            name=random_employee['department'], business=business
        )

        # creating level in db
        level, _ = org_models.Level.objects.get_or_create(name=random_employee['level'], business=business)

        # creating role in db
        role, _ = org_models.Role.objects.get_or_create(
            name=random_employee['role'], department=department, level=level
        )

        #removing level and department and updating the role key to contain the role obj
        random_employee.pop('level')
        random_employee.pop('department')
        random_employee['role'] = role

        employee = org_models.Employee.objects.create(**random_employee)

        employee.start_date = random_employee['start_date']
        employee.end_date = random_employee['end_date']
        employee.save()

        if employee is not None:
            return True

        return False

    def _assign_special_role_relations(self, business):
        # Assigning line managers to these roles
        # if anyone can think of a better approach to this then just change it
        ceo = org_models.Employee.objects.get(role__department__business=business, role__name="CEO")
        cto = org_models.Employee.objects.get(role__department__business=business,role__name="Chief Technology Officer")
        cro = org_models.Employee.objects.get(role__department__business=business,role__name="Chief Revenue Officier")
        hos_emea = org_models.Employee.objects.get(role__department__business=business,role__name="Head of Sales EMEA")
        hos_a = org_models.Employee.objects.get(role__department__business=business,role__name="Head of Sales Americas")
        hocs = org_models.Employee.objects.get(role__department__business=business,role__name="Head of Client Services")
        hom = org_models.Employee.objects.get(role__department__business=business,role__name="Head of Marketing")
        cpd = org_models.Employee.objects.get(role__department__business=business,role__name="Chief People Director")
        hop_a = org_models.Employee.objects.get(role__department__business=business,role__name="Head of People Americas")
        hop_emea = org_models.Employee.objects.get(role__department__business=business,role__name="Head of People EMEA")
        pa_ceo = org_models.Employee.objects.get(role__department__business=business,role__name="PA to CEO")

        cto.add_line_manager(ceo)
        cro.add_line_manager(ceo)
        hos_a.add_line_manager(cro)
        hos_emea.add_line_manager(cro)
        hocs.add_line_manager(ceo)
        hom.add_line_manager(cro)
        cpd.add_line_manager(ceo)
        hop_a.add_line_manager(cpd)
        hop_emea.add_line_manager(cpd)
        pa_ceo.add_line_manager(ceo)

    def _get_line_manager(self, business, level, department, role):
        if level == "S":
            return None
        
        if department == "Administation" and level == "B":
            cpd = org_models.Employee.objects.get(role__department__business=business, role__name="Chief Person Director")
            return cpd

        line_managers = None
        
        if level == "D":
            line_managers = org_models.Employee.objects.filter(role__department__business=business, role__department__name=department, role__level__name="C")
        elif level == "C":
            line_managers = org_models.Employee.objects.filter(role__department__business=business, role__department__name=department, role__level__name="B")
        elif level == "B":
            line_managers = org_models.Employee.objects.filter(role__department__business=business, role__department__name=department, role__level__name="A")
        
        line_manager = None
        if len(line_managers) > 0:
            line_manager_index = random.randrange(len(line_managers))
            line_manager = line_managers[line_manager_index]
        return line_manager
