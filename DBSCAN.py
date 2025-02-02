import math
import cv2
import matplotlib.pyplot as plt
import numpy

# Функция для вычисления евклидова расстояния между двумя точками в 3D
def euclideanDistance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


# Функция для поиска соседей точки в радиусе eps
def regionQuery(data, point_idx, radius):
    neighbors = []
    for i, point in enumerate(data):
        if euclideanDistance(data[point_idx], point) <= radius:
            neighbors.append(i)
    return neighbors


# Алгоритм DBSCAN
def dbscan(data, radius, min_samples):
    labels = [-1] * len(data)  # -1 обозначает шум
    cluster_id = 0

    for i in range(len(data)):
        if labels[i] != -1:  # Если точка уже помечена, пропускаем её
            continue

        # Находим соседей точки
        neighbors = regionQuery(data, i, radius)

        # Если недостаточно соседей для формирования кластера, помечаем как шум
        if len(neighbors) < min_samples:
            labels[i] = -1
        else:
            # Создаем новый кластер
            cluster_id += 1
            labels[i] = cluster_id
            # Расширяем кластер с помощью соседей
            neighbors_queue = neighbors.copy()
            while neighbors_queue:
                current_idx = neighbors_queue.pop(0)

                if labels[current_idx] == -1:  # Если точка была шумом, превращаем её в кластер
                    labels[current_idx] = cluster_id

                if labels[current_idx] != -1:  # Если точка уже помечена, пропускаем
                    continue

                labels[current_idx] = cluster_id
                # Ищем соседей для текущей точки
                current_neighbors = region_query(data, current_idx, radius)

                # Если у текущей точки достаточно соседей, добавляем их в очередь для расширения
                if len(current_neighbors) >= min_samples:
                    neighbors_queue.extend(current_neighbors)

    # Группировка точек по кластерам
    clusters = {i: [] for i in set(labels) if i != -1}
    for i, label in enumerate(labels):
        if label != -1:
            clusters[label].append(data[i])

    return clusters

def usingMask(imageHSV,hue_min,hue_max,saturation_min,saturation_max,value_min,value_max):
    filteredArray = []
    width,height, _ = imageHSV.shape
    for i in range(width):
        for j in range(height):
            pixel = imageHSV[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue in range(hue_min,hue_max)) and (saturation in range(saturation_min,saturation_max)) and (value in range(value_min,value_max)):
                filteredArray.append([hue,saturation,value])
    return filteredArray
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')
image = cv2.imread("Urtit2.jpg")
imageInHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
data = usingMask(imageInHSV,0,19,20,169,60,205)
clusters = dbscan(data, 30,  5 )
cmap = plt.cm.viridis
num_colors = len(clusters)
colors = [cmap(i/ num_colors) for i in range(num_colors)]
for idx, (cluster_id, points) in enumerate(clusters.items()):
    color = colors[idx]
    ax.scatter([point[0] for point in points] ,[point[1] for point in points], [point[2] for point in points] , label=f'Cluster {cluster_id}', color=color)
plt.show()