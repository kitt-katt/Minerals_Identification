import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Загрузка изображения (Апатит)
image1 = cv2.imread('img.png')
# Конвертация изображения в HSV
hsv_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

#Нижний диапозон
Hmin = 0
Smin = 36
Vmin = 124

#Верхний диапозон
Hmax = 360
Smax = 65
Vmax = 158

# Диапозон из ползунков
lower_bound = np.array([Hmin, Smin, Vmin])
upper_bound = np.array([Hmax, Smax, Vmax])

# Создание маски к изображениям
mask_img1 = cv2.inRange(hsv_image1, lower_bound, upper_bound)
# Применение маски к изображениям
masked_image1 = cv2.bitwise_and(image1, image1, mask=mask_img1)


# Отображение маски и итогового изображения
plt.figure(figsize=(40, 20))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
plt.title('HSV')
plt.axis('off')

# plt.subplot(1, 2, 2)
# plt.imshow(cv2.cvtColor(hsv_image1, cv2.COLOR_BGR2RGB))
# plt.title('HSV Image')
# plt.axis('off')
#
# plt.subplot(1, 2, 1)
# plt.imshow(mask_img1, cmap='gray')
# plt.title('Mask Image 1')
# plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(masked_image1, cv2.COLOR_BGR2RGB))
plt.title('Masked Image 1')
plt.axis('off')

plt.show()
