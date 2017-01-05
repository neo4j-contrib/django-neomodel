from django.db.models import signals
from django.test.testcases import TestCase as DjangoTestCase

from neomodel import StructuredNode, StringProperty

SENT_SIGNAL = {}
HOOK_CALLED = {}


class Emitter(StructuredNode):
    name = StringProperty()

    def pre_save(self):
        HOOK_CALLED['pre_save'] = True


def pre_save(sender, instance, signal):
    SENT_SIGNAL['pre_save'] = True
signals.pre_save.connect(pre_save, sender=Emitter)


def post_save(sender, instance, signal):
    SENT_SIGNAL['post_save'] = True
signals.post_save.connect(post_save, sender=Emitter)


def pre_delete(sender, instance, signal):
    SENT_SIGNAL['pre_delete'] = True
signals.pre_delete.connect(pre_delete, sender=Emitter)


def post_delete(sender, instance, signal):
    SENT_SIGNAL['post_delete'] = True
signals.post_delete.connect(post_delete, sender=Emitter)


class SignalsTest(DjangoTestCase):

    def test_signals(self):
        test = Emitter(name=1).save()
        assert 'post_save' in SENT_SIGNAL
        assert 'pre_save' in SENT_SIGNAL
        assert 'pre_save' in HOOK_CALLED

        test.delete()
        assert 'post_delete' in SENT_SIGNAL
        assert 'pre_delete' in SENT_SIGNAL
