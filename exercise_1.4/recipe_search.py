import pickle

def display_recipe(recipe):
  print(f"Recipe: {recipe['name']}")
  print(f"Cooking Time (min):  {recipe['cooking_time']}")
  print(f"Ingredients:")
  for ingredient in recipe['ingredients']:
    print(f"{ingredient}")
  print(f"Difficulty level: {recipe['difficulty']}")

def search_ingredient(data):
  # Access all_ingredients from data dictionary
  all_ingredients = data["all_ingredients"]

  # Print enumerated list
  print("All Ingredients:")
  for index, ingredient in enumerate(all_ingredients, start=1):
    print(f"{index}. {ingredient}")
  
  try:
    ingredient_number = int(input("Enter the number of the ingredient you want to search for: "))

    # Retrieve ingredient
    ingredient_searched = all_ingredients[ingredient_number - 1]
    print(f"\nSearching for recipes containing: {ingredient_searched}")
  
  except ValueError:
    print("Invalid input. Please enter a number matching an ingredient.")

  else:
    found_recipes = []
    for recipe in data["recipes_list"]:
      if ingredient_searched in recipe["ingredients"]:
        found_recipes.append(recipe)
    
    if found_recipes:
      print(f"\nFound {len(found_recipes)} recipe(s) containing '{ingredient_searched}':\n")
      for recipe in found_recipes:
        display_recipe(recipe)
        print("-" * 30)

file_name = input("Enter the recipe file name: ")

try:
  with open(file_name, 'rb') as file:
    data = pickle.load(file)
  print("Data loaded successfully!")

except FileNotFoundError:
  print("File not found. Please check the file name and try again.")

else:
  search_ingredient(data)
