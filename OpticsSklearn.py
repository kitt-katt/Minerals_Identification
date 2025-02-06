import math
import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import OPTICS


def applyingMask(imageHSV, hue_min, hue_max, saturation_min, saturation_max, value_min, value_max):
    array = []
    width, height, _ = imageHSV.shape
    for i in range(width):
        for j in range(height):
            pixel = imageHSV[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue in range(hue_min, hue_max)) and (saturation in range(saturation_min, saturation_max)) and (value in range(value_min, value_max)):
                array.append([hue, saturation, value])
    return array


image = cv2.imread("Urtit2.jpg")
imageInHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
data = usingMask(imageInHSV, 0, 19, 20, 169, 60, 205)

data_np = np.array(data)
optics = OPTICS(min_samples=5, xi=0.05, min_cluster_size=0.1)

optics.fit(data_np)

cluster_labels = optics.labels_

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')

colorMap = plt.cm.viridis
num_colors = len(np.unique(cluster_labels))
colors = [colorMap(i / num_colors) for i in range(num_colors)]

for cluster_id in np.unique(cluster_labels):
    points = data_np[cluster_labels == cluster_id]
    color = colors[cluster_id] if cluster_id != -1 else (0.5, 0.5, 0.5, 1)  # -1 - шум
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], label=f'Cluster {cluster_id}' if cluster_id != -1 else 'Noise', color=color)

plt.legend()
plt.show()
