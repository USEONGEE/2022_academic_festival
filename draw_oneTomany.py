import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from openpyxl import load_workbook
ox.config(use_cache=True, log_console=True)
ox.__version__
import random
import folium

## 좌표 데이터 가져오기
def get_CorData(filePath_,fileName_) :
    f = open(filePath_+ fileName_ +'.txt','r')
    data = f.readlines()
    
    return data

## 좌표 데이터 -> list로 저장하기 (x,y) 형태
def get_cordinate(cor_) :
    li = []
    for i in cor_ :
        start = i.find(':')
        comma = i.find(',')
        newline = i.find('\n')
        x_cor = i[start+1:comma]
        if (newline != -1):
            y_cor = i[comma+1:newline]
        else :
            y_cor = i[comma+1:]
        li.append((float(x_cor),float(y_cor)))
    
    return li

## 시작 지점, 끝 지점 map 에 추가하기
def addMark(m, startCor, endCor) :
    
    mark1 = folium.Marker(
        list(startCor),
        popup = '<b>시작 지점</b>', # 툴팁을 클릭시 나타나는 설명창
        icon = folium.Icon(color = 'blue'), # 아이콘의 모양과 색을 바꿀 수 있음
        tooltip="시작 지점"
    )
    mark2 = folium.Marker(
        list(endCor),
        popup = '<b>도착 지점</b>',
        icon = folium.Icon(color = 'green'), # Icon에 mouse pointer를 가져다대면 다양한 parameter 종류를 볼 수 있음.
        tooltip = "도착 지점"
    )
    mark1.add_to(m), mark2.add_to(m)
    
    return m

## 노드 생성, parameter data type should be list
def create_node(cor_):
    node_list_ = []
    for i in cor_:
        node_list_.append(ox.get_nearest_node(G, i))
    return node_list_

######### main ########

# 맵 가져오기 (www.openstreetmap.org에서 검색 결과가 city-state-country 단위로 나와야 함 - '마포구, 서울, 대한민국')
G = ox.graph_from_place('관악구, 서울, 대한민국', network_type='walk', simplify=False) 

# 출발 노드
orig_cor = (37.47956882138677,126.90245851205108)
orig_node = create_node([orig_cor])
orig_node = orig_node[0]
# 도착 노드
filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/좌표데이터/'
fileName = '관악구_노인복지시설'
data = get_CorData(filePath, fileName)
dest_cor_list = get_cordinate(data)
dest_cor_list.append((37.4790136047124,126.90667912157463))
dest_node_list = create_node(dest_cor_list)
####### simulation #######
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
mpl.rc('font', family='NanumGothic') #한글 폰트 적용시
plt.rcParams["figure.figsize"] = (15,15) #차트 사이즈


count = 0
countFordest = 0
for i in dest_node_list :
    file = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/시각화자료_관악구/보고서용2/'
    
    route = nx.shortest_path(G, orig_node, i, weight='length')

    route_graph_map = ox.plot_route_folium(G, route,
    # route_map=G, 
    popup_attribute='length'
    )

    file = file + str(count) + '.html'
    route_graph_map = addMark(route_graph_map, orig_cor, dest_cor_list[countFordest]) # data type : folium.folium.map
    route_graph_map.save(file)
    
    count += 1
    countFordest += 1