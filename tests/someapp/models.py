from django.db import models
from neomodel import StructuredNode, StringProperty


class Library(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        app_label = 'someapp'


class Book(StructuredNode):
    title = StringProperty(unique_index=True)