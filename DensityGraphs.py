import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Параметры
image_path = "img.png"  # Укажите путь к вашему изображению
h_range = (0, 180)   # Диапазон H
s_range = (36, 65)   # Диапазон S
v_range = (124, 158) # Диапазон V

def plot_hsv_distribution_combined(image_path, h_range, s_range, v_range):
    """
    Построение графика распределения значений HSV каналов на одной плоскости.

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

    h_filtered = h[mask]
    s_filtered = s[mask]
    v_filtered = v[mask]

    # Построение графика распределения на одной плоскости
    plt.figure(figsize=(10, 6))

    # Используем KDE для плавных линий
    sns.kdeplot(h_filtered.ravel(), color='red', label='Hue (H)', bw_adjust=0.5)
    sns.kdeplot(s_filtered.ravel(), color='green', label='Saturation (S)', bw_adjust=0.5)
    sns.kdeplot(v_filtered.ravel(), color='blue', label='Value (V)', bw_adjust=0.5)

    plt.title('HSV Distribution')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.xlim(0, max(h_range[1], s_range[1], v_range[1]))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_hsv_distribution_combined(image_path, h_range, s_range, v_range)
