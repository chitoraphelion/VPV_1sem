import numpy as np
from astropy.time import Time

# Гравитационная постоянная
G = 6.67430e-11  # м^3/(кг*с^2)
M_sun = 1.98847e30  # масса Солнца в кг
M_earth = 5.97219e24  # масса Земли в кг
m_cruithne = 1.3e14

# M_sun = 1.98847e30  # масса Солнца в кг
# M_earth = 5.89813e27  # масса Земли в кг
# m_cruithne = 9.95e19


M_jupiter = 1.89813e27  # масса Юпитера в кг
M_saturn = 5.68319e26  # масса Сатурна в кг
m_hector = 2.6e18

# 1 астрономическая единица в метрах
AU_IN_METERS = 149597870700

GM_sun = G * M_sun  # Гравитационный параметр Солнца (м^3/с^2)
GM_earth = G * M_earth   # Гравитационный параметр Земли в м^3/с^2


date = '2000-01-01'
delta_t = 600   # years
VECTORS_NUM = 40000

rtol_val = 1e-12
atol_val = 1e-18

# Преобразуем в юлианскую дату
t = Time(date, format='iso')
julian_date = t.jd


epochs = [julian_date]  # Юлианская дата (или укажи строку даты '2024-01-01')
CRUITHNE_ID = "3753"  # ID для астероида Круитни 3753
EARTH_ID = "399"  # ID земли 399

# CRUITHNE_ID = "624"  # ID для астероида Круитни 3753
# EARTH_ID = "699"  # ID земли 399

INTERVAL = 1
FRAME_NUM = 80