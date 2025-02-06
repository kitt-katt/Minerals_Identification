import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS
from sklearn.datasets import make_blobs

# Генерация искусственного набора данных
X, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.60, random_state=0)

# 1. Начальное изображение: Распределение точек без кластеризации
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], color='gray', marker='o')
plt.title('Начальное распределение точек')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# Применение метода OPTICS
optics = OPTICS(min_samples=10, xi=0.05, min_cluster_size=0.1)
optics.fit(X)

# 2. Промежуточное изображение: Упорядоченные точки по методу OPTICS
plt.figure(figsize=(8, 6))
plt.scatter(X[optics.ordering_][:, 0], X[optics.ordering_][:, 1], c=optics.reachability_[optics.ordering_], cmap='viridis', marker='o')
plt.title('Упорядоченные точки по методу OPTICS')
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar(label='Достижимость (reachability)')
plt.show()

# 3. Финальное изображение: Кластеры, определенные методом OPTICS
plt.figure(figsize=(8, 6))

# Получаем уникальные метки кластеров
unique_labels = np.unique(optics.labels_)

# Отображаем точки с цветами, соответствующими меткам кластеров
scatter = plt.scatter(X[:, 0], X[:, 1], c=optics.labels_, cmap='viridis', marker='o')

# Добавляем легенду для кластеров
# Мы добавляем метки кластеров, исключая метку -1 (шум)
handles = []
for label in unique_labels:
    if label != -1:  # Исключаем шум (-1)
        handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plt.cm.viridis(label / len(unique_labels)), markersize=10, label=f'Кластер {label}'))

plt.legend(handles=handles, title="Кластеры")

plt.title('Результат кластеризации методом OPTICS')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
