import pytest
from django.test import override_settings

from .utils import override_tenc_graphene_settings


@pytest.mark.django_db
class TestDefaultUserType:
    query_data = {'query': """{
        allUsers{
            username
        }
    }
    """}

    def test_default_user_type_disabled(self, client, user):
        client.force_login(user)

        with override_tenc_graphene_settings(DEFAULT_USER_TYPE=False):
            response = client.post(
                '/graphql/',
                data=self.query_data,
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 400
            assert 'errors' in response.json()
            errors = map(lambda e: e['message'], response.json()['errors'])
            assert 'Cannot query field "allUsers" on type "Query".' in errors

    def test_default_user_type_enabled(self, client, user):
        client.force_login(user)

        with override_tenc_graphene_settings(DEFAULT_USER_TYPE=True):
            response = client.post(
                '/graphql/',
                data=self.query_data,
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 200
            data = response.json()['data']
            assert 'allUsers' in data


@pytest.mark.django_db
class TestDjangoSettingsQuery:

    @pytest.mark.parametrize("debug_flag", (True, False))
    def test_debug(self, client, user, debug_flag):
        client.force_login(user)

        with override_settings(DEBUG=debug_flag):
            response = client.post(
                '/graphql/',
                data={'query': """{
                    djangoSettings{
                        debug
                    }
                }
                """},
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 200
            data = response.json()['data']
            assert 'djangoSettings' in data
            assert data['djangoSettings']['debug'] == debug_flag

    @pytest.mark.parametrize("timezone_value", ("UTC", "Europe/Warsaw"))
    def test_timezone(self, client, user, timezone_value):
        client.force_login(user)

        with override_settings(TIME_ZONE=timezone_value):
            response = client.post(
                '/graphql/',
                data={'query': """{
                    djangoSettings{
                        timezone
                    }
                }
                """},
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 200
            data = response.json()['data']
            assert 'djangoSettings' in data
            assert response.json()['data']['djangoSettings']['timezone'] == timezone_value


@pytest.mark.django_db
class TestUserQuery:
    def test_all_users(self, client, user):
        client.force_login(user)

        with override_tenc_graphene_settings(DEFAULT_USER_TYPE=True):
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
            data = response.json()['data']
            assert 'allUsers' in data
            all_users = data['allUsers']
            assert isinstance(all_users, list)
            assert len(all_users) == 1
            assert all_users[0]['username'] == user.username

    def test_user(self, client, user):
        client.force_login(user)

        with override_tenc_graphene_settings(DEFAULT_USER_TYPE=True):
            response = client.post(
                '/graphql/',
                data={'query': f"""{{
                    user(id: "{user.id}"){{
                        username
                    }}
                }}
                """},
                headers={'Content-Type': 'application/json'}
            )

            assert response.status_code == 200
            data = response.json()['data']
            assert 'user' in data
            assert data['user']['username'] == user.username
