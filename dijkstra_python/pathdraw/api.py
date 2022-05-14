import flask
from flask import jsonify, request, make_response
# from flask_cors import CORS
import numpy as np
import pandas as pd
import cv2
x = float('inf')
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = True

spotPosition = pd.read_csv("spotPosition.csv")
spotFull_list = []
spotPosition_list = []
nrows = spotPosition.shape[0]
for i in range(nrows):
    ser = spotPosition.loc[i, :]
    row_dict = []
    for idx, val in zip(ser.index[1:3], ser.values[1:3]):
        if type(val) is str:
            row_dict.append(val)
        elif type(val) is np.int64:
            row_dict.append(int(val))
        elif type(val) is np.float64:
            row_dict.append(float(val))
    spotPosition_list.append(row_dict)
    row_dict2 = {}
    for idx, val in zip(ser.index[:3], ser.values[:3]):
        if type(val) is str:
            row_dict2[idx] = val
        elif type(val) is np.int64:
            row_dict2[idx] = int(val)
        elif type(val) is np.float64:
            row_dict2[idx] = float(val)
    spotFull_list.append(row_dict2)
    # print(spotPosition_list)
spotBranch_list = []
for i in range(nrows):
    ser = spotPosition.loc[i]
    row_dict = []
    # count = 0
    for idx, val in zip(ser.index[3:], ser.values[3:]):
        # count += 1
        if val == 'x':
            row_dict.append(float('inf'))
        else :
            row_dict.append(int(val))
    spotBranch_list.append(row_dict)
    # print(spotBranch_list)
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
            if (collected[i]==False) and (distTo[v] + mat[v][i] < distTo[i]):     #更新最短距离 ？？GET重複值時進不去該判斷             
                parent[i] = v
                print(parent)
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
    for i in range(len(path)):
        spotpath.append(spotPosition[path[i]])
    finalPath = np.array(spotpath, np.int32)
    print(finalPath)
    stationMap_img = cv2.imread('stationMap_Daan.jpg')
    red_color = (0, 0, 255)
    cv2.polylines(stationMap_img, pts=[finalPath], isClosed=False, color=red_color, thickness=10)
    # cv2.imshow('image',stationMap_img)
    cv2.imwrite('stationPath.png', stationMap_img)  #儲存圖片
    # 按任意鍵關閉圖片視窗
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return stationMap_img
@app.route('/spotPositionALL', methods=['GET'])
def spotPosition_ALL():
    return jsonify(spotFull_list)

@app.route('/spotBranchALL', methods=['GET'])
def spotBranch_ALL():
    return jsonify(spotBranch_list)

@app.route('/pathdraw', methods=['GET'])
def pathdraw():
    if 'startPoint' in request.args:
        startPoint = request.args.get('startPoint', None)
    if 'endPoint' in request.args:
        endPoint = request.args.get('endPoint', None)
    else:
        return "Error: No position provided. Please specify another."
    startPoint_order = 0
    for startSpot in spotFull_list:
        if startSpot['position'] == startPoint:
            break
        startPoint_order+=1
    endPoint_order = 0
    for endSpot in spotFull_list:
        if endSpot['position'] == endPoint:
            break
        endPoint_order+=1
    path = dijkstra(mat = spotBranch_list,begin = startPoint_order,end = endPoint_order)
    print(path)
    stationMap_img = drawPath(spotPosition_list, path)
    retval, buffer = cv2.imencode('.png', stationMap_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    # return jsonify(path)
    return response


app.run()
