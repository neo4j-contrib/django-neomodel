from __future__ import absolute_import

from django.test.testcases import TestCase as DjangoTestCase

from tests.someapp.models import Library


class SimpleTest(DjangoTestCase):

    def test_save_model(self):
        thing = Library.objects.create(name=u'Foo')

