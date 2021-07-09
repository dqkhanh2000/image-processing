from tensorflow import keras
import numpy as np
import cv2
IMAGE_SIZE = (256, 256)
MASK_PREDICT_SHAPE = (1, 256, 256, 3)
model = None

def get_model():
    global model
    if model == None:
        model = keras.models.load_model("model.h5")
    return model

def get_mask_from_image(image, threshold_value = 0.5, same_size = False):
    copy_image = cv2.resize(image, IMAGE_SIZE)
    copy_image = np.reshape(copy_image, MASK_PREDICT_SHAPE)
    predict_mask = get_model().predict(copy_image)[0]
    
    _, threshsold_mask = cv2.threshold(predict_mask, threshold_value, 1, cv2.THRESH_BINARY)
    mask = cv2.normalize(threshsold_mask, None, 0, 1, cv2.NORM_MINMAX).astype(np.uint8)
    mask = np.reshape(mask, (256, 256, 1))
    if not same_size:
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
    return mask

def get_object_from_image(image, threshold_value = 0.5, mask = None):
    if len(mask) == 0:
        mask = get_mask_from_image(image, threshold_value)
    copy_image = image.copy()
    copy_image[mask == 0 ] = 0
    return copy_image

def get_bokeh_image(image, blur_shape = (21,21), blur_sigma = 1.5, threshold_value = 0.5, mask = None, background_image = None):
    width = image.shape[1]
    height = image.shape[0]
    if len(mask) == 0:
        mask = get_mask_from_image(image, threshold_value, False)
        mask = np.reshape(mask, (height, width, 1))
    else:
        mask = np.reshape(mask, (height, width, 1))
    if background_image is None or background_image == []:
        blur_image = cv2.GaussianBlur(image, blur_shape, blur_sigma)
    else:
        background_image = cv2.resize(background_image, (width, height))
        blur_image = cv2.GaussianBlur(background_image, blur_shape, blur_sigma)
    background_image = cv2.normalize(blur_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    result = np.where(mask == 0, background_image, image)
    return result