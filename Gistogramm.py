import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Параметры
image_path = "img.png"  # Укажите путь к вашему изображению
h_range = (0, 180)  # Диапазон H
s_range = (36, 65)  # Диапазон S
v_range = (124, 158)  # Диапазон V

def create_3d_hsv_histogram(image_path, h_range, s_range, v_range):
    """
    Создает 3D точечную гистограмму значений HSV каналов изображения.

    :param image_path: Путь к изображению
    :param h_range: Диапазон значений для H (например, (0, 180))
    :param s_range: Диапазон значений для S (например, (0, 255))
    :param v_range: Диапазон значений для V (например, (0, 255))
    """
    # Загружаем изображение
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение по указанному пути.")

    # Преобразуем изображение в пространство HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Извлекаем каналы HSV
    h, s, v = cv2.split(hsv_image)

    # Фильтрация по заданным диапазонам
    mask = (
            (h >= h_range[0]) & (h <= h_range[1]) &
            (s >= s_range[0]) & (s <= s_range[1]) &
            (v >= v_range[0]) & (v <= v_range[1])
    )

    # Применяем маску к каналам
    h_filtered = h[mask]
    s_filtered = s[mask]
    v_filtered = v[mask]

    # Создаем 3D-гистограмму
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Отображение точек
    ax.scatter(h_filtered, s_filtered, v_filtered, c=np.stack((h_filtered, s_filtered, v_filtered), axis=-1) / 255.0,
               s=1)

    # Настройка осей
    ax.set_xlabel('H (Hue)')
    ax.set_ylabel('S (Saturation)')
    ax.set_zlabel('V (Value)')
    ax.set_xlim(h_range)
    ax.set_ylim(s_range)
    ax.set_zlim(v_range)

    plt.title('3D HSV Histogram')
    plt.show()

create_3d_hsv_histogram(image_path, h_range, s_range, v_range)
