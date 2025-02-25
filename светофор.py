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


def visualize_images(original, mask, clustered):
    """
    Визуализирует исходное изображение, маску и результат кластеризации.
    """
    plt.figure(figsize=(15, 5))

    # Исходное изображение
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    # Маска
    plt.subplot(1, 3, 2)
    plt.imshow(mask, cmap='gray')
    plt.title('Mask')
    plt.axis('off')

    # Результат кластеризации
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(clustered, cv2.COLOR_BGR2RGB))
    plt.title('Clustered Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


def plot_3d_histogram_all_ranges(pixels_list, labels_list, n_clusters, titles):
    """
    Рисует 3D-гистограмму для всех диапазонов HSV на одном графике.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Фиксированные цвета для каждого диапазона
    range_colors = ['red', 'yellow', 'green', 'darkred']  # Красный, желтый, зеленый, темно-красный

    # Отображение точек для каждого диапазона
    for range_idx, (pixels, labels) in enumerate(zip(pixels_list, labels_list)):
        # Отображение точек для каждого кластера
        for i in range(n_clusters):
            cluster_points = pixels[labels == i]
            if len(cluster_points) > 0:
                # Отображение точек с фиксированным цветом
                ax.scatter(
                    cluster_points[:, 0],  # Hue
                    cluster_points[:, 1],  # Saturation
                    cluster_points[:, 2],  # Value
                    c=range_colors[range_idx],  # Используем фиксированный цвет для диапазона
                    label=f'{titles[range_idx]} Cluster {i + 1} (n={len(cluster_points)})',
                    alpha=0.7,
                    s=50
                )

    # Настройка осей
    ax.set_xlabel('Hue')
    ax.set_ylabel('Saturation')
    ax.set_zlabel('Value')
    ax.set_title('3D Histogram of HSV Channels for All Ranges')
    ax.legend()

    plt.show()


# Загрузка изображения
image_path = '4f37760e-ed34-48e6-9782-1436174b4c51.jpg'  # Укажите путь к вашему изображению
image = cv2.imread(image_path)

if image is None:
    raise ValueError("Изображение не загружено. Проверьте путь к файлу.")

# Диапазоны HSV
hsv_ranges = [
    ((0, 7), (114, 255), (77, 255)),  # Красные тона
    ((8, 26), (93, 255), (83, 255)),  # Желтый
    ((58, 88), (150, 255), (77, 255)),  # Сзеленый
    ((172, 180), (105, 255), (89, 255)),  # Красные 2
]

# Количество кластеров
n_clusters = 3

# Списки для хранения данных всех диапазонов
pixels_list = []
labels_list = []
titles = ['Red', 'Yellow', 'Green', 'Red 2']

# Применяем кластеризацию для каждого диапазона
for h_range, s_range, v_range in hsv_ranges:
    try:
        # Замер времени начала кластеризации
        start_time = time.time()

        # Применяем кластеризацию
        result_image, mask, clustered_pixels, labels = cluster_hsv_with_birch(
            image, h_range, s_range, v_range, n_clusters=n_clusters
        )

        # Замер времени окончания кластеризации
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Выводим время кластеризации
        print(f"Время кластеризации для диапазона {h_range}: {elapsed_time:.4f} секунд")

        # Сохраняем данные для графика
        pixels_list.append(clustered_pixels)
        labels_list.append(labels)

        # Визуализация изображений (опционально)
        visualize_images(image, mask, result_image)
    except Exception as e:
        print(f"Произошла ошибка для диапазона: {e}")

# Построение 3D-гистограммы для всех диапазонов
plot_3d_histogram_all_ranges(pixels_list, labels_list, n_clusters, titles)
