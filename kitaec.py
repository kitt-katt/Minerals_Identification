import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Получение значений на примере образца иолита
image = cv2.imread("3-1-21RGB.jpg")
HChannel = []
SChannel = []
VChannel = []
HeightWidthChannel = []
d = {}
width, height, _ = image.shape

# Фильтрация пикселей по условию
for i in range(width):
    for j in range(height):
        pixel = image[i, j]
        B = int(pixel[0])
        G = int(pixel[1])
        R = int(pixel[2])
        if (B in range(52, 97)) and (G in range(52, 78)) and (R in range(78, 120)):
            HeightWidthChannel.append((i, j))  # Сохраняем координаты (i, j)

# Преобразуем изображение в HSV
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Сбор данных для кластеризации
for i in range(width):
    for j in range(height):
        if (i, j) in HeightWidthChannel:  # Проверяем, что пиксель прошёл фильтрацию
            pixel = imageHSV[i, j]
            H = int(pixel[0])
            S = int(pixel[1])
            V = int(pixel[2])
            key = (H, S, V)  # Используем кортеж как ключ
            if key in d:
                d[key] += 1
            else:
                d[key] = 1

# Преобразуем данные в формат, подходящий для k-means
pixels = np.array(list(d.keys()))  # Массив кортежей (H, S, V)
counts = np.array(list(d.values()))  # Массив количеств

# Повторяем каждый пиксель count раз
pixel_values = np.repeat(pixels, counts, axis=0)

# Задаем количество кластеров
k = 5  # Увеличиваем количество кластеров

# Применяем метод k-средних
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(pixel_values)

# Получаем центры кластеров и метки для каждого пикселя
centroids = kmeans.cluster_centers_
labels = kmeans.labels_

# Подсчёт количества точек
total_points = len(pixel_values)  # Общее количество точек
cluster_counts = np.bincount(labels)  # Количество точек в каждом кластере

# Вывод информации о количестве точек
print(f"Общее количество точек: {total_points}")
for i in range(k):
    print(f"Кластер {i}: {cluster_counts[i]} точек")

# Визуализация в 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Цвета для каждого кластера
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']  # Добавляем больше цветов

# Отображаем точки для каждого кластера
for i in range(k):
    cluster_points = pixel_values[labels == i]
    ax.scatter(cluster_points[:, 0], cluster_points[:, 1], cluster_points[:, 2],
               c=colors[i], label=f'Кластер {i} ({cluster_counts[i]} точек)', s=50)

# Отображаем центры кластеров
ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2],
           c='black', marker='X', s=200, label='Центры кластеров')

# Настройка осей
ax.set_xlabel('H (Hue)')
ax.set_ylabel('S (Saturation)')
ax.set_zlabel('V (Value)')
ax.set_title('3D визуализация кластеризации методом k-средних')

# Легенда
ax.legend()

# Показать график
plt.show()