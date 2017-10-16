"""
# Collection Views

## Defines
- CollectionViewSet
- ItemViewSet
- ColletionMembershipViweSet
- DocumentviewSet
"""


# Imports
# #############################################################################


from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework_json_api import pagination
from rest_framework import exceptions as drf_exceptions
from rest_framework import permissions as drf_permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_haystack.viewsets import HaystackViewSet
from guardian.shortcuts import assign_perm

from collection.permissions import (
    CanEditCollection,
    CanEditItem,
    CanEditGroup
)
from collection.models import (
    Collection,
    Item,
    Document,
    CollectionMembership,
    Schema
)
from collection.serializers import (
    CollectionSerializer,
    ItemSerializer,
    DocumentSerializer,
    CollectionMembershipSerializer,
    SchemaSerializer,
    CollectionSearchSerializer,
    ItemSearchSerializer,
)


# Views
# #############################################################################


class CollectionViewSet(ModelViewSet):
    """
    # `CollectionViewSet`

    `ViewSet` for inteacting with Collection models.

    ## `Collection` Attributes

        name           type                description
        =======================================================================
        title          string              group title
        description    string              group description
        date_created   iso8601 timestamp   date/time when the group was created
        date_updated   iso8601 timestamp   date/time when the group was last
                                           updated

    ## Actions

    ### Creating New Groups

        Method:        POST
        URL:           /api/groups
        Query Params:  <none>
        Body (JSON):   {
                         "data": {
                           "type": "groups",                         # required
                           "attributes": {
                             "title":        {title},                # required
                             "description":  {description}           # optional
                           },
                           "relationships": {
                             "collection": {
                               "data": {
                                 "type": "meetings" | "collections"  # required
                                 "id": {collection_id}               # required
                               }
                             }
                           }
                         }
                       }
        Success:       201 CREATED + group representation

    Note: Since the route does not include the collection or meeting id, it
    must be specified in the payload.

    ## This Request/Response
    """

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_queryset(self):

        queryset = Collection.objects.all().order_by('-date_created')

        user_id = self.request.query_params.get('user')
        username = self.request.query_params.get('username')
        org_name = self.request.query_params.get("org")

        if user_id:
            queryset = queryset.filter(created_by_id=user_id)
        if username:
            queryset = queryset.filter(created_by__username=username)
        if org_name:
            queryset = queryset.filter(created_by_org=org_name)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        collection = serializer.save()
        assign_perm('api.approve_collection_items', user, collection)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.has_perm("view", instance):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(serializer.data)


class ItemViewSet(ModelViewSet):
    """
    # `ItemViewSet`
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        collection = self.request.data.get('collection')
        if collection:
            queryset = queryset.filter(collection_id=collection)
        return queryset.filter(Q(status='approved') | Q(created_by=user.id) | Q(collection__created_by=user.id))

    def perform_create(self, serializer):
        user = self.request.user
        collection = Collection.objects.get(self.request.data.get("collection"))
        if not user.has_perm('collection.AddItem', collection):
            return HttpResponse('Unauthorized', status=401)
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.has_perm("view", instance):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return HttpResponse('Not Found', status=404)


class DocumentViewSet(ModelViewSet):
    """
    # `ItemViewSet`
    """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):

        queryset = self.queryset
        user = self.request.user
        collection_id = self.request.data.get('collection')
        item_id = self.request.data.get('item')
        type = self.request.data.get('type')
        schema = self.request.data.get("schema")
        role = self.request.data.get("role")

        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        if item_id:
            queryset = queryset.filter(item_id=item_id)
        if type:
            queryset = queryset.filter(item__type=type)
        if schema:
            queryset = queryset.filter(schema__item__title=schema)
        if role:
            queryset - queryset.filter(memberships__role=role)

        return queryset

    def perform_create(self, serializer):

        user = self.request.user
        doc = serializer.validated_data

        for collection in doc.collections:
            if not user.has_perm('collection.ViewCollection', collection):
                return HttpResponse('Collection Not Found', status=404)
            if not user.has_perm('collection.AddItem', collection):
                return HttpResponse('Unauthorized', status=401)

        serializer.save()

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        if not request.user.has_perm("view", instance):
            return HttpResponse('Document Not Found', status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CollectionMembershipViewSet(ModelViewSet):
    """
    # `ItemViewSet`
    """

    queryset = CollectionMembership.objects.all()
    serializer_class = CollectionMembershipSerializer

    def get_queryset(self):

        queryset = self.queryset
        user = self.request.user
        collection_id = self.request.data.get('collection')
        item_id = self.request.data.get('item')
        type = self.request.data.get('type')
        schema = self.request.data.get("schema")
        role = self.request.data.get("role")

        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        if item_id:
            queryset = queryset.filter(item_id=item_id)
        if type:
            queryset = queryset.filter(item__type=type)
        if schema:
            queryset = queryset.filter(item__schema__item__title=schema)
        if role:
            queryset - queryset.filter(role=role)

    def perform_create(self, serializer):

        user = self.request.user
        _membership = serializer.validated_data

        if not user.has_perm("collection.AddItem", _memberhip.collection):
            return HttpResponse('Unauthorized', status=401)

        if not user.has_perm("collection.ViewItem", _membership.item):
            return HttpResponse('Item Not Found', status=404)

        if not user.has_perm("collection.ViewDocument", _membership.item):
            return HttpResponse('Document Not Found', status=404)

        membership = serializer.save()

        assign_perm('api.EditMembership', user, membership)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        if request.user.has_perm("view", instance):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return HttpResponse('Not Found', status=404)


class SchemaViewSet(ModelViewSet):
    """
    # `SchemaViewSet`
    """

    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        if request.user.has_perm("view", instance):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return HttpResponse('Not Found', status=404)


# Search Views
# #############################################################################


class CollectionSearchView(HaystackViewSet):
    index_models = [Collection]
    serializer_class = CollectionSearchSerializer


class ItemSearchView(HaystackViewSet):
    index_models = [Item]
    serializer_class = ItemSearchSerializer

# Put in `service.views`
class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


# EOF
# #############################################################################
