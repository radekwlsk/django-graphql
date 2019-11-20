import pytest
from django.urls import resolve

from tenc_graphene.views import TencGrapheneView
from .utils import override_tenc_graphene_settings


class TestUserURLs:

    def test_foo_url_path(self):
        with override_tenc_graphene_settings(URL_PATH='foo/'):
            found = resolve('/graphql/foo/')
            assert found.func.view_class == TencGrapheneView

    def test_empty_url_path(self):
        with override_tenc_graphene_settings(URL_PATH=''):
            found = resolve('/graphql/')
            assert found.func.view_class == TencGrapheneView

