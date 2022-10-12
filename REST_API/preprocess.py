import os
import base64
import numpy as np
import cv2
from .configs import type_images


def convert_res2json(pred_class, pred_softmax):
    """Convert results to str for sending like json data"""
    pred_class = int(pred_class)
    pred_softmax = [str(i) for i in pred_softmax]
    return pred_class, pred_softmax


def convert_json2img(img):
    """Converting json data to cv2 array"""
    img = base64.b64decode(img)
    img = np.frombuffer(img, dtype=np.uint8)
    img = cv2.imdecode(img, flags=1)
    return img


def check_type_img(type_img):
    """Check image of classes diceases"""
    if not type_img in type_images:
        return None
    else:
        if not os.path.exists(type_images[type_img]['model_path']):
            print(f'model in dir {type_images[type_img]["model_path"]} doesnt exist')
            return None
        else:
            return type_images[type_img]


def preprocess_img(img, size):
    """Preprocess image for analise
    1. Resize image
    2. Convert to numpy array
    3.* Rescaling (if model consist rescaling don't use)"""
    img = cv2.resize(img, size)
    img = np.array((img, ))
    return img