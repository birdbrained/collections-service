from haystack import indexes
from django.contrib.auth.models import User

from collection.models import Collection, Item


class CollectionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='title')
    created_by = indexes.CharField(model_attr='created_by')

    def get_model(self):
        return Collection

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated
        """
        return self.get_model().objects.all()


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    created_by = indexes.CharField(model_attr='created_by__full_name')
    collection = indexes.CharField(model_attr='collection__pk')

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated
        """
        return self.get_model().objects.all()


