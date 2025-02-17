import numpy as np
from global_consts import GM_sun

def kepler_to_vectors(a, e, i_deg, Omega_deg, omega_deg, M_deg):
    """
    Переводит орбитальные элементы Кеплера (a, e, i, Omega, omega, M)
    в прямоугольные координаты r(t) и v(t) в гелиоцентрической 
    (эклиптической) системе координат.
    
    Параметры:
        a (float):       Большая полуось орбиты (в а.е.).
        e (float):       Эксцентриситет.
        i_deg (float):   Наклонение орбиты в градусах.
        Omega_deg (float): Долгота восходящего узла в градусах.
        omega_deg (float): Аргумент перицентра (перигелия) в градусах.
        M_deg (float):   Средняя аномалия в градусах (на заданную эпоху).
        
    Возвращает:
        (r_sun, v_sun) кортеж из двух numpy-векторов (по 3 элемента):
         - r_sun (м)   : радиус-вектор от Солнца
         - v_sun (м/с) : вектор скорости относительно Солнца
    """

    i = np.radians(i_deg)
    Omega = np.radians(Omega_deg)
    omega = np.radians(omega_deg)
    M = np.radians(M_deg)

    a_m = a * 1.496e11

    # --- 1) Решаем уравнение Кеплера для эксцентрической аномалии E ---
    def solve_kepler(M, e, tol=1e-14, max_iter=100):
        """
        Численно решаем уравнение Кеплера M = E - e sin(E)
        методом Ньютона.
        """
        E = M  # начальное приближение
        for _ in range(max_iter):
            f = E - e * np.sin(E) - M
            fprime = 1 - e * np.cos(E)
            E_new = E - f / fprime
            if abs(E_new - E) < tol:
                E = E_new
                break
            E = E_new
        return E

    E = solve_kepler(M, e)

    # --- 2) Истинная аномалия theta ---
    # theta = 2 * arctan( sqrt((1+e)/(1-e)) * tan(E/2) ) 
    # но лучше использовать arctan2 для устойчивости
    sin_E = np.sin(E)
    cos_E = np.cos(E)
    # Можно напрямую через формулу с arctan2:
    theta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                           np.sqrt(1 - e) * np.cos(E / 2))

    # --- 3) Радиус вектора r ---
    # r = a (1 - e cos(E)) в метрах
    r = a_m * (1 - e * cos_E)

    # --- 4) Параметр орбиты (p = a(1 - e^2)) ---
    p = a_m * (1 - e**2)

    # --- 5) Скорости в полярных координатах орбитальной плоскости ---
    # Радиационная компонента скорости:
    #  vr = sqrt(mu/p)* e*sin(theta)
    # Тангенциальная компонента:
    #  vt = sqrt(mu/p)* (1 + e*cos(theta))
    mu = GM_sun  # гравитационный параметр Солнца
    vr = np.sqrt(mu / p) * e * np.sin(theta)
    vt = np.sqrt(mu / p) * (1 + e * np.cos(theta))

    # --- 6) Переходим в декартовы координаты в орбитальной плоскости ---
    # Положение (x_orb, y_orb):
    x_orb = r * np.cos(theta)
    y_orb = r * np.sin(theta)
    z_orb = 0.0

    # Скорость (vx_orb, vy_orb):
    # Формулы (см. стандартный вывод в учебниках по небесной механике):
    # vx_orb = vr*cos(theta) - vt*sin(theta)
    # vy_orb = vr*sin(theta) + vt*cos(theta)
    vx_orb = vr * np.cos(theta) - vt * np.sin(theta)
    vy_orb = vr * np.sin(theta) + vt * np.cos(theta)
    vz_orb = 0.0

    # Собираем вектора в орбитальной плоскости
    r_orb = np.array([x_orb, y_orb, z_orb])
    v_orb = np.array([vx_orb, vy_orb, vz_orb])

    # --- 7) Переходим из орбитальной плоскости в гелиоцентрическую ---
    # Матрицы поворота: Rz(Omega) * Rx(i) * Rz(omega)
    R_z_Omega = np.array([
        [np.cos(Omega), -np.sin(Omega), 0],
        [np.sin(Omega),  np.cos(Omega), 0],
        [0,              0,             1]
    ])

    R_x_i = np.array([
        [1,          0,           0],
        [0,  np.cos(i), -np.sin(i)],
        [0,  np.sin(i),  np.cos(i)]
    ])

    R_z_omega = np.array([
        [np.cos(omega), -np.sin(omega), 0],
        [np.sin(omega),  np.cos(omega), 0],
        [0,              0,             1]
    ])

    # Общая матрица поворота
    rotation_matrix = R_z_Omega @ R_x_i @ R_z_omega

    # Применяем поворот к r_orb и v_orb:
    r_sun = rotation_matrix @ r_orb   # координаты в эклиптической системе
    v_sun = rotation_matrix @ v_orb   # скорости в эклиптической системе

    return r_sun, v_sun