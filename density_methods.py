import cv2
import matplotlib.pyplot as plt

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

def creating_histogram(dictionary):
     dictionary_count = {}
     for j in range(max(dictionary.values())+1):
         if j in dictionary.values():
             dictionary_count[j] = list(dictionary.values()).count(j)
     xdata = list(dictionary_count.keys())
     ydata = list(dictionary_count.values())
     plt.bar(xdata, ydata, color='blue')
     plt.show()
     
def creating_density_graph_three_lines(list_hue, list_saturation, list_value):
     count_hue_channel, count_saturation_channel, count_value_channel = [], [], []
     for i in range(0,256):
        count_hue_channel.append(list_hue.count(i))
        count_saturation_channel.append(list_saturation.count(i))
        count_value_channel.append(list_value.count(i))
     x = [i for i in range(0,256)]
     plt.title("HSV")
     plt.plot(x, count_hue_channel, color="red", label="Hue")
     plt.plot(x, count_saturation_channel, color="black", label="Saturation")
     plt.plot(x, count_value_channel, color="blue", label="Value")
     plt.legend()
     plt.show()