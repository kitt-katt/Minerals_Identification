import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy



def applying_mask(image_hsv,hue_min,hue_max,saturation_min,saturation_max,value_min,value_max) -> dict:
    dictionary_filtered = {}
    width,height, _ = image_hsv.shape
    for i in range(width):
        for j in range(height):
            pixel = image_hsv[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if (hue in range(hue_min,hue_max)) and (saturation in range(saturation_min,saturation_max)) and (value in range(value_min,value_max)):
                if f"{[hue, saturation, value]}" in dictionary_filtered:
                     dictionary_filtered[f"{[hue, saturation, value]}"] += 1
                else:
                     dictionary_filtered[f"{[hue, saturation, value]}"] = 1
    return dictionary_filtered
#Гистограммы
def creating_histogram(dictionary):
    dictionary_count = {}
    for j in range(max(dictionary.values())+1):
        if j in dictionary.values():
            dictionary_count[j] = list(dictionary.values()).count(j)
    xdata = list(dictCount.keys())
    ydata = list(dictCount.values())
    plt.bar(xdata,ydata, color = list((matplotlib.colors.XKCD_COLORS).keys()))
    plt.show()
# Метод порогов
def threshold_method(dictionary_after_filter, threshold):
    width,height, _ = image.shape
    list_hue, list_saturation, list_value = [], [], []
    for i in range(width):
        for j in range(height):
            pixel = imageHSV[i, j]
            hue = int(pixel[0])
            saturation = int(pixel[1])
            value = int(pixel[2])
            if f"{[hue, saturation, value]}" in dictionary_after_filter:
                if dictionary_after_filter[f"{[hue, saturation, value]}"] >= threshold:
                    list_hue.append(hue)
                    list_saturation.append(saturation)
                    list_value.append(value)
    return list_hue, list_saturation, list_value
#2D Графики плотности точек с процентными значениями по оси ординат
def creating_density_graph_three_lines(list_hue, list_saturation, list_value):
    count_hue_channel, count_saturation_channel, count_value_channel = [], [], []
    for i in range(0,256):
       count_hue_channel.append(list_hue.count(i))
       count_saturation_channel.append(list_saturation.count(i))
       count_value_channel.append(list_value.count(i))
    x = [i for i in range(0,256)]
    plt.title("HSV")
    plt.plot(x,count_hue_channel,color = "red")
    plt.plot(x,count_saturation_channel,color = "green")
    plt.plot(x,count_value_channel,color = "blue")

def creating_density_graph_three_lines_procent(list_hue, list_saturation, list_value):
    count_hue_channel, count_saturation_channel, count_value_channel = [], [], []
    len(list_hue)
    for i in range(0,256):
       count_hue_channel.append(100 * list_hue.count(i)/ len(list_hue))
       count_saturation_channel.append(100 * list_saturation.count(i)/ len(list_saturation))
       count_value_channel.append(100 * list_value.count(i) / len(list_value))
    x = [i for i in range(0,256)]
    plt.title("HSV")
    plt.plot(x, count_hue_channel, color = "red" )
    plt.plot(x, count_saturation_channel, color = "green")
    plt.plot(x, count_value_channel, color = "blue")
    plt.show()
#3D
def creating_point_3d_model_hsv(list_hue, list_saturation, list_value, legend):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Hue')
    ax.set_ylabel('Saturation')
    ax.set_zlabel('Value')
    ax.scatter(list_hue, list_saturation, list_value)
    plt.legend (legend)
    plt.show()

#Пример
image = cv2.imread("Urtit2.jpg")
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
list_hue, list_saturation, list_value = threshold_method(applying_mask(imageHSV,0,19,20,169,60,205),5)
creating_density_graph_three_lines_procent(list_hue,list_saturation,list_value)

