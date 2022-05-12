import tensorflow as tf
import Settings
import os
import numpy as np
import Train
import mediapipe as mp
import cv2

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
IMAGE_HEIGHT=Settings.IMAGE_HEIGHT
IMAGE_WIDTH=Settings.IMAGE_WIDTH

def load():
    global model
    # model=tf.keras.models.load_model(Settings.MODEL_NAME)
    model=tf.keras.models.load_model(Settings.MOBILE_NET_V2)

def predict_file(image_path:str)->float:
    global model
    img = tf.keras.utils.load_img(
        image_path, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence.{}"
        .format(os.path.basename((Train.class_names[np.argmax(score)])), 100 * np.max(score),score)
    )
    return score

def predict():
    IMAGE_FILES = []
    test_path="test"
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        for i, (dirpath, dirnames, filenames) in enumerate(os.walk(test_path)):
            if dirpath is not test_path:
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
                        if crop_height<64 or crop_width<64:
                            continue
                        annotated_image = image.copy()
                        mp_drawing.draw_detection(annotated_image, detection)
                        crop_img=cv2.resize(crop_img,(IMAGE_HEIGHT,IMAGE_WIDTH))
                        img_array = tf.expand_dims(crop_img, 0)
                        predictions = model.predict(img_array)
                        score = tf.nn.softmax(predictions[0])
                        cv2.imshow("This image most likely belongs to {} with a {:.2f} percent confidence.{}"
                            .format(os.path.basename((Train.class_names[np.argmax(score)])), 100 * np.max(score),score),annotated_image)
                        cv2.waitKey()
    return
load()
# predict_file("test.jpg")
predict()