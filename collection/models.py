"""
Collection Models
"""


# Imports
# #############################################################################


from django.conf import settings
from django.db.models import (
    Model,
    CharField,
    TextField,
    ForeignKey,
    DateTimeField,
    ManyToManyField,
    SET_NULL
)
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField

from tests import resources


# Models
# #############################################################################


class Collection(Model):
    """
    # `collection.models.Collection`

    The `Collection` model represents a collection in the collections app.
    These are not separate models because using the same model allows a
    collection to be an item in another collection, leading to collections of
    collections.

    Every collection has basic information that should be stored about it, such
    as its title and description, and various dates pertaining to creation and
    updates.

    Each collection also has items
    """

    title = CharField(max_length=200)
    description = TextField(null=True, blank=True)
    page_settings = JSONField(default={}, blank=True)
    owner = ForeignKey(settings.AUTH_USER_MODEL)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)

    schemas = ManyToManyField(
        "Schema",
        through="CollectionMembership",
        related_name="collections"
    )

    items = ManyToManyField(
        "Item",
        through="CollectionMembership",
        related_name="collections"
    )

    workflow = ForeignKey(
        'workflow.Workflow',
        null=True,
        blank=True,
        related_name="collections",
        on_delete=SET_NULL
    )

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ('approve_collection_items', 'Approve collection items'),
        )


class Item(Model):
    """
    # `collection.model.Item`

    The `Item` model represents an in a collection. Every `Item` has basic
    information that should be stored about it, such as its title and
    description, and various dates pertaining to creation and updates.

    Each `Item` also has content, this may be the information stored on the node,
    and/or other metadata. This content is defined by the related Schema.
    """

    title = CharField(max_length=200)
    description = TextField(null=True, blank=True)
    type = CharField(max_length=200)
    owner = ForeignKey(settings.AUTH_USER_MODEL)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)

    schemas = ManyToManyField(
        "Schema",
        through="Document",
        related_name="items"
    )

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ('approve_collection_items', 'Approve collection items'),
        )


class Document(Model):
    """
    # `collection.models.Document`

    The `Document` model represents the data of an `Item` for a particular
    schema. A given `Item` may have different representations of the data it
    contains. The `Document` model is an instance of one of those
    representations.

    A `Items`'s document may only be applicable to certain collections, so the
    `Document` represents this with relatioships to `Collection` through
    `CollectionMembership`.
    """

    content = JSONField(default={}, null=True, blank=True)
    owner = ForeignKey(settings.AUTH_USER_MODEL)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)

    schema = ForeignKey(
        "Schema",
        related_name="documents",
        null=False,
        blank=False,
    )

    collections = ManyToManyField(
        "Collection",
        related_name="documents",
    )

    item = ForeignKey(
        "Item",
        related_name="documents"
    )


class CollectionMembership(Model):
    """
    # `collection.models.CollectionMembership`

    The `CollectionMembership` model represents a relationship between an item
    and a collection it is a member of.

    `CollectionMembership` may be used to constrain content instances to limit
    the `Item`'s content if it only applies whe the node is viewed as a member
    of a particular `Collection`.

    A label is also available.
    """

    label = CharField(max_length=200, null=True)
    role = CharField(max_length=200, null=True)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)

    item = ForeignKey(
        "Item",
        related_name="memberships",
        blank=False,
        null=False
    )

    collection = ForeignKey(
        "Collection",
        blank=False,
        null=False,
        related_name="collection_memberships"
    )

    document = ForeignKey(
        "Document",
        blank=False,
        null=False,
        related_name="memberships"
    )

    schema = ForeignKey(
        "Schema",
        related_name="memberships",
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = ["item", "collection"]


class Schema(Model):
    """
    # `Schema`

    The schema defines what valid data for a document'content looks like.
    """

    name = CharField(max_length=200, null=True)
    definition = JSONField(default={}, null=True, blank=True)
    owner = ForeignKey(settings.AUTH_USER_MODEL)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)


# EOF
# #############################################################################
