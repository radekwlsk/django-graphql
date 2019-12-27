from django.conf import settings
from django.contrib.auth import get_user_model
from graphene import Field, List, String, ObjectType, Boolean
from graphene_django import DjangoObjectType

from .settings import tenc_graphene_settings

user_model = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = user_model
        exclude = tenc_graphene_settings.DEFAULT_USER_EXCLUDE


class UsersQuery(object):
    user = Field(type=UserType, id=String(required=True))
    all_users = List(of_type=UserType)

    def resolve_user(self, info, id, **kwargs):
        return user_model.objects.get(pk=id)

    def resolve_all_users(self, info, **kwargs):
        return user_model.objects.all()


class DjangoSettingsType(ObjectType):
    debug = Boolean()
    timezone = String()

    def resolve_debug(self, info, **kwargs):
        return getattr(settings, 'DEBUG', False)

    def resolve_timezone(self, info, **kwargs):
        return getattr(settings, 'TIME_ZONE', 'n/a')


class DjangoSettingsQuery(object):
    django_settings = Field(type=DjangoSettingsType)

    def resolve_django_settings(self, info, **kwargs):
        return DjangoSettingsType()


if tenc_graphene_settings.DEFAULT_USER_TYPE:
    class TencGrapheneQuery(
        DjangoSettingsQuery,
        UsersQuery,
    ):
        pass
else:
    class TencGrapheneQuery(
        DjangoSettingsQuery,
    ):
        pass
