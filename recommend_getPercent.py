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
filePath = 'C:/Users/shdbt/Desktop/DATAFILE/학술제/추천시스템_관악구/simulation_19/'
fileName = '관악구_recommend'
file = filePath + fileName + '.txt'

# 000_recommend.txt 파일 갯수
LEN = 15
STANDARD = 0.6 ## 기준점 : 단위 킬로미터
for i in range(LEN) :
    # 개행문자 제거하기
    file = filePath + fileName + str(i) + '.txt'
    r = open(file, 'r')
    short_dist = r.readlines()
    short_dist = delNewLine(short_dist)
    # 파일에서 거리 획득하기
    for i in range(len(short_dist)):
        short_dist[i] = float(short_dist[i])
    # 비율 계산
    count = 0
    for i in short_dist :
        if(i <= STANDARD) :
            count += 1
    # 비율 계산 후 시각화
    percent = count/len(short_dist)
    print("{}% is available".format(int(percent*100)))
    r.close()


# # 개행문자 제거하기
# r = open(file, 'r')
# short_dist = r.readlines()
# short_dist = delNewLine(short_dist)

# # 파일에서 거리 획득하기
# for i in range(len(short_dist)):
#     short_dist[i] = float(short_dist[i])

# # 비율 계산
# count = 0
# standardDist = 0.6 ## 기준점 : 단위 킬로미터
# for i in short_dist :
#     if(i <= standardDist) :
#         count += 1

# percent = count/len(short_dist)
# print("{}% is available".format(int(percent*100)))