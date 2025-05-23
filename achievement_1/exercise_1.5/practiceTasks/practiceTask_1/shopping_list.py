class ShoppingList():
  def __init__(self, list_name):
    self.list_name = list_name
    self.shopping_list = []
  
  def add_item(self, item):
    # adds an item to self.shopping_list if the item isn't already there
    if item not in self.shopping_list:
      self.shopping_list.append(item)
  
  def remove_item(self, item):
    # removes an item from self.shopping_list if it is there
    if item in self.shopping_list:
      self.shopping_list.remove(item)
  
  def view_list(self):
    # prints the contents of self.shopping_list
    print(f"Shopping list: {self.shopping_list}")

pet_store_list = ShoppingList("Pet Store Shopping List")

pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

pet_store_list.remove_item("flea collars")

pet_store_list.add_item("frisbee")

pet_store_list.view_list()



