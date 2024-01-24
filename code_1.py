import math
import time
from ultralytics import YOLO



start = time.time()

model = YOLO('best.pt')
results = model.predict(source='.')  # save predictions as labels
result = results[1]

clsList = result.boxes.cls
xywhList = result.boxes.xywh
nameList = result.names
confList = result.boxes.conf

myNameIndex = -1
for i in range(len(nameList)):
    if nameList[i] == 'me':
        myNameIndex = i

# myNameIndex 못찾을 시 예외처리

detectSize = len(clsList)

meIndex = -1
for i in range(detectSize):
    
    cls = clsList[i]
    conf = confList[i]
    if conf > 0.4 and cls == myNameIndex:
        meIndex = i

# meIndex 찾지 못했을대 예외처리
# 여러개를 찾았을때 예외처리

right = False
left = False
xRange = 750
yRange = 250
meX = xywhList[meIndex][0]
meY = xywhList[meIndex][1]

for i in range(detectSize):
    if i == meIndex:
        continue
    cls = clsList[i]
    xywh = xywhList[i]
    # xywh[0] xywh[1] meX meY
    difX =  meX - xywh[0]
    difY = meY - xywh[1] # 양수 == 몬스터가 위에 있음
    if abs(difX) < xRange and difY < yRange:
        if difX < 0:
            print(f"{nameList[int(cls)]} 발견 오른쪽을 공격하세요")
        else:
            print(f"{nameList[int(cls)]} 발견 왼쪽을 공격하세요")
    else:
        print(f"{nameList[int(cls)]}의 거리가 {difX} 으로 멀어서 공격하지 않음")

print(f"걸린 시간 : {time.time()-start}")