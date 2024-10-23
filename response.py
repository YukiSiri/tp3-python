from abc import ABC, abstractmethod
import math
import threading
import time
from contextlib import contextmanager


# Exercice 1: Classe Abstraite Simple
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# Exercice 2: Surcharge d'Opérateurs

class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance

    def __add__(self, amount):
        if amount < 0:
            raise ValueError("Cannot add a negative amount")
        self.balance += amount
        return self

    def __sub__(self, amount):
        if amount < 0:
            raise ValueError("Cannot subtract a negative amount")
        if amount > self.balance:
            raise ValueError("Cannot subtract more than the current balance")
        self.balance -= amount
        return self


# Exercice 4: Propriétés (Property)
class Car:
    def __init__(self):
        self._speed = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value <= 0 or value > 200:
            raise ValueError("Speed must be greater than 0 and less than or equal to 200 km/h")
        self._speed = value


# Exercice 5: Gestion des Exceptions

class AgeError(Exception):
    """Exception raised for invalid ages."""

    def __init__(self, age, message="Age must be between 0 and 150"):
        self.age = age
        self.message = message
        super().__init__(self.message)


class Person:
    def __init__(self, name, age):
        self.name = name
        if age < 0 or age > 150:
            raise AgeError(age)
        self.age = age


# Exercice 6: Context Manager
class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls, *args, **kwargs)
            cls._instance.entries = []
        return cls._instance

    def add_entry(self, entry):
        self.entries.append(entry)

    def remove_by_id(self, entry_id):
        self.entries = [entry for entry in self.entries if entry["id"] != entry_id]

    def drop_all(self):
        self.entries = []


class DbContext:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.temp_entries = []

    def __enter__(self):
        return self

    def add_entry(self, entry):
        self.temp_entries.append(entry)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db_connection.entries.extend(self.temp_entries)
        self.temp_entries = []


# Exercice 7: Factory Pattern
# ShapeFactory class
class ShapeFactory:
    @staticmethod
    def create(shape, **kwargs):
        if shape == "circle":
            return Circle(kwargs.get("radius"))
        elif shape == "rectangle":
            return Rectangle(kwargs.get("width"), kwargs.get("height"))
        else:
            raise ValueError("Unknown shape type")


# Exercice 8: Décorateurs avec Paramètres
class TimeoutError(Exception):
    pass


def timeout_limit(seconds, raise_exception=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [TimeoutError("Function execution exceeded timeout limit")]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                if raise_exception:
                    raise TimeoutError("Function execution exceeded timeout limit")
                return TimeoutError("Function execution exceeded timeout limit")
            if isinstance(result[0], Exception):
                raise result[0]
            return result[0]

        return wrapper

    return decorator


# Exercice 9: Opérateur Avancé (Matrice)
class Matrix:
    def __init__(self, values):
        self.values = values
        self.rows = len(values)
        self.cols = len(values[0]) if values else 0

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")
        result = [
            [self.values[i][j] + other.values[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrices must have compatible dimensions for multiplication")
        result = [
            [
                sum(self.values[i][k] * other.values[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return Matrix(result)


# Exercice 10: Classes Abstraites et Factory (Animal)
class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def speak(self):
        return "Meow"


class AnimalFactory:
    @staticmethod
    def create(animal_type, name):
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        else:
            raise ValueError("Unknown animal type")


# Exercice 11: Surcharge d'Opérateurs (Comparaison)
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        return self.price == other.price

    def __lt__(self, other):
        return self.price < other.price

    def __le__(self, other):
        return self.price <= other.price

    def __gt__(self, other):
        return self.price > other.price

    def __ge__(self, other):
        return self.price >= other.price

    def __ne__(self, other):
        return self.price != other.price


def top_product(products, k):
    return sorted(products, key=lambda product: product.price, reverse=True)[:k]


# Exercice 12: Propriétés et Gestion d’Exceptions (Compte)
class Account:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds")
        self.balance -= amount


# Exercice 14: Surcharge d'Opérateurs (Vecteur)
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


# Exercice 15: Mock et Monkey-Patch
class MockFunction:
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self, *args, **kwargs):
        return self.return_value

@contextmanager
def patch(target, return_value):
    original = target
    target = MockFunction(return_value)
    yield
    target = original
