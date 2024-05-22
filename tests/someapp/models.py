from datetime import datetime

from django.db import models
from django_neomodel import DjangoNode 
from neomodel import StringProperty, DateTimeProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, AliasProperty, StructuredRel
from neomodel.sync_.cardinality import OneOrMore, ZeroOrOne


class Library(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        app_label = 'someapp'


class BaseRel(StructuredRel):
    """ A simple relationship that stores timestqmps as properties on the relationship """


    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    group_id = StringProperty()
    
    def pre_save(self):
        self.updated_at = datetime.utcnow()
    def post_save(self):
        pass

class Author(DjangoNode):
    unique_id = UniqueIdProperty(primary_key=True)
    name = StringProperty()
    wrote = RelationshipTo('Book','WROTE',model=BaseRel)

    class Meta:
        app_label = "someapp"

    def __str__(self):
        return self.name

class Book(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    title = StringProperty(unique_index=True, help_text="Catchy title of the book")
    format = StringProperty(required=True)  # check required field can be omitted on update
    
    status = StringProperty(choices=(
            ('available', 'A'),
            ('on_loan', 'L'),
            ('damaged', 'D'),
        ), default='available', coerce=str)
    created = DateTimeProperty(default=datetime.utcnow)

    # A book can only be stored in one shelf, thus ZeroOrOne
    shelf = RelationshipTo('Shelf', 'STORED_IN',cardinality=ZeroOrOne)  
    
    #A book can be written by multiple authors, so the default ZeroOrMore 
    # applies. As example this relationship has a model with properties: BaseRel
    authored_by = RelationshipFrom('Author','WROTE', model=BaseRel) 

    class Meta:
        app_label = "someapp"

    def __str__(self):
        return self.title


class Shelf(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    name = StringProperty()
    contains = RelationshipFrom('Book','STORED_IN')

    class Meta:
        app_label = "someapp"

    def __str__(self):
        return self.name
