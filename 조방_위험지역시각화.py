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
import folium

## 좌표 데이터 가져오기
def get_CorData() :
    filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/좌표데이터/' 
    fileName = input("좌표 데이터 파일 이름을 입력하세요 :")
    f = open(filePath+fileName+'.txt','r')
    data = f.readlines()
    
    return data

## 좌표 데이터 -> list로 저장하기 (x,y) 형태
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
        
## excel 파일에서 경로당 이름 가져오기
def getExcelData(FilePath, sheetName, startCell, endCell) : # All parameter types are 'String',
    load_wb = load_workbook(FilePath, data_only = True)
    load_ws = load_wb[sheetName]
    get_cells = load_ws[startCell : endCell]
    
    data = []
    for row in get_cells:
        for cell in row :
            data.append(cell.value)
            
    return data # cell을 저장한 list를 반환함.

## 좌표 데이터 list -> 노드 list 생성 후 반환
def create_node(cor_):
    node_list_ = []
    for i in cor_:
        node_list_.append(ox.get_nearest_node(G, i))
    return node_list_

## 난수를 발생시켜 출발 지점을 생성
def generation_oneSector(number,cor_dict_):
    orig_node_=[]
    for i in range(number) :
        ran = random.random()
        x = cor_dict_['x_min'] + (cor_dict_['x_max'] - cor_dict_['x_min']) * ran
        ran = random.random()
        y = cor_dict_['y_min'] + (cor_dict_['y_max'] - cor_dict_['y_min']) * ran
        orig_node_.append((x,y))
    
    return orig_node_

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

## simulation, parameter should be list
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

## 파일 저장
def saveFile(m_,filePath_, fileName_):
    m_.save(filePath_ + fileName_ +'.html')

## 난수발생을 위한 정보
NUM = 300
FIXVALUE = 0.008  # 1km는 약 0.008도 이다
#### 난수 발생 dictonary 선택
## 1. generations method를 사용
# 관악구_서울
cor_dict1 = {'x_min' : 37.46296967116968, 'x_max' : 37.49010541289464, 'y_min' : 126.91680711200942, 'y_max': 126.94262024467017} # 300
cor_dict2 = {'x_min' : 37.477961325918585, 'x_max' : 37.48798576400957, 'y_min' : 126.94581206859225, 'y_max': 126.95874020780428} # 150
cor_dict3 = {'x_min' : 37.46839824329764, 'x_max' : 37.47618828174779, 'y_min' : 126.95997182908718, 'y_max': 126.9813574398222} # 150
cor_dict_list = [cor_dict1, cor_dict2, cor_dict3]
cor_number_list = [60,30,30] # Σvalue = 노인 인구수


#  맵 가져오기 (www.openstreetmap.org에서 검색 결과가 city-state-country 단위로 나와야 함 - '마포구, 서울, 대한민국')
G = ox.graph_from_place('관악구, 서울, 대한민국', network_type='walk', simplify=False) 

# 출발 노드
orig_cor_list = generations_manySector(cor_number_list, cor_dict_list)
orig_cor_dict = convert_List_to_Dict(orig_cor_list)
orig_node_list = create_node(orig_cor_list)
orig_node_dict = convert_List_to_Dict(orig_node_list)

# 도착 노드
corData = get_CorData()
dest_cor_list = get_cordinate(corData)
dest_cor_dict = convert_List_to_Dict(dest_cor_list)
dest_node_list = create_node(dest_cor_list)
dest_node_dict = convert_List_to_Dict(dest_node_list)

# 출발 지점 -> 도착 지점(여러개) 중 최단거리를 저장
short_dist = []

####### simulation #######

short_dist_list = trySimulation(orig_cor_dict, orig_node_dict, dest_cor_dict, dest_node_dict)

## 난수지역시각화
m = folium.Map(location= [37.47852702960704,126.951747165343], zoom_start=15,
               tiles='cartodbpositron'
                #  tiles='Stamen Toner'
               )
for i in orig_cor_list :
     folium.Marker(
            i,
            icon = folium.Icon(color='green')
        ).add_to(m)
for i in dest_cor_list :
     folium.Marker(
            i,
        ).add_to(m)

saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/조방/시각화자료/'   
saveFileName = '난수지역시각화'

saveFile(m,saveFilePath,saveFileName)

## 위험지역시각화
m = folium.Map(location= [37.47852702960704,126.951747165343], zoom_start=15,
               tiles='cartodbpositron'
                #  tiles='Stamen Toner'
               )
for i,value in enumerate(short_dist_list) :
    if value > 2.4 :
        folium.Marker(
                orig_cor_list[i],
                icon = folium.Icon(color='green')
        ).add_to(m)
        
for i in dest_cor_list :
     folium.Marker(
            i,
        ).add_to(m)
        

saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/조방/시각화자료/'   
saveFileName = '위험지역시각화'

saveFile(m,saveFilePath,saveFileName)


