from django.test import TestCase
from neomodel import db, clear_neo4j_database
from django.db import transaction
import django
django.setup()

from tests.someapp.models import Book, Library


class AtomicityTestClass(TestCase):
    def setUp(self):
        clear_neo4j_database(db)

    def test_create_object(self):
        try:
            with transaction.atomic(using="default"):
                with db.transaction:
                    # sql_row
                    Library.objects.create(name="example")
                    # neo4j_node
                    Book(title="example", format="foo").save()
                    raise Exception
        except Exception as e:
            pass

        neo4j_q = Book.nodes.get_or_none(title="example")
        self.assertIsNone(neo4j_q)

        sql_q = Library.objects.filter(name="example").first()
        self.assertIsNone(sql_q)
