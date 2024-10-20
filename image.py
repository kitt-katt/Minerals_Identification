# import cv2 module
import cv2

# читаем картинку
img = cv2.imread('image.png')

# shape выводит кортеж (рост, вес, каналы)
print(img.shape)

# выводим RGB всех пикселей
print(img)

# выводим RGB конкретного пикселя, расположенного на сотой строке, сотом столбце
print(img[100, 100])

range1 = {
    "R": [255, 255],
    "G": [255, 255],
    "B": [255, 255],
}

# Проходимся по всем пикселям изображения и получаем значения пикселей
width, height, _ = img.shape
for i in range(width):
    for j in range(height):
        pixel = img[i, j]
        print(f"R = {pixel[0]}")
        print(f"G = {pixel[1]}")
        print(f"B = {pixel[2]}")


