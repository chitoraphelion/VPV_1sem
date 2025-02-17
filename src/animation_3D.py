import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.time import Time, TimeDelta
from global_consts import INTERVAL, FRAME_NUM, VECTORS_NUM, date, delta_t, AU_IN_METERS

def plot_orbits(earth_positions, cruithne_positions):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(earth_positions[0], earth_positions[1], earth_positions[2], label='Земля', color='#0000FF')
    ax.plot(cruithne_positions[0], cruithne_positions[1], cruithne_positions[2], label='Круитни', color='#FF0000')

    max_range = max(max(earth_positions[0]), max(earth_positions[1]), max(earth_positions[2]))
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])

    ax.scatter(0, 0, 0, color='orange', s=100, label='Солнце')  # Желтая точка для Солнца

    ax.set_xlabel(r'X, (m)', fontsize=12)
    ax.set_ylabel(r'Y, (m)', fontsize=12)
    ax.set_zlabel(r'Z, (m)', fontsize=12)
    ax.legend()

    plt.show()

def animate_orbits(earth_positions, cruithne_positions):
    """Создает анимацию орбит Земли и Круитни в абсолютной системе отсчета с отображением текущей даты."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    line_earth, = ax.plot([], [], [], label='Земля', color='#0000FF')
    line_cruithne, = ax.plot([], [], [], label='Круитни', color='#FF0000')
    sun_marker, = ax.plot([], [], [], marker='o', markersize=10, color='orange', label='Солнце', linestyle='None')
    earth_marker, = ax.plot([], [], [], marker='o', markersize=10, color='blue', label='Земля (точка)', linestyle='None')
    cruithne_marker, = ax.plot([], [], [], marker='o', markersize=10, color='black', label='Круитни (точка)', linestyle='None')

    # Добавим текст для отображения даты
    date_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

    max_range = max(np.max(np.abs(earth_positions)), np.max(np.abs(cruithne_positions)))
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])

    ax.scatter(0, 0, 0, color='orange', s=100, label='Солнце')  # Желтая точка для Солнца

    ax.set_xlabel(r'X, (м)', fontsize=12)
    ax.set_ylabel(r'Y, (м)', fontsize=12)
    ax.set_zlabel(r'Z, (м)', fontsize=12)
    ax.legend()

    # Преобразуем начальную дату в формат Time (Astropy)
    t_start = Time(date, format='iso')

    def update(frame):
        # Показываем только последние FRAME_NUM точек
        start = max(0, frame - FRAME_NUM)

        line_earth.set_data(earth_positions[0, start:frame+1], earth_positions[1, start:frame+1])
        line_earth.set_3d_properties(earth_positions[2, start:frame+1])

        line_cruithne.set_data(cruithne_positions[0, start:frame+1], cruithne_positions[1, start:frame+1])
        line_cruithne.set_3d_properties(cruithne_positions[2, start:frame+1])

        sun_marker.set_data([0], [0])
        sun_marker.set_3d_properties([0])

        # Обновляем маркеры Земли и Круитни
        earth_marker.set_data([earth_positions[0, frame]], [earth_positions[1, frame]])
        earth_marker.set_3d_properties([earth_positions[2, frame]])

        cruithne_marker.set_data([cruithne_positions[0, frame]], [cruithne_positions[1, frame]])
        cruithne_marker.set_3d_properties([cruithne_positions[2, frame]])

        # Обновляем текст с текущей датой
        current_time = t_start + TimeDelta(frame * delta_t, format='jd')  # Шаг времени в днях
        date_text.set_text(f"Дата: {current_time.iso[:10]}")  # Показываем дату в формате 'YYYY-MM-DD'

        return line_earth, line_cruithne, sun_marker, earth_marker, cruithne_marker, date_text

    # Количество кадров
    frames = range(FRAME_NUM, earth_positions.shape[1])  # Начинаем с FRAME_NUM-го кадра

    anim = FuncAnimation(fig, update, frames=frames, interval=INTERVAL, blit=True)
    plt.show()

    return anim

def animate_relative_orbit(cruithne_relative_positions):
    """Создает анимацию орбиты Круитни относительно Земли с отображением текущей даты."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    earth_marker, = ax.plot([], [], [], marker='o', markersize=8, color='blue', label='Земля', linestyle='None')
    cruithne_marker, = ax.plot([], [], [], marker='o', markersize=4, color='black', label='Круитни', linestyle='None')
    line_cruithne, = ax.plot([], [], [], label='Круитни относительно Земли', color='#FF0000')

    # Добавим текст для отображения даты
    date_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

    max_range = np.max(np.abs(cruithne_relative_positions))
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])

    ax.set_xlabel(r'X (м)', fontsize=12)
    ax.set_ylabel(r'Y (м)', fontsize=12)
    ax.set_zlabel(r'Z (м)', fontsize=12)
    ax.legend()

    # Преобразуем начальную дату в формат Time (Astropy)
    t_start = Time(date, format='iso')

    def update(frame):
        # Показываем только последние FRAME_NUM точек
        start = max(0, frame - FRAME_NUM)

        line_cruithne.set_data(cruithne_relative_positions[0, start:frame+1], cruithne_relative_positions[1, start:frame+1])
        line_cruithne.set_3d_properties(cruithne_relative_positions[2, start:frame+1])

        earth_marker.set_data([0], [0])
        earth_marker.set_3d_properties([0])

        # Обновляем маркер Круитни
        # cruithne_marker.set_data([cruithne_relative_positions[0, frame]], [cruithne_relative_positions[1, frame]])
        # cruithne_marker.set_3d_properties([cruithne_relative_positions[2, frame]])

        # Обновляем текст с текущей датой
        current_time = t_start + TimeDelta(frame * delta_t * 365 / VECTORS_NUM, format='jd')  # Шаг времени в днях
        date_text.set_text(f"Дата: {current_time.iso[:10]}")  # Показываем дату в формате 'YYYY-MM-DD'

        return line_cruithne, earth_marker, cruithne_marker, date_text

    frames = range(FRAME_NUM, cruithne_relative_positions.shape[1], 11)  # Начинаем с FRAME_NUM-го кадра
    # frames = range(FRAME_NUM, cruithne_relative_positions.shape[1])  # Начинаем с FRAME_NUM-го кадра

    anim = FuncAnimation(fig, update, frames=frames, interval=INTERVAL, blit=False)
    plt.show()

    return anim

def save_animation(anim, filename, file_format='mp4', fps=30):
    """
    Сохраняет анимацию в указанный файл.

    Параметры:
    - anim: объект анимации (FuncAnimation)
    - filename: имя выходного файла без расширения
    - file_format: формат файла ('mp4' или 'gif')
    - fps: частота кадров в секунду
    """
    if file_format == 'mp4':
        anim.save(f'{filename}.mp4', writer='ffmpeg', fps=fps)
    elif file_format == 'gif':
        anim.save(f'{filename}.gif', writer='imagemagick', fps=fps)
    else:
        print(f"Неподдерживаемый формат: {file_format}. Используйте 'mp4' или 'gif'.")
        return

    print(f"Анимация сохранена как {filename}.{file_format}")

def plot_distances(earth_positions, cruithne_positions):
    """
    Строит график изменения расстояния от Круитни до Земли и до Солнца с течением времени.
    Ось X: годы от 'date' до 'date + delta_t'.
    Ось Y: расстояние в астрономических единицах (AU).
    """
    # Вычисляем расстояние от Круитни до Земли
    cruithne_to_earth_distances = np.linalg.norm(cruithne_positions - earth_positions, axis=0) / AU_IN_METERS

    # Вычисляем расстояние от Круитни до Солнца (Солнце находится в центре координат)
    cruithne_to_sun_distances = np.linalg.norm(cruithne_positions, axis=0) / AU_IN_METERS

    # Вычисляем расстояние от Земли до Солнца
    earth_to_sun_distances = np.linalg.norm(earth_positions, axis=0) / AU_IN_METERS

    # Преобразуем начальную дату в формат Astropy
    t_start = Time(date, format='iso')

    # Создаем массив временных меток для оси X (в годах)
    time_values = t_start + np.linspace(0, delta_t * 365.25, VECTORS_NUM)  # шаги в днях
    time_values_years = time_values.decimalyear  # преобразование в дробные годы

    # Создаем график
    fig, ax = plt.subplots()

    ax.plot(time_values_years, cruithne_to_earth_distances, label="Расстояние Круитни-Земля", color='r', alpha = .5)
    ax.plot(time_values_years, cruithne_to_sun_distances, label="Расстояние Круитни-Солнце", color='b', alpha = .5)
    ax.plot(time_values_years, earth_to_sun_distances, label="Расстояние Земля-Солнце", color='g', linestyle='--', alpha = .5)

    ax.set_xlabel("Время (годы)", fontsize=12)
    ax.set_ylabel("Расстояние (AU)", fontsize=12)
    ax.legend()
    ax.grid(True)
    plt.title("Изменение расстояний Круитни до Земли и Солнца")
    plt.show()
