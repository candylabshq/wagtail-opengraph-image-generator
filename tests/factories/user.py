import factory

from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttributeSequence(
        lambda user, n: '{}{}_{}'.format(user.first_name, user.last_name, n)
    )
    email = factory.LazyAttributeSequence(
        lambda user, n: '{}{}@example.com'.format(user.username, n)
    )
    password = 'supersecret'
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = get_user_model()
