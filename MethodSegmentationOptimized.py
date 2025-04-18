# Повторно импортируем всё после сброса
import cv2
import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_mask_coords_by_hsv_range(image_hsv, h_range, s_range, v_range):
    h, s, v = cv2.split(image_hsv)
    mask = (
        (h >= h_range[0]) & (h <= h_range[1]) &
        (s >= s_range[0]) & (s <= s_range[1]) &
        (v >= v_range[0]) & (v <= v_range[1])
    )
    coords = np.column_stack(np.where(mask))
    return coords[:, [1, 0]]  # (x, y)

def segment_pixels_fast(image_hsv, mask_coords, color_thresh=20, spatial_radius=10):
    hsv_vals = np.array([image_hsv[y, x] for x, y in mask_coords])
    tree = cKDTree(mask_coords)
    n = len(mask_coords)
    visited = np.zeros(n, dtype=bool)
    clusters = []

    for i in range(n):
        if visited[i]:
            continue

        cluster_idx = [i]
        visited[i] = True
        queue = [i]

        while queue:
            current = queue.pop()
            neighbors = tree.query_ball_point(mask_coords[current], spatial_radius)
            neighbors = [j for j in neighbors if not visited[j]]

            if not neighbors:
                continue

            cluster_mean = np.mean(hsv_vals[cluster_idx], axis=0)
            color_diffs = np.linalg.norm(hsv_vals[neighbors] - cluster_mean, axis=1)
            accepted = [neighbors[j] for j in range(len(neighbors)) if color_diffs[j] < color_thresh]

            for j in accepted:
                visited[j] = True
                cluster_idx.append(j)
                queue.append(j)

        clusters.append(cluster_idx)

    return clusters, mask_coords, hsv_vals

def average_hsv_color(hsv_values):
    mean_hsv = np.mean(hsv_values, axis=0).astype(np.uint8)
    rgb = cv2.cvtColor(np.uint8([[mean_hsv]]), cv2.COLOR_HSV2RGB)[0][0]
    return [c / 255 for c in rgb]

def visualize_clusters_fast(clusters, coords, hsv_vals):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    handles = []
    labels = []

    for i, cluster in enumerate(clusters):
        if len(cluster) < 30:
            continue
        hsv_cluster = hsv_vals[cluster]
        color = average_hsv_color(hsv_cluster)
        ax.scatter(hsv_cluster[:,0], hsv_cluster[:,1], hsv_cluster[:,2], color=[color], s=5)
        handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=6))
        labels.append(f"Сегмент {i+1}: {len(cluster)} пикс.")

    ax.legend(handles, labels)
    ax.set_xlabel("H (Hue)")
    ax.set_ylabel("S (Saturation)")
    ax.set_zlabel("V (Value)")
    ax.set_title("Сегментация")
    plt.tight_layout()
    plt.show()

image = cv2.imread("third.png")
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h_range = (0, 180)
s_range = (0, 255)
v_range = (0, 255)

mask_coords = get_mask_coords_by_hsv_range(image_hsv, h_range, s_range, v_range)
clusters, coords, hsv_vals = segment_pixels_fast(image_hsv, mask_coords,
                                                  color_thresh=50, spatial_radius=20)
visualize_clusters_fast(clusters, coords, hsv_vals)