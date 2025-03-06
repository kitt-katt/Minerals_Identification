import numpy as np
import cv2
import matplotlib.pyplot as plt

image = cv2.imread("GreenColor.png")
imageInHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
def takeData(imageHSV):
    hue, saturation, value = [],[],[]
    width, height, _ = imageHSV.shape
    for i in range(width):
        for j in range(height):
            pixel = imageHSV[i, j]
            h = int(pixel[0])
            s = int(pixel[1])
            v = int(pixel[2])
            hue.append(h)
            saturation.append(s)
            value.append(v)
    return hue, saturation, value

# Получение значений маски зеленого цвета
dataHue, dataSaturation, dataValue = takeData(imageInHSV)
minValueDataHue, minValueDataSaturation, minValueDataValue = sorted(dataHue)[0],sorted(dataSaturation)[0], sorted(dataValue)[0]
print("Минимальные значения маски(Hue,Saturation,Value): "+ str(minValueDataHue) + "; " + str(minValueDataSaturation) + "; " + str(minValueDataValue))
maxValueDataHue, maxValueDataSaturation, maxValueDataValue = sorted(dataHue)[-1],sorted(dataSaturation)[-1], sorted(dataValue)[-1]
print("Максимальные значения маски(Hue,Saturation,Value): "+ str(maxValueDataHue) + "; " + str(maxValueDataSaturation) + "; " + str(maxValueDataValue))
# Создаем 3D график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Отображаем точки на графике
ax.scatter(dataHue,dataSaturation,dataValue, c = "green", label = "Количество точек: " + f'{len(dataValue)}')

# Добавляем подписи осей
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')

# Заголовок графика
plt.title("Эталонные значения зеленого цвета из светофора", fontsize = 25, fontweight = "bold")
plt.legend(fontsize = 15)
# Показать график
plt.show()