from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy import or_

# Create engine object to connect to database
engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

# Declarative base class stored in variable called Base
Base = declarative_base()

# Create session object to make changes to database
Session = sessionmaker(bind=engine)
session = Session()

# Define Recipe Model
class Recipe(Base):
  __tablename__ = "final_recipes"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  # Quick recipe info
  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + " - Name: " + self.name + " - Difficulty: " + self.difficulty + ">"
  
  # Full recipe printout
  def __str__(self):
        output = "\nRecipe: " + str(self.name) + \
            "\nIngredients: " + str(self.ingredients) + \
            "\nCooking Time: " + str(self.cooking_time) + " minutes" + \
            "\nDifficulty: " + str(self.difficulty) + \
            "\n" + "-"*20 
        return output
  
  # Calculates recipe difficulty
  def calculate_difficulty(self):
    ingredient_list = self.ingredients.split(',') 
    ingredient_list = [item.strip() for item in ingredient_list]
    num_ingredients = len(ingredient_list)
    if self.cooking_time < 10 and num_ingredients < 4:
        self.difficulty = "Easy"
    elif self.cooking_time < 10 and num_ingredients >= 4:
        self.difficulty = "Medium"
    elif self.cooking_time >= 10 and num_ingredients < 4:
        self.difficulty = "Intermediate"
    elif self.cooking_time >= 10 and num_ingredients >= 4:
        self.difficulty = "Hard"
  
  # Returns ingredients as a list
  def return_ingredients_as_list(self):
    if self.ingredients == "":
      return []
    else:
      return [item.strip() for item in self.ingredients.split(',')]

# Creates the table on the database
Base.metadata.create_all(engine)

def create_recipe():
  # Collects and checks recipe name
  while True:
    name = input("Enter the name of the recipe: ")
    if len(name) > 50:
       print("Hark! The recipe name cannot be longer than 50 characters. Please try again.")
    elif not name.isalpha():
       print("Hark! The recipe name can only be comprised of alphabetical characters. Please try again.")
    else:
       break
  
  # Collects and checks cooking time
  while True:
    cooking_time_input = input("Enter the cooking time (in minutes): ")
    if not cooking_time_input.isnumeric():
       print("Hark! The cooking time can only be represented by a number. Please try again.")
    else:
       cooking_time = int(cooking_time_input)
       break
  
  # Collects ingredients
  ingredients = []
  while True:
    try:
      num_ingredients = int(input("How many ingredients are in this recipe? "))
      break
    except ValueError:
       print("Please enter a valid number.")

  for i in range(num_ingredients):
    ingredient = input(f"Enter ingredient {i + 1}: ")
    ingredients.append(ingredient.strip())

  ingredients_str = ", ".join(ingredients)

  # Creates recipe object
  recipe_entry = Recipe(
     name=name,
     ingredients=ingredients_str,
     cooking_time=cooking_time,
  )

  # Calculates difficulty
  recipe_entry.calculate_difficulty()

  # Adds to database
  session.add(recipe_entry)
  session.commit()
  print("Recipe successfully added!\n")

# Function to view all recipes
def view_all_recipes():
   all_recipes = session.query(Recipe).all()
   if not all_recipes:
      print("There are no recipe entries in your database.")
      return None
   else:
      for recipe in all_recipes:
        print(recipe)
        print("") 

# Search by ingredients
def search_by_ingredients():
  # Checks if table has entries
  if session.query(Recipe).count() == 0:
    print("Your table has no recipe entries!")
    return

  # Retrieves and stores values from ingredients column  
  results = session.query(Recipe.ingredients).all()

  # Initialize ingredients list  
  all_ingredients = []
    
  # Go through results entries 
  for row in results:
    ingredients_string = row[0] 
    ingredients = ingredients_string.split(', ')

    # Check each ingredient is unique before adding
    for item in ingredients:
        if item not in all_ingredients:
          all_ingredients.append(item)

  # Display ingredients, each ingredient is numbered
  for index, item in enumerate(all_ingredients, start=1):
    print(f"{index}.{item}")

  # Asking user which ingredient they would like to search for recipes
  try:
    input_selection = input("Pick ingredients by number (separated by spaces): ")
    selected_index = [int(i) -1 for i in input_selection.split()]

    # Check the user's inputs match the options available
    if all(0 <= index < len(all_ingredients) for index in selected_index):
      search_ingredients = [all_ingredients[index] for index in selected_index]
      print(f"You chose: {','.join(search_ingredients)}")

      # Initialize empty list called conditions
      conditions = []

      for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))
      
      # Retrieves all recipes from database
      matching_recipes = session.query(Recipe).filter(or_(*conditions)).all()

      if matching_recipes:
         print("\nMatching Recipes:")
         for recipe in matching_recipes:
            print(recipe)
      else:
         print("No recipes were found.")

  except ValueError:
        print("Please enter valid numbers.")

# Edits recipe
def edit_recipe():
  # Checks if table has entries
  if session.query(Recipe).count() == 0:
    print("Your table has no recipe entries!")
    return

  # Retrieves and stores id and name from each recipe in database
  results = session.query(Recipe.id, Recipe.name).all()

  # From each item in results, display the recipes available
  for row in results:
    print(f"ID: {row[0]} | Name: {row[1]}")
    print()
  
  # User picks recipe by id
  try:
    recipe_id = int(input("Enter the ID of the recipe you want to update: "))
  except ValueError:
    print("Invalid ID")
    return

  # Retrieves entire recipe that corresponds to id
  recipe_to_edit = session.query(Recipe).filter_by(id=recipe_id).first()
  if recipe_to_edit is None:
     print("Recipe not found.")
     return
  
  # Display recipe info
  options = [
     ("Name", recipe_to_edit.name),
     ("Ingredients", recipe_to_edit.ingredients),
     ("Cooking Time", f"{recipe_to_edit.cooking_time} minutes")
  ]

  print(f"\nWhich part of the recipe would you like to edit?:")
  for i, (label, value) in enumerate(options, start=1):
    print(f"{i}. {label}: {value}")
  
  # Ask the user to choose which attribute they would like to edit
  try:
    choice = int(input("Enter the number of the field you want to edit: "))
    if choice == 1:
       new_name = input("Enter new name: ")
       recipe_to_edit.name = new_name
    elif choice == 2:
       new_ingredients = input("Enter new ingredients: ")
       recipe_to_edit.ingredients = new_ingredients
    elif choice == 3:
       new_cooking_time = int(input("Enter new cooking time (in minutes): "))
       recipe_to_edit.cooking_time = new_cooking_time
    else:
       print("Invalid choice.")
       return

    recipe_to_edit.calculate_difficulty()

    session.commit()
  except ValueError:
     print("Invalid input.")

# Deletes recipes
def delete_recipe():
  if session.query(Recipe).count() == 0:
    print("Your table has no recipe entries!")
    return

  # Retrieves and stores id and name from each recipe in database
  results = session.query(Recipe.id, Recipe.name).all()

  # From each item in results, display the recipes available
  for row in results:
    print(f"ID: {row[0]} | Name: {row[1]}")
    print()
  
  # User picks recipe by id
  try:
    recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
  except ValueError:
    print("Invalid ID")
    return
  
  recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).first()
  if recipe_to_delete is None:
     print("Recipe not found.")
     return

  user_permission = input("Are you sure you want to delete this recipe? (Yes or No) ")
  if user_permission.strip().lower() == "yes":
     session.delete(recipe_to_delete)
     session.commit()
     print("Recipe deleted.")
  else:
    print("Deletion canceled.")
    return

def main_menu():
  choice = ''
# Main menu loop, loops as long as the user doesn't choose to quit
  while(choice != 'quit'):
    print("\nWhat would you like to do? Pick a choice!")
    print("1. Create a new recipe")
    print("2. View all recipes")
    print("3. Search for a recipe by ingredient")
    print("4. Update an existing recipe")
    print("5. Delete a recipe")
    print("Type 'quit' to exit the program.")
    choice = input("Your choice: ")

    if choice == '1':
      create_recipe()
    elif choice == '2':
      view_all_recipes()
    elif choice == '3':
      search_by_ingredients()
    elif choice == '4':
      edit_recipe()
    elif choice == '5':
      delete_recipe()
    elif choice.lower() == 'quit':
      print("Goodbye!")
      session.commit()
      session.close()
      break
    else:
      print("Invalid choice, try again.")

# run program
main_menu()
