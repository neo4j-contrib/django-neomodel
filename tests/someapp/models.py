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
    condition = StringProperty(default='new')  # check fields can be omitted
    format = StringProperty(required=True)  # check required field can be ommitted on update
    title = StringProperty(unique_index=True)
    status = StringProperty(choices=(
            ('Available', 'A'),
            ('On loan', 'L'),
            ('Damaged', 'D'),
        ), default='Available')

    created = DateTimeProperty(default=datetime.utcnow)

    class Meta:
        app_label = 'someapp'