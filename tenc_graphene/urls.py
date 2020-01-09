from django.conf.urls import url

from .settings import tenc_graphene_settings
from .views import TencGrapheneView


urlpatterns = [
    url(rf'^{tenc_graphene_settings.URL_PATH}$', TencGrapheneView.as_view(graphiql=True), name=tenc_graphene_settings.URL_NAME)
]
