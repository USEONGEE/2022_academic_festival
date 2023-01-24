import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from openpyxl import load_workbook
ox.config(use_cache=True, log_console=True)
ox.__version__
import random


## 좌표 데이터 가져오기
def get_CorData() :
    filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/' 
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

## 난수를 발생시켜 출발 지점을 생성
def generation(number,cor_dict):
    orig_node_=[]
    for i in range(number) :
        ran = random.random()
        x = cor_dict['x_min'] + (cor_dict['x_max'] - cor_dict['x_min']) * ran
        ran = random.random()
        y = cor_dict['y_min'] + (cor_dict['y_max'] - cor_dict['y_min']) * ran
        orig_node_.append((x,y))
    
    return orig_node_

## simulation, parameter should be list
def trySimulation(onl,dnl):
    short_dist_ = []
    for i in onl :
        len_ = []
        for j in dnl :
            len = nx.shortest_path_length(G, i, j, weight='length') / 1000
            len_.append(float(round(len,1)))    
        short_dist_.append(min(len_))
        print(min(len_))
    
    return short_dist_

## 난수발생을 위한 정보
NUM = 300
NUM_RECOMMEND = 10
cor_dict_ = {'x_min' : 37.6924881, 'x_max' : 37.7493383, 'y_min' : 127.04230256, 'y_max': 127.06457463} # 300
# cor_dict_ = {'x_min' : 37.7336474, 'x_max' : 37.7559856, 'y_min' : 127.03343195, 'y_max': 127.04978286} # 150
# cor_dict_ = {'x_min' : 37.7310480, 'x_max' : 37.7582719, 'y_min' : 127.08030422, 'y_max': 127.11668179} # 150
cor_recommend_ = {'x_min' : 37.7053666, 'x_max' : 37.7534205, 'y_min' : 127.0447139, 'y_max': 127.1068870}

######### main ########
# '용산구, 서울, 대한민국'  
# '인제군, 강원도, 대한민국'
# '의정부시, 경기도, 대한민국'
#  맵 가져오기 (www.openstreetmap.org에서 검색 결과가 city-state-country 단위로 나와야 함 - '마포구, 서울, 대한민국')
G = ox.graph_from_place('의정부시, 경기도, 대한민국', network_type='walk', simplify=False) 

# 출발 노드
orig_cor = generation(NUM, cor_recommend_)
orig_node_list = []
for i in orig_cor :
    orig_node_list.append(ox.get_nearest_node(G, i))

# 도착 노드
data = get_CorData() 
dest_cor = get_cordinate(data)
dest_node_list = []
for i in dest_cor :
    dest_node_list.append(ox.get_nearest_node(G, i))
    
# 추천 지역 노드
recom_cor = generation(NUM_RECOMMEND, cor_recommend_)
recom_cor_list = []
for i in recom_cor :
    recom_cor_list.append(ox.get_nearest_node(G, i))

# 출발 지점 -> 도착 지점(여러개) 중 최단거리를 저장
short_dist = []
saveFileName = '의정부시_recommend'
####### simulation #######
for i in range(len(recom_cor_list)):
    dest_node_list.append(recom_cor_list[i]) # 추천 노드 추가하기
    short_dist = trySimulation(orig_node_list,dest_node_list) # 추천 노드를 포함해 최단거리 구하기
    # 파일 열기
    w = open('C:/Users/shdbt/Desktop/DATAFILE/학술제/추천시스템_의정부시/' + saveFileName + str(i) + '.txt','w')
    
    for j, value in enumerate(short_dist) : # 저장 부분
        w.write(("{}th person ---> {}").format(j,value) + '\n')
    
    dest_node_list.pop()
    w.close()

# 생선한 파일들과 매핑 되는 추천 지역의 위치 정보 저장하기
w = open('C:/Users/shdbt/Desktop/DATAFILE/학술제/추천시스템_의정부시/추천_지역_위치.txt', 'w')
for i in range(len(recom_cor)) :
    w.write(("{}{}.txt 파일에 추가된 추천 지역의 좌표 값 : {}, {} \n").format(saveFileName,i,recom_cor[i][0],recom_cor[i][1]))
w.close()