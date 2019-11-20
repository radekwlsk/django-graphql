import pytest

from .utils import override_tenc_graphene_settings


class TestPrivateEndpoint:

    @pytest.mark.django_db
    def test_private_view_protected_authenticated(self, client, user):
        with override_tenc_graphene_settings(PROTECTED_URL=True, DEFAULT_USER_TYPE=True):
            client.force_login(user)

            response = client.post(
                '/graphql/',
                data={'query': """{
                    allUsers{
                        username
                    }
                }
                """},
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 200
            assert 'data' in response.json()

    def test_private_view_protected_unauthenticated(self, settings, client):
        with override_tenc_graphene_settings(PROTECTED_URL=True, DEFAULT_USER_TYPE=True):

            response = client.post(
                '/graphql/',
                data={'query': """{
                    allUsers{
                        username
                    }
                }
                """},
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 302
            assert response['Location'].startswith(settings.LOGIN_URL)

    @pytest.mark.django_db
    def test_private_view_unprotected_unauthenticated(self, client):
        with override_tenc_graphene_settings(PROTECTED_URL=False, DEFAULT_USER_TYPE=True):

            response = client.post(
                '/graphql/',
                data={'query': """{
                    allUsers{
                        username
                    }
                }
                """},
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 200
            assert 'data' in response.json()

