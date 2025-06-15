import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import os
from matplotlib.widgets import CheckButtons
from matplotlib.gridspec import GridSpec

def create_cluster_mask(image_shape, coords, color, alpha=0.6):
    """Создание полупрозрачной маски для кластера"""
    mask = np.zeros((*image_shape, 4))
    for y, x in coords:
        mask[y, x] = (*color, alpha)
    return mask

def toggle_cluster(label):
    """Переключение видимости кластера"""
    index = labels_list.index(label)
    scatters[index].set_visible(not scatters[index].get_visible())
    images[index].set_visible(not images[index].get_visible())
    plt.draw()

# Основные параметры
IMAGE_PATH = "ore.png"
K_CLUSTERS = 6
ALPHA = 0.6  # Прозрачность масок

# Загрузка и подготовка изображения
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise ValueError("Изображение не загружено, проверьте путь")
    
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
height, width = image.shape[:2]

# Подготовка данных для кластеризации
pixels = image_hsv.reshape((-1, 3))

# K-means кластеризация
kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=42)
labels = kmeans.fit_predict(pixels)

# Создание DataFrame
df = pd.DataFrame(pixels, columns=['H', 'S', 'V'])
df['cluster'] = labels
df['row'] = np.repeat(np.arange(height), width)
df['col'] = np.tile(np.arange(width), height)

# Подготовка данных для визуализации
cluster_info = []
cluster_coords = {i: {'rows': [], 'cols': []} for i in range(K_CLUSTERS)}
for idx, row in df.iterrows():
    cluster = row['cluster']
    cluster_coords[cluster]['rows'].append(row['row'])
    cluster_coords[cluster]['cols'].append(row['col'])

# Цвета для кластеров
cluster_colors = [
    ( (0.0, 1.0, 0.0), 'Зеленый'),    # Lime
    ( (1.0, 0.0, 0.0), 'Красный'),    # Red
    ( (0.0, 0.0, 1.0), 'Синий'),      # Blue
    ( (0.5, 0.0, 0.5), 'Фиолетовый'), # Purple
    ( (1.0, 1.0, 0.0), 'Желтый'),     # Yellow
    ( (0.0, 1.0, 1.0), 'Бирюзовый')   # Cyan
]

# Создание фигуры с сеткой для расположения элементов
fig = plt.figure(figsize=(20, 12))
gs = GridSpec(2, 2, figure=fig, height_ratios=[3, 1], hspace=0.4)

# Область для 3D графика
ax3d = fig.add_subplot(gs[0, 0], projection='3d')

# Область для изображения
ax_img = fig.add_subplot(gs[0, 1])  # Исправлено add_sub_subplot → add_subplot

# Область для чекбоксов
ax_check = fig.add_subplot(gs[1, :])

# Настройка 3D визуализации
scatters = []
images = []
labels_list = []

# Отображение исходного изображения
ax_img.imshow(image_rgb)
ax_img.axis('off')
ax_img.set_title('Распределение кластеров на изображении')

# Создание масок и scatter plot'ов
for cluster_num in range(K_CLUSTERS):
    # Получение данных кластера
    cluster_data = df[df['cluster'] == cluster_num]
    color_rgb, color_name = cluster_colors[cluster_num]
    
    # 3D визуализация
    scat = ax3d.scatter(
        cluster_data['H'], 
        cluster_data['S'], 
        cluster_data['V'],
        c=np.array([color_rgb]),
        s=5,
        alpha=0.6,
        label=f'Кластер {cluster_num} ({color_name})'
    )
    scatters.append(scat)
    labels_list.append(f'Кластер {cluster_num}')
    
    # Создание маски
    mask = create_cluster_mask(
        image.shape[:2],
        list(zip(cluster_coords[cluster_num]['rows'], cluster_coords[cluster_num]['cols'])),
        color_rgb,
        ALPHA
    )
    img = ax_img.imshow(mask, alpha=ALPHA)
    images.append(img)

# Настройка 3D графика
ax3d.set_xlabel('H (Hue)')
ax3d.set_ylabel('S (Saturation)')
ax3d.set_zlabel('V (Value)')
ax3d.set_title('3D визуализация кластеров в HSV пространстве')

# Настройка чекбоксов
check = CheckButtons(
    ax=ax_check,
    labels=labels_list,
    actives=[True]*K_CLUSTERS
)
ax_check.axis('off')

# Привязка обработчика событий
check.on_clicked(toggle_cluster)

# Сохранение результатов
os.makedirs("results", exist_ok=True)
df.to_csv("results/clusters.csv", index=False)

with open("results/cluster_info.txt", "w") as f:
    f.write("Соответствие кластеров и цветов:\n")
    for i, (color, name) in enumerate(cluster_colors):
        f.write(f"Кластер {i}: {name}\n")

print("Анализ завершен. Результаты сохранены в папке 'results'")

plt.tight_layout()
plt.show()