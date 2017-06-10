from django.test.testcases import TestCase as DjangoTestCase
from django.forms import ModelForm
from tests.someapp.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'status', 'format']


class UpdateBookStatusForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'status']


class ModelFormTest(DjangoTestCase):

    def test_define(self):
        self.assertTrue(issubclass(BookForm, ModelForm))

    def test_can_validate(self):
        bf = BookForm(data={'title': 'Harry Potter 3', 'format': 'P'})
        self.assertTrue(bf.is_valid())

    def test_can_save(self):
        bf = BookForm(data={'title': 'Harry Potter 2', 'format': 'P'})
        bf.save(True)

    def test_unique_is_checked(self):
        BookForm(data={'title': 'book1', 'format': 'P'}).save()
        self.assertFalse(BookForm(data={'title': 'book1', 'format': 'P'}).is_valid())

    def test_can_update(self):
        hp = Book(title='Harrry', format='P').save()
        bf = BookForm(data={'title': 'Harry Potter', 'format': 'P'}, instance=hp)
        bf.save(True)

    def test_can_update_w_out_required_field(self):
        hp = Book(title='Hairy', format='P').save()
        bf = UpdateBookStatusForm(data={'title': 'Hairy', 'status': 'Damaged'}, instance=hp)
        bf.save(True)

    def test_can_render(self):
        bf = BookForm(data={'title': 'Harry Potter', 'format': 'P'})
        self.assertIn('Harry Potter', bf.__html__())
        self.assertIn('<select', bf.__html__())

    def test_choices(self):
        bf = BookForm(data={'title': 'Select1', 'status': 'Damaged', 'format': 'P'})
        self.assertTrue(bf.is_valid())
        book = bf.save()
        self.assertEqual(book.status, 'Damaged')

    def test_invalid_choice(self):
        bf = BookForm(data={'title': 'Select1', 'status': 'D'})
        self.assertFalse(bf.is_valid())