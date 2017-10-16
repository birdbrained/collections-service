from django.conf import settings
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.helpers import ActionForm

from user.models import User

from collection.admin import (
    AdminForm,
    add_admins
)



class CollectionUserAdmin(UserAdmin):
    model = get_user_model()
    action_form = AdminForm
    actions = [add_admins]


admin.site.register(User, CollectionUserAdmin)


# EOF
# #############################################################################
