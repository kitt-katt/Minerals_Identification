# Шаблон однотонных гистограмм
import matplotlib
import matplotlib.pyplot as plt
xdata = list([1,2,3,4,5,6]) # данные для примера
ydata = list([10,10,25,20,14,6]) # данные для примера
plt.bar(xdata,ydata)
plt.show()
# Шаблон разноцветных гистограмм (более 1000 различных цветов)
xdata = list([1,2,3,4,5,6,7,8,9]) # данные для примера
ydata = list([10,10,25,20,14,6,10,20,54]) # данные для примера
plt.bar(xdata,ydata, color = list((matplotlib.colors.XKCD_COLORS).keys()))
plt.show()
# Шаблон разноцветных гистограмм (базовые цвета)
xdata = list([1,2,3,4,5,6,7,8,9,10,11]) # данные для примера
ydata = list([10,10,25,20,14,6,10,20,54,5,6]) # данные для примера
plt.bar(xdata,ydata, color = list((matplotlib.colors.BASE_COLORS).keys()))
plt.show()