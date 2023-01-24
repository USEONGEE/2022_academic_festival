import os
## 개행문자 제거
def delNewLine(li) : 
    newList = []
    for i in li :
        cramps =0
        cramps = i.find('>')
        newline = 0
        newline = i.find('\n')
        if(newline != -1) :
            newList.append(i[cramps+2:newline])
        else :
            newList.append(i[cramps+2: ])
    
    return newList

# 파일 경로
filePath = 'C:/Users/shdbt/Desktop/DATAFILE/조방/시뮬레이션 결과/'
fileName = '수지구'
file = filePath + fileName + '.txt'

# 개행문자 제거하기
r = open(file, 'r')
short_dist = r.readlines()
short_dist = delNewLine(short_dist)

# 파일에서 거리 획득하기
for i in range(len(short_dist)):
    short_dist[i] = float(short_dist[i])

# 비율 계산
count = 0
standardDist = 2.4 ## 기준점 : 단위 킬로미터
for i in short_dist :
    if(i <= standardDist) :
        count += 1

percent = count/len(short_dist)
print("{}% is available".format(int(percent*100)))