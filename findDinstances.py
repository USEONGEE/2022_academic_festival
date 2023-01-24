import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from openpyxl import load_workbook
ox.config(use_cache=True, log_console=True)
ox.__version__

## 좌표 데이터 가져오기
def get_CorData() :
    filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/' 
    fileName = input("TYPE FILE NAME :")
    f = open(filePath+fileName+'.txt','r')
    data = f.readlines()
    
    return data

## 좌표 데이터 -> list로 저장하기 (x,y) 형태
cordinates = []
def get_cordinate(li) :
    for i in li :
        rest = i.find(',')
        newline = i.find('\n')
        x_cor = i[0:rest]
        y_cor = i[rest+1:newline]
        cordinates.append((float(x_cor),float(y_cor)))

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

## hard coding 수정 필요
filePath = 'C:/Users/shdbt/Desktop/22년도 학술제/'
fileName = '인천시.xlsx'
sheet = '경로당'
dest_name = getExcelData(filePath+fileName,sheet,'C3','C103') ## 경로당 도로명주소 가져오기
short_dist = []



######### main ########
data = get_CorData()
get_cordinate(data)

# www.openstreetmap.org에서 검색 결과가 city-state-country 단위로 나와야 함 - '마포구, 서울, 대한민국'
G = ox.graph_from_place('중구, 인천, 대한민국', network_type='drive', simplify=False) 

# 출발 지점 /// 나중에 난수로 돌려야 함
orig_node = ox.get_nearest_node(G, (37.44144082986024,126.54219009902306))

#### 최단거리 분석 및 저장 
for i in cordinates :
    dest_node = ox.get_nearest_node(G, i) # 도착 지점
    len = nx.shortest_path_length(G, orig_node, dest_node, weight='length') / 1000
    short_dist.append(str(round(len,1)))
    # print(round(len, 1), "킬로미터")
    
# txt 파일로 저장
w = open('C:/Users/shdbt/Desktop/22년도 학술제/result.txt','w')
forPrint = list(zip(dest_name,short_dist))
for i in forPrint :
    w.write(i[0] + '---->' + i[1] + '\n')



## 여기 밑에는 지금 현재 필요없음


# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import seaborn as sns
# mpl.rc('font', family='NanumGothic') #한글 폰트 적용시
# plt.rcParams["figure.figsize"] = (15,15) #차트 사이즈



# # find the route between these nodes then plot it
# route = nx.shortest_path(G, orig_node, dest_node, weight='length')
# fig, ax = ox.plot_graph_route(G, route, node_size=0, figsize=(15,15))

# # 최단거리 분석 결과의 길이를 확인
# len = nx.shortest_path_length(G, orig_node, dest_node, weight='length') / 1000
# print(round(len, 1), "킬로미터")

# # folium을 통해 파일로 저장
# route_graph_map = ox.plot_route_folium(G, route,
#     # route_map=G, 
#     popup_attribute='length'
# )
# filepath = 'C:/Users/shdbt/Desktop/GRAPH.txt' # 파일 저장 경로
# route_graph_map.save(filepath)



### 2D array 형태로 위치데이터 저장
### for 문으로 라이브러리를 이용해 a -> b 로 가는 경로를 하나씩 분석
### folium과 연동해 자료 저장 or 거리를 측정해 저장 후 txt 파일로 출력
