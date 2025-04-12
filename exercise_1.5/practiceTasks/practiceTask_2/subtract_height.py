class Height:
  def __init__(self, feet, inches):
    self.feet = feet
    self.inches = inches
  
  def __str__(self):
    return f"{self.feet} feet, {self.inches} inches"

  def __sub__(self, other):
    total_inches = (self.feet * 12 + self.inches) + (other.feet * 12 + other.inches)
    feet = total_inches // 12
    inches = total_inches % 12
    return Height(feet, inches)

person_A = Height(5, 10)
person_B = Height(3, 9)
height_sum = person_A - person_B
print("Total height:", height_sum)