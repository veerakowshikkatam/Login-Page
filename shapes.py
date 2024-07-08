from math import pi

class Rectangle:

    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def area(self):
        return self.length*self.breadth

    def perimeter(self):
        return 2*(self.length + self.breadth)

class Circle:

    def __init__(self, radius):
        self.radius = radius

    def area_of_circle(self):
        return pi*self.radius**2

    def circumference(self):
        return 2*pi*self.radius

class Square:

    def __init__(self, side):
        self.side = side

    def area_of_square(self):
        return self.side**2

    def perimeter_of_square(self):
        return 4*self.side


