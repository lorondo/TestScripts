class Recipe:
  all_ingredients = []

  def __init__(self, name, cooking_time, difficulty):
    self.name = name
    self.ingredients = []
    self.cooking_time = cooking_time
    self.difficulty = None
    self.calculate_difficulty()
  
  def get_name(self):
    return self.name
  
  def set_name(self, new_name):
    self.name = new_name

  def get_cooking_time(self):
    return self.cooking_time

  def set_cooking_time(self, new_cooking_time):
    self.cooking_time = new_cooking_time
    self.calculate_difficulty()

  def get_ingredients(self):
    return self.ingredients

  def get_difficulty(self):
    if self.difficulty is None:
      self.calculate_difficulty()
    return self.difficulty
  
  def calculate_difficulty(self):
    num_ingredients = len(self.ingredients)
    if self.cooking_time < 10 and num_ingredients < 4:
      self.difficulty = "Easy"
    elif self.cooking_time < 10 and num_ingredients >= 4:
      self.difficulty = "Medium"
    elif self.cooking_time >= 10 and num_ingredients < 4:
      self.difficulty = "Intermediate"
    elif self.cooking_time >= 10 and num_ingredients >= 4:
      self.difficulty = "Hard"
  
  def add_ingredients(self, *ingredients):
    for ingredient in ingredients:
      if ingredient not in self.ingredients:
        self.ingredients.append(ingredient)
    self.update_all_ingredients()
    self.calculate_difficulty() 
 
  def search_ingredient(self, ingredient):
    return ingredient in self.ingredients

  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      if ingredient not in Recipe.all_ingredients:
        Recipe.all_ingredients.append(ingredient)

  def __str__(self):
    return f"Recipe: {self.name}\nCooking Time (in minutes): {self.cooking_time}\nIngredients: {', '.join(self.ingredients)}\nDifficulty: {self.difficulty}"
  
  def recipe_search(data, search_term):
    for recipe in data:
      if recipe.search_ingredient(search_term):
        print(recipe)

tea = Recipe("Tea", 5, None)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
print(tea)

coffee = Recipe("Coffee", 5, None)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
print(coffee)

cake = Recipe("Cake", 50, None)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
print(cake)

banana_smoothie = Recipe("Banana Smoothie", 5, None)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

print("\nRecipes with 'Water':")
Recipe.recipe_search(recipes_list, "Water")

print("\nRecipes with 'Sugar':")
Recipe.recipe_search(recipes_list, "Sugar")

print("\nRecipes with 'Bananas':")
Recipe.recipe_search(recipes_list, "Bananas")