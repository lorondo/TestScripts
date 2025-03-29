# Lesson Task 1.1 - Simple Addition in Python

## Description  
This Python script prompts the user to input two numbers, adds them together, and displays the result. It is a beginner-friendly exercise demonstrating basic user input handling and arithmetic operations.

---

## How It Works  
1. Prompts the user to enter two numbers.  
2. Converts the input into integers and stores them in variables.  
3. Adds the two numbers together.  
4. Displays the sum to the user.

---

## Usage Instructions  
### **1 Clone the Repository**
To use this script, clone the repository to your local machine:
```sh
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO

### **2 Run the Script**
python lesson_task1.1.py

### **3 Example Input/Output**
Give me one number: 5
Give me a second number: 3
Those two numbers added together are: 8

## Code Snippet
import math  # (Not required but included)

first_number = int(input("Give me one number: "))
second_number = int(input("Give me a second number: "))

a = first_number
b = second_number

c = a + b

print("Those two numbers added together are: ", c)

# Lesson Task 1.2 - Recipe Collection
For each recipe, I used a dictionary data structure. I chose this structure because the recipe layout fits the idea of a key-value pair. One of those key-value pairs can be a list, which works great for ingredients, and it would allow you to update the values in the recipe should you ever need to modify the data within.

I stored these recipes in the list all_recipes because lists are perfect for storing things in an ordered sequence. In addition, a list will still allow for greater flexibility with its contents. 
