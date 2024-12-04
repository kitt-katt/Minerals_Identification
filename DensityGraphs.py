ListForH = []
ListForS = []
ListForV = []
# 2D Графики плотности точек с числовыми значениями по оси ординат
countHChannel = []
for i in range(0,256):
   countHChannel.append(ListForH.count(i))
countSChannel = []
for i in range(0,256):
   countSChannel.append(ListForS.count(i))
countVChannel = []
for i in range(0,256):
   countVChannel.append(ListForV.count(i))
x = []
for i in range(0,256):
    x.append(i)
plt.title("HSV")
# для создания одного графика в 2D пространстве комментируем две из 3 следующих строк
plt.plot(x,countHChannel,color = "red") # Значения Hue канала
plt.plot(x,countSChannel,color = "black") # Значения Saturation канала
plt.plot(x,countVChannel,color = "blue") # Значения Value канала