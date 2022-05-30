import tensorflow as tf
import Settings
import pathlib

BATCH_SIZE=Settings.BATCH_SIZE
IMAGE_HEIGHT=Settings.IMAGE_HEIGHT
IMAGE_WIDTH=Settings.IMAGE_WIDTH
AUTOTUNE = tf.data.AUTOTUNE
USE_GPU=True
data_dir ="datasets"
data_dir = pathlib.Path(data_dir)
# class_names=["people","winnie","zeus","stella"]
class_names=list(data_dir.glob('*/'))
print(class_names)
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size=BATCH_SIZE)
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size=BATCH_SIZE)
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal_and_vertical'),
    tf.keras.layers.RandomRotation(0.3),
    tf.keras.layers.RandomZoom(0.4),
    tf.keras.layers.RandomTranslation(0.05,0.05),
    tf.keras.layers.RandomContrast(0.2)
])
preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
rescale = tf.keras.layers.Rescaling(1./127.5, offset=-1)
IMG_SIZE = (IMAGE_HEIGHT, IMAGE_WIDTH)
IMG_SHAPE = IMG_SIZE + (3,)
base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(len(class_names))
inputs = tf.keras.Input(shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = base_model(x, training=False)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = tf.keras.Model(inputs, outputs)
base_learning_rate = 0.0001
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
model.summary()
initial_epochs = 100
history = model.fit(train_ds,
                    epochs=initial_epochs,
                    validation_data=val_ds)
model.save(Settings.MOBILE_NET_V2,save_format='h5')