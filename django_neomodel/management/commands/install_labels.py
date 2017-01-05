from django.core.management.base import BaseCommand

from neomodel import install_all_labels


class Command(BaseCommand):
    help = 'Install labels and constraints for your neo4j database'

    def handle(self, *args, **options):
        install_all_labels(stdout=self.stdout)