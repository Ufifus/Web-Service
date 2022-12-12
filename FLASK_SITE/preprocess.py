import os
import numpy as np
import cv2
from .configs import type_images, allowed_types


def convert_bit2img(img):
    """Converting bit data to cv2 array"""
    img = np.frombuffer(img, dtype=np.uint8) # Загужаем биты в numpy буффер с кодировкой utf-8
    img = cv2.imdecode(img, flags=1) # Переводим биты в изображение
    return img

def check_type_img(type_img):
    if not type_img in allowed_types: # Проверяем на нужный тип изображения
        return False
    return True

def check_class_img(type_class):
    """Check image of classes diceases"""
    if not type_class in type_images: # Ищем класс в доступных
        return None
    else:
        if not os.path.exists(type_images[type_class]['model_path']): # Смотрим есть ли у данного класса модель
            print(f'model in dir {type_images[type_class]["model_path"]} doesnt exist')
            return None
        else:
            return type_images[type_class] # Отдаем назад класс dict формата

def preprocess_img(img, size):
    """Preprocess image for analise
    1. Resize image
    2. Convert to numpy array
    3.* Rescaling (if model consist rescaling don't use)"""
    img = cv2.resize(img, size) # Изменяем размер
    img = np.array((img, )) # Переводим в массив numpy вида (1, height, width, deep)
    return img