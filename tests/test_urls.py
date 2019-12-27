import pytest
from django.urls import resolve

from .utils import override_tenc_graphene_settings


class TestUserURLs:

    def test_foo_url_path(self):
        with override_tenc_graphene_settings(URL_PATH='foo/'):
            from tenc_graphene.views import TencGrapheneView
            found = resolve('/graphql/foo/')
            assert found.func.view_class == TencGrapheneView

    def test_empty_url_path(self):
        with override_tenc_graphene_settings(URL_PATH=''):
            from tenc_graphene.views import TencGrapheneView
            found = resolve('/graphql/')
            assert found.func.view_class == TencGrapheneView

