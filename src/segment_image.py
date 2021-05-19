from tensorflow import keras
import numpy as np
import cv2
IMAGE_SIZE = (256, 256)
MASK_PREDICT_SHAPE = (1, 256, 256, 3)
# model = keras.models.load_model("model.h5")

def get_mask_from_image(image, threshold_value = 0.5, same_size = True):
    copy_image = cv2.resize(image, IMAGE_SIZE)
    copy_image = np.reshape(copy_image, MASK_PREDICT_SHAPE)
    predict_mask = model.predict(copy_image)[0]

    _, threshsold_mask = cv2.threshold(predict_mask, threshold_value, 1, cv2.THRESH_BINARY)
    mask = cv2.normalize(threshsold_mask, None, 0, 1, cv2.NORM_MINMAX).astype(np.uint8)
    mask = np.reshape(mask, (256, 256, 1))
    if not same_size:
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
    return mask

def get_object_from_image(image, threshold_value = 0.5, mask = None):
    if mask == None:
        mask = get_mask_from_image(image, threshold_value)
    copy_image = image.copy()
    copy_image[mask == 0 ] = 0
    return copy_image

def get_bokeh_image(image, blur_shape = (21,21), blur_sigma = 1.5, threshold_value = 0.5, mask = None):
    if mask == None:
        mask = get_mask_from_image(image, threshold_value, False)
    width = image.shape[1]
    height = image.shape[0]
    mask = np.reshape(mask, (height, width, 1))
    
    copy_image = image.copy()
    blur_image = cv2.GaussianBlur(copy_image, blur_shape, blur_sigma)
    blur_image = cv2.normalize(blur_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    result = np.where(mask == 0, blur_image, copy_image)
    return result