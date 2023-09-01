from django.core.management.base import BaseCommand

from ._remove_labels import remove_all_labels
from neomodel import install_all_labels



class Command(BaseCommand):
    help = 'Install labels and constraints for your neo4j database'

    def handle(self, *args, **options):
        remove_all_labels()
        install_all_labels()



