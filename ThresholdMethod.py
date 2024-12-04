#Метод порогов
k = 1
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