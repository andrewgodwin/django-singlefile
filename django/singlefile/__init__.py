import os
import sys
import inspect

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

    def __init__(self, template_directory="templates"):
        # Figure out project root directory via some... shenanigans
        previous_filename = inspect.getframeinfo(inspect.currentframe().f_back)[0]
        self.root_directory = os.path.dirname(previous_filename)
        # Do initial settings configuration
        envsettings = EnvironmentSettings()
        settings.configure(
            DEBUG=envsettings.get_bool("DJANGO_DEBUG"),
            ALLOWED_HOSTS=["*"],  # Disable host header validation
            ROOT_URLCONF=__name__,  # Could be fancier with middleware?
            SECRET_KEY=envsettings.get("DJANGO_SECRET_KEY", get_random_string(50)),
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [os.path.join(self.root_directory, template_directory)],
                },
            ],
        )
        self.urlpatterns = []
        self.app = get_wsgi_application()

    def path(self, route: str):
        """
        Decorator that adds a url pattern
        """

        def inner(view):
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


# This gets set by the app __init__
urlpatterns = []
