import random
import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from faker import Faker

from apps.api.models import Transportation, Checkpoint, Device
from apps.catalog.models import HazardousMaterial

faker = Faker()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )
    username = faker.user_name()
    email = faker.email()
    password = make_password('password')


class HazardousMaterialFactory(factory.DjangoModelFactory):
    kind = factory.Iterator(["Flammable liquids", "Flammable gases"])
    coefficient = random.uniform(5.0, 30.0)

    class Meta:
        model = HazardousMaterial


class DeviceFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Device
        django_get_or_create = ('user',)


class TransportationFactory(factory.DjangoModelFactory):
    device = factory.SubFactory(DeviceFactory)
    start_point = Point(random.uniform(6.0, 6.5), random.uniform(53.0, 53.5))
    end_point = Point(random.uniform(6.0, 6.5), random.uniform(53.0, 53.5))
    type_of_hazardous_material = factory.SubFactory(HazardousMaterialFactory)
    volume = random.uniform(5.0, 30.0)
    distance = random.uniform(50.0, 500.0)
    data = {}

    class Meta:
        model = Transportation
        django_get_or_create = ('data', )


class CheckpointFactory(factory.DjangoModelFactory):
    transportation = factory.SubFactory(TransportationFactory)
    location = Point(random.uniform(6.0, 6.5), random.uniform(53.0, 53.5))
    data = {
        'temperature': faker.random_digit_not_null(),
    }

    class Meta:
        model = Checkpoint
        django_get_or_create = ('data', )
