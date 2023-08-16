# YOLO object detection
import cv2 as cv
import numpy as np
import time
import os
import requests
from tqdm import tqdm


# this function is used to download the yolo3 weignts if they aren't already downloaded
def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    with open(save_path, "wb") as file, tqdm(
        desc=save_path,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


WHITE = (255, 255, 255)
img = None
img0 = None
outputs = None


current_directory = os.path.dirname(__file__)

classes = open(os.path.join(current_directory, "coco.names")).read().strip().split("\n")
np.random.seed(42)


# Give the configuration and weight files for the model and load the network.
weights_path = os.path.join(
    current_directory, "yolov3.weights"
)  # Specify the file name here
url = "https://pjreddie.com/media/files/yolov3.weights"  # Specify the URL to download from

if not os.path.exists(weights_path):
    print(f"Downloading {weights_path}...")
    download_file(url, weights_path)
    print(f"{weights_path} downloaded.")

net = cv.dnn.readNetFromDarknet(
    os.path.join(current_directory, "yolov3.cfg"), weights_path
)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# determine the output layer
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


def process_image(imagefile):
    global img, img0, outputs, ln
    # Convert bytes to numpy array
    nparr = np.frombuffer(imagefile, np.uint8)
    open_cv_image = cv.imdecode(nparr, cv.IMREAD_COLOR)
    img0 = open_cv_image
    img = img0.copy()
    blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    net.setInput(blob)
    outputs = net.forward(ln)
    outputs = np.vstack(outputs)

    mon_text = post_process(img, outputs, 0.7)
    return set(mon_text)


def post_process(img, outputs, conf):
    H, W = img.shape[:2]

    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        scores = output[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        if confidence > conf:
            x, y, w, h = output[:4] * np.array([W, H, W, H])
            p0 = int(x - w // 2), int(y - h // 2)
            p1 = int(x + w // 2), int(y + h // 2)
            boxes.append([*p0, int(w), int(h)])
            confidences.append(float(confidence))
            classIDs.append(classID)

    indices = cv.dnn.NMSBoxes(boxes, confidences, conf, conf - 0.1)
    mo_text = []
    if len(indices) > 0:
        for i in indices.flatten():
            mo_text.append(classes[classIDs[i]])
    return mo_text
