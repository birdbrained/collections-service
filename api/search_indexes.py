from haystack import indexes
from api.models import Collection, Item
from django.contrib.auth.models import User
from api.tasks import (
    scrape_text,
    do_update
)
from celery import chain

class CollectionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    description = indexes.EdgeNgramField(model_attr='title')
    created_by = indexes.EdgeNgramField(model_attr='created_by', boost=2.0)

    def get_model(self):
        return Collection

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated
        """
        return self.get_model().objects.all()

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    description = indexes.EdgeNgramField (model_attr='description', null=True)
    created_by = indexes.EdgeNgramField(model_attr='created_by__full_name', null=True)
    collection = indexes.EdgeNgramField(model_attr='collection__pk')
    kind = indexes.EdgeNgramField(model_attr='kind', null=True)

    def update_object(self, instance, using=None, **kwargs):
        """
        Update the index for a single object. Attached to the class's
        post-save hook.
        If ``using`` is provided, it specifies which connection should be
        used. Default relies on the routers to decide which backend should
        be used.
        """
        # Check to make sure we want to index this first.
        if self.should_update(instance, **kwargs):
            backend = self.get_backend(using)

            instance.content = "test filename"


            if backend is not None:
                chain(scrape_text.s(), do_update.s(self, backend))

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated
        """
        return self.get_model().objects.all()


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr="first_name")
    last_name = indexes.CharField(model_attr="last_name")

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated
        """
        return self.get_model().objects.all()
