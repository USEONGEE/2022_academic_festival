import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from openpyxl import load_workbook
ox.config(use_cache=True, log_console=True)
ox.__version__
import random
from math import sqrt


def get_CorData(fileName_) :
    filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/좌표데이터/' 
    f = open(filePath+fileName_+'.txt','r')
    data = f.readlines()
    
    return data

def get_cordinate(cor_) :
    li = []
    for i in cor_ :
        comma = i.find(',')
        newline = i.find('\n')
        x_cor = i[0:comma]
        if (newline != -1):
            y_cor = i[comma+1:newline]
        else :
            y_cor = i[comma+1:]
        li.append((float(x_cor),float(y_cor)))
    
    return li

def create_node(cor_):
    node_list_ = []
    for i in cor_:
        node_list_.append(ox.get_nearest_node(G, i))
    return node_list_

## sector가 1개 일 때 난수 발생, parameter => number : 발생시킬 난수(int), cor_dict_ : 형식을 맞춘 최대 최소 좌표값
def generation_oneSector(number, cor_dict_):
    orig_cor_list_=[]
    for i in range(number) :
        ran = random.random()
        x = cor_dict_['x_min'] + (cor_dict_['x_max'] - cor_dict_['x_min']) * ran
        ran = random.random()
        y = cor_dict_['y_min'] + (cor_dict_['y_max'] - cor_dict_['y_min']) * ran
        orig_cor_list_.append((x,y))
    
    return orig_cor_list_

## sector가 n개 일 때 난수 발생, parameter => number_list : 발생시킬 난수의 list (int_list) / cor_dict_list : sector dictionary 를 모아놓은 list
def generations_manySector(number_list_, cor_dict_list_) : # caution : 두 parameter 의 len()은 같아야함
    orig_cor_list_ = []
    for i in range(len(number_list_)) :
        for j in range(number_list_[i]) :
            ran = random.random()
            x = cor_dict_list_[i]['x_min'] + (cor_dict_list_[i]['x_max'] - cor_dict_list_[i]['x_min']) * ran
            ran = random.random()
            y = cor_dict_list_[i]['y_min'] + (cor_dict_list_[i]['y_max'] - cor_dict_list_[i]['y_min']) * ran
            orig_cor_list_.append((x,y))
    
    return orig_cor_list_ 

## 도착지의 좌표값을 index를 부여해 2가지의 dictionary를 만든다.
def convert_List_to_Dict(li):
    dict_ = {}
    for i in range(len(li)) :
        dict_[i] = li[i]
    return dict_

## 현재 지점으로부터 일정한 거리 내에 있는 노인복지시설 search, 없으면 fixValue를 증가해서 다시 search, fixValue를 몇 번 증가했는지를 반환한다.
def get_nearests(currentCor,destCorDict,fixValue) :
    li = []
    flag = 0
    cnt = 0
    while(flag == 0) : 
        cnt += 1
        for i in range(len(destCorDict)) :
            if (currentCor[0] - fixValue < destCorDict[i][0] < currentCor[0] + fixValue and 
                currentCor[1] - fixValue < destCorDict[i][1] < currentCor[1] + fixValue)  :
                li.append(destCorDict[i])
        if(len(li) != 0):
            flag = 1
            break
        fixValue  = fixValue + FIXVALUE

    return cnt

## get_nearests 에서 얻은 count * sqrt(2) 범위 내에 있는 경로당의 정보를 넘김 (indexList)
def get_nearestIndex(currentCor,destCorDict,fixValue,count_) : # 
    indexList_ = []
    for i in range(len(destCorDict)) :
        if (currentCor[0] - fixValue * count_ * sqrt(2) < destCorDict[i][0] < currentCor[0] + fixValue * count_ * sqrt(2) and 
            currentCor[1] - fixValue * count_ * sqrt(2) < destCorDict[i][1] < currentCor[1] + fixValue * count_ * sqrt(2))  :
            indexList_.append(i)
    return indexList_

def trySimulation(ocd,ond,dcd,dnd): # ocd : 시작 지점 좌표값 dict, ond : 시작 지점 노드 dict, dcd : 도착지점 좌표값 dict, dnd : 도착지점 노드값 dict
    short_dist_ = []
    for i in range(len(ocd)) : 
        len_ = []
        count = get_nearests(ocd[i],dcd,FIXVALUE) # fixCount를 필요한만큼 증가
        indexList = [] # 리스트 비워주기
        indexList = get_nearestIndex(ocd[i],dcd,FIXVALUE,count)       
        test_node_list = [] # 리스트 비워주기
        for cnt in indexList :
            test_node_list.append(dnd[cnt])
        
        for j in test_node_list :
            length = nx.shortest_path_length(G, ond[i], j, weight='length') / 1000
            len_.append(float(round(length,1)))    
        short_dist_.append(min(len_))
        print(min(len_))
        
    return short_dist_

####### 시뮬레이션 시작 전 수정해줘야하는 정보 #######
NUM_FOLDER = 20 # 전체 폴더 수
FIXVALUE = 0.008  # 1km는 약 0.008도 이다


## 1차 시뮬레이션 (관악구_서울)

# 관악구_서울
cor_dict1 = {'x_min' : 37.46296967116968, 'x_max' : 37.49010541289464, 'y_min' : 126.91680711200942, 'y_max': 126.94262024467017} # 300
cor_dict2 = {'x_min' : 37.477961325918585, 'x_max' : 37.48798576400957, 'y_min' : 126.94581206859225, 'y_max': 126.95874020780428} # 150
cor_dict3 = {'x_min' : 37.46839824329764, 'x_max' : 37.47618828174779, 'y_min' : 126.95997182908718, 'y_max': 126.9813574398222} # 150
cor_dict_list = [cor_dict1, cor_dict2, cor_dict3]
cor_number_list = [150,75,75] # Σvalue = 노인 인구수
recommend_number_list = [7,4,4] # Σvalue = 추천 지역수


####### main #######
G = ox.graph_from_place('관악구, 서울, 대한민국', network_type='walk', simplify=False)

# 시작 노드
orig_cor_list = generations_manySector(cor_number_list, cor_dict_list)
orig_cor_dict = convert_List_to_Dict(orig_cor_list)
orig_node_list = create_node(orig_cor_list)
orig_node_dict = convert_List_to_Dict(orig_node_list)

# 도착 노드
corData = get_CorData('관악구_노인복지시설')
dest_cor_list = get_cordinate(corData)
dest_cor_dict = convert_List_to_Dict(dest_cor_list)
dest_node_list = create_node(dest_cor_list)
dest_node_dict = convert_List_to_Dict(dest_node_list)

saveFileName = '관악구_recommend'
saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/추천시스템_관악구/simulation_'


##### main #####
for i in range(NUM_FOLDER) :
    # 추천 노드 
    recommend_cor_list = generations_manySector(recommend_number_list, cor_dict_list)
    recommend_node_list = create_node(recommend_cor_list)
    for j in range(len(recommend_cor_list)) :
        dest_cor_dict[len(dest_cor_dict)]= recommend_cor_list[j]
        dest_node_dict[len(dest_node_dict)] = recommend_node_list[j]
        
        short_dist_list = trySimulation(orig_cor_dict, orig_node_dict, dest_cor_dict, dest_node_dict)
        
        w = open(saveFilePath + str(i) +'/' + saveFileName + str(j) + '.txt','w')

        for k, value in enumerate(short_dist_list) : # 저장 부분
            w.write(("{}th person ---> {}").format(k,value) + '\n')
            
        del dest_cor_dict[len(dest_cor_dict)-1]
        del dest_node_dict[len(dest_node_dict)-1]
        w.close()
    w = open(saveFilePath + str(i) +'/' + '추천_지역_위치' + '.txt','w')
    for j in range(len(recommend_cor_list)) :
        w.write(("{}{}.txt 파일에 추가된 추천 지역의 좌표 값 : {}, {} \n").format(saveFileName,j,recommend_cor_list[j][0],recommend_cor_list[j][1]))
    w.close()



## 2차 시뮬레이션 (강서구_부산)

# 강서구_부산
cor_dict1 = {'x_min' : 35.1458000922412, 'x_max' : 35.16017795522076, 'y_min' : 128.82541781131204, 'y_max': 128.88431721847112} # 300
cor_dict2 = {'x_min' : 35.083607544669825, 'x_max' : 35.11112672588399, 'y_min' : 128.83764754690546, 'y_max': 128.88599457208755} # 150
cor_dict3 = {'x_min' : 35.14843484853444, 'x_max' : 35.20834459833122, 'y_min' : 128.87913085491334, 'y_max': 128.92056633124875} # 300
cor_dict4 = {'x_min' : 35.08912058520656, 'x_max' : 35.10455307593542, 'y_min' : 128.95530715174672, 'y_max': 129.01664695926277} # 150
cor_dict5 = {'x_min' : 35.1975298225176, 'x_max' : 35.22288213993739, 'y_min' : 128.9251422654295, 'y_max': 128.98029978176305} # 250
cor_dict_list = [cor_dict1, cor_dict2, cor_dict3, cor_dict4, cor_dict5]
cor_number_list=[100,50,100,50,100]
recommend_number_list = [2,1,2,1,2]

G = ox.graph_from_place('강서구, 부산, 대한민국', network_type='walk', simplify=False)

# 시작 노드
orig_cor_list = generations_manySector(cor_number_list, cor_dict_list)
orig_cor_dict = convert_List_to_Dict(orig_cor_list)
orig_node_list = create_node(orig_cor_list)
orig_node_dict = convert_List_to_Dict(orig_node_list)

# 도착 노드
corData = get_CorData('부산_강서구_노인복지시설')
dest_cor_list = get_cordinate(corData)
dest_cor_dict = convert_List_to_Dict(dest_cor_list)
dest_node_list = create_node(dest_cor_list)
dest_node_dict = convert_List_to_Dict(dest_node_list)

saveFileName = '강서구_부산_recommend'
saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/추천시스템_강서구_부산/simulation_'

##### main #####
for i in range(NUM_FOLDER) :
    # 추천 노드 
    recommend_cor_list = generations_manySector(recommend_number_list, cor_dict_list)
    recommend_node_list = create_node(recommend_cor_list)
    for j in range(len(recommend_cor_list)) :
        dest_cor_dict[len(dest_cor_dict)]= recommend_cor_list[j]
        dest_node_dict[len(dest_node_dict)] = recommend_node_list[j]
        
        short_dist_list = trySimulation(orig_cor_dict, orig_node_dict, dest_cor_dict, dest_node_dict)
        
        w = open(saveFilePath + str(i) +'/' + saveFileName + str(j) + '.txt','w') 

        for k, value in enumerate(short_dist_list) : # 저장 부분
            w.write(("{}th person ---> {}").format(k,value) + '\n')
            
        del dest_cor_dict[len(dest_cor_dict)-1]
        del dest_node_dict[len(dest_node_dict)-1]
        w.close()
    w = open(saveFilePath + str(i) +'/' + '추천_지역_위치' + '.txt','w') 
    for j in range(len(recommend_cor_list)) :
        w.write(("{}{}.txt 파일에 추가된 추천 지역의 좌표 값 : {}, {} \n").format(saveFileName,j,recommend_cor_list[j][0],recommend_cor_list[j][1]))
    w.close()