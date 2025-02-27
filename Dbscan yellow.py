import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import cv2
import time

start = time.time()
def dbscan_clustering(x_list, y_list, z_list, eps=0.5, min_samples=5):

    # Объединяем все три списка в один массив
    data = np.array(list(zip(x_list, y_list, z_list)))

    # Применяем кластеризацию DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples)
    db.fit(data)

    # Возвращаем метки кластеров
    return db.labels_, data

def usingMask(imageHSV, hue_min, hue_max, saturation_min, saturation_max, value_min, value_max):
    huek, satur, valuek = [], [], []
    width, height, _ = imageHSV.shape
    for i in range(width):
        for j in range(height):
            pixel = imageHSV[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue in range(hue_min, hue_max)) and (saturation in range(saturation_min, saturation_max)) and (
                    value in range(value_min, value_max)):
                huek.append(hue)
                satur.append(saturation)
                valuek.append(value)
    return huek, satur, valuek

def plot_clusters(x_list, y_list, z_list, labels):

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Для каждой метки кластера рисуем точки своим цветом
    scatter = ax.scatter(x_list, y_list, z_list, c=labels, cmap='viridis', s=50)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D кластеризация методом DBSCAN')

    # Добавляем легенду для кластеров
    ax.legend(*scatter.legend_elements(), title="Clusters")

    plt.show()

# Чтение изображения и преобразование в HSV
image = cv2.imread("svetofor.jpg")
imageInHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Визуализируем результаты на графике 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')

data1, data2, data3 = usingMask(imageInHSV, 8, 26, 93, 255, 83, 255)

# Применяем DBSCAN для кластеризации
cluster_labels, data = dbscan_clustering(data1, data2, data3, eps=5, min_samples=250)

# Отображаем точки с метками кластеров и добавляем количество точек в легенду
for cluster_id in np.unique(cluster_labels):
    if cluster_id != -1:  # Пропускаем точки с меткой -1 (шум)
        points = data[cluster_labels == cluster_id]
        cluster_size = len(points)
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], label=f'Кластер {cluster_id} ({cluster_size} points)')
plt.title("DBSCAN для желтого цвета", fontsize = 25, fontweight = "bold")
plt.legend(fontsize = 20)
end = time.time()
result = end - start
# plt.show()
print(str(result) + " в секундах")