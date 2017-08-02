import factory
from api import models
import pytz


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('username')
    password = "password123"


class ItemFactory(factory.Factory):
    class Meta:
        model = models.Item

    title = factory.Faker('text', max_nb_chars=25)
    description = factory.Faker('text', max_nb_chars=125)


class GroupFactory(factory.Factory):
    class Meta:
        model = models.Group


class CollectionFactory(factory.Factory):
    class Meta:
        model = models.Collection

    title = factory.Faker('text', max_nb_chars=25)
    description = factory.Faker('text', max_nb_chars=125)
    tags = "foo, bar, baz"
    settings = {}
    submission_settings = {}


class MeetingFactory(factory.Factory):
    class Meta:
        model = models.Meeting

    address = str(factory.Faker('street_address')) + " " + str(factory.Faker('city')) + " " + str(factory.Faker('state_abbr')) + " " + str(
        factory.Faker('zipcode'))
    location = str(factory.Faker('city')) + ", " + str(factory.Faker('state_abbr'))
    title = factory.Faker('text', max_nb_chars=25)
    description = factory.Faker('text', max_nb_chars=125)
    tags = "foo, bar, baz"
    start_date = factory.Faker('date_time_between', start_date="-1w", end_date="-1d", tzinfo=pytz.timezone('US/Eastern'))
    end_date = factory.Faker('date_time_between', start_date="+1d", end_date="+1w", tzinfo=pytz.timezone('US/Eastern'))
    settings = {}
    submission_settings = {}