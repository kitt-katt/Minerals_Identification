import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy

pyroxene = cv2.imread("Urtit 4-1-21.jpg")
pyroxene = cv2.cvtColor(pyroxene, cv2.COLOR_BGR2HSV)
H = []
S = []
V = []
dictionaryMask = {}
width,height, _ = pyroxene.shape
for i in range(width):
    for j in range(height):
        pixel = pyroxene[i, j]
        h = int(f"{pixel[0]}")
        s = int(f"{pixel[1]}")
        v = int(f"{pixel[2]}")
        if (h in range(37,121)) and (s in range(26,130)) and (v in range(32,116)):
            if f"{[h,s,v]}" in dictionaryMask:
                 dictionaryMask[f"{[h,s,v]}"] += 1
            else:
                 dictionaryMask[f"{[h,s,v]}"] = 1
            H.append(h)
            S.append(s)
            V.append(v)

dictCount = {}
for j in range(max(dictionaryMask.values())+1):
    if j in dictionaryMask.values():
        dictCount[j] = list(dictionaryMask.values()).count(j)
#Создание и вывод гистограммы
x = list(dictCount.keys())
y = list(dictCount.values())
plt.bar(x,y, color = list((matplotlib.colors.XKCD_COLORS).keys()))
plt.show()
# 3 списка для порога k
ListForH = [];ListForS = [];ListForV = []
# 3 списка для порога kRed
ListForHRed = [];ListForSRed = [];ListForVRed = []
# 3 списка для порога kYellow
ListForHYellow = [] ;ListForSYellow = [] ;ListForVYellow = []
# 3 списка для порога kGreen
ListForHGreen = [];ListForSGreen = []; ListForVGreen = []
# 3 списка для порога kPurple
ListForHPurple = []; ListForSPurple = []; ListForVPurple = []
# 3 списка для порога kBlue
ListForHBlue = []; ListForSBLue = []; ListForVBlue = []
# Метод пороговых значений
k = 6
kRed = 1
kGreen = 2
kYellow = 3
kPurple = 4
kBlue = 5
for i in range(width):
    for j in range(height):
        pixel = pyroxene[i, j]
        H = int(f"{pixel[0]}")
        S = int(f"{pixel[1]}")
        V = int(f"{pixel[2]}")
        if f"{[H, S, V]}" in dictionaryMask and dictionaryMask[f"{[H, S, V]}"] >= k:
            ListForH.append(H)
            ListForS.append(S)
            ListForV.append(V)
        if f"{[H, S, V]}" in dictionaryMask and dictionaryMask[f"{[H, S, V]}"] == kRed:
            ListForHRed.append(H)
            ListForSRed.append(S)
            ListForVRed.append(V)
        if f"{[H, S, V]}" in dictionaryMask and dictionaryMask[f"{[H, S, V]}"] == kGreen:
            ListForHGreen.append(H)
            ListForSGreen.append(S)
            ListForVGreen.append(V)
        if f"{[H, S, V]}" in dictionaryMask and dictionaryMask[f"{[H, S, V]}"] == kYellow:
            ListForHYellow.append(H)
            ListForSYellow.append(S)
            ListForVYellow.append(V)
        if f"{[H, S, V]}" in dictionaryMask and dictionaryMask[f"{[H, S, V]}"] == kPurple:
            ListForHPurple.append(H)
            ListForSPurple.append(S)
            ListForVPurple.append(V)
        if f"{[H, S, V]}" in dictionaryMask and dictionaryMask[f"{[H, S, V]}"] == kBlue:
            ListForHBlue.append(H)
            ListForSBLue.append(S)
            ListForVBlue.append(V)
# Создание 3D модели
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')
ax.scatter(ListForH,ListForS,ListForV)
ax.scatter(ListForHRed,ListForSRed,ListForVRed,color = "red")
ax.scatter(ListForHGreen,ListForSGreen,ListForVGreen, color = "green")
ax.scatter(ListForHYellow,ListForSYellow,ListForVYellow, color = "Yellow")
ax.scatter(ListForVPurple,ListForVPurple,ListForVPurple, color = "purple")
ax.scatter(ListForHBlue,ListForSBLue,ListForVBlue, color = "blue")
plt.legend (("Количество точек больше или равно 6","Количество точек = 1","Количество точек = 2", "Количетво точек = 3","Количество точек = 4", "Количество точек = 5"))
plt.show()
# # 2D Графики плотности точек с числовыми значениями по оси ординат ( не учитывая пороги)
countH = []
for i in range(0,256):
   countH.append(H.count(i))
countS = []
for i in range(0,256):
   countS.append(S.count(i))
countV = []
for i in range(0,256):
   countV.append(V.count(i))
x = []
for i in range(0,256):
    x.append(i)

plt.plot(x,countH,color = "red")
plt.plot(x,countS,color = "green")
plt.plot(x,countV,color = "purple")
plt.title("HSV")
plt.show()