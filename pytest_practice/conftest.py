import pytest
from pytest_practice import shapes


@pytest.fixture
def my_rectangle():
    return shapes.Rectangle(10, 20)
@pytest.fixture
def my_circle():
    return shapes.Circle(10)

@pytest.fixture
def my_square():
    return shapes.Square(10)