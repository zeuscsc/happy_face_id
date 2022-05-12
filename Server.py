import tensorflow as tf
from sanic import Sanic, json
from sanic_cors import CORS, cross_origin
import os
import base64
import Settings
import pathlib
import mediapipe as mp
import cv2
import numpy as np
import time
import json as JSON
app = Sanic("Happy-Face-ID")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

data_dir ="datasets"
data_dir = pathlib.Path(data_dir)
class_names=list(data_dir.glob('*/'))

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
IMAGE_HEIGHT=Settings.IMAGE_HEIGHT
IMAGE_WIDTH=Settings.IMAGE_WIDTH

UPLOAD_DIR="uploads"

def load():
    global model
    model=tf.keras.models.load_model(Settings.MOBILE_NET_V2)
def predict_file(image_path:str)->str:
    global model
    img = tf.keras.utils.load_img(
        image_path, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH)
    )
    return predict_image(img)
def predict_image(img)->str:
    global model
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence.{}"
        .format(os.path.basename((class_names[np.argmax(score)])), 100 * np.max(score),score)
    )
    class_name=os.path.basename((class_names[np.argmax(score)]))
    print(class_name)
    return class_name
    # return JSON.dumps({"classification":class_name, "score":score})
    # return f'{"class":{class_name},"score":{score}}'

@app.post("/get-identity")
async def get_identity(request):
    url_blob=request.body
    blob=base64.b64decode(url_blob)
    current_time=time.time()
    image_path=f"{UPLOAD_DIR}/{current_time}.jpg"
    image_result = open(image_path, 'wb')
    image_result.write(blob)
    return json(predict_file(image_path))
@app.post("/test")
async def test(request):
    return json({"status":"success"})
app.static("","public")

if __name__ == "__main__":
    load()
    app.run(host="0.0.0.0", port=8000)