from django.utils import timezone
from rest_framework import exceptions
from rest_framework_json_api import serializers
from guardian.shortcuts import assign_perm
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.core.exceptions import ObjectDoesNotExist
from drf_haystack.serializers import HaystackSerializer
from rest_framework_json_api.relations import ResourceRelatedField

from user import search_indexes
from user.models import User
from collection.models import Collection
from workflow.models import Workflow

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    collection = ResourceRelatedField(
        queryset=Collection.objects.all(),
        many=False,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'last_login',
            'is_active',
            'gravatar',
            'token',
            "collection"
        ]

    class JSONAPIMeta:
        resource_name = 'users'

    def get_token(self, obj):
        if not obj.id:
            return None
        try:
            account = SocialAccount.objects.get(user=obj)
            token = SocialToken.objects.get(account=account).token
        except ObjectDoesNotExist:
            return None
        return token


class UserSearchSerializer(HaystackSerializer):

    class Meta:
        index_classes = [search_indexes.UserIndex]
        fields = [
            'text',
            'first_name',
            'last_name',
            'email',
            'full_name'
        ]


# EOF
# #############################################################################
