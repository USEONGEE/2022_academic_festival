### big-O(n^4)
### 효율이 쓰레기인 코드지만 일단 남겨놓는다. big-O notation이 훨씬 작은 코드를 test.py로 만들었다.

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

# 발생한 난수로 노드 설정하기
def create_node(cor_):
    node_list_ = []
    for i in cor_:
        node_list_.append(ox.get_nearest_node(G, i))
    return node_list_

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

## 변경해줘야하는 값
NUM = 300 # 노인 거주지 선정하기
NUM_RECOMMEND = 10 # 추천 지역 선정하기
NUM_FOLDER = 20 # 전체 폴더 수

## 난수발생을 위한 정보
# 용산구
cor_recommend_ = {'x_min' : 37.52558806471245, 'x_max' : 37.54258917365419, 'y_min' : 126.95558585557764, 'y_max': 127.00530974768438}
# 의정부시
# cor_recommend_ = {'x_min' : 37.7053666, 'x_max' : 37.7534205, 'y_min' : 127.0447139, 'y_max': 127.1068870}

######### main ########
# '용산구, 서울, 대한민국'  
# '의정부시, 경기도, 대한민국'
#  맵 가져오기 (www.openstreetmap.org에서 검색 결과가 city-state-country 단위로 나와야 함 - '마포구, 서울, 대한민국')
G = ox.graph_from_place('용산구, 서울, 대한민국', network_type='walk', simplify=False) 

# 출발 노드
orig_cor = generation(NUM, cor_recommend_)
orig_node_list = create_node(orig_cor)


# 도착 노드
data = get_CorData() 
dest_cor = get_cordinate(data)
dest_node_list = create_node(dest_cor)
    
# 출발 지점 -> 도착 지점(여러개) 중 최단거리를 저장
short_dist = []
saveFileName = '용산구_recommend'
saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/추천시스템_용산구/simulation_'

####### simulation #######
# FILENUM 만큼 추천시스템 돌리기
for i in range(NUM_FOLDER):
    recom_cor = generation(NUM_RECOMMEND, cor_recommend_)
    recom_cor_list = create_node(recom_cor)
    for j in range(len(recom_cor_list)):
        dest_node_list.append(recom_cor_list[j]) # 추천 노드 추가하기
        short_dist_list = trySimulation(orig_node_list,dest_node_list) # 추천 노드를 포함해 최단거리 구하기
        # 파일 열기
        w = open(saveFilePath + str(i) +'/' + saveFileName + str(j) + '.txt','w')

        for k, value in enumerate(short_dist_list) : # 저장 부분
            w.write(("{}th person ---> {}").format(k,value) + '\n')
        
        dest_node_list.pop() # 추천 노드 제거 (중요)
        w.close()
    # 생선한 파일들과 매핑 되는 추천 지역의 위치 정보 저장하기
    w = open(saveFilePath + str(i) +'/' + '추천_지역_위치' + '.txt','w')
    for j in range(len(recom_cor)) :
        w.write(("{}{}.txt 파일에 추가된 추천 지역의 좌표 값 : {}, {} \n").format(saveFileName,j,recom_cor[j][0],recom_cor[j][1]))
    w.close()

