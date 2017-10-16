"""
Collection Mixins
"""


# Library Imports
# #############################################################################


from django.db.models import ForeignKey
from django.contrib.postgres.fields import JSONField


# App Imports
# #############################################################################


from collection.models import Collection
from tests import resources


# Models
# #############################################################################



class CollectionUserMixin:

    _collection = ForeignKey(
        "Collection",
        blank=True,
        null=True
    )

    @property
    def collection(self, *args, **kwargs):
        if getattr(self._collection, "null", None):
            self._collection = Collection()
            self._collection.title = self.full_name + "'s Collection"
            self._collection.description = "My Collection"
            self._collection.owner = self
            self._collection.save()
        return self._collection


