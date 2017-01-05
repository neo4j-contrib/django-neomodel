WORK IN PROGRESS
================

TODO
====

2. signals integration
3. management commands: change password?
4. test utils w transaction / reset
5. django debug tool bar interop (w rest interface)
6. model form integration

.. image:: https://raw.githubusercontent.com/robinedwards/neomodel/master/doc/source/_static/neomodel-300.png
   :alt: neomodel

Allows you to use the neo4j_ graph database through neomodel_ with Django.

.. _neo4j: https://www.neo4j.org
.. _neomodel: http://neomodel.readthedocs.org

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
