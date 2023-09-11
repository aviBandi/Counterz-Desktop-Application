from ultralytics import YOLO
import cv2
import cvzone
import math
from workingOnAppv9.detectionCode.sort import *



model = YOLO("../Yolo-Weights/yolov8n.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

#
# mask = cv2.imread('mask.png')

tracker = Sort(max_age=20,min_hits=3,iou_threshold=0.3)
totalCount = []
limits = [300,397,673,397]
# limits = [0,0,100,100]

# limits = [int(190.2857142857143), int(478.28571428571433), int(628.7142857142858), int(489.8571428571429)]
# limits = [92.57142857142858, 504.00000000000006, 618.4285714285714, 509.14285714285717]
# for each in limits:
#     each = int(each)
def count(limits, classType, cap, mask):
    try:
        while True:
            new_frame_time = time.time()
            success, img = cap.read()
            imgRegion = cv2.bitwise_and(img,mask)
            results = model(imgRegion, stream=True)

            detections = np.empty((0,5))

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Bounding Box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                    w, h = x2 - x1, y2 - y1
                    # Confidence.

                    conf = math.ceil((box.conf[0] * 100)) / 100
                    # Class Name
                    cls = int(box.cls[0])
                    currentclass = classNames[cls]

                    if currentclass == classType and conf > 0.3:
                        # cvzone.putTextRect(img, f'{currentclass} {conf}', (max(0, x1), max(35, y1)), scale=0.6, thickness=1,offset=3)
                        # cvzone.cornerRect(img, (x1, y1, w, h), l=10,rt=5)
                        currentArray = np.array([x1,y1,x2,y2,conf])
                        detections = np.vstack((detections,currentArray))

            resultsTracker = tracker.update(detections)

            cv2.line(img,(limits[0],limits[1]),(limits[2],limits[3]),(0,0,255),5)
            for result in resultsTracker:
                x1,y1,x2,y2,ID = result
                x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
                print(result)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h), l=10, rt=2,colorR=(255,0,255))
                # cvzone.putTextRect(img, f'{int(ID)}', (max(0, x1), max(35, y1)), scale=2, thickness=3, offset=10)

                cx,cy = x1+w//2,y1+h//2
                cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1]-15<cy<limits[1]+15:
                    if totalCount.count(ID) == 0:
                        totalCount.append(ID)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

            cvzone.putTextRect(img, f'{classType} Count: {len(totalCount)}', (50,50))


            cv2.imshow("Image", img)
            cv2.imshow('imgregion',imgRegion)
            cv2.waitKey(1)
    except:
        return len(totalCount)

if __name__ == '__main__':
    limits = [77, 520, 649, 520]
    count(limits,"car", cv2.VideoCapture("cars.mp4"), cv2.imread("../images/mask.png"))