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

def get_CorData(filePath_) :
    f = open(filePath_+'/'+'추천_지역_위치'+'.txt','r')
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
    

# # 관악구_서울
cor_dict1 = {'x_min' : 37.46296967116968, 'x_max' : 37.49010541289464, 'y_min' : 126.91680711200942, 'y_max': 126.94262024467017} # 300
cor_dict2 = {'x_min' : 37.477961325918585, 'x_max' : 37.48798576400957, 'y_min' : 126.94581206859225, 'y_max': 126.95874020780428} # 150
cor_dict3 = {'x_min' : 37.46839824329764, 'x_max' : 37.47618828174779, 'y_min' : 126.95997182908718, 'y_max': 126.9813574398222} # 150
cor_dict4 = {'x_min' : 37.475565108574706, 'x_max' : 37.4804503816687, 'y_min' : 126.95803480443627, 'y_max': 126.96345895949703} # 50
cor_dict_list = [cor_dict1, cor_dict2, cor_dict3, cor_dict4]
cor_number_list = [150,75,75,20] # Σvalue = 노인 인구수

m = folium.Map(location= [37.47852702960704,126.951747165343], zoom_start=15,
               tiles='cartodbpositron'
                #  tiles='Stamen Toner'
               )

cordinates = generations_manySector(cor_number_list, cor_dict_list)

for i in range(len(cordinates)) :
    folium.Marker(
            cordinates[i],
            color='darkblue'
        ).add_to(m)
        
        
## 저장 파일 경로
saveFilePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/시각화자료_관악구/'   
saveFileName = '난수노인시각화'
savaFileNum = 55

saveFile(m,saveFilePath,saveFileName,savaFileNum)