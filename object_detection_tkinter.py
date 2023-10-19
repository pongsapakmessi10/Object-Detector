import numpy as np
import cv2

all_class = ["BACKGROUND", "AEROPLANE", "BICYCLE", "BIRD", "BOAT",
	"BOTTLE", "BUS", "CAR", "CAT", "CHAIR", "COW", "DININGTABLE",
	"COINS", "HORSE", "MOTORBIKE", "PERSON", "POTTEDPLANT", "BOOK",
	"SOFA", "TRAIN", "TVMONITOR", "BOTTLE", "GLASS", "FAN", "SCISSOR", "CAT", "EYEGLASSES"]

colors = np.random.uniform(0, 100, size=(len(all_class), 3))

network = cv2.dnn.readNetFromCaffe("./MobileNetSSD/MobileNetSSD.prototxt", "./MobileNetSSD/MobileNetSSD.caffemodel")


def process_frame(frame):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    network.setInput(blob)
    detections = network.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.4:
            class_index = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{} [{:.0f}%]".format(all_class[class_index], confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY), colors[class_index], 2)

            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX + 20, y + 5), cv2.FONT_HERSHEY_PLAIN, 1.6, (255, 255, 255), 1)

    return frame
