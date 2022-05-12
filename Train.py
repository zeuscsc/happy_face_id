import imp
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import pathlib
import Settings

data_dir ="datasets"
data_dir = pathlib.Path(data_dir)
image_count = len(list(data_dir.glob('*/*.jpg')))

BATCH_SIZE=Settings.BATCH_SIZE
IMAGE_HEIGHT=Settings.IMAGE_HEIGHT
IMAGE_WIDTH=Settings.IMAGE_WIDTH
AUTOTUNE = tf.data.AUTOTUNE
USE_GPU=True

class_names=list(data_dir.glob('*/'))
print(class_names)

if USE_GPU is False:
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

print("Num CPUs Available: ", len(tf.config.list_physical_devices('CPU')))
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def prepare():
    global train_ds
    global val_ds

    # Loading dataset from folders
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

    # Configure the dataset for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    return

def train():
    global model
    global train_ds
    global val_ds

    prepare()

    # Data augmentation
    data_augmentation = tf.keras.Sequential(
    [
        tf.keras.layers.RandomFlip("horizontal_and_vertical",
                        input_shape=(IMAGE_HEIGHT,
                                    IMAGE_WIDTH,
                                    3)),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomTranslation(0.05,0.05)
    ]
    )

    # Preparing model
    num_classes = len(class_names)
    mirrored_strategy = tf.distribute.MirroredStrategy()
    with mirrored_strategy.scope():
        model = tf.keras.Sequential([
        data_augmentation,# Data augmentation Layer
            tf.keras.layers.Rescaling(1./255),# Standardize the data (0~1)
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(180, activation='relu'),
            tf.keras.layers.Dense(num_classes)
        ])
        base_learning_rate = 0.0001
        model.compile(
            # optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])
        model.summary()
        history=model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=100
        )
        model.save(Settings.MODEL_NAME,save_format='h5')
    return

if __name__ == '__main__':
    train()

