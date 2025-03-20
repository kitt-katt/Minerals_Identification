import cv2
import numpy as np
from sklearn.cluster import Birch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def create_hsv_mask(hsv_image, h_range, s_range, v_range):
    """
    Создает бинарную маску на основе диапазонов HSV.
    """
    h_min, h_max = h_range
    s_min, s_max = s_range
    v_min, v_max = v_range

    # Создание масок для каждого канала
    mask_h = cv2.inRange(hsv_image[:, :, 0], h_min, h_max)
    mask_s = cv2.inRange(hsv_image[:, :, 1], s_min, s_max)
    mask_v = cv2.inRange(hsv_image[:, :, 2], v_min, v_max)

    # Комбинирование масок
    mask = cv2.bitwise_and(mask_h, mask_s)
    mask = cv2.bitwise_and(mask, mask_v)

    return mask

def cluster_hsv_with_birch(image, h_range, s_range, v_range, n_clusters=5):
    """
    Применяет кластеризацию BIRCH к изображению в HSV.
    """
    # Преобразование в HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Создание маски на основе диапазонов HSV
    mask = create_hsv_mask(hsv_image, h_range, s_range, v_range)

    # Извлечение пикселей под маской
    pixels = hsv_image[mask > 0]

    # Проверка, что есть пиксели для кластеризации
    if pixels.shape[0] == 0:
        raise ValueError("Маска не содержит пикселей для кластеризации.")

    # Применение BIRCH
    birch = Birch(n_clusters=n_clusters)
    birch.fit(pixels)
    labels = birch.labels_

    # Вычисление центров кластеров
    centers = np.zeros((n_clusters, 3), dtype=np.uint8)
    for i in range(n_clusters):
        if np.any(labels == i):
            centers[i] = np.mean(pixels[labels == i], axis=0).astype(np.uint8)

    # Замена пикселей под маской на центры кластеров
    segmented_hsv = hsv_image.copy()
    segmented_hsv[mask > 0] = centers[labels]

    # Преобразование обратно в BGR
    result = cv2.cvtColor(segmented_hsv, cv2.COLOR_HSV2BGR)

    return result, mask, pixels, labels

def plot_3d_histogram_two_ranges(pixels_list, labels_list, n_clusters, titles):
    """
    Рисует 3D-гистограмму для двух диапазонов HSV на одном графике.
    Кластеры внутри каждого диапазона отображаются разными цветами.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Цвета для кластеров внутри каждого диапазона
    cluster_colors = [
        ['#753939', '#a84d4d', '#d46a6a'],  # Оттенки красного для первого диапазона
        ['#449586', '#5fb3a6', '#7ad1c2']   # Оттенки зелено-голубого для второго диапазона
    ]

    # Отображение точек для каждого диапазона
    for range_idx, (pixels, labels) in enumerate(zip(pixels_list, labels_list)):
        # Отображение точек для каждого кластера
        for i in range(n_clusters):
            cluster_points = pixels[labels == i]
            if len(cluster_points) > 0:
                # Отображение точек с разными цветами для каждого кластера
                ax.scatter(
                    cluster_points[:, 0],  # Hue
                    cluster_points[:, 1],  # Saturation
                    cluster_points[:, 2],  # Value
                    c=cluster_colors[range_idx][i],  # Используем цвет для текущего кластера
                    label=f'{titles[range_idx]} Cluster {i + 1} (n={len(cluster_points)})',
                    alpha=0.7,
                    s=50
                )

    # Настройка осей
    ax.set_xlabel('Hue')
    ax.set_ylabel('Saturation')
    ax.set_zlabel('Value')
    ax.set_title('3D Histogram of HSV Channels for Two Ranges')
    ax.legend()

    plt.show()

# Загрузка изображения
image_path = 'obrez_original_t0196_802_1_vidimy_s_zheltym_filtrom_2.png'  # Укажите путь к вашему изображению
image = cv2.imread(image_path)

if image is None:
    raise ValueError("Изображение не загружено. Проверьте путь к файлу.")

# Диапазоны HSV (два диапазона)
hsv_ranges = [
    ((45, 90), (7, 255), (0, 105)),  # Красные тона
    ((30, 90), (0, 31), (106, 255)),  # Зеленый
]

# Количество кластеров
n_clusters = 2  # Увеличено количество кластеров для демонстрации

# Списки для хранения данных двух диапазонов
pixels_list = []
labels_list = []
titles = ['Пироксен', 'Блик']

# Применяем кластеризацию для каждого диапазона
for h_range, s_range, v_range in hsv_ranges:
    try:
        # Применяем кластеризацию
        result_image, mask, clustered_pixels, labels = cluster_hsv_with_birch(
            image, h_range, s_range, v_range, n_clusters=n_clusters
        )

        # Сохраняем данные для графика
        pixels_list.append(clustered_pixels)
        labels_list.append(labels)
    except Exception as e:
        print(f"Произошла ошибка для диапазона: {e}")

# Построение 3D-гистограммы для двух диапазонов
plot_3d_histogram_two_ranges(pixels_list, labels_list, n_clusters, titles)