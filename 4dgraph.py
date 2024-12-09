import cv2
import matplotlib.pyplot as plt
import matplotlib
import heapq
import numpy


#Получение значений на примере образца иолита
image = cv2.imread("3-1-210.jpg")
HChannel = []
SChannel = []
VChannel = []
HeightWidthChannel = []
d = {}
width, height, _ = image.shape
for i in range(width):
    for j in range(height):
        pixel = image[i, j]
        B = int(f"{pixel[0]}")
        G = int(f"{pixel[1]}")
        R = int(f"{pixel[2]}")
        if (B in range(0,255)) and (G in range(187,255)) and (R in range(151,252)):
            HeightWidthChannel.append(f"{[width,height]}")

imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
for i in range(width):
    for j in range(height):
        pixel = imageHSV[i, j]
        H = int(f"{pixel[0]}")
        S = int(f"{pixel[1]}")
        V = int(f"{pixel[2]}")
        if (f"{[width,height]}" in HeightWidthChannel):
            HChannel.append(H)
            SChannel.append(S)
            VChannel.append(V)
            if f"{[H,S,V]}" in d:
                 d[f"{[H,S,V]}"] += 1
            else:
                 d[f"{[H,S,V]}"] = 1
#В итоге словарь содержит ключ - значение маски, значения словаря - количество пикселей с таким значением маски
#Метод порогов
k = 400
#списки, в которые в будущем добавятся подходящие значения маски
ListForH = []
ListForS = []
ListForV = []
#в словаре d содержится ключ - это значение маски, значение словаря - количество точек с данным значением маски
for i in range(width):
    for j in range(height):
        pixel = imageHSV[i, j]
        H = int(f"{pixel[0]}")
        S = int(f"{pixel[1]}")
        V = int(f"{pixel[2]}")
        if f"{[H, S, V]}" in d and d[f"{[H, S, V]}"] >= k:
            ListForH.append(H)
            ListForS.append(S)
            ListForV.append(V)

k = 300
#списки, в которые в будущем добавятся подходящие значения маски
ListForCiclyHRed = []
ListForCiclySRed = []
ListForCiclyVRed = []
#в словаре d содержится ключ - это значение маски, значение словаря - количество точек с данным значением маски
for i in range(width):
    for j in range(height):
        pixel = imageHSV[i, j]
        H = int(f"{pixel[0]}")
        S = int(f"{pixel[1]}")
        V = int(f"{pixel[2]}")
        if 400 > (f"{[H, S, V]}" in d and d[f"{[H, S, V]}"]) > k:
            ListForCiclyHRed.append(H)
            ListForCiclySRed.append(S)
            ListForCiclyVRed.append(V)

k = 200
#списки, в которые в будущем добавятся подходящие значения маски
ListForCiclyHGreen = []
ListForCiclySGreen = []
ListForCiclyVGreen = []
#в словаре d содержится ключ - это значение маски, значение словаря - количество точек с данным значением маски
for i in range(width):
    for j in range(height):
        pixel = imageHSV[i, j]
        H = int(f"{pixel[0]}")
        S = int(f"{pixel[1]}")
        V = int(f"{pixel[2]}")
        if 300 > (f"{[H, S, V]}" in d and d[f"{[H, S, V]}"]) > k:
            ListForCiclyHGreen.append(H)
            ListForCiclySGreen.append(S)
            ListForCiclyVGreen.append(V)

k = 100
#списки, в которые в будущем добавятся подходящие значения маски
ListForCiclyHYellow = []
ListForCiclySYellow = []
ListForCiclyVYellow = []
#в словаре d содержится ключ - это значение маски, значение словаря - количество точек с данным значением маски
for i in range(width):
    for j in range(height):
        pixel = imageHSV[i, j]
        H = int(f"{pixel[0]}")
        S = int(f"{pixel[1]}")
        V = int(f"{pixel[2]}")
        if 200 > (f"{[H, S, V]}" in d and d[f"{[H, S, V]}"]) > k:
            ListForCiclyHYellow.append(H)
            ListForCiclySYellow.append(S)
            ListForCiclyVYellow.append(V)

#Одиночный
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel('Hue')
# ax.set_ylabel('Saturation')
# ax.set_zlabel('Value')
# ax.scatter(ListForH,ListForS,ListForV)
# plt.show()


#Одиночный
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel('Hue')
# ax.set_ylabel('Saturation')
# ax.set_zlabel('Value')
# ax.scatter(ListForH,ListForS,ListForV)
# plt.show()
#Цветной с разными точками
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel('Hue')
# ax.set_ylabel('Saturation')
# ax.set_zlabel('Value')
# ax.scatter(ListForH,ListForS,ListForV)
# ax.scatter(ListForCiclyHRed,ListForCiclySRed,ListForCiclyVRed)
# ax.scatter(ListForCiclyHGreen,ListForCiclySGreen,ListForCiclyVGreen)
# ax.scatter(ListForCiclyHYellow,ListForCiclySYellow,ListForCiclyVYellow)
# plt.legend (("Количество точек больше 400","Количество точек =400-300","Количество точек =300-200", "Количество точек =200-100"))
# plt.show()
