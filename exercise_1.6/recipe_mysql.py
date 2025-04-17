import mysql.connector

conn = mysql.connector.connect(
  host='localhost',
  user='cf-python',
  passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute("""
CREATE TABLE If NOT EXISTS Recipes(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50),
  ingredients VARCHAR(255),
  cooking_time INT,
  difficulty VARCHAR(20)
)
""")

def main_menu(conn, cursor):
  choice = ''
  # Calculates recipe difficulty
  def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        return "Hard"

  # Definition for creating a new recipe
  def create_recipe(conn, cursor):
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    ingredients = []
    while True:
      ingredient = input("Enter an ingredient (type 'done' to finish): ")
      if ingredient.lower() == 'done':
        break
      ingredients.append(ingredient.strip())
    
    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_string = ", ".join(ingredients)

    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, ingredients_string, cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    print("Recipe added successfully!")

  # Definition for searching for a recipe by ingredient
  def search_recipe(conn, cursor):
    all_ingredients = []

    # 1. Get all the ingredients
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    # 2. Extract unique ingredients
    for row in results:
      ingredients_string = row[0] 
      ingredients = ingredients_string.split(', ')

      for item in ingredients:
        if item not in all_ingredients:
          all_ingredients.append(item)
    
    # 3. Display numbered ingredients
    for index, item in enumerate(all_ingredients, start=1):
      print(f"{index}. {item}")
          
    # 4. Get user selection
    try:
        selected_index = int(input("Pick an ingredient by number: ")) - 1
        if 0 <= selected_index < len(all_ingredients):
          search_ingredient = all_ingredients[selected_index]
          print(f"You chose: {search_ingredient}")

          # 5. Search database for recipes with that ingredient
          sql = "SELECT name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s"
          val = f"%{search_ingredient}%"
          cursor.execute(sql, (val,))
          matching_recipes = cursor.fetchall()

          if matching_recipes:
            print("\nMatching Recipes:")
            for recipe in matching_recipes:
              print(f"Name: {recipe[0]}")
              print(f"Ingredients: {recipe[1]}")
              print(f"Cooking Time: {recipe[2]} minutes")
              print(f"Difficulty: {recipe[3]}\n")

          else:
            print("No recipes found with that ingredient.")
        
        else:
          print("That number is out of range.")  
      except ValueError:
        print("Please enter a valid number.")

  # Definition for updating a recipe
  def update_recipe(conn, cursor):
    # fetch all recipes
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    
    # list recipes to user
    for row in results:
      print(f"ID: {row[0]}")
      print(f"Name: {row[1]}")
      print(f"Ingredients: {row[2]}")
      print(f"Cooking Time: {row[3]} minutes")
      print(f"Difficulty: {row[4]}")
      print()
      
    # select recipe by id
    try:
      recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    except ValueError:
      print("Invalid ID")
      return
    
    # select column to update
    column = input("Which field would you like to update? (name, cooking_time, ingredients)")
    if column not in ["name", "cooking_time", "ingredients"]:
        print("Invalid column choice.")
        return
    
    # get the new value
    new_value = input(f"Enter the new value for {column}: ").strip()

    # Update query
    if column == "cooking_time":
      try:
        new_value_int = int(new_value)
      except ValueError:
        print("Cooking time must be a number.")
        return
      cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_value_int, recipe_id))
    elif column == "ingredients":
      cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_value, recipe_id))
    else: # name
      cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_value, recipe_id))

    # Recalculates difficulty
    if column in ["cooking_time", "ingredients"]:
      cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
      recipe = cursor.fetchone()
      if recipe:
        cooking_time = recipe[0]
        ingredients_list = recipe[1].split(", ")
        new_difficulty = calculate_difficulty(cooking_time, ingredients_list)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
    
    conn.commit()
    print("Recipe updated successfully!")

  # Definition for deleting a recipe
  def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    
    # list recipes to user
    for row in results:
      print(f"ID: {row[0]}")
      print(f"Name: {row[1]}")
      print(f"Ingredients: {row[2]}")
      print(f"Cooking Time: {row[3]} minutes")
      print(f"Difficulty: {row[4]}")
      print()
      
    # select recipe by id
    try:
      recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
    except ValueError:
      print("Invalid ID")
      return

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    print("Recipe deleted successfully!") 

  # Main menu loop, loops as long as the user doesn't choose to quit
  while(choice != 'quit'):
    print("\nWhat would you like to do? Pick a choice!")
    print("1. Create a new recipe")
    print("2. Search for a recipe by ingredient")
    print("3. Update an existing recipe")
    print("4. Delete a recipe")
    print("Type 'quit' to exit the program.")
    choice = input("Your choice: ")

    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)
    elif choice.lower() == 'quit':
      print("Goodbye!")
      conn.commit()
      conn.close()
      break
    else:
      print("Invalid choice, try again.")

# run program
main_menu(conn, cursor)
   

