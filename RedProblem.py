import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def applying_mask(image, hueMin,hueMax,saturationMin,saturationMax,valueMin,valueMax):
    width,height, _ = image.shape
    list_hue, list_saturation, list_value = [], [], []
    for i in range(width):
        for j in range(height):
            pixel = image[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue >=hueMin and hue <= hueMax) and (saturation >= saturationMin and saturation <= saturationMax) and (value >= valueMin and value <= valueMax) :
                list_hue.append(hue)
                list_saturation.append(saturation)
                list_value.append(value)
    return list_hue, list_saturation, list_value

# Чтение изображения и преобразование в HSV
image = cv2.imread("TrafficLightDedicated.jpg")
imageInHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Параметры для фильтрации цвета (например, для красного)
hue_min, hue_max = 172, 180
sat_min, sat_max = 105, 255
val_min, val_max = 89, 255

# Получаем отфильтрованные данные
dataHue,dataSaturation,dataValue = applying_mask(imageInHSV, hue_min, hue_max, sat_min, sat_max, val_min, val_max)

# Преобразуем список точек в numpy массив для удобства

# Создаем 3D график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Отображаем точки на графике
ax.scatter(dataHue, dataSaturation, dataValue, c = "red", label = "Группа точек, относящихся к заданной маске: " + f'{len(dataHue)}')

# Добавляем подписи осей
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')

# Заголовок графика
plt.title("Применения второй маски для красного цвета"+" для обрезанного изображения светофора", fontsize = 20, fontweight = "bold")
plt.legend(fontsize = 15)
# Показать график
plt.show()