import cv2
import numpy


#Получение значений на примере образца иолита
image = cv2.imread("iolit.jpg")
HChannel = []
SChannel = []
VChannel = []
HeightWidthChannel = []
d = {}
width,height, _ = image.shape
for i in range(width):
    for j in range(height):
        pixel = image[i, j]
        B = int(f"{pixel[0]}")
        G = int(f"{pixel[1]}")
        R = int(f"{pixel[2]}")
        if (B in range(52,97)) and (G in range(52,78)) and (R in range(78,120)):
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