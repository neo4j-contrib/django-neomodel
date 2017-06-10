from functools import total_ordering

from django.db.models import signals
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings
from django.forms import fields
from django.db.models.options import Options
from django.core.exceptions import ValidationError

from neomodel import RequiredProperty, DeflateError, StructuredNode


__author__ = 'Robin Edwards'
__email__ = 'robin.ge@gmail.com'
__license__ = 'MIT'
__package__ = 'django_neomodel'
__version__ = '0.0.4'


default_app_config = 'django_neomodel.apps.NeomodelConfig'


def classproperty(f):
    class cpf(object):
        def __init__(self, getter):
            self.getter = getter

        def __get__(self, obj, type=None):
            return self.getter(type)
    return cpf(f)


@total_ordering
class DjangoField(object):
    """
    Fake Django model field object which wraps a neomodel Property
    """
    is_relation = False
    concrete = True
    editable = True
    creation_counter = 0

    def __init__(self, prop, name):
        self.prop = prop

        self.name = name
        self.help_text = getattr(prop, 'help_text', '')
        self.primary_key = getattr(prop, 'primary_key', False)
        self.label = prop.label if prop.label else name

        form_cls = getattr(prop, 'form_field_class', 'Field')  # get field string
        self.form_class = getattr(fields, form_cls, fields.CharField)

        self._has_default = prop.has_default
        self.required = prop.required
        self.blank = not self.required
        self.choices = getattr(prop, 'choices', None)

        self.creation_counter = DjangoField.creation_counter
        DjangoField.creation_counter += 1

    def __eq__(self, other):
        # Needed for @total_ordering
        if isinstance(other, DjangoField):
            return self.creation_counter == other.creation_counter
        return NotImplemented

    def __lt__(self, other):
        # This is needed because bisect does not take a comparison function.
        if isinstance(other, DjangoField):
            return self.creation_counter < other.creation_counter
        return NotImplemented

    def has_default(self):
        return self._has_default

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

    def to_python(self, value):
        return value

    def get_choices(self, include_blank=True):
        blank_defined = False
        blank_choice = BLANK_CHOICE_DASH
        choices = list(self.choices) if self.choices else []
        for choice, __ in choices:
            if choice in ('', None):
                blank_defined = True
                break

        first_choice = (blank_choice if include_blank and
                        not blank_defined else [])
        return first_choice + choices


class DjangoNode(StructuredNode):
    __abstract_node__ = True

    @classproperty
    def _meta(self):
        if hasattr(self.Meta, 'unique_together'):
            raise NotImplementedError('unique_together property not supported by neomodel')

        opts = Options(self.Meta, app_label=self.Meta.app_label)
        opts.contribute_to_class(self.__class__, self.__class__.__name__)

        for key, prop in self.__all_properties__:
            opts.add_field(DjangoField(prop, key), getattr(prop, 'private', False))

        return opts

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

