import random
import folium
import json
import requests
import branca
def generation_oneSector(number, cor_dict_):
    orig_cor_list_=[]
    for i in range(number) :
        ran = random.random()
        x = cor_dict_['x_min'] + (cor_dict_['x_max'] - cor_dict_['x_min']) * ran
        ran = random.random()
        y = cor_dict_['y_min'] + (cor_dict_['y_max'] - cor_dict_['y_min']) * ran
        orig_cor_list_.append((x,y))
    
    return orig_cor_list_

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

def get_CorData(filePath_,fileName_) :
    f = open(filePath_+'/'+fileName_+'.txt','r')
    data = f.readlines()
    
    return data

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

def saveFile(m_,filePath_, fileName_, fileNum_):
    m_.save(filePath_ + fileName_ +str(fileNum_)+'.html')
    



m = folium.Map(location= [37.47852702960704,126.951747165343], zoom_start=15,
               tiles='cartodbpositron'
                #  tiles='Stamen Toner'
               )

# 로드 파일 경로
filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/추천시스템_관악구/simulation_'
fileName = '추천_지역_위치'
folderNum = 0

filePath = filePath + str(folderNum)

data = get_CorData(filePath,fileName)
cordinates = get_cordinate(data)


for i in range(len(cordinates)) :
    folium.Marker(
            cordinates[i],
            icon=folium.Icon(color='beige')
        ).add_to(m)
   
        
        
## 저장 파일 경로
saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/시각화자료_관악구/'   
saveFileName = '추천지역시각화'
savaFileNum = 13

saveFile(m,saveFilePath,saveFileName,savaFileNum)