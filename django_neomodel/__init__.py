from functools import total_ordering

from django.db.models import signals
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.base import ModelState
from django.db.models import ManyToManyField

from django.conf import settings
from django.forms import fields as form_fields
from django.forms import ModelMultipleChoiceField as form_ModelMultipleChoiceField 
from django.db.models.options import Options
from django.core.exceptions import ValidationError 

from neomodel import RequiredProperty, DeflateError, StructuredNode, UniqueIdProperty, AliasProperty, UniqueProperty 
from neomodel.core import NodeMeta
from neomodel.match import NodeSet
from neomodel.cardinality import OneOrMore, One, ZeroOrOne, ZeroOrMore

from types import SimpleNamespace
from django.apps import apps as current_apps

# Need to following to get the relationships to work
RECURSIVE_RELATIONSHIP_CONSTANT = 'self'

from django.db.models.fields.related import resolve_relation, RECURSIVE_RELATIONSHIP_CONSTANT, lazy_related_operation
from django.db.models.utils import make_model_tuple
from functools import partial


__author__ = 'Robin Edwards'
__email__ = 'robin.ge@gmail.com'
__license__ = 'MIT'
__package__ = 'django_neomodel'
__version__ = '0.0.6'


default_app_config = 'django_neomodel.apps.NeomodelConfig'


def classproperty(f):
    class cpf(object):
        def __init__(self, getter):
            self.getter = getter

        def __get__(self, obj, type=None):
            return self.getter(type)
    return cpf(f)


class NOT_PROVIDED:
    pass


class DjangoFormFieldMultipleChoice(form_fields.MultipleChoiceField):
    """ Sublcass of Djangos MultipleChoiceField but without working validator """
    def validate(self, value):
        return True 


class DjangoFormFieldTypedChoice(form_fields.TypedChoiceField):
    """ Sublcass of Djangos TypedChoiceField but without working validator """
    def validate(self, value):
        return True


@total_ordering
class DjangoBaseField(object):
    """ Base field where Properties and Relations Field should subclass from """

    is_relation = False
    concrete = True
    editable = True
    creation_counter = 0
    unique = False
    primary_key = False
    auto_created = False

    # Then from class RelatedField(FieldCacheMixin, Field): see https://docs.djangoproject.com/en/2.0/_modules/django/db/models/fields/related/
    # Field flags
    one_to_many = None
    one_to_one = None
    many_to_many = None
    many_to_one = None
   
    creation_counter = 0

    def __init__(self):
        self.creation_counter = DjangoBaseField.creation_counter
        DjangoBaseField.creation_counter += 1

    def __eq__(self, other):
        # Needed for @total_ordering
        if isinstance(other, DjangoBaseField):
            return self.creation_counter == other.creation_counter
        return NotImplemented

    def __lt__(self, other):
        # This is needed because bisect does not take a comparison function.
        if isinstance(other, DjangoBaseField):
            return self.creation_counter < other.creation_counter
        return NotImplemented

    def has_default(self):
        return self._has_default

    def to_python(self, value):
        return value

    def __hash__(self):
        # The delete function in the Admin requires a hash
        return hash(self.creation_counter)

    def clone(self):
        return self
    

class DjangoEmptyField(DjangoBaseField):
    """ Empty  field """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remote_field = None
        

class DjangoPropertyField(DjangoBaseField):
    """
    Fake Django model field object which wraps a neomodel Property
    """
    is_relation = False
    concrete = True
    editable = True   
    unique = False
    primary_key = False
    auto_created = False

    def __init__(self, prop, name):
        self.prop = prop
        self.name = name
        self.remote_field = name
        self.remote_field = None
        self.attname = name
        self.verbose_name = name
        self.help_text = getattr(prop, 'help_text', '')

        if isinstance(prop, UniqueIdProperty):
            # this seems that can be implemented in neomodel
            # django-neomodel does have the needed code already but neomodel does not support
            prop.primary_key = True

        self.primary_key = getattr(prop, 'primary_key', False)
        self.label = prop.label if prop.label else name

        form_cls = getattr(prop, 'form_field_class', 'Field')  # get field string
        self.form_class = getattr(form_fields, form_cls, form_fields.CharField)

        self._has_default = prop.has_default
        self.required = prop.required
        self.blank = not self.required
        self.choices = getattr(prop, 'choices', None)

        super().__init__()

    def save_form_data(self, instance, data):
        setattr(instance, self.name, data)

    def value_from_object(self, instance):
        return getattr(instance, self.name)

    def formfield(self, **kwargs):
        """
        Returns a django.forms.Field instance for this database Property.

        """
        defaults = {'required': self.required,
                    'label': self.label or self.name,
                    'help_text': self.help_text}

        if self.has_default():
                defaults['initial'] = self.prop.default_value()

        if self.choices:
            # Fields with choices get special treatment.
            include_blank = (not self.required or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)
            defaults['coerce'] = self.to_python

            # Many of the subclass-specific formfield arguments (min_value,
            # max_value) don't apply for choice fields, so be sure to only pass
            # the values that TypedChoiceField will understand.
            for k in list(kwargs):
                if k not in ('coerce', 'empty_value', 'choices', 'required',
                             'widget', 'label', 'initial', 'help_text',
                             'error_messages', 'show_hidden_initial'):
                    del kwargs[k]

        defaults.update(kwargs)
        return self.form_class(**defaults)

    def get_choices(self, include_blank=True):
        blank_defined = False
        blank_choice = BLANK_CHOICE_DASH
        choices = list(self.choices) if self.choices else []
        if issubclass(type(self.choices), dict):
            # Ensure list of tuples with proper key-value pairing
            choices = [(k, v) for k, v in self.choices.items()] 
        for choice, __ in choices:
            if choice in ('', None):
                blank_defined = True
                break

        first_choice = (blank_choice if include_blank and
                        not blank_defined else [])
        return first_choice + choices

    def clone(self):
        return self


class DjangoRemoteField(object):
    """ Fake RemoteField to let the Django Admin work """

    def __init__(self, name):
        # Fake this call https://github.com/django/django/blob/ac5cc6cf01463d90aa333d5f6f046c311019827b/django/contrib/admin/widgets.py#L278
        self.related_name = name 
        self.related_query_name = name
        self.model = name
        self.through = SimpleNamespace(_meta=SimpleNamespace(auto_created=True))
    
    def get_related_field(self):
        # Fake call https://github.com/django/django/blob/ac5cc6cf01463d90aa333d5f6f046c311019827b/django/contrib/admin/widgets.py#L282
        # from the Django Admin
        return SimpleNamespace(name=self.model.pk.target)
       

class DjangoRelationField(DjangoBaseField):
    """
    Fake Django model field object which wraps a neomodel Relationship
    """
    one_to_many = False
    one_to_one = False
    many_to_one = False

    many_to_many = True

    @property
    def __class__(self):
        # Fake the class for 
        # https://github.com/django/django/blob/ac5cc6cf01463d90aa333d5f6f046c311019827b/django/contrib/admin/options.py#L144
        # so we can get the admin ManyToMany field widgets to work
        return ManyToManyField

    def __init__(self, prop, name):
        self.prop = prop
        self.choices = None 
        
        self.required = False
        if prop.manager is OneOrMore or prop.manager is One:
            self.required = True

        self.blank = False 
       
        # See https://docs.djangoproject.com/en/2.0/_modules/django/db/models/fields/
        # Need a way to signal that there is no default
        self._has_default = NOT_PROVIDED

        self.name = name
        self.attname = name
        self.verbose_name = name
        self.help_text = getattr(prop, 'help_text', '')
        
        if prop.manager is ZeroOrOne: 
            # This form_class has its validator set to True
            self.form_class = DjangoFormFieldTypedChoice
        else:
            # This form_class has its validator set to True
            self.form_class = DjangoFormFieldMultipleChoice 
    
        # Need to load the related model in so we can fetch
        # all nodes. 
        self.remote_field = DjangoRemoteField(self.prop._raw_class)

        super().__init__()

    def set_attributes_from_rel(self):
        """ From https://github.com/django/django/blob/1be99e4e0a590d9a008da49e8e3b118b57e14075/django/db/models/fields/related.py#L393 """
        self.name = (
            self.name or
            (self.remote_field.model._meta.model_name + '_' + self.remote_field.model._meta.pk.name)
        )
        if self.verbose_name is None:
            self.verbose_name = self.remote_field.model._meta.verbose_name
        # self.remote_field.set_field_name()

    def do_related_class(self, other, cls):
        """ from https://github.com/django/django/blob/1be99e4e0a590d9a008da49e8e3b118b57e14075/django/db/models/fields/related.py#L402 """
        self.set_attributes_from_rel()
        # self.contribute_to_related_class(other, self.remote_field)

    def value_from_object(self, instance):
        instance_relation = getattr(instance, self.name)
        node_ids_selected = []
        for this_object in instance_relation.all():
            node_ids_selected.append(this_object.pk)
        return node_ids_selected
   
    def save_form_data(self, instance, data):
        # instance is the current node which needs to get connected
        # data is a list of ids/uids of the nodes-to-connect-to

        instance_relation = getattr(instance, self.name)
        # Need to define which nodes to disconnect from first!

        related_model = current_apps.get_model(self.prop.module_name.split('.')[-2],
            self.prop._raw_class)

        all_possible_nodes = related_model.nodes.all()
        
        # Gather the pks from these nodes
        list_of_ids = []
        for this_node in all_possible_nodes:
            list_of_ids.append(this_node.pk)
        # So which nodes are not selected?
        should_not_be_connected = set(list_of_ids) - set(data)
       
        # Need to save the instance before relations can be made
        try:
            instance.save()
        except UniqueProperty as e:
            raise ValidationError(e)  
        # Cardinality needs to be observed, so use following order:
        # if One: replace
        # if OneOreMore: first connect, then disconnect
        # if ZeroOrMore: doesn't matter
        # if ZeroOrOne: First disconnect, then connect
     
        if self.prop.manager is ZeroOrMore or self.prop.manager is ZeroOrOne:
            # Instead of checking the relationship exists, just disconnect 
            # In the future when specific relationships are implemented, this
            # should be updated
            self._disconnect_node(should_not_be_connected, instance_relation)

            # Now time to setup new connections
            if data:  # In case we selected an empty unit, don't do anything 
                self._connect_node(data, instance_relation)
        
        elif self.prop.manager is OneOrMore:
            # First setup new connections
            self._connect_node(data, instance_relation)
            try:
                instance.save()
            except UniqueProperty as e:
                raise ValidationError(e)  
        
            # Instead of checking the relationship exists, just disconnect 
            self._disconnect_node(should_not_be_connected, instance_relation)
        else:
            # This would require replacing the current relation with a new one
            raise NotImplementedError('Cardinality of One is not supported yet')

    def _disconnect_node(self, should_not_be_connected, instance_relation):
        """ Given a list pk's, remove the relationship """

        related_model = current_apps.get_model(self.prop.module_name.split('.')[-2],
            self.prop._raw_class)

        # Internals used by save_form_data to 
        # TODO: first get list of connected nodes, so don't run lots of disconnects
        for this_object in should_not_be_connected:
            remover = related_model.nodes.get_or_none(pk=this_object)
            if remover:
                instance_relation.disconnect(remover)

    def _connect_node(self, data, instance_relation):
        """ Given a list pk's, add the relationship """

        related_model = current_apps.get_model(self.prop.module_name.split('.')[-2],
            self.prop._raw_class)

        # If ChoiceField, it is not a list
        data = [data] if not isinstance(data, list) else data  
        
        for this_object in data:
            # Retreive the node-to-connect-to
            adder = related_model.nodes.get_or_none(pk=this_object)
            # If the connection is there, leave it
            if not adder:
                raise ValidationError({self.name: ' not found'})

            if not instance_relation.is_connected(adder):
                instance_relation.connect(adder)
   
    def formfield(self, *args, **kwargs):
        """Return a django.forms.Field instance for this field."""
        
        node_options = []

        # Fetch the related_module from the apps registry (instead of circular imports)
        related_model = current_apps.get_model(self.prop.module_name.split('.')[-2],
            self.prop._raw_class)

        if self.prop.manager is ZeroOrOne:
            node_options = BLANK_CHOICE_DASH.copy()
   
        for this_object in related_model.nodes.all():
            node_options.append((this_object.pk, this_object.__str__))

        defaults = {'required': self.required,
                    'label': self.verbose_name,
                    'help_text': self.help_text,
                    **kwargs,
                    }

        defaults['choices'] = node_options
        return self.form_class(**defaults)

    def clone(self):
        """ 
        Upon cloning a relationship, provide an empty field wrapper, so circular
        imports are prevented by the Django app registry
        """

        return DjangoEmptyField()

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        """ Modified from https://github.com/django/django/blob/2a66c102d9c674fadab252a28d8def32a8b626ec/django/db/models/fields/related.py#L305 """
        #super().contribute_to_class(cls, name, private_only=private_only, **kwargs)
        self.opts = cls._meta

        if not cls._meta.abstract:
            if self.remote_field.related_name:
                related_name = self.remote_field.related_name
            else:
                related_name = self.opts.default_related_name
            if related_name:
                related_name = related_name % {
                    'class': cls.__name__.lower(),
                    'model_name': cls._meta.model_name.lower(),
                    'app_label': cls._meta.app_label.lower()
                }
                self.remote_field.related_name = related_name

            if self.remote_field.related_query_name:
                related_query_name = self.remote_field.related_query_name % {
                    'class': cls.__name__.lower(),
                    'app_label': cls._meta.app_label.lower(),
                }
                self.remote_field.related_query_name = related_query_name

            def resolve_related_class(model, related, field):
                field.remote_field.model = related
                field.do_related_class(related, model)
            lazy_related_operation(resolve_related_class, cls, self.remote_field.model, field=self)


class Query:
    select_related = False
    order_by = ['pk']


class NeoNodeSet(NodeSet):
    query = Query()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self.source
    
    def count(self):
        return len(self)

    def _clone(self):
        return self

    def iterator(self):
        """ Needed to run pytest after adding app/model register """
        return []


class NeoManager:
    def __init__(self, model):
        self.model = model
        
    def get_queryset(self):
        return NeoNodeSet(self.model)

    def using(self, connection):
        """ Needed to run pytest after adding app/model register"""
        return NeoNodeSet(self.model)


class MetaClass(NodeMeta):
    def __new__(cls, *args, **kwargs):
        super_new = super().__new__
        new_cls = super_new(cls, *args, **kwargs)
        setattr(new_cls, "_default_manager", NeoManager(new_cls))

        # Needed to run pytest, after adding app/model register
        setattr(new_cls, "_base_manager", NeoManager(new_cls))

        if new_cls.__module__ is __package__: # Do not populate DjangoNode
            pass
        elif new_cls.__module__.split('.')[-2] == 'tests': # Also skip test signals
            pass
        else:
            
            meta = getattr(new_cls, 'Meta', None)
            current_apps.register_model(new_cls.__module__.split('.')[-2],  new_cls)

        return new_cls


class DjangoNode(StructuredNode, metaclass=MetaClass):
    __abstract_node__ = True
  
    @classproperty
    def _meta(self):

        if hasattr(self.Meta, 'unique_together'):
            raise NotImplementedError('unique_together property not supported by neomodel')

        # Need a ModelState for the admin to delete an object
        self._state = ModelState() 
        self._state.adding = False 

        opts = Options(self.Meta, app_label=self.Meta.app_label)
        opts.contribute_to_class(self, self.__name__)

        # Again, otherwise delete from admin doesn't work, see: 
        # https://github.com/django/django/blob/0e656c02fe945389246f0c08f51c6db4a0849bd2/django/db/models/deletion.py#L252 
        opts.concrete_model = self 

        for key, prop in self.__all_properties__:
            opts.add_field(DjangoPropertyField(prop, key), getattr(prop, 'private', False))
            if getattr(prop, "primary_key", False):
                # a reference using self.pk = prop fails in some cases where
                # django references the .pk attribute directly. ie in 
                # https://github.com/django/django/blob/ac5cc6cf01463d90aa333d5f6f046c311019827b/django/contrib/admin/options.py#L860
                # causes non-consistent behaviour because Django sometimes looks up the 
                # attribute name via 'pk = cl.lookup_opts.pk.attname'.
                # instead provide an AliasProperty to the property tagged
                # as primary_key
                self.pk = AliasProperty(to=key)
        
        for key, relation in self.__all_relationships__:
            new_relation_field = DjangoRelationField(relation, key)
            new_relation_field.contribute_to_class(self, key)
            opts.add_field(new_relation_field, getattr(prop, 'private', False))

        # Need to do some model reloading here ^^

        # Register the model in the Django app registry. 
        # Django will try to clone to make a ModelState and upon cloning
        # the relations will result in an empty object, so there are no
        # circular imports
        #current_apps.register_model(self.__module__.split('.')[-2],  self)
        

        return opts

    @classmethod
    def check(cls, **kwargs):
        """ Needed for app registry, always provide empty list of errors """
        return []

    def __hash__(self):
        # The delete function in the Admin requires a hash
        return hash(self.pk)
   
    def full_clean(self, exclude, validate_unique=False):
        """
        Validate node, on error raising ValidationErrors which can be handled by django forms

        :param exclude:
        :param validate_unique: Check if conflicting node exists in the labels indexes
        :return:
        """

        # validate against neomodel
        try:
            self.deflate(self.__properties__, self)
        except DeflateError as e:
            raise ValidationError({e.property_name: e.msg})
        except RequiredProperty as e:
            raise ValidationError({e.property_name: 'is required'})
        except UniqueProperty as e:
            raise ValidationError({e.property_name: e.msg})  

    def validate_unique(self, exclude):
        # get unique indexed properties
        unique_props = []
        for k, p in self.__class__.defined_properties(aliases=False, rels=False).items():
            if k not in exclude and p.unique_index:
                unique_props.append(k)
        cls = self.__class__

        props = self.__properties__

        # see if any nodes already exist with each property
        for key in unique_props:
            if key == 'pk' and getattr(self.__class__, key).auto_created:
                continue
            val = getattr(self.__class__, key).deflate(props[key])
            node = cls.nodes.get_or_none(**{key: val})

            # if exists and not this node
            if node and node.id != getattr(self, 'id', None):
                raise ValidationError({key, 'already exists'})

    def pre_save(self):
        if getattr(settings, 'NEOMODEL_SIGNALS', True):
            self._creating_node = getattr(self, 'id', None) is None
            signals.pre_save.send(sender=self.__class__, instance=self)

    def post_save(self):
        if getattr(settings, 'NEOMODEL_SIGNALS', True):
            created = self._creating_node
            delattr(self, '_creating_node')
            signals.post_save.send(sender=self.__class__, instance=self, created=created)

    def pre_delete(self):
        if getattr(settings, 'NEOMODEL_SIGNALS', True):
            signals.pre_delete.send(sender=self.__class__, instance=self)

    def post_delete(self):
        if getattr(settings, 'NEOMODEL_SIGNALS', True):
            signals.post_delete.send(sender=self.__class__, instance=self)

    def serializable_value(self, attr):
        return str(getattr(self, attr))
