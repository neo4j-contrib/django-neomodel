from datetime import datetime

from django.db import models
from django_neomodel import DjangoNode
from neomodel import StringProperty, DateTimeProperty, UniqueIdProperty


class Library(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        app_label = 'someapp'


class Book(DjangoNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True)
    format = StringProperty(required=True)  # check required field can be omitted on update
    status = StringProperty(choices=(
            ('available', 'A'),
            ('on_loan', 'L'),
            ('damaged', 'D'),
        ), default='available', coerce=str)
    created = DateTimeProperty(default=datetime.utcnow)

    class Meta:
        app_label = 'someapp'
