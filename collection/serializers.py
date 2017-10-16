"""
Collection Serializers
"""


# Library Imports
# #############################################################################


from django.contrib.auth import get_user_model
from rest_framework.utils import model_meta
from rest_framework.serializers import (
    ModelSerializer,
    JSONField,
    raise_errors_on_nested_writes
)
from rest_framework_json_api.serializers import (
    Serializer,
    CharField,
    DateTimeField
)
from rest_framework_json_api.relations import ResourceRelatedField
from drf_haystack.serializers import HaystackSerializer


# App Imports
# #############################################################################


from collection.models import (
    Collection,
    Item,
    Document,
    CollectionMembership,
    Schema
)

# TODO Use app import so `Workflow` doesn't need to be imported here.
from workflow.models import Workflow

from collection import search_indexes


# Model Serializers
# #############################################################################


class CollectionModelSerializer(ModelSerializer):
    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:
            return ExampleModel.objects.create(**validated_data)
        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:
            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance
        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass.objects.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():

                # If the m2m has a model defined as a through table, then
                # relations cannot be added by that relationship's .add() method,
                # but should be created using the model's constructor.
                # This loop checks to ensure that if the relation does not exist
                # it is created. The way this is set up now, it requires the relation
                # to be unique.
                if field_name in info.relations and info.relations[field_name].has_through_model:
                    field = info.relations[field_name].model_field
                    for related_instance in value:
                        through_class = field.rel.through
                        through_instance = through_class()
                        existing_through_instances = through_class.objects\
                            .filter(**{field.m2m_field_name()+"_id": instance.id})\
                            .filter(**{field.m2m_reverse_field_name()+"_id": related_instance.id})
                        if existing_through_instances.exists():
                            continue
                        setattr(through_instance, field.m2m_field_name(), instance)
                        setattr(through_instance, field.m2m_reverse_field_name(), related_instance)
                        through_instance.save()

                else:
                    field = getattr(instance, field_name)
                    field.set(value)
        return instance

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():

            # If the m2m has a model defined as a through table, then
            # relations cannot be added by that relationship's .add() method,
            # but should be created using the model's constructor.
            # This loop checks to ensure that if the relation does not exist
            # it is created. The way this is set up now, it requires the relation
            # to be unique.
            if attr in info.relations and info.relations[attr].has_through_model:
                field = info.relations[attr].model_field
                for related_instance in value:
                    through_class = field.rel.through
                    through_instance = through_class()
                    existing_through_instances = through_class.objects\
                        .filter(**{field.m2m_field_name()+"_id": instance.id})\
                        .filter(**{field.m2m_reverse_field_name()+"_id": related_instance.id})
                    if existing_through_instances.exists():
                        continue
                    setattr(through_instance, field.m2m_field_name(), instance)
                    setattr(through_instance, field.m2m_reverse_field_name(), related_instance)
                    through_instance.save()

            elif attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)

            else:
                setattr(instance, attr, value)

        instance.save()

        return instance


class CollectionSerializer(CollectionModelSerializer):
    """
    # `collection.serializers.CollectionSerializer`

    The `CollectionSerializer` takes incoming payloads and builds `Collection`
    objects, and takes `Collection` objects and returns payloads.
    """

    id = CharField(read_only=True)
    title = CharField()
    description = CharField(required=False, allow_null=True)
    owner = ResourceRelatedField(
        queryset=get_user_model().objects.all(),
        many=False,
        required=True
    )
    date_created = DateTimeField(read_only=True)
    date_updated = DateTimeField(read_only=True)

    schemas = ResourceRelatedField(
        queryset=Schema.objects.all(),
        many=True,
        required=False
    )

    items = ResourceRelatedField(
        queryset=Item.objects.all(),
        many=True,
        required=False
    )

    workflow = ResourceRelatedField(
        queryset=Workflow.objects.all(),
        many=False,
        required=True
    )

    collection_memberships =  ResourceRelatedField(
        queryset=CollectionMembership.objects.all(),
        many=True,
        required=False
    )

    documents = ResourceRelatedField(
        queryset=Document.objects.all(),
        many=True,
        required=False
    )


    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "description",
            "page_settings",
            "owner",
            "date_created",
            "date_updated",
            "schemas",
            "items",
            "workflow",
            "collection_memberships",
            "documents"
        ]

    class JSONAPIMeta:
        resource_name = 'collection'


class ItemSerializer(CollectionModelSerializer):
    """
    # `collection.serializers.ItemSerializer`

    Serializer for the `Item` model
    """

    id = CharField(read_only=True)
    title = CharField()
    description = CharField(required=False, allow_null=True)
    owner = ResourceRelatedField(
        queryset=get_user_model().objects.all(),
        many=False,
        required=True
    )
    date_created = DateTimeField(read_only=True)
    date_updated = DateTimeField(read_only=True)

    collections = ResourceRelatedField(
        queryset=Collection.objects.all(),
        many=True,
        required=False
    )

    documents = ResourceRelatedField(
        queryset=Document.objects.all(),
        many=True,
        required=False
    )

    memberships = ResourceRelatedField(
        queryset=CollectionMembership.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "description",
            "type",
            "owner",
            "date_created",
            "date_updated",
            "collections",
            "documents",
            "memberships"
        ]

    class JSONAPIMeta:
        resource_name = 'item'


class DocumentSerializer(CollectionModelSerializer):
    """
    # `collection.serializers.DocumentSerializer`

    Serializer for the `Document` model
    """

    id = CharField(read_only=True)
    content = CharField(required=False, allow_null=True)
    owner = ResourceRelatedField(
        queryset=get_user_model().objects.all(),
        many=False,
        required=True
    )
    date_created = DateTimeField(read_only=True)
    date_updated = DateTimeField(read_only=True)

    memberships = ResourceRelatedField(
        queryset=CollectionMembership.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Document
        fields = [
            "id",
            "content",
            "owner",
            "date_created",
            "date_updated",
            "schema",
            "collections",
            "item",
            "memberships"
        ]

    class JSONAPIMeta:
        resource_name = 'document'


class CollectionMembershipSerializer(CollectionModelSerializer):
    """
    # `collection.serializers.CollectionMembershipSerializer`

    Serializer for the `CollectionMembership` model
    """

    id = CharField(read_only=True)
    label = CharField(required=False, allow_blank=False)
    role = CharField(required=False, allow_blank=False)
    date_created = DateTimeField(read_only=True)
    date_updated = DateTimeField(read_only=True)

    item = ResourceRelatedField(
        queryset=Item.objects.all(),
        many=False,
        required=True
    )

    collection = ResourceRelatedField(
        queryset=Collection.objects.all(),
        many=False,
        required=True
    )

    document = ResourceRelatedField(
        queryset=Document.objects.all(),
        many=False,
        required=True
    )

    class Meta:
        model = CollectionMembership
        fields = [
            "label",
            "role",
            "date_created",
            "date_updated",
            "item",
            "collection",
            "document"
        ]

    class JSONAPIMeta:
        resource_name = "collection-membership"


class SchemaSerializer(CollectionModelSerializer):
    """
    # `collection.serializers.SchemaSerializer`

    Serializer for the `Schema` model
    """

    owner = ResourceRelatedField(
        queryset=get_user_model().objects.all(),
        many=False,
        required=True
    )

    class Meta:
        model = Schema
        fields = [
            "name",
            "definition",
            "owner",
            "date_created",
            "date_updated",
            "documents",
            "items",
            "collections"
        ]

    class JSONAPIMeta:
        resoure_name = "schema"


# Search Serializers for Collections
# #############################################################################


class ItemSearchSerializer(HaystackSerializer):
    """
    # `collection.serializers.ItemSearchSerializer`

    The `ItemSearchSerializer`
    """

    class Meta:
        index_classes = [search_indexes.ItemIndex]
        fields = [
            'text',
            'title',
            'description',
            'created_by',
            'collection'
        ]


class CollectionSearchSerializer(HaystackSerializer):
    """
    # `collection.serializers.CollectionSearchSerializer`

    The `CollectionSearchSerializer`
    """

    class Meta:
        index_classes = [search_indexes.ItemIndex]
        fields = [
            'text',
            'title',
            'description',
            'created_by',
            'collection'
        ]


# EOF
# #############################################################################
