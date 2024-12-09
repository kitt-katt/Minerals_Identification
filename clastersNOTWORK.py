# import cv2 module
import cv2
import random
import copy
from sklearn.cluster import KMeans
# читаем картинку
img = cv2.imread('3-1-210.jpg')

# shape выводит кортеж (рост, вес, каналы)
# print(img.shape)
range1 = {
    "R": [255, 255],
    "G": [255, 255],
    "B": [255, 255],
}
RGB=[]
# Проходимся по всем пикселям изображения и получаем значения пикселей
width, height, _ = img.shape
for i in range(width):
    for j in range(height):
        RGB = img[i, j]


def clusterization(array, k):
	n = len(RGB)
	dim = len(array[0])

	cluster = [[0 for i in range(dim)] for q in range(k)]
	cluster_content = [[] for i in range(k)]

	for i in range(dim):
		for q in range(k):
			cluster[q][i] = random.randint(0, max_cluster_value)

	cluster_content = data_distribution(array, cluster)

	privious_cluster = copy.deepcopy(cluster)
	while 1:
		cluster = cluster_update(cluster, cluster_content, dim)
		cluster_content = data_distribution(array, cluster)
		if cluster == privious_cluster:
			break
		privious_cluster = copy.deepcopy(cluster)

