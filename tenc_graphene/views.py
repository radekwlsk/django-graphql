from django.contrib.auth.mixins import AccessMixin
from graphene_django.views import GraphQLView

from .settings import tenc_graphene_settings


class TencGrapheneView(AccessMixin, GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        if tenc_graphene_settings.PROTECTED_URL and not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
