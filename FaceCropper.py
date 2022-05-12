import os
import cv2
import mediapipe as mp
import numpy as np
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

IMAGE_FILES = ["ORIGINAL_IMAGE.jpg"]
IMAGE_FILES = []
assets_path="assets"
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(assets_path)):
        if dirpath is not assets_path:
            dirpath=dirpath.replace("\\","/")
            dirpath_components = dirpath.split("/")
            label = dirpath_components[-1]
            for f in filenames:
                file_path = os.path.join(dirpath, f)
                # IMAGE_FILES.append(file_path)
                image = cv2.imread(file_path)
                if image is None:
                    continue
                HEIGHT, WIDTH, channels = image.shape
                if HEIGHT<120 or WIDTH<120:
                    continue
                results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if not results.detections:
                    continue
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
                    if crop_height<120 or crop_width<120:
                        continue
                    cv2.imwrite(f"datasets/{label}/{f}_({j}).jpg", crop_img)