from django.contrib.auth import get_user_model
from graphene import Field, List, String
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


if tenc_graphene_settings.DEFAULT_USER_TYPE:
    class TencGrapheneQuery(UsersQuery):
        pass
else:
    class TencGrapheneQuery(object):
        pass
