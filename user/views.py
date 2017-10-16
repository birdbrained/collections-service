"""
# Service Views

- CurrentUser
- UserDetail
- UserList
- UserSearchView
"""


# Library Imports
# #############################################################################


from rest_framework import generics
from rest_framework_json_api import pagination
from rest_framework import exceptions as drf_exceptions
from rest_framework.viewsets import ModelViewSet
from drf_haystack.viewsets import HaystackViewSet

from user.models import User
from user.serializers import (
    UserSerializer,
    UserSearchSerializer
)


# Model Views
# #############################################################################


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        pk = self.kwargs.get("pk")
        if pk == "me":
            return self.request.user
        try:
            return User.objects.get(id=pk)
        except:
            raise drf_exceptions.NotFound


# Search Views
# #############################################################################


class UserSearchView(HaystackViewSet):
    index_models = [User]
    serializer_class = UserSearchSerializer


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


# EOF
# #############################################################################
