import pickle

# Function to take user input and return a recipe dictionary
def take_recipe():
  name = input("Enter the recipe name: ")
  cooking_time = int(input("Enter the cooking time (in minutes): "))
  ingredients_input = input("Enter ingredients separated by commas: ")
  ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]
  difficulty = calc_difficulty(cooking_time, ingredients)
      
  recipe = {
    "name": name,
    "cooking_time": cooking_time,
    "ingredients": ingredients,
    "difficulty": difficulty
  }
      
  return recipe

# Function to determine recipe difficulty
def calc_difficulty(cooking_time, ingredients):
  num_ingredients = len(ingredients)

  if cooking_time < 10 and num_ingredients < 4:
    difficulty = "Easy"
  elif cooking_time < 10 and num_ingredients >= 4:
    difficulty = "Medium"
  elif cooking_time >= 10 and num_ingredients < 4:
    difficulty = "Intermediate"
  elif cooking_time >= 10 and num_ingredients >= 4:
    difficulty = "Hard"
  
  return difficulty

# File loading / data initialization
file_name = input("Enter binary file name")

try:
  with open(file_name, 'rb') as file:
    data = pickle.load(file_name)
  print("Data loaded successfully!")
except FileNotFoundError:
  print("File not found. Creating a new data dictionary.")
  data = {
    "recipes_list": [],
    "all_ingredients": []
  }
except Exception as e: 
  print(f"An unexpected error occurred: {e}")
  print("Creating a new data dictionary.")
  data = {
    "recipes_list": [],
    "all_ingredients": []
  }
else: 
  file.close()
finally:
  recipes_list = data["recipes_list"]
  all_ingredients = data["all_ingredients"]

# Get recipes from user input
n = int(input("How many recipes would you like to enter: "))

for i in range(n):
  recipe = take_recipe()
  
  for ingredient in recipe["ingredients"]:
    if ingredient not in all_ingredients:
      all_ingredients.append(ingredient)
  
  recipes_list.append(recipe)

# Save updated data back to file
data["recipes_list"] = recipes_list
data["all_ingredients"] = all_ingredients

with open(file_name, 'wb') as file:
  pickle.dump(data, file)


