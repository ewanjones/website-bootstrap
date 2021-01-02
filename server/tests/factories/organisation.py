import factory

from . import core


class Business(factory.DjangoModelFactory):
    user = factory.SubFactory(core.User)
    name = "Test Business"
    description = "This is a description"

    class Meta:
        model = "organisation.Business"


class Level(factory.DjangoModelFactory):
    name = "Level A"
    description = "This is the lowest level"

    class Meta:
        model = "organisation.Level"


class Department(factory.DjangoModelFactory):
    name = "Tech"
    description = "This is the tech team"

    class Meta:
        model = "organisation.Department"


class Role(factory.DjangoModelFactory):
    name = "Some Role"

    class Meta:
        model = "organisation.Role"


class Employee(factory.DjangoModelFactory):
    name = "Someone"
    salary = 20000

    class Meta:
        model = "organisation.Employee"
