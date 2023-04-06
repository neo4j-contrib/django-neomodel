from django.test.testcases import TestCase as DjangoTestCase
from django.forms.models import ModelForm
import django
django.setup()
from tests.someapp.models import Book, Author, Shelf
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

from neomodel import db, clear_neo4j_database
  
from django.apps import AppConfig, apps

GEEKS_CHOICES =(('available', 'A'),
            ('on_loan', 'L'),
            ('damaged', 'D'),)


class BookForm(ModelForm):
    status = forms.ChoiceField(choices=GEEKS_CHOICES, initial='available', required=False)

    class Meta:
        model = Book
        fields = ('title', 'status', 'format', 'authored_by', 'shelf')


class UpdateBookStatusForm(ModelForm):
    status = forms.ChoiceField(choices=GEEKS_CHOICES,initial='available', required=False)

    class Meta:
        model = Book
        fields = ('title', 'status', 'authored_by')


class BookFormTest(DjangoTestCase):

    def setUp(self):
        pass 
        # clear_neo4j_database(db)

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
        bf = BookForm(data={'title': 'Harry Potter the New One', 'status': 'damaged', 'format': 'P'}, instance=hp)
        self.assertTrue(bf.is_valid())
        bf.save(True)

    def test_can_update_subclass(self):
        hp = Book(title='potterr', format='P').save()
        bf = UpdateBookStatusForm(data={'title': 'Hary Potter', 'format': 'P','status':'damaged'}, instance=hp)
        self.assertTrue(bf.is_valid())
        bf.save(True)

    def test_can_update_w_out_required_field(self):
        hp = Book(title='Hairy', status='damaged', format='P').save()
        bf = UpdateBookStatusForm(data={'title': 'Hairy', 'status': 'damaged'}, instance=hp)

        self.assertTrue(bf.is_valid())
        bf.save(True)

    def test_can_render(self):
        
        author_ageta = Author(name='Ageta').save()
        author_jk = Author(name='JK').save()
        author_medea = Author(name='Medea').save()
        
        shelf_drama = Shelf(name='Drama').save()
        shelf_travel = Shelf(name='Travel').save()

        # Need a new form, otherwise the choices don't load
        class BookForm2(ModelForm):
            status = forms.ChoiceField(choices=GEEKS_CHOICES, initial='available', required=False)

            class Meta:
                model = Book

                fields = ('title', 'status', 'format', 'authored_by', 'shelf')
         
        bf = BookForm2(data={'title': 'Harry Potter', 'format': 'P'})
        
        self.assertIn('Harry Potter', bf.__html__())
        self.assertIn('<select name="status"', bf.__html__())
       
        # The multi choices lists for authored_by 
        self.assertIn('<select name="authored_by" id="id_authored_by" multiple', bf.__html__())
        
        # Check possible authers are listed
        
        self.assertIn(author_ageta.pk + '">Ageta</option>', bf.__html__())
        self.assertIn(author_jk.pk + '">JK</option>', bf.__html__())
        self.assertIn(author_medea.pk + '">Medea</option>', bf.__html__())
        
        # Emtpy value should NOT be present in the MultiChoiceField of ZeroOrMore
        self.assertNotIn(BLANK_CHOICE_DASH[0], bf.fields['authored_by']._choices)
        
        # The single choice list for shelf 
        self.assertIn('<select name="shelf" id="id_shelf">', bf.__html__())

        # Test shelve options

        self.assertIn(shelf_drama.pk + '">Drama</option>', bf.__html__())
        self.assertIn(shelf_travel.pk + '">Travel</option>', bf.__html__())
       
        # Emtpy value should be present in the TypedChoiceField of ZeroOrOne
        self.assertIn(BLANK_CHOICE_DASH[0], bf.fields['shelf']._choices)
        
        # Also make sure the empty value is present in the HTML (not limited 
        # to the specific shelf field though.
        self.assertIn(BLANK_CHOICE_DASH[0][1], bf.__html__())

        # Next test also show the right one is 'selected'
        book_instance = Book(title='Harry Potter 308', format='P').save()
        
        book_instance.shelf.connect(shelf_drama)
        book_instance.authored_by.connect(author_jk)
        book_instance.authored_by.connect(author_medea)

        book_instance.save()

        bf = BookForm2(instance=book_instance) 
        self.assertIn(author_ageta.pk + '">Ageta</option>', bf.__html__())
        self.assertIn(author_jk.pk + '" selected>JK</option>', bf.__html__())
        self.assertIn(author_medea.pk + '" selected>Medea</option>', bf.__html__())
        
        self.assertIn(shelf_drama.pk + '" selected>Drama</option>', bf.__html__())
        self.assertIn(shelf_travel.pk + '">Travel</option>', bf.__html__())
        
    def test_choices(self):
        bf = BookForm(data={'title': 'Select1', 'status': 'damaged', 'format': 'P'})
        self.assertTrue(bf.is_valid())
        book = bf.save()
        self.assertEqual(book.status, 'damaged')

    def test_invalid_choice(self):
        bf = BookForm(data={'title': 'Select3', 'status': 'Damaged', 'format': 'P'})
        self.assertFalse(bf.is_valid())
   
    def test_book_by_author(self):
        author_patrick = Author(name='Patrick').save()
        bf = BookForm(data={'title': 'Written by Patrick', 'status': 'damaged', 
                            'format': 'P', 'authored_by' : [author_patrick.pk]})
       
        self.assertTrue(bf.is_valid())
        
        book = bf.save()
        self.assertEqual(book.status, 'damaged')
        self.assertEqual(author_patrick.name, 'Patrick')
        self.assertEqual(book.authored_by.all(), [author_patrick])
        
    def test_book_by_invalid_author(self):
        bf = BookForm(data={'title': 'Written by Kees', 'status': 'damaged',
                            'format': 'P', 'authored_by': ['notavalidpk']})

        self.assertFalse(bf.is_valid())
        
    def test_can_update_book_with_relationship(self):
        """
        Start with a Book and add Authors and remove them again 
        """

        hp = Book(title='potterr', format='P').save()

        author_hera = Author(name='Hera').save()
        author_jason = Author(name='Jason').save()
        
        # Set Hera as Author of the book
        bf = UpdateBookStatusForm(data={'title': 'Hary Potter has an author!', 
                                        'format': 'P', 'status': 'damaged',
                                        'authored_by': [author_hera.pk]}, instance=hp)

        self.assertTrue(bf.is_valid())
        bf.save(True)
        
        self.assertEqual(hp.authored_by.all(),[author_hera])
        
        # Now make Jason also author
        bf = UpdateBookStatusForm(data={'title': 'Hary Potter has an author!', 
                                        'format': 'P', 'status': 'damaged',
                                        'authored_by': [author_hera.pk, author_jason.pk]}, instance=hp)
        self.assertTrue(bf.is_valid())
        bf.save(True)
        self.assertEqual(set([hp.authored_by.all()[0].pk, hp.authored_by.all()[1].pk]),
            set([author_hera.pk, author_jason.pk]))
        
        # This will fail if object can't be hashed
        self.assertEqual(set(hp.authored_by.all()), 
            set([author_hera, author_jason]))
        
        # And remove both as author
        bf = UpdateBookStatusForm(data={'title': 'Hary Potter has an author!', 
                                        'format': 'P', 'status': 'damaged', 
                                        'authored_by': []}, instance=hp)
        self.assertTrue(bf.is_valid())
        bf.save(True)
        self.assertEqual(hp.authored_by.all(), [])
    
    def test_book_with_single_shelf(self):
        """
        A book can only be put nowhere or in one shelf (ZeroOrOne)
        """
        shelf_fiction = Shelf(name='fiction').save()
        bf = BookForm(data={'title': 'A book with a lot of fantasy', 
                            'status': 'damaged', 'format': 'P', 
                            'shelf': shelf_fiction.pk})
       
        self.assertTrue(bf.is_valid())
        book = bf.save()
        self.assertEqual(book.status, 'damaged')
        self.assertEqual(shelf_fiction.name, 'fiction')
        self.assertEqual(book.shelf.all(), [shelf_fiction])
    
    def test_book_with_two_shelfs_invalid(self):
        """
        A book can only be put nowhere or in one shelf (ZeroOrOne)
        """
        
        shelf_thriller = Shelf(name='thriller').save()
        shelf_nf = Shelf(name='non-fiction').save()
        
        bf = BookForm(data={'title': 'A book with a lot of truth', 'status': 'damaged', 
                            'format': 'P', 'shelf': [shelf_nf.pk, shelf_thriller]})
      
        # Im working on this test case. It is running the 'not found' validation error
        # but it should already have chooked on receiving 2 pks?! 
        bf.is_valid()
        self.assertFalse(bf.is_valid())

    def test_app_registry(self):
        """
        To parse the relationships, models need to be loaded in the app registry
        """
        #from django.apps.registry import Apps
        
        model_return = apps.get_model('someapp','book')
        self.assertEqual(model_return, Book)


        model_return = apps.get_model('someapp','Author')
        self.assertEqual(model_return, Author)


        model_return = apps.get_model('someapp','Shelf')
        self.assertEqual(model_return, Shelf)

    def test_app_registry_non_model(self):
        import pytest
        with pytest.raises(Exception) as execinfo:
            model_return = apps.get_model('someapp','nonxsitingmodel')
 
        assert execinfo.value.args[0] == "App 'someapp' doesn't have a 'nonxsitingmodel' model."
