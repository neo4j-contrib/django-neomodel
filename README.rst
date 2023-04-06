Django Neomodel (beta!)
=======================

.. image:: https://raw.githubusercontent.com/robinedwards/neomodel/master/doc/source/_static/neomodel-300.png
   :alt: neomodel

This module allows you to use the neo4j_ graph database with Django using neomodel_

.. _neo4j: https://www.neo4j.org
.. _neomodel: http://neomodel.readthedocs.org

Warnings
=======================

* Admin functionality is very experimental. `Please see todos / issues here <https://github.com/neo4j-contrib/django-neomodel/projects/1>`_

Live Examples (add yours here)
===============================

* `ResoTrack <https://resotrack.herokuapp.com/>`_

Getting started
===============

Install the module::

    $ pip install django_neomodel

Add the following settings to your `settings.py`::

    NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:foobarbaz@localhost:7687')

    # Make sure django_neomodel comes before your own apps
    INSTALLED_APPS = (
        # django.contrib.auth etc
        'django_neomodel',
        'yourapp'
    )

Write your first node definition in `yourapp/models.py`::

    from neomodel import StructuredNode, StringProperty, DateProperty

    class Book(StructuredNode):
        title = StringProperty(unique_index=True)
        published = DateProperty()

Create any constraints or indexes for your labels. This needs to be done after you change your node definitions
much like `manage.py migrate`::

    $ python manage.py install_labels

Now in a view `yourapp/views.py`::

    from .models import Book

    def get_books(request):
        return render('yourapp/books.html', request, {'books': Book.nodes.all()})

In your `yourapp/admin.py`::

    from django_neomodel import admin as neo_admin
    from .models import Book

    class BookAdmin(dj_admin.ModelAdmin):
        list_display = ("title", "created")
    neo_admin.register(Book, BookAdmin)

And you're ready to go. Don't forget to check the neomodel_ documentation.

Model forms
===========

Switch the base class from `StructuredNode` to `DjangoNode` and add a 'Meta' class::

    from datetime import datetime
    from django_neomodel import DjangoNode
    from neomodel import StructuredNode, StringProperty, DateTimeProperty, UniqueIdProperty

    class Book(DjangoNode):
        uid = UniqueIdProperty()
        title = StringProperty(unique_index=True)
        status = StringProperty(choices=(
                ('Available', 'A'),
                ('On loan', 'L'),
                ('Damaged', 'D'),
            ), default='Available')
        created = DateTimeProperty(default=datetime.utcnow)

        class Meta:
            app_label = 'library'

Create a model form class for your `DjangoNode`::

    class BookForm(ModelForm):
        class Meta:
            model = Book
            fields = ['title', 'status']

This class may now be used just like any other Django form.

Settings
========
The following config options are available in django settings (default values shown).
These are mapped to neomodel.config as django is started::

    NEOMODEL_NEO4J_BOLT_URL = 'bolt://neo4j:neo4j@localhost:7687'
    NEOMODEL_SIGNALS = True
    NEOMODEL_FORCE_TIMEZONE = False
    NEOMODEL_MAX_CONNECTION_POOL_SIZE = 50

Signals
=======
Signals work with `DjangoNode` sub-classes::

    from django.db.models import signals
    from django_neomodel import DjangoNode
    from neomodel import StringProperty

    class Book(DjangoNode):
      title = StringProperty(unique_index=True)

    def your_signal_func(sender, instance, signal, created):
        pass

    signals.post_save.connect(your_signal_func, sender=Book)

The following are supported: `pre_save`, `post_save`, `pre_delete`, `post_delete`.
On freshly created nodes `created=True` in the `post_save` signal argument.

Testing
=======

You can create a setup method which clears the database before executing each test::

    from neomodel import db, clear_neo4j_database

    class YourTestClass(DjangoTestCase):
        def setUp(self):
            clear_neo4j_database(db)

        def test_something(self):
            pass

Management Commands
===================

The following django management commands have been included.

install_labels
--------------
Setup constraints and indexes on labels for your node definitions. This should be executed after any schema changes::

    $ python manage.py install_labels
    Setting up labels and constraints...

    Found tests.someapp.models.Book
    + Creating unique constraint for title on label Book for class tests.someapp.models.Book
    Finished 1 class(es).

clear_neo4j
-----------
Delete all nodes in your database, warning there is no confirmation!

Requirements
============

- Python 3.7+
- neo4j 5.x, 4.4 (LTS)

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/robinedwards/neomodel
   :target: https://gitter.im/robinedwards/neomodel?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Docker Example
===================


Using Docker Compose.

Commands to setup Docker Container docker-entrypoint.sh::

    # Go to tests
    $ cd tests/
    # Docker Command (Make sure Docker is running and up to date)
    $ docker-compose up
    # login in admin with username=admin password=1234

Go to http://localhost:7474/browser/

Go to http://localhost:8000/admin/


Running Tests
===================

Setup Neo4j Desktop with a local database with password 'foobarbaz' and version 5.x or 4.4.x (Neo4j LTS version).

Commands to run tests::

    # create local venv and install dependencies.
    $ pip install -e '.[dev]'; export DJANGO_SETTINGS_MODULE=tests.settings;
    $ tests/manage.py install_labels
    $ tests/manage.py migrate
    $ pytest

    # example output:

    platform darwin -- Python 3.9.0, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
    pick 0900469 Neo4J-update-t-4.1
    collected 16 items

    someapp/tests/test_atomicity.py .                                                                                                                                                                                                                      [  6%]
    someapp/tests/test_commands.py ..                                                                                                                                                                                                                      [ 18%]
    someapp/tests/test_model_form.py ...........                                                                                                                                                                                                           [ 87%]
    someapp/tests/test_sanity.py .                                                                                                                                                                                                                         [ 93%]
    someapp/tests/test_signals.py .
    16 passed, 11 warnings in 1.62s

