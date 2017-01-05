from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


class TestCommands(TestCase):

    def test_install_labels_command(self):
        out = StringIO()
        call_command('install_labels', stdout=out)
        self.assertIn('Creating unique constraint for title on label Book for class tests.someapp.models.Book', out.getvalue())

    def test_clear_neo4j_command(self):
        out = StringIO()
        call_command('clear_neo4j', stdout=out)
        self.assertIn('Done', out.getvalue())