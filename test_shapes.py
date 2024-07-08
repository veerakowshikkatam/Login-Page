import shapes, time
from math import pi
import pytest

def test_area(my_rectangle):
    assert my_rectangle.area() == 10*20

#This test will be skipped and will be shown in the command prompt with the letter "s"
@pytest.mark.skip
def test_perimeter(my_rectangle):
    assert my_rectangle.perimeter() == 2*(10 + 20)

def test_area_of_circle(my_circle):
    circle = shapes.Circle(4.5)
    assert my_circle.area_of_circle() == pi*10*10
    time.sleep(5)
    assert circle.area_of_circle() == pi*4.5*4.5

#We are telling ourselves that it will fail, it will be shown as "x" in cmd
@pytest.mark.xfail
def test_circumference():
    my_circle = shapes.Circle(0)
    assert my_circle.circumference() == 2*pi*10

#For multiple tests of a single test instead of for loop but it will show each test case as differently in cmd
@pytest.mark.parametrize("side, expected_area",[(1,1), (2,4), (3,9)])
def test_area_of_square(side, expected_area):
    assert shapes.Square(side).area_of_square() == expected_area

def test_perimeter_of_square(my_square):
    assert my_square.perimeter_of_square() == 4*10



