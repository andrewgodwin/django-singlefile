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
* **Read-Only Models/Databases**: See the notes below!

# Unsupported Features

If you want to use these, just go make a normal Django project; trying to fit
them into a single file is a bad idea due to their innate complexity.

* Mutable Models/Databases/Migrations
* Admin
* Authentication

# Desired Features

* **Project Conversion**: An easy way to take a single-file app like this and
  expand it into a "full" Django project, like `startproject` would make.

# Using Models

While allowing full mutable models with migrations would be too much for
a single-file project - for that, just use a normal Django project - one nice
way of doing a dynamic site is to pre-compile a read-only SQLite database file
with the content.

This way, you can still use Django models to select data and do queries against
it to display dynamic pages, but you don't have to worry about migrations or
a central database server; thus, this is the only mode that we support.

To use models, do two things:

* Supply a `database_file` argument to the `SingleFileApp` constructor with
  the path to your SQLite database file. It will be opened in read-only mode.

* Define one or more models in your app file. They'll be added to a default
  Django app called `app`; thus, you probably want to specify `db_table` on
  your models unless you want call your tables `app_modelname`.

Here's a basic example:

```
from django.http import HttpResponse
from django.singlefile import SingleFileApp
from django.db import models

app = SingleFileApp(database_file="demo.sqlite3")


class Product(models.Model):

    name = models.TextField()
    category = models.CharField(max_length=255)

    class Meta:
        db_table = "product"


@app.path("")
def index(request):
    return HttpResponse(f"I know about {Product.objects.count()} things!")


if __name__ == "__main__":
    app.main()
```
