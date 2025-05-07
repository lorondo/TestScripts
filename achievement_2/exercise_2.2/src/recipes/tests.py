from django.test import TestCase
from .models import Recipe
# Create your tests here.
class RecipeModelTest(TestCase):
  def setUpTestData():
    Recipe.objects.create(
      name='Top Ramen', 
      ingredients='Top ramen packet, boiling water', 
      cooking_time=10, 
      difficulty='easy'
      )
  
  def test_recipe_name_max_length(self):
    recipe = Recipe.objects.get(recipe_id=1)
    max_length = recipe._meta.get_field('name').max_length
    self.assertEqual(max_length, 120)
  
  def test_difficulty_choices(self):
    field = Recipe._meta.get_field('difficulty')
    expected_choices = (
      ('easy', 'Easy'),
      ('medium', 'Medium'),
      ('intermediate', 'Intermediate'),
      ('hard', 'Hard'),
    )
    self.assertEqual(field.choices, expected_choices)