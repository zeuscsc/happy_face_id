import tensorflow as tf
import Settings
import os
import numpy as np
import Train
import mediapipe as mp
import cv2
import time

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
IMAGE_HEIGHT=Settings.IMAGE_HEIGHT
IMAGE_WIDTH=Settings.IMAGE_WIDTH
process_created_time=time.time()
capture_count=0

def load():
    global model
    # model=tf.keras.models.load_model(Settings.MODEL_NAME)
    model=tf.keras.models.load_model(Settings.MOBILE_NET_V2)
    # model=tf.keras.models.load_model(Settings.UNET)
load()
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.75) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        image=cv2.flip(image, 1)
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if image is None:
            continue
        # image=cv2.flip(image, 1)
        key_pressed=cv2.waitKey(5)
        HEIGHT, WIDTH, channels = image.shape
        if HEIGHT<120 or WIDTH<120:
            continue
        if results.detections:
            for j,detection in enumerate(results.detections):
                crop_img=None
                box=detection.location_data.relative_bounding_box
                point1=[np.int32(box.xmin*WIDTH),np.int32(box.ymin*HEIGHT)]
                point2=[np.int32((box.xmin+box.width)*WIDTH),np.int32((box.ymin+box.height)*HEIGHT)]
                if point1[0]<0:
                    point1[0]=0
                if point1[1]<0:
                    point1[1]=0
                if point2[0]>WIDTH:
                    point2[0]=WIDTH
                if point2[1]>HEIGHT:
                    point2[1]=HEIGHT
                crop_img = image[point1[1]:point2[1], point1[0]:point2[0]]
                crop_height, crop_width, crop_channels = crop_img.shape
                if crop_height<64 or crop_width<64:
                    continue
                
                crop_img=cv2.resize(crop_img,(IMAGE_HEIGHT,IMAGE_WIDTH))
                img_array = tf.expand_dims(crop_img, 0)
                predictions = model.predict(img_array)
                score = tf.nn.softmax(predictions[0])
                if key_pressed & 0xFF == 32:
                    cv2.imwrite(f"faces/{process_created_time}_{capture_count}_{j}.jpg", crop_img)
                    capture_count+=1
                mp_drawing.draw_detection(image, detection)
                max_score=np.max(score)
                if max_score>0.99:
                    label=os.path.basename((Train.class_names[np.argmax(score)]))
                else:
                    label="people"
                cv2.putText(image,f"{label}",(np.int32(box.xmin*WIDTH),np.int32(box.ymin*HEIGHT)),
                    cv2.FONT_HERSHEY_SIMPLEX,3, (0, 255, 0), 2, cv2.LINE_AA)
                if label=="people":
                    cv2.rectangle(image, point1, point2, (0, 255, 0), -1)
        cv2.imshow('Face ID', image)
        if key_pressed & 0xFF == 27:
            break
        
cap.release()