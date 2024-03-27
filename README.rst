django-singlefile
=================

This is a small library that makes it easier to write single-file Django
applications in a similar way to how you'd write Flask applications.

It's still alpha; in particular, I'd like to:

 - Add some more environment variable overrides for settings
 - Add in some basic database support

But hey, it's a fun start.


Example App
-----------

::

    from django.http import HttpResponse
    from django.singlefile import SingleFileApp

    app = SingleFileApp()


    @app.path("")
    def index(request):
        name = request.GET.get("name", "World")
        return HttpResponse(f"Hello, {name}!")


    if __name__ == "__main__":
        app.main()


To run the app, you can just call it from the command line::

    python app.py runserver

Or you can pass the `app` object inside it to a WSGI server as normal!
