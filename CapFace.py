import os
import cv2
import mediapipe as mp
import numpy as np
import time
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
process_created_time=time.time()
frame_count=0
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    HEIGHT, WIDTH, channels = image.shape
    results = face_detection.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    key_pressed=cv2.waitKey(5)
    if results.detections:
      for j,detection in enumerate(results.detections):
        if key_pressed & 0xFF == 32:
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
            cv2.imwrite(f"faces/{process_created_time}_{frame_count}_{j}.jpg", crop_img)
        mp_drawing.draw_detection(image, detection)
    frame_count+=1
    if key_pressed & 0xFF != 27:
        cv2.imshow(f'MediaPipe Face Detection With key pressed:{key_pressed}', cv2.flip(image, 1))
    if key_pressed & 0xFF == 27:
      break
cap.release()