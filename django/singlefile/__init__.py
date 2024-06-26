import os
import sys
import inspect

from django.apps import AppConfig
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.utils.crypto import get_random_string
from django.core.management import execute_from_command_line
from django.singlefile.environment import EnvironmentSettings


class SingleFileApp:
    """
    Class that aids in making a single-file Django app.

    Inspired by Flask, but not trying to be API compatible in the slightest.
    """

    urlpatterns: list

    def __init__(
        self,
        template_directory: str = "templates",
        static_directory: str = "static",
        ssl_header: str | None = None,
        installed_apps: list[str] | None = None,
        database_file: str | None = None,
    ):
        # Figure out project root directory via some... shenanigans
        previous_frame = inspect.currentframe().f_back
        previous_filename = inspect.getframeinfo(previous_frame)[0]
        previous_module_name = previous_frame.f_globals["__name__"]
        self.root_directory = os.path.dirname(previous_filename)

        # Prepare settings
        envsettings = EnvironmentSettings()
        settings_values = {
            "DEBUG": envsettings.get_bool("DJANGO_DEBUG"),
            "ALLOWED_HOSTS": ["*"],  # Disable host header validation
            "ROOT_URLCONF": __name__,  # Could be fancier with middleware?
            "SECRET_KEY": envsettings.get("DJANGO_SECRET_KEY", get_random_string(50)),
            "TEMPLATES": [
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [os.path.join(self.root_directory, template_directory)],
                },
            ],
            "STATIC_URL": "static/",
            "STATIC_ROOT": os.path.join(self.root_directory, static_directory),
            "MIDDLEWARE": [
                "django.middleware.security.SecurityMiddleware",
                "whitenoise.middleware.WhiteNoiseMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.middleware.clickjacking.XFrameOptionsMiddleware",
            ],
            "SECURE_PROXY_SSL_HEADER": (ssl_header, "https") if ssl_header else None,
            "INSTALLED_APPS": [
                SingleFileAppConfig(self.root_directory, previous_module_name)
            ]
            + (installed_apps or []),
            "DEFAULT_AUTO_FIELD": "django.db.models.BigAutoField",
        }

        # Add database if needed
        if database_file:
            settings_values["DATABASES"] = {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": f"file:{database_file}?mode=ro",
                }
            }

        # Finish setting up Django
        settings.configure(**settings_values)
        self.urlpatterns = []
        self.app = get_wsgi_application()

    def path(self, route: str):
        """
        Decorator that adds a url pattern
        """

        def inner(view):
            # Ensure we dispatch class-based views correctly
            if hasattr(view, "as_view"):
                self.add_urlpattern(path(route, view.as_view()))
            else:
                self.add_urlpattern(path(route, view))
            return view

        return inner

    def __call__(self, environ, start_response):
        """
        WSGI entrypoint
        """
        return self.app(environ, start_response)

    def add_urlpattern(self, pattern):
        """
        Adds a urlpattern and ensures the global variable matches
        """
        global urlpatterns
        self.urlpatterns.append(pattern)
        urlpatterns = self.urlpatterns

    def main(self):
        """
        Dispatch point - has to be called for now.
        """
        execute_from_command_line(sys.argv)


class SingleFileAppConfig(AppConfig):

    def __init__(self, path: str, module_name: str):
        self.name = module_name
        self.module = sys.modules[module_name]
        self.label = "app"
        self.path = path


# This gets set by the app __init__
urlpatterns = []
