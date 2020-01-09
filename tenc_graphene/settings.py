from django.conf import settings
from django.core.signals import setting_changed
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from graphene_django.settings import GrapheneSettings

USER_SETTINGS = getattr(settings, 'TENC_GRAPHENE', None)

DEFAULTS = {
    'PROTECTED_URL': False,
    'URL_PATH': '',
    'URL_NAME': 'graphql',
    'DEFAULT_USER_TYPE': True,
    'DEFAULT_USER_EXCLUDE': [],
}

IMPORT_STRINGS = []

REMOVED_SETTINGS = []


class TencGrapheneSettings(GrapheneSettings):  # pragma: no cover

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            for setting in REMOVED_SETTINGS:
                if setting in user_settings:
                    raise RuntimeError(format_lazy(
                        _("The '{}' setting has been removed. Please refer to docs for available settings."),
                        setting,
                    ))
            if 'DEFAULT_USER_EXCLUDE' in user_settings and 'password' not in user_settings['DEFAULT_USER_EXCLUDE']:
                user_settings['DEFAULT_USER_EXCLUDE'] += ('password',)
        super().__init__(user_settings=user_settings, defaults=defaults, import_strings=import_strings)


tenc_graphene_settings = TencGrapheneSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_graphql_settings(*args, **kwargs):  # pragma: no cover
    global tenc_graphene_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'TENC_GRAPHENE':
        tenc_graphene_settings = TencGrapheneSettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_graphql_settings)
