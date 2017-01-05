Django Neomodel - Neo4j for Django
==================================

WORK IN PROGRESS
================

.. image:: https://raw.githubusercontent.com/robinedwards/neomodel/master/doc/source/_static/neomodel-300.png
   :alt: neomodel

This module allows you to use the neo4j_ graph database with Django using neomodel_

.. _neo4j: https://www.neo4j.org
.. _neomodel: http://neomodel.readthedocs.org

Settings
========
The following settings are available with default value shown::

   NEOMODEL_NEO4J_BOLT_URL = 'bolt://neo4j:neo4j@localhost:7687'
   NEOMODEL_SIGNALS = True

Signals
=======
Signals work as expected with `StructuredNode` sub-classes::

    from django.db.models import signals
    from neomodel import StructuredNode, StringProperty

    class Book(StructuredNode):
      title = StringProperty(unique_index=True)

    signals.post_save.connect(your_func, sender=Library)


Management Commands
===================

The following django management commands have been included.

install_labels
--------------
Setup constraints and indexes on labels to match your node definitions. This should be executed after any schema changes::

   $ python manage.py install_all_labels
   Setting up labels and constraints...

   + Creating unique constraint for title on label Book for class tests.someapp.models.Book
   tests.someapp.models.Book done.
   Finished.

clear_neo4j
-----------
Delete all nodes in your database, warning there is no confirmation!

Requirements
============

- Python 2.7, 3.3+
- neo4j 3.0+

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/robinedwards/neomodel
   :target: https://gitter.im/robinedwards/neomodel?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
