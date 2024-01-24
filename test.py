from ultralytics import YOLO

model = YOLO('best.pt')

results = model.predict(source='1.png', save=True, save_txt=True)  # save predictions as labels

for result in results:
    # detection
    print(result.boxes.xyxy)   # box with xyxy format, (N, 4)
    print(result.boxes.xywh)  # box with xywh format, (N, 4)
    print(result.boxes.xyxyn)  # box with xyxy format but normalized, (N, 4)
    print(result.boxes.xywhn)  # box with xywh format but normalized, (N, 4)
    print(result.boxes.conf)   # confidence score, (N, 1)
    print(result.boxes.cls)    # cls, (N, 1)

