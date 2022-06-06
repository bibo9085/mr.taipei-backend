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
def getSpotPosition(stationName):
    spotPosition = pd.read_csv("stationSpotPosition/spotPosition_"+ stationName +".csv", encoding="Big5")
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
        # print(spotFull_list)
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
    return spotPosition_list, spotFull_list, spotBranch_list
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
            if (collected[i]==False) and (distTo[v] + mat[v][i] <= distTo[i]):     #更新最短距离 ？？GET重複值時進不去該判斷             
                parent[i] = v
                distTo[i] = distTo[v] + mat[v][i]
    e = end    
    while e != -1:      #利用parent-v繼承關係，循環回朔更新path並輸出        		
        path.append(e)  
        e = parent[e]    
    path.append(begin)                     
    path.reverse()    
    
    # print("path: ",path)    
    # print("distance: ",distTo[end])
    path.append(distTo[end])
    return  path
def getStartStationPath(startPoint, startTrainHeadto, destiTrainHeadto, spotFull_list, spotBranch_list, getPathCount):
    # 入口是在矩陣中第幾個
    startPoint_order = 0
    if(getPathCount == 0):
        destination = startTrainHeadto
        for startSpot in spotFull_list:
            if startSpot['position'] == startPoint:
                break
            startPoint_order+=1
    elif(getPathCount == 1):
        destination = destiTrainHeadto
        for startSpot in spotFull_list:
            if startTrainHeadto in startSpot['position']:
                if startPoint in startSpot['position']:
                    break
            startPoint_order+=1
        
    endPoint_order = []
    count = 0
    # 在正確月台的列車有哪些
    for endSpot in spotFull_list:
        if destination in endSpot['position']:
            endPoint_order.append(count)
        count +=1
    shortPath = []
    endPoint_results = []
    path = []
    # 計算入口雨正確列車哪節車廂最近，並輸出路徑
    for i in endPoint_order:
       endPoint_results.append(dijkstra(mat = spotBranch_list,begin = startPoint_order,end = i))
    for j in range(len(endPoint_results)):
        path.append(endPoint_results[j][:-1])
        shortPath.append(endPoint_results[j][-1])
    indexMinPath = shortPath.index(min(shortPath))
    return path[indexMinPath], spotFull_list[indexMinPath]['position']
def getDestiStationPath(spotFull_list, destiTrainHeadto, inCarNumber, endPoint):
    inCarNumberCount = 0
    # 在正確月台的列車有哪些
    for endSpot in spotFull_list:
        if destiTrainHeadto in endSpot['position']:
            if inCarNumber[0:4] in endSpot['position']:
                break
        inCarNumberCount += 1
    endPointOrder = 0
    for Spot in spotFull_list:
        if Spot['position'] == endPoint:
            break
        endPointOrder+=1
    return inCarNumberCount, endPointOrder
@app.route('/spotPositionALL', methods=['GET'])
def spotPosition_ALL():
    if 'startStation' in request.args:
        startStation = request.args.get('startStation', None)
    else:
        return "Error: No position provided. Please specify another."
    spotFull_list = getSpotPosition(startStation)
    return jsonify(spotFull_list)

@app.route('/spotBranchALL', methods=['GET'])
def spotBranch_ALL():
    if 'startStation' in request.args:
        startStation = request.args.get('startStation', None)
    else:
        return "Error: No position provided. Please specify another."
    spotBranch_list = getSpotPosition(startStation)
    return jsonify(spotBranch_list)
    

@app.route('/pathdraw', methods=['GET']) 
def pathdraw():
    if 'startPoint' in request.args:
        startPoint = request.args.get('startPoint', None)
    if 'startStation' in request.args:
        startStation = request.args.get('startStation', None)
    if 'endPoint' in request.args:
        endPoint = request.args.get('endPoint', None)
    if 'transferStation' in request.args:
        transferStation = request.args.get('transferStation', None)
    if 'destiStation' in request.args:
        destiStation = request.args.get('destiStation', None)
    if 'startTrainHeadto' in request.args:
        startTrainHeadto = request.args.get('startTrainHeadto', None)
    if 'destiTrainHeadto' in request.args:
        destiTrainHeadto = request.args.get('destiTrainHeadto', None)
    if 'imgNum' in request.args:
        imgNum = request.args.get('imgNum', None)
    else:
        return "Error: No position provided. Please specify another."
    
    spotPosition_list, spotFull_list, spotBranch_list = getSpotPosition(startStation)
    pathStartStation, inCarNumber = getStartStationPath(startPoint, startTrainHeadto, destiTrainHeadto, spotFull_list, spotBranch_list, getPathCount=0)
    response = drawPath(spotPosition_list, pathStartStation, startStation)
    imgList = []
    imgList.append(response)
app.run()
