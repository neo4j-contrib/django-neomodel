from datetime import datetime

from django.db import models
from django_neomodel import DjangoNode
from neomodel import StringProperty, DateTimeProperty


class Library(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        app_label = 'someapp'


class Book(DjangoNode):
    title = StringProperty(unique_index=True)
    created = DateTimeProperty(default=datetime.utcnow)

    class Meta:
        app_label = 'someapp'