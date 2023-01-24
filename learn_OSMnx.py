import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
ox.config(use_cache=True, log_console=True)
ox.__version__

# www.openstreetmap.org에서 검색 결과가 city-state-country 단위로 나와야 함 - '마포구, 서울, 대한민국'
G = ox.graph_from_place('성남시, 경기도, 대한민국', network_type='drive', simplify=False) 

# fig, ax = ox.plot_graph(G, figsize=(12,12), node_size=0, edge_linewidth=0.5)

orig_node = ox.get_nearest_node(G, (37.450976636253976,127.12898487760484 )) #가천대
dest_node = ox.get_nearest_node(G, ( 37.394757853461066,127.1110396967335)) #근호네

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
mpl.rc('font', family='NanumGothic') #한글 폰트 적용시
plt.rcParams["figure.figsize"] = (15,15) #차트 사이즈

# find the route between these nodes then plot it
route = nx.shortest_path(G, orig_node, dest_node, weight='length')
fig, ax = ox.plot_graph_route(G, route, node_size=0, figsize=(15,15)) # osmnx 메소드로 시각화 

# 최단거리 분석 결과의 길이를 확인
len = nx.shortest_path_length(G, orig_node, dest_node, weight='length') / 1000
print(round(len, 1), "킬로미터")



# folium을 통해 파일로 저장
route_graph_map = ox.plot_route_folium(G, route,
    # route_map=G, 
    popup_attribute='length'
)
filepath = 'C:/Users/shdbt/Desktop/GRAPH.html' # 파일 저장 경로
route_graph_map.save(filepath)

### 2D array 형태로 위치데이터 저장
### for 문으로 라이브러리를 이용해 a -> b 로 가는 경로를 하나씩 분석
### folium과 연동해 자료 저장 or 거리를 측정해 저장 후 txt 파일로 출력
