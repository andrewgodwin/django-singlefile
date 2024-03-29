# django-singlefile

[![PyPI](https://img.shields.io/pypi/v/django-singlefile.svg)](https://pypi.python.org/pypi/django-singlefile)

This is a small library that makes it easier to write single-file Django
applications in a similar way to how you'd write Flask applications.

It's still alpha, but hey, it works for small projects.


## Example App

```
from django.http import HttpResponse
from django.singlefile import SingleFileApp

app = SingleFileApp()


@app.path("")
def index(request):
    name = request.GET.get("name", "World")
    return HttpResponse(f"Hello, {name}!")


if __name__ == "__main__":
    app.main()
```

To run the app, you can just call it from the command line::

    python app.py runserver

Or you can pass the `app` object inside it to a WSGI server as normal!

If you'd like to see a more in-depth example app, take a look at the project
I initially wrote this for: [andrewgodwin/emf-equipment](https://github.com/andrewgodwin/emf-equipment/).


# Supported Features

* **Templates**: Put them in a `templates/` directory.
* **Static Files**: Put them in a `static/` directory.
* **Class-Based Views**: Work fine; use `@app.path()` on the class itself.
* **Forms**: Use them as normal.

# Unsupported Features

If you want to use these, just go make a normal Django project; trying to fit
them into a single file is a bad idea due to their innate complexity.

* Models/Migrations (maybe in future, if I can figure out how nicely)
* Admin
* Authentication
