class Recipe:
  def __init__(self, name, ingredients, cooking_time, difficulty):
    self.name = name
    self.ingredients = ingredients
    self.cooking_time = cooking_time
    self.difficulty = None
    self.calculate_difficulty()
  
  def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(self.ingredients)

    if cooking_time < 10 and num_ingredients < 4:
      self.difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
      self.difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
      self.difficulty = "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
      self.difficulty = "Hard"
 
