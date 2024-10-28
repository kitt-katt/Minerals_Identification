import cv2
import matplotlib.pyplot as plt
import numpy as np
image = cv2.imread("image2.png")
RedChannelValues = []
GreenChannelValues = []
BlueChannelValues = []
RGB = []
width, height, _ = image.shape

for i in range(width):
    for j in range(height):
       pixel = image[i, j]
       Blue = int(f"{pixel[0]}")
       Green = int(f"{pixel[1]}")
       Red = int(f"{pixel[2]}")
       RedChannelValues.append(Red)
       GreenChannelValues.append(Green)
       BlueChannelValues.append(Blue)
       RGB.append([Red,Green,Blue])

countDifferentValuesRedChannel = []
for i in range(0,256):
   countDifferentValuesRedChannel.append(RedChannelValues.count(i))
countDifferentValuesGreenChannel = []
for i in range(0,256):
   countDifferentValuesGreenChannel.append(GreenChannelValues.count(i))
countDifferentValuesBlueChannel = []
for i in range(0,256):
   countDifferentValuesBlueChannel.append(BlueChannelValues.count(i))
Discreteness = []
countPixelInDistance = []
for i in range(0,251,50):
   for g in range(0,251,50):
      for j in range(0,251,50):
         listValues = [i,g,j]
         Discreteness.append(listValues)
countDistanceRed = [0,sum(countDifferentValuesRedChannel[0:51]),sum(countDifferentValuesRedChannel[50:101]),sum(countDifferentValuesRedChannel[100:151]),sum(countDifferentValuesRedChannel[150:201]),sum(countDifferentValuesRedChannel[200:251])]
countDistanceGreen = [0,sum(countDifferentValuesGreenChannel[0:51]),sum(countDifferentValuesGreenChannel[50:101]),sum(countDifferentValuesGreenChannel[100:151]),sum(countDifferentValuesGreenChannel[150:201]),sum(countDifferentValuesGreenChannel[200:251])]
countDistanceBlue = [0,sum(countDifferentValuesBlueChannel[0:51]),sum(countDifferentValuesBlueChannel[50:101]),sum(countDifferentValuesBlueChannel[100:151]),sum(countDifferentValuesBlueChannel[150:201]),sum(countDifferentValuesBlueChannel[200:251])]
allPossibleSum = {}
allPossibleSumList = []
for i in range(6):
   for g in range(6):
      for j in range(6):
         allPossibleSumList.append(countDistanceRed[i] + countDistanceGreen[g] + countDistanceBlue[j])
         allPossibleSum.update({countDistanceRed[i] + countDistanceGreen[g] + countDistanceBlue[j]: [i*50,g*50,j*50]})
frequentValue1 = sorted(allPossibleSumList)[-1]
frequentValue2 = sorted(allPossibleSumList)[-2]
frequentValue3 = sorted(allPossibleSumList)[-3]
frequentValue4 = sorted(allPossibleSumList)[-4]
frequentValue5 = sorted(allPossibleSumList)[-5]

x1Red = range(allPossibleSum.get(frequentValue1)[0] - 50,allPossibleSum.get(frequentValue1)[0])
x1Green = range(allPossibleSum.get(frequentValue1)[1] - 50,allPossibleSum.get(frequentValue1)[1])
x1Blue = range(allPossibleSum.get(frequentValue1)[2] - 50,allPossibleSum.get(frequentValue1)[2])
y1Red = countDifferentValuesRedChannel[(allPossibleSum.get(frequentValue1))[0]-50 : allPossibleSum.get(frequentValue1)[0]]
y1Green = countDifferentValuesGreenChannel[(allPossibleSum.get(frequentValue1))[1]-50 : allPossibleSum.get(frequentValue1)[1]]
y1Blue = countDifferentValuesBlueChannel[(allPossibleSum.get(frequentValue1))[2]-50 : allPossibleSum.get(frequentValue1)[2]]
plt.subplot(5,3,1)
lineRed = plt.plot(x1Red,y1Red,color = 'Red')
plt.subplot(5,3,2)
lineGreen = plt.plot(x1Green,y1Green,color = 'Green')
plt.title("RGB1 "+f"{allPossibleSum.get(frequentValue1)}")
plt.subplot(5,3,3)
lineBlue = plt.plot(x1Blue,y1Blue, color = 'Blue')


x2Red = range(allPossibleSum.get(frequentValue2)[0] - 50,allPossibleSum.get(frequentValue2)[0])
x2Green = range(allPossibleSum.get(frequentValue2)[1] - 50,allPossibleSum.get(frequentValue2)[1])
x2Blue = range(allPossibleSum.get(frequentValue2)[2] - 50,allPossibleSum.get(frequentValue2)[2])
y2Red = countDifferentValuesRedChannel[(allPossibleSum.get(frequentValue2))[0]-50 : allPossibleSum.get(frequentValue2)[0]]
y2Green = countDifferentValuesGreenChannel[(allPossibleSum.get(frequentValue2))[1]-50 : allPossibleSum.get(frequentValue2)[1]]
y2Blue = countDifferentValuesBlueChannel[(allPossibleSum.get(frequentValue2))[2]-50 : allPossibleSum.get(frequentValue2)[2]]
plt.subplot(5,3,4)
lineRed2 = plt.plot(x1Red,y1Red,color = 'Red')
plt.subplot(5,3,5)
lineGreen2 = plt.plot(x2Green,y2Green,color = 'Green')
plt.title("RGB2 "+f"{allPossibleSum.get(frequentValue2)}")
plt.subplot(5,3,6)
lineBlue2 = plt.plot(x2Blue,y2Blue, color = 'Blue')

x3Red = range(allPossibleSum.get(frequentValue3)[0] - 50,allPossibleSum.get(frequentValue3)[0])
x3Green = range(allPossibleSum.get(frequentValue3)[1] - 50,allPossibleSum.get(frequentValue3)[1])
x3Blue = range(allPossibleSum.get(frequentValue3)[2] - 50,allPossibleSum.get(frequentValue3)[2])
y3Red = countDifferentValuesRedChannel[(allPossibleSum.get(frequentValue3))[0]-50 : allPossibleSum.get(frequentValue3)[0]]
y3Green = countDifferentValuesGreenChannel[(allPossibleSum.get(frequentValue3))[1]-50 : allPossibleSum.get(frequentValue3)[1]]
y3Blue = countDifferentValuesBlueChannel[(allPossibleSum.get(frequentValue3))[2]-50 : allPossibleSum.get(frequentValue3)[2]]
plt.subplot(5,3,7)
lineRed3 = plt.plot(x3Red,y3Red,color = 'Red')
plt.subplot(5,3,8)
lineGreen3 = plt.plot(x3Green,y3Green,color = 'Green')
plt.title("RGB3 "+f"{allPossibleSum.get(frequentValue3)}")
plt.subplot(5,3,9)
lineBlue3 = plt.plot(x3Blue,y3Blue, color = 'Blue')


x4Red = range(allPossibleSum.get(frequentValue4)[0] - 50,allPossibleSum.get(frequentValue4)[0])
x4Green = range(allPossibleSum.get(frequentValue4)[1] - 50,allPossibleSum.get(frequentValue4)[1])
x4Blue = range(allPossibleSum.get(frequentValue4)[2] - 50,allPossibleSum.get(frequentValue4)[2])
y4Red = countDifferentValuesRedChannel[(allPossibleSum.get(frequentValue4))[0]-50 : allPossibleSum.get(frequentValue4)[0]]
y4Green = countDifferentValuesGreenChannel[(allPossibleSum.get(frequentValue4))[1]-50 : allPossibleSum.get(frequentValue4)[1]]
y4Blue = countDifferentValuesBlueChannel[(allPossibleSum.get(frequentValue4))[2]-50 : allPossibleSum.get(frequentValue4)[2]]
plt.subplot(5,3,10)
lineRed4 = plt.plot(x4Red,y4Red,color = 'Red')
plt.subplot(5,3,11)
lineGreen4 = plt.plot(x4Green,y4Green,color = 'Green')
plt.title("RGB4 "+f"{allPossibleSum.get(frequentValue4)}")
plt.subplot(5,3,12)
lineBlue4 = plt.plot(x4Blue,y4Blue, color = 'Blue')


x5Red = range(allPossibleSum.get(frequentValue5)[0] - 50,allPossibleSum.get(frequentValue5)[0])
x5Green = range(allPossibleSum.get(frequentValue5)[1] - 50,allPossibleSum.get(frequentValue5)[1])
x5Blue = range(allPossibleSum.get(frequentValue5)[2] - 50,allPossibleSum.get(frequentValue5)[2])
y5Red = countDifferentValuesRedChannel[(allPossibleSum.get(frequentValue5))[0]-50 : allPossibleSum.get(frequentValue5)[0]]
y5Green = countDifferentValuesGreenChannel[(allPossibleSum.get(frequentValue5))[1]-50 : allPossibleSum.get(frequentValue5)[1]]
y5Blue = countDifferentValuesBlueChannel[(allPossibleSum.get(frequentValue5))[2]-50 : allPossibleSum.get(frequentValue5)[2]]
plt.subplot(5,3,13)
lineRed5 = plt.plot(x5Red,y5Red,color = 'Red')
plt.subplot(5,3,14)
lineGreen5 = plt.plot(x5Green,y5Green,color = 'Green')
plt.title("RGB5 "+f"{allPossibleSum.get(frequentValue5)}")
plt.subplot(5,3,15)
lineBlue5 = plt.plot(x5Blue,y5Blue, color = 'Blue')

plt.tight_layout()
plt.show()