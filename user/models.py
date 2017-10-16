"""
Auth Models
"""


# Library Imports
# #############################################################################


from django.db.models import (
    AutoField,
    URLField
)
from django.contrib.auth.models import AbstractUser


# App Imports
# #############################################################################


from collection.mixins import CollectionUserMixin


# Models
# #############################################################################


class User(AbstractUser, CollectionUserMixin):
    id = AutoField(primary_key=True)
    gravatar = URLField(blank=True)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

# EOF
# #############################################################################
