import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.utils.crypto import get_random_string
from django.core.management import execute_from_command_line


class SingleFileApp:
    """
    Class that aids in making a single-file Django app.

    Inspired by Flask, but not trying to be API compatible in the slightest.
    """

    urlpatterns: list

    def __init__(self):
        # Do initial settings configuration
        settings.configure(
            DEBUG=(os.environ.get("DJANGO_DEBUG", "") == "1"),
            ALLOWED_HOSTS=["*"],  # Disable host header validation
            ROOT_URLCONF=__name__,  # Could be fancier with middleware?
            SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY", get_random_string(50)),
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
