import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import OPTICS
import time


# Выводим время работы программы
start_time = time.time()

def usingMask(imageHSV, hue_min, hue_max, saturation_min, saturation_max, value_min, value_max):
    filteredArray = []
    width, height, _ = imageHSV.shape
    for i in range(width):
        for j in range(height):
            pixel = imageHSV[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue in range(hue_min, hue_max)) and (saturation in range(saturation_min, saturation_max)) and (
                    value in range(value_min, value_max)):
                filteredArray.append([hue, saturation, value])
    return filteredArray

# Чтение изображения и преобразование в HSV
image = cv2.imread("svetofor.jpg")
imageInHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Параметры для фильтрации цвета (например, для желтого)
hue_min, hue_max = 172, 180
sat_min, sat_max = 105, 255
val_min, val_max = 89, 255

# Получаем отфильтрованные данные
data = usingMask(imageInHSV, hue_min, hue_max, sat_min, sat_max, val_min, val_max)

# Преобразуем список точек в numpy массив для удобства
data_np = np.array(data)

# Применяем кластеризацию методом OPTICS с подобранными параметрами
optics = OPTICS(min_samples=500, xi=0.005, min_cluster_size=0.02)
cluster_labels = optics.fit_predict(data_np)

# Создаем 3D график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Визуализируем данные с разными цветами для каждого кластера и выводим количество точек в кластере
for cluster_id in np.unique(cluster_labels):
    if cluster_id != -1:  # Игнорируем шум (метка -1)
        points = data_np[cluster_labels == cluster_id]
        cluster_size = len(points)  # Количество точек в текущем кластере
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], label=f"Cluster {cluster_id} ({cluster_size} points)")

# Добавляем подписи осей
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')

# Заголовок графика
plt.title('OPTICS для второй маски красного цвета', fontsize=20, fontweight="bold")
plt.legend(fontsize=15)
end_time = time.time()
elapsed_time = end_time - start_time
# Показать график
# plt.show()
print(f"Время работы программы: {elapsed_time:.2f} секунд")