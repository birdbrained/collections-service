"""
# Collection Router
"""


# Library Imports
# #############################################################################


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers
from collections import namedtuple


# App Imports
# #############################################################################


from collection.views import (
    CollectionViewSet,
    ItemViewSet,
    DocumentViewSet,
    CollectionMembershipViewSet,
    SchemaViewSet
)


# Router Setup
# #############################################################################


collection_router = routers.DefaultRouter(trailing_slash=False)

collection_router.register(r'collections', CollectionViewSet)
collection_router.register(r'items', ItemViewSet)
collection_router.register(r'documents', DocumentViewSet)
collection_router.register(r'collection-memberships', CollectionMembershipViewSet)
collection_router.register(r'schemas', SchemaViewSet)


# EOF
# #############################################################################
