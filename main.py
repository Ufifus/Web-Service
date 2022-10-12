import os.path

import streamlit as st
from PIL import Image
import json
import base64
import numpy as np
import requests
import cv2
import matplotlib.pyplot as plt


def get_predict(type_img, name, image, url="http://127.0.0.1:5000/analize"):
    task_url = f'{url}/{type_img}/{name}'
    return requests.post(task_url, json=image).json()


def get_result(img, choice):
    img = np.array(img)
    print(img.shape)

    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    string_img = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    jstr = {"img_json": string_img}

    try:
        results = get_predict(choice, file.name, jstr)
        print(results)
    except Exception as e:
        print(e)
        st.write('Ошибка при анализе изображения', results)
    else:
        st.write('Модель соотнесла к классу', results['pred_class'])

        ini_array = np.array(results['pred_softmax'])
        ini_array = ini_array.astype(np.float)

        plot_result(ini_array)  # выводим предсказание на страницу


def plot_result(prediction):
    classes = np.arange(1, 6)
    predictions = np.array(prediction)
    fig, ax = plt.subplots()
    ax.bar(classes, predictions)
    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)  # ширина Figure
    fig.set_figheight(6)  # высота Figure
    st.pyplot(fig)


if __name__ == '__main__':
    # index_to_class_label_dict = load_index_to_label_dict()
    st.title('Thyroid TIRADS-EU DL-Model')
    types = requests.get("http://127.0.0.1:5000/analize/get_types").json()
    file = st.file_uploader('Загрузите файл с УЗ-изображением :')

    if file:  # if user uploaded file
        print(types)
        print(file)
        img = Image.open(file)
        st.image(img, caption='Загружен', channels="RGB")
        choice = st.selectbox(label='Choice type of disease', options=types['keys'])

        if st.button('GET RESULT'):
            get_result(img, choice)
        else:
            pass


