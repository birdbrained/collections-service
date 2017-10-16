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


from user.views import (
    UserViewSet,
    UserSearchView,
)


# Router Setup
# #############################################################################


user_router = routers.DefaultRouter(trailing_slash=False)

user_router.register(r'users', UserViewSet)
user_router.register("users/search", UserSearchView, base_name="user-search")


# EOF
# #############################################################################
