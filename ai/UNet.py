import tensorflow as tf
import Settings
import pathlib
import numpy as np

BATCH_SIZE=Settings.BATCH_SIZE
IMAGE_HEIGHT=Settings.IMAGE_HEIGHT
IMAGE_WIDTH=Settings.IMAGE_WIDTH
N_CHANNELS=3
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
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(len(class_names))

NODE_SCALER=np.int32(IMAGE_HEIGHT/128)

initializer = 'he_normal'
inputs = tf.keras.layers.Input(shape=(IMAGE_HEIGHT,IMAGE_WIDTH,N_CHANNELS))
data_augment = data_augmentation(inputs)
conv_enc_1 = tf.keras.layers.Conv2D(64*NODE_SCALER, 3, activation='relu', padding='same', kernel_initializer=initializer)(data_augment)
conv_enc_1 = tf.keras.layers.Conv2D(64*NODE_SCALER, 3, activation = 'relu', padding='same', kernel_initializer=initializer)(conv_enc_1)

max_pool_enc_2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_1)
conv_enc_2 = tf.keras.layers.Conv2D(128*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(max_pool_enc_2)
conv_enc_2 = tf.keras.layers.Conv2D(128*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_2)

max_pool_enc_3 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_2)
conv_enc_3 = tf.keras.layers.Conv2D(256*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(max_pool_enc_3)
conv_enc_3 = tf.keras.layers.Conv2D(256*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_3)

max_pool_enc_4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_3)
conv_enc_4 = tf.keras.layers.Conv2D(512*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(max_pool_enc_4)
conv_enc_4 = tf.keras.layers.Conv2D(512*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv_enc_4)

maxpool = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_enc_4)
conv = tf.keras.layers.Conv2D(1024*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(maxpool)
conv = tf.keras.layers.Conv2D(1024*NODE_SCALER, 3, activation = 'relu', padding = 'same', kernel_initializer = initializer)(conv)
x = global_average_layer(conv)
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
model.save(Settings.UNET,save_format='h5')