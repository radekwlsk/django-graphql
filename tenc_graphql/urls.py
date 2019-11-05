from django.conf.urls import url
from graphene_django.views import GraphQLView

from .views import PrivateGraphQLView
from .settings import graphql_settings

view_class = PrivateGraphQLView if graphql_settings.PROTECTED_URL else GraphQLView

urlpatterns = [
    url(rf'^{graphql_settings.URL_PATH}$', view_class.as_view(graphiql=True), name=graphql_settings.URL_NAME)
]
