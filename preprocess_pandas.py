## 하나의 엑셀파일에 존재하는 '도로명주소 + 위도' 를 시군구 별로 구별해서 파일로 저장해주기
## 

import pandas as pd

filePath = 'C:/Users/shdbt/Desktop/DATAFILE/조방/'
fileName = 'policeStation.xlsx'
sheetName = 'DATA'

address_df = pd.read_excel(filePath+fileName, engine='openpyxl', sheet_name=sheetName, usecols='C')
cor_df = pd.read_excel(filePath+fileName, engine='openpyxl', sheet_name=sheetName, usecols='E')

# 도로명 주소
address_list = list(address_df.values) # list의 개체는 아직 numpy의 string이다. -> str로 형변환 필요.

address_list2 = []
for i in address_list : # typecasing 후 list에 저장 => set()으로 typecasting이 안되는 문제 해결
    i = str(i)
    index1 = i.find(' ')
    tmp = i[index1+1:]
    index2 = tmp.find(' ')
    address_list2.append(i[2:index1 + index2 + 1])

address_list = address_list2
del address_list2

# 위도
cor_list = list(cor_df.values)
cor_list2 = []
for i in cor_list :
    cor_list2.append(str(i)[2:-2])
cor_list = cor_list2
del cor_list2

# 데이터 합치기 (2D list, data[0] == 도로명주소, data[1] == 위도)
data = list(zip(address_list, cor_list))

# ~~구 까지 하나로 묶어서 set으로 표현 => 몇 개의 구가 전국에 존재하는지 파악
address_set = set(address_list)

# ~~구 까지의 주소를 key값, key에 해당하는 주소들을 value로 가지는 dictionary 생성
address_dict = {}
for i in address_set :
    address_dict[i] = []

for i in data :
    for j in address_dict.keys() :
        if i[0] == j :
            address_dict[i[0]].append(i[1])

## key를 파일명, value를 값으로 갖는 파일 생성
filePath = 'C:/Users/shdbt/Desktop/DATAFILE/조방/예시/'
for key, value in address_dict.items() :
    f = open(filePath + key + '.txt', 'w')
    for i in value :
        f.write(i + '\n')
    f.close()