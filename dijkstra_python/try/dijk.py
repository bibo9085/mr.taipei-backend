import numpy as np
import cv2
x = float('inf')      #定義無窮大    
def dijkstra(mat,begin,end):
    n = len(mat)
    parent = []       #用妤紀錄每个结點的父輩结點    
    collected = []      #用妤紀錄是否經過該结點    
    distTo = mat[begin]       #用妤紀錄該點到begin结點路徑長度,初始值存所有點到起始點距離   
    path = []       #用妤紀錄路径
    for i in range(0,n):        #初始化工作        
        if i == begin:            
            collected.append(True)     #所有结點均未被收集        
        else:            
            collected.append(False)        
        parent.append(-1)       #均不存在父輩結點    
    while True:        
        if collected[end]==True:            
            break        
        min_n = x        
        for i in range(0,n):            
            if collected[i]==False:                
                if distTo[i] < min_n:       #代表頭結點
                    min_n = distTo[i]                    
                    v = i        
        collected[v] = True        
        for i in range (0,n):            
            if (collected[i]==False) and (distTo[v] + mat[v][i] < distTo[i]):     #更新最短距离                
                parent[i] = v
                distTo[i] = distTo[v] + mat[v][i]
    e = end    
    while e != -1:      #利用parent-v繼承關係，循環回朔更新path並輸出        		
        path.append(e)        
        e = parent[e]    
    path.append(begin)                     
    path.reverse()    
    
    # print("path: ",path)    
    print("distance: ",distTo[end])
    return path

def drawPath(spotPosition, path):   #繪製路徑
    spotpath = []
    print(path)
    for i in range(len(path)):
        spotpath.append(spotPosition[path[i]])

    finalPath = np.array(spotpath, np.int32)
    # print(finalPath)
    stationMap_img = cv2.imread('stationMap_Daan.jpg')
    red_color = (0, 0, 255)
    cv2.polylines(stationMap_img, pts=[finalPath], isClosed=False, color=red_color, thickness=10)
    # cv2.imshow('image',stationMap_img)
    cv2.imwrite('stationPath.png', stationMap_img)  #儲存圖片
    # 按任意鍵關閉圖片視窗
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


stationData = np.array([['A1',850,1505,x,600,820,1060,1720,x,x,295,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x],        
['A2',1450,1505,600,x,x,x,x,x,x,x,295,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x],        
['A3',1670,1505,820,x,x,x,x,x,x,x,x,295,x,x,x,x,x,x,x,x,x,x,x,x,x,x],        
['A4',1910,1505,1060,x,x,x,x,x,x,x,x,x,295,x,x,x,x,x,x,x,x,x,x,x,x,x],        
['A5',2570,1505,1720,x,x,x,x,x,x,x,x,x,x,x,x,590,x,x,x,x,x,x,x,x,x,x],        
['B1',330,1295,x,x,x,x,x,x,440,650,1010,1190,1440,1610,x,x,600,x,x,x,x,x,x,x,x,x],
['B2',750,1295,x,x,x,x,x,440,x,210,570,750,1000,1170,x,x,x,590,x,x,x,x,x,x,x,x],
['B3',980,1295,295,x,x,x,x,650,210,x,360,540,790,960,x,x,x,x,x,x,x,x,x,x,x,x],
['B4',1340,1295,x,295,x,x,x,1010,570,360,x,180,430,600,x,x,x,x,x,x,x,x,x,x,x,x],
['B5',1520,1295,x,x,x,x,x,1190,750,540,180,x,250,420,x,x,x,x,x,x,x,x,x,x,x,x],
['B6',1770,1295,x,x,x,x,x,1440,1000,790,430,250,x,150,x,x,x,x,x,x,x,x,x,x,x,x],
['B7',1940,1295,x,x,x,x,x,1610,1170,960,600,420,150,x,295,x,x,x,x,x,x,x,x,x,x,x],
['C1',2080,1055,x,x,x,x,x,x,x,x,x,x,x,295,x,770,x,x,x,x,x,x,x,x,x,x],
['C2',2850,1055,x,x,x,x,590,x,x,x,x,x,x,x,770,x,x,x,x,x,x,x,x,x,x,x],
['D1',75,868,x,x,x,x,x,600,x,x,x,x,x,x,x,x,x,425,2455,35,290,510,2175,2280,2725,x],
['D2',500,868,x,x,x,x,x,x,590,x,x,x,x,x,x,x,425,x,2030,390,135,85,1750,1855,2300,x],
['D3',2530,868,x,x,x,x,x,x,x,x,x,x,x,x,x,x,2455,2030,x,2420,2180,1945,280,175,270,295],
['Exit2',110,868,x,x,x,x,x,x,x,x,x,x,x,x,x,x,35,390,2420,x,x,x,x,x,x,x],
['Exit1',365,868,x,x,x,x,x,x,x,x,x,x,x,x,x,x,290,135,2180,x,x,x,x,x,x,x],
['Exit3',585,868,x,x,x,x,x,x,x,x,x,x,x,x,x,x,510,85,1945,x,x,x,x,x,x,x],
['Exit5',2250,868,x,x,x,x,x,x,x,x,x,x,x,x,x,x,2175,1750,280,x,x,x,x,x,x,x],
['Exit6',2355,868,x,x,x,x,x,x,x,x,x,x,x,x,x,x,2280,1855,175,x,x,x,x,x,x,x],
['Exit4',2800,868,x,x,x,x,x,x,x,x,x,x,x,x,x,x,2725,2300,270,x,x,x,x,x,x,x],
['E1',2390,630,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,295,x,x,x,x,x,x,x]], dtype=object)
spotPosition = stationData[:,1:3]        #取得各點座標
matrix = stationData[:,3:27]            #取得各點連接
# print(spotPosition)
print(type(matrix[0][0]))
path = dijkstra(mat = matrix,begin = 0,end = 23)    #計算起點目的地最短距離
drawPath(spotPosition, path)