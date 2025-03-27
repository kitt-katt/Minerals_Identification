import sys
import subprocess

# Проверяем и устанавливаем необходимые библиотеки
for package in ['matplotlib', 'numpy']:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import matplotlib.pyplot as plt
import numpy as np

# Генерация данных
np.random.seed(42)
data1 = np.random.randn(1000)
data2 = np.random.randn(1000) + 2
data3 = np.random.randn(1000) - 2
data4 = np.random.randn(1000) * 1.5

# Создание фигуры и осей
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Первая гистограмма
axes[0, 0].hist(data1, bins=30, color='blue', alpha=0.7)
axes[0, 0].set_title("Количество попаданий в цель")

# Вторая гистограмма
axes[0, 1].hist(data2, bins=30, color='red', alpha=0.7)
axes[0, 1].set_title("Количество промахов по цели")

# Третья гистограмма
axes[1, 0].hist(data3, bins=30, color='green', alpha=0.7)
axes[1, 0].set_title("Количество попаданий в шум")

# Четвертая гистограмма
axes[1, 1].hist(data4, bins=30, color='purple', alpha=0.7)
axes[1, 1].set_title("Количество промахов по шуму")

# Улучшаем макет
plt.tight_layout()
plt.show()
