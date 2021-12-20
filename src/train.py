import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *
from sklearn.model_selection import train_test_split
import cv2
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
IMG_CHANNELS, IMG_WIDTH, IMG_HEIGHT = 3, 256, 256

X_ids = next(os.walk('data/images'))[2]
y_ids = next(os.walk('data/masks'))[2]

LENGTH_DATA = 20000

x = np.zeros((LENGTH_DATA+1, 256, 256, 3), dtype=np.float32)
y = np.zeros((LENGTH_DATA+1, 256, 256, 1), dtype=np.bool)

for n, id_ in enumerate(X_ids):
    os.system("cls")
    print(f'load image {id_}. Loaded {n}/{LENGTH_DATA} image')
    image = cv2.imread(f'data/images/{id_}')
    image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    x[n] = image

    mask = cv2.imread(f'data/masks/{y_ids[n]}', 0)
    mask = cv2.resize(mask, (IMG_WIDTH, IMG_HEIGHT))
    y[n] = np.reshape(mask, (IMG_WIDTH, IMG_HEIGHT, 1))
    if n == LENGTH_DATA:
      break

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

# fig = plt.figure()
# ax1, ax2 = fig.subplots(1, 2)
# ax1.imshow(tf.keras.preprocessing.image.array_to_img(X_train[1]))
# ax2.imshow(tf.keras.preprocessing.image.array_to_img(y_train[1]))
# plt.show()

inputs = tf.keras.layers.Input((256, 256, 3))
s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)

#Contraction path
c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
c1 = tf.keras.layers.Dropout(0.1)(c1)
c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)

c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
c2 = tf.keras.layers.Dropout(0.1)(c2)
c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2)
 
c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
c3 = tf.keras.layers.Dropout(0.2)(c3)
c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
p3 = tf.keras.layers.MaxPooling2D((2, 2))(c3)
 
c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
c4 = tf.keras.layers.Dropout(0.2)(c4)
c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
p4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)
 
c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
c5 = tf.keras.layers.Dropout(0.3)(c5)
c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

#Expansive path 
u6 = tf.keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
u6 = tf.keras.layers.concatenate([u6, c4])
c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
c6 = tf.keras.layers.Dropout(0.2)(c6)
c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)
 
u7 = tf.keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
u7 = tf.keras.layers.concatenate([u7, c3])
c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
c7 = tf.keras.layers.Dropout(0.2)(c7)
c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)
 
u8 = tf.keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
u8 = tf.keras.layers.concatenate([u8, c2])
c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
c8 = tf.keras.layers.Dropout(0.1)(c8)
c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)
 
u9 = tf.keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
u9 = tf.keras.layers.concatenate([u9, c1], axis=3)
c9 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
c9 = tf.keras.layers.Dropout(0.1)(c9)
c9 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)
 
outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)
 
model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# model.summary()

# tf.keras.utils.plot_model(model, show_shapes=True)

results = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=3, epochs=25)
model.save("model.h5")

# summarize history for accuracy
plt.plot(results.history['accuracy'])
plt.plot(results.history['val_accuracy'])
plt.plot(results.history['loss'])
plt.plot(results.history['val_loss'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train_acc', 'test_acc', 'train_loss', 'test_loss'], loc='upper left')
plt.show()

# # summarize history for loss
# plt.plot(results.history['loss'])
# plt.plot(results.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()

# import random
# model.save("/content/gdrive/MyDrive/ml/model.h5")
# test_id = random.choice(X_ids)
# img = tf.keras.preprocessing.image.load_img(f"/content/gdrive/MyDrive/ml/images/{test_id}", target_size=(256, 256))
# input_array = tf.keras.preprocessing.image.img_to_array(img)
# input_array = np.array([input_array])  # Convert single image to a batch.
# mask = model.predict(input_array)[0]
# mask = np.reshape(mask, (256 *256))
# mask = np.where(mask < 0.5, 0, 1)
# mask = np.reshape(mask, (256, 256, 1))
# mask = cv2.normalize(mask, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# fig = plt.figure(figsize=(16,9))
# ax1, ax2, ax3 = fig.subplots(1, 3)
# ax1.imshow(img)
# ax2.imshow(tf.keras.preprocessing.image.load_img(f"/content/gdrive/MyDrive/ml/masks/{test_id}", target_size=(256, 256)))
# ax3.imshow(mask, cmap="gray")
# plt.show()

# mask

# model.save("model_2.h5")

# model_g = tf.keras.models.load_model("/content/gdrive/MyDrive/ml/model.h5")
# model_l = tf.keras.models.load_model("model.h5")

# import random
# import cv2
# # model.save("/content/gdrive/MyDrive/ml/model.h5")
# test_id = random.choice(X_ids)

# img = tf.keras.preprocessing.image.load_img(f"/content/gdrive/MyDrive/ml/images/{test_id}", target_size=(256, 256))
# input_array = tf.keras.preprocessing.image.img_to_array(img)
# input_array = np.array([input_array])  # Convert single image to a batch.
# predictions = model.predict(input_array)
# m = np.array(predictions[0])
# m_g = np.array(model_g.predict(input_array)[0])
# m_l = np.array(model_l.predict(input_array)[0])

# m = cv2.normalize(m, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
# m_g = cv2.normalize(m_g, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
# m_l = cv2.normalize(m_l, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# fig = plt.figure(figsize=(16,9))
# (ax1, ax2), (ax3, ax4), (ax5, ax6) = fig.subplots(3, 2)
# # ax3, ax4 = fig.subplots(1, 2)
# # ax5, ax6 = fig.subplots(1, 2)
# ax1.imshow(img)
# ax2.imshow(tf.keras.preprocessing.image.load_img(f"/content/gdrive/MyDrive/ml/masks/{test_id}", target_size=(256, 256)))
# ax3.imshow(m, cmap="gray")
# ax4.imshow(m_g, cmap="gray")
# ax5.imshow(m_l, cmap="gray")
# ax6.imshow(img)
# plt.show()

# fig.subplots(3, 2)

