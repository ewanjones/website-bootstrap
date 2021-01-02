import factory


class User(factory.DjangoModelFactory):
    full_name = "Test Person"
    nickname = "Test"
    email = "test.person@example.com"
    phone = "07123456789"
    is_active = True

    class Meta:
        model = "accounts.User"

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        obj.set_password(obj.password)
