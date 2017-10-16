from django.conf.urls import url, include
from collection.views import (
    CollectionSearchView,
    ItemSearchView
)
from rest_framework.routers import DefaultRouter

from collection.routers import collection_router
from workflow.routers import workflow_router, case_router
from user.routers import user_router

from api.views import api_root

search_router = DefaultRouter()
search_router.register("collections/search", CollectionSearchView, base_name="collection-search")
search_router.register("items/search", ItemSearchView, base_name="item-search")

urlpatterns = [

    url(r'^$', api_root),
    url(r'', include(collection_router.urls)),
    url(r'', include(workflow_router.urls)),
    url(r'', include(case_router.urls)),
    url(r'', include(search_router.urls)),
    url(r'', include(user_router.urls)),

]
