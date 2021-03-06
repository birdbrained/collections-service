from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from .factories import UserFactory, ItemFactory, CollectionFactory, MeetingFactory

class TestBase(TestCase):
    def setUp(self):

        # All users have password "password123" by default
        # Username defaults to first_initial+last_name (i.e. jdoe)
        self.owner = UserFactory(username="owner")
        self.owner.save()

        self.submitter = UserFactory(username="submitter")
        self.submitter.save()

        self.rand_user = UserFactory(username="random")
        self.rand_user.save()

        # all foreign keys must be specified, everything else is auto-generated by default, or can be left blank
        # make a collection with 100 items
        self.collection = CollectionFactory(created_by=self.owner)
        self.collection.save()

        items = ItemFactory.build_batch(100, collection=self.collection, created_by=self.submitter)
        for i in items:
            i.save()

        self.item = ItemFactory(collection=self.collection, created_by=self.submitter)
        self.item.save()
        # make a meeting with 100 items
        self.meeting = MeetingFactory(created_by=self.owner)
        self.meeting.save()

        items = ItemFactory.build_batch(100, collection=self.meeting, created_by=self.submitter)
        for i in items:
            i.save()

        self.factory = APIRequestFactory()
        self.client = APIClient()
