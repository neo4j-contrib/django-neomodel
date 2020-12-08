from django.test.testcases import TestCase as DjangoTestCase
from django.forms.models import ModelForm
import django
django.setup()
from tests.someapp.models import Book
from django import forms

GEEKS_CHOICES =(('available', 'A'),
            ('on_loan', 'L'),
            ('damaged', 'D'),)


class BookForm(ModelForm):
    status = forms.ChoiceField(choices=GEEKS_CHOICES, initial='available', required=False)

    class Meta:
        model = Book
        fields = ('title', 'status', 'format')


class UpdateBookStatusForm(ModelForm):
    status = forms.ChoiceField(choices=GEEKS_CHOICES,initial='available', required=False)

    class Meta:
        model = Book
        fields = ('title', 'status')


class BookFormTest(DjangoTestCase):

    def test_define(self):
        self.assertTrue(issubclass(BookForm, ModelForm))

    def test_define_update(self):
        self.assertTrue(issubclass(UpdateBookStatusForm, ModelForm))

    def test_can_validate(self):
        bf = BookForm(data={'title': 'Harry Potter 3', 'format': 'P'})
        self.assertTrue(bf.is_valid())

    def test_can_save(self):
        bf = BookForm(data={'title': 'Harry Potter 2', 'format': 'P'})

        self.assertTrue(bf.is_valid())
        bf.save(True)

    def test_unique_is_checked(self):
        BookForm(data={'title': 'book1', 'format': 'P'}).save()
        bf = BookForm(data={'title': 'book1', 'format': 'P'})
        self.assertFalse(bf.is_valid())

    def test_can_update(self):
        hp = Book(title='Harrry', format='P').save()
        bf = BookForm(data={'title': 'Harry Potter', 'status': 'damaged', 'format': 'P'}, instance=hp)
        self.assertTrue(bf.is_valid())
        bf.save(True)

    def test_can_update_subclass(self):
        hp = Book(title='potterr', format='P').save()
        bf = UpdateBookStatusForm(data={'title': 'Hary Potter', 'format': 'P'}, instance=hp)
        self.assertTrue(bf.is_valid())
        bf.save(True)

    def test_can_update_w_out_required_field(self):
        hp = Book(title='Hairy', status='damaged', format='P').save()
        bf = UpdateBookStatusForm(data={'title': 'Hairy', 'status': 'damaged'}, instance=hp)

        self.assertTrue(bf.is_valid())
        bf.save(True)

    def test_can_render(self):
        bf = BookForm(data={'title': 'Harry Potter', 'format': 'P'})
        self.assertIn('Harry Potter', bf.__html__())
        self.assertIn('<select', bf.__html__())

    def test_choices(self):
        bf = BookForm(data={'title': 'Select1', 'status': 'damaged', 'format': 'P'})
        self.assertTrue(bf.is_valid())
        book = bf.save()
        self.assertEqual(book.status, 'damaged')

    def test_invalid_choice(self):
        bf = BookForm(data={'title': 'Select1', 'status': 'Damaged'})
        self.assertFalse(bf.is_valid())