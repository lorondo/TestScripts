recipes_list = []
ingredients_list = []

def take_recipe():
  name = input("Enter the recipe name: ")
  cooking_time = int(input("Enter the cooking time (in minutes): "))
    
  ingredients_input = input("Enter ingredients separated by commas: ") 
  ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")] 
    
  recipe = {
    "name": name,
    "cooking_time": cooking_time, 
    "ingredients": ingredients
  }
  return recipe

n = int(input("How many recipes would you like to enter: "))

for i in range(n):
  recipe = take_recipe()
  
  for ingredient in recipe["ingredients"]:
    if ingredient not in ingredients_list:
      ingredients_list.append(ingredient)
  
  recipes_list.append(recipe)

for recipe in recipes_list:
  num_ingredients = len(recipe["ingredients"])
  cooking_time = recipe["cooking_time"]

  if cooking_time < 10 and num_ingredients < 4:
    difficulty = "Easy"
  elif cooking_time < 10 and num_ingredients >= 4:
    difficulty = "Medium"
  elif cooking_time >= 10 and num_ingredients < 4:
    difficulty = "Intermediate"
  elif cooking_time >= 10 and num_ingredients >= 4:
    difficulty = "Hard" 

  recipe["difficulty"] = difficulty

for recipe in recipes_list:
  print(f"Recipe: <{recipe['name']}")
  print(f"Cooking Time (min):  <{recipe['cooking_time']}")
  print(f"Ingredients:")
  for ingredient in recipe['ingredients']:
    print(f"{ingredient}")
  print(f"Difficulty level: <{recipe['difficulty']}")
  print()

print("Ingredients Available Across All Recipes")
ingredients_list.sort() 
for ingredient in ingredients_list:
  print({ingredient})


  
