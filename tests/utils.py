import contextlib
import sys
from importlib import reload, import_module

from django.conf import settings
from django.urls import clear_url_caches
from graphene_django.settings import graphene_settings
from tenc_graphene.settings import tenc_graphene_settings


@contextlib.contextmanager
def override_graphene_settings(**settings):
    return _override_settings(graphene_settings, **settings)


@contextlib.contextmanager
def override_tenc_graphene_settings(**settings):
    return _override_settings(tenc_graphene_settings, callback_before=reload_urls, callback_after=reload_urls,
                              **settings)


def _override_settings(settings_module, callback_before=None, callback_after=None, **settings):
    old_settings = {}

    for k, v in settings.items():
        # Save settings
        try:
            old_settings[k] = settings_module.user_settings[k]
        except KeyError:
            pass

        # Install temporary settings
        settings_module.user_settings[k] = v

        # Delete any cached settings
        try:
            delattr(settings_module, k)
        except AttributeError:
            pass

    if callable(callback_before):
        callback_before()

    yield

    for k in settings.keys():
        # Delete temporary settings
        settings_module.user_settings.pop(k)

        # Restore saved settings
        try:
            settings_module.user_settings[k] = old_settings[k]
        except KeyError:
            pass

        # Delete any cached settings
        try:
            delattr(settings_module, k)
        except AttributeError:
            pass

    if callable(callback_after):
        callback_after()


def reload_urls(urlconf=None):
    from tenc_graphene import urls, settings as tenc_graphene_settings
    clear_url_caches()
    reload(tenc_graphene_settings)
    reload(urls)
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
    else:
        import_module(urlconf)
