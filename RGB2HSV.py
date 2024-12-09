import cv2 #as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

image1 = cv2.imread('3-1-21.jpg')

#Преобразование изображения в цветовое пространство HSV
#с помощью функции cvtColor и сохранение полученного изображения
imageresult = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

#Вывод результата
cv2.imshow("Start image", image1)
cv2.imshow("End image", imageresult)
cv2.waitKey(0)
cv2.imwrite("3-1-21.jpg",imageresult)

plt.show()