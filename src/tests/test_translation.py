import numpy as np
import sys
import os

# Добавить родительскую директорию sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from global_consts import CRUITHNE_ID, EARTH_ID, epochs
from get_coordinates import get_orbital_elements
from translation import kepler_to_vectors

# Получаем орбитальные элементы из JPL Horizons
df = get_orbital_elements(EARTH_ID, epochs)
    
# Извлекаем орбитальные элементы
a = df['a'][0]  # Семейная ось (AU)
e = df['e'][0]  # Эксцентриситет
i_deg = df['incl'][0]  # Наклонение (градусы)
Omega_deg = df['Omega'][0]  # Долгота восходящего узла (градусы)
omega_deg = df['w'][0]  # Аргумент перигелия (градусы)
M_deg = df['M'][0]  # Средняя аномалия (градусы)

# Переводим орбитальные элементы в радиус-вектор и вектор скорости
r, v = kepler_to_vectors(a, e, i_deg, Omega_deg, omega_deg, M_deg)

print("Радиус-вектор:", r)
print("Вектор скорости:", v)