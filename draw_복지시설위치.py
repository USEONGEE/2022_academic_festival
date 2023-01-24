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
    

m = folium.Map(location= [37.47852702960704,126.951747165343], zoom_start=15,
               tiles='cartodbpositron'
                #  tiles='Stamen Toner'
               )

filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/좌표데이터/'
fileName = '관악구_노인복지시설'

data = get_CorData(filePath,fileName)
cordinates = get_cordinate(data)

for i in range(len(cordinates)) :
    folium.Marker(
            cordinates[i],
            # icon = folium.Icon(color='black')
        ).add_to(m)
        
        
        
## 저장 파일 경로
saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/시각화자료_관악구/'   
saveFileName = '복지시설위치'

saveFile(m,saveFilePath,saveFileName)