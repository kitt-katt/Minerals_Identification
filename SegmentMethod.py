import cv2
import matplotlib.pyplot as plt
import ast
import numpy as np

def data_from_image(image):
    dictionary_filtered = {}
    list_hue, list_saturation, list_value = [],[],[]
    width, height, _ = image.shape
    for i in range(width):
        for j in range(height):
            pixel = image[i, j]
            hue = (int(pixel[0]))
            saturation = (int(pixel[1]))
            value = (int(pixel[2]))
            list_hue.append(hue)
            list_saturation.append(saturation)
            list_value.append(value)
            if f"{[hue, saturation, value]}" in dictionary_filtered:
                dictionary_filtered[f"{[hue, saturation, value]}"] += 1
            else:
                dictionary_filtered[f"{[hue, saturation, value]}"] = 1
    return dictionary_filtered

def euclidean_distance(first_point, second_point):
    return ((second_point[0] - first_point[0])**2 + (second_point[1] - first_point[1])**2 + (second_point[2] - first_point[2])**2)**0.5

def check_difference_channels(point,next_point,difference_channels):
    if abs(point[0] - next_point[0]) + abs(point[1] - next_point[1]) + abs(point[2] - next_point[2]) < difference_channels:
        return True
    else:
        return False
def check_difference_in_density(next_point,dictionary_filtered,difference_in_density,point_density):
    if ((abs(dictionary_filtered[next_point] - point_density) * 100) / point_density) <= difference_in_density:  # Подумать над вычислением разницы от кластера)
        return True
    else:
        return False
def check_distance(point, next_point, radius):
    if euclidean_distance(point, next_point) <= radius:
        return True
    else:
        return False

def segmentation(image_hsv,difference_channels,difference_in_density,radius):
    raw_points = data_from_image(image_hsv)
    clusters = []
    checked = []
    for point in raw_points:
        point_density = raw_points[point]
        checked.append(point)
        cluster = [ast.literal_eval(point)]
        for next_point in raw_points:
            if check_distance(ast.literal_eval(point),ast.literal_eval(next_point),radius) and check_difference_channels(ast.literal_eval(point),ast.literal_eval(next_point),difference_channels) \
                  and check_difference_in_density(next_point,raw_points,difference_in_density, point_density) and next_point not in checked:
                cluster.append(ast.literal_eval(next_point))
                checked.append(next_point)
        clusters.append(cluster)
    return clusters

def average_hsv_color(cluster):
    cluster_np = np.array(cluster)
    avg_hsv = np.mean(cluster_np, axis=0).astype(int)  # Среднее по HSV
    avg_rgb = cv2.cvtColor(np.uint8([[avg_hsv]]), cv2.COLOR_HSV2RGB)[0, 0]  # Перевод в RGB
    return avg_rgb / 255  # Нормализация для matplotlib

# Загружаем изображение
image = cv2.imread("firstMineral.png")
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Переводим в HSV

# Сегментируем изображение
clusters = segmentation(image_hsv, 10, 10, 5)

# Визуализация 3D-графика
# Визуализация 3D-графика
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Для добавления легенды, создадим словарь для legend
legend_labels = {}

# Рисуем каждый кластер
for idx, cluster in enumerate(clusters):
    cluster = np.array(cluster)
    avg_color = average_hsv_color(cluster)  # Средний цвет HSV-кластера
    ax.scatter(cluster[:, 0], cluster[:, 1], cluster[:, 2], color=[avg_color], s=10)

    # Добавляем информацию о сегменте для легенды
    # legend_labels[f"Сегмент №{idx + 1}: {len(cluster)} точек"] = avg_color

# Добавляем легенду на график
# handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_labels.values()]
# ax.legend(handles, legend_labels.keys(), loc='best')

# Настройки осей
ax.set_xlabel("H (Оттенок)")
ax.set_ylabel("S (Насыщенность)")
ax.set_zlabel("V (Яркость)")
ax.set_title("Метод сегментации")

plt.show()
