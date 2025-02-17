import numpy as np
from global_consts import EARTH_ID, CRUITHNE_ID, epochs, delta_t, VECTORS_NUM
from get_coordinates import get_orbital_elements
from translation import kepler_to_vectors
from animation_3D import animate_relative_orbit, save_animation, plot_orbits, plot_distances
from diff_equation_solver import solve_orbits, equations_of_motion, calculate_energy, calculate_angular_momentum
import time

def main():
    start_time = time.time()

    # Получение орбитальных элементов
    earth_elements = get_orbital_elements(EARTH_ID, epochs)
    cruithne_elements = get_orbital_elements(CRUITHNE_ID, epochs)

    # Преобразование Кеплеровых элементов в векторы
    earth_r, earth_v = kepler_to_vectors(
        earth_elements['a'][0], earth_elements['e'][0], earth_elements['incl'][0],
        earth_elements['Omega'][0], earth_elements['w'][0], earth_elements['M'][0]
    )

    cruithne_r, cruithne_v = kepler_to_vectors(
        cruithne_elements['a'][0], cruithne_elements['e'][0], cruithne_elements['incl'][0],
        cruithne_elements['Omega'][0], cruithne_elements['w'][0], cruithne_elements['M'][0]
    )

    y0 = np.concatenate([earth_r, earth_v, cruithne_r, cruithne_v])

    # Определение временного интервала и точек для вычислений
    t_span = (0, delta_t * 365.25 * 24 * 3600)
    t_eval = np.linspace(t_span[0], t_span[1], VECTORS_NUM)

    # Решение системы уравнений движения
    solution = solve_orbits(equations_of_motion, t_span, y0, t_eval)

    earth_positions = solution.y[:3, :]
    cruithne_positions = solution.y[6:9, :]

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time:.2f} секунд")

    # Анализ энергии
    initial_energy = calculate_energy(y0)
    final_energy = calculate_energy(solution.y[:, -1])

    energy_error = np.abs(final_energy - initial_energy) / np.abs(initial_energy)
    print(f"Относительная ошибка энергии: {energy_error:.2e}")

    # Анализ момента импульса
    initial_moment = np.linalg.norm(calculate_angular_momentum(y0))
    final_moment =  np.linalg.norm(calculate_angular_momentum(solution.y[:, -1]))

    moment_error = np.abs(final_moment - initial_moment) / np.abs(initial_moment)
    print(f"Относительная ошибка момента импульса: {moment_error:.2e}")

    # Вычисление относительных позиций
    cruithne_relative_positions = cruithne_positions - earth_positions

    plot_orbits(earth_positions, cruithne_positions)

    # Создание анимации

    anim = animate_relative_orbit(cruithne_relative_positions)

    # # Сохранение анимации
    # save_animation(anim, 'relative_orbit_animation', file_format='gif', fps=60)

    plot_distances(earth_positions, cruithne_positions)

if __name__ == "__main__":
    main()
