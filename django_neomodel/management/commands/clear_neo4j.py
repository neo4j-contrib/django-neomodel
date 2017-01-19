from django.core.management.base import BaseCommand

from neomodel import db, clear_neo4j_database


class Command(BaseCommand):
    help = 'Clear the neo4j database'

    def handle(self, *args, **options):
        self.stdout.write('Deleting all nodes..\n')
        clear_neo4j_database(db)
        self.stdout.write('Done.\n')