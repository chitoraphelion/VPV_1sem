import pandas as pd
import os
import sys

# Добавить родительскую директорию sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from global_consts import CRUITHNE_ID, EARTH_ID, epochs
from get_coordinates import get_orbital_elements 

result_earth = get_orbital_elements(EARTH_ID, epochs)
print("Orbital elements:", result_earth)

df_earth = pd.DataFrame(result_earth)
df_earth.to_csv('orbital_elements_earth.csv', index=False)


result = get_orbital_elements(CRUITHNE_ID, epochs)
print("Orbital elements:", result) 

df = pd.DataFrame(result)
df.to_csv('orbital_elements_cruithne.csv', index=False)