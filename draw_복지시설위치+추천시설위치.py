import random
import folium
import json
import requests
import branca

def get_CorData(filePath_,fileName_) :
    f = open(filePath_+'/'+fileName_+'.txt','r')
    data = f.readlines()
    
    return data

def get_cordinate(cor_) :
    li = []
    for i in cor_ :
        comma = i.find(',')
        x_cor = i[0:comma]
        y_cor = i[comma+1:]
        li.append((float(x_cor),float(y_cor)))
    
    return li

def saveFile(m_,filePath_, fileName_):
    m_.save(filePath_ + fileName_ +'.html')
    
# 맵 만들기
m = folium.Map(location= [37.47852702960704,126.951747165343], zoom_start=15,
               tiles='cartodbpositron'
                #  tiles='Stamen Toner'
               )

# 복지 시설 위치
filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/좌표데이터/'
fileName = '관악구_노인복지시설'
data = get_CorData(filePath,fileName)
cordinates = get_cordinate(data)

# 추천 시설 위치
recommed_cor = [37.4788978429662,126.90279007817432]
cordinates.append([ 37.4790136047124,126.90667912157463 ])

# 기존 복지 시설 마크 추가하기
for i in range(len(cordinates)) :
    folium.Marker(
            cordinates[i],
            icon = folium.Icon(color='green')
        ).add_to(m)
        
# 추천 시설 마크 추가하기 ## 다시 활성화 해야함
folium.Marker(
    recommed_cor,
    icon = folium.Icon()
).add_to(m)

# cordinates = [
#     [37.48379569432363, 126.95350174295902],
#     [37.48432652661339, 126.95288450855216],
#     [37.48438736941458, 126.95313364571426],
#     [37.484341828032164, 126.95394018005828],
#     [37.479975746602555, 126.95226996718144],
#     [37.484663139017286, 126.95448140402966]
# ]


# for i in range(len(cordinates)) :
#     folium.Marker(
#             cordinates[i],
#             icon = folium.Icon(color='red')
#     ).add_to(m)

## 저장 파일 경로
saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/시각화자료_관악구/'   
saveFileName = '비효율'

saveFile(m,saveFilePath,saveFileName)