import shapes
from math import pi

def test_area(my_rectangle):
    assert my_rectangle.area() == 10*20

def test_perimeter(my_rectangle):
    assert my_rectangle.perimeter() == 2*(10 + 20)

def test_area_of_circle(my_circle):
    circle = shapes.Circle(4.5)
    assert my_circle.area_of_circle() == pi*10*10
    assert circle.area_of_circle() == pi*4.5*4.5

def test_circumference(my_circle):
    assert my_circle.circumference() == 2*pi*10

def test_area_of_square(my_square):
    assert my_square.area_of_square() == 10*10

def test_perimeter_of_square(my_square):
    assert my_square.perimeter_of_square() == 4*10



