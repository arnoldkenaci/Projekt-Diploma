
from django.test import TestCase
from .forms import IngredientForm

class IngredientFormTest(TestCase):
	def test_invalid_data(self):
		form = IngredientForm(data={})
		self.assertFalse(form.is_valid())
		self.assertIn('name', form.errors)
		self.assertIn('quantity', form.errors)
		self.assertIn('price', form.errors)
