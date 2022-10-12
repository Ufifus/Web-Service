import tensorflow as tf
import numpy as np


def check_device():
    """Checking GPU device or return CPU"""
    try:
        device_name = tf.test.gpu_device_name()
        if device_name != '/device:GPU:0':
            raise SystemError('GPU device not found')
    except Exception as e:
        return e
    else:
        return 'Found GPU at: {}'.format(device_name)


def analize_img(img, modelpath):
    """Upload image in model and on result return max_pred class and prediction_softmax"""
    model = tf.keras.models.load_model(modelpath)
    predicted_softmax = model.predict(img)
    predicted_class = [np.argmax(i) for i in predicted_softmax][0] + 1
    predicted_softmax = np.around(predicted_softmax, decimals=2)[0]
    return predicted_class, predicted_softmax