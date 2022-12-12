from . import check_type_img, analize_img, preprocess_img, check_class_img, convert_bit2img
from flask import Blueprint, current_app, jsonify, request, render_template


analise = Blueprint('analise', __name__)


@analise.route('/analise/image', methods=['GET', 'POST'])
def analise_img():
    """Page for load img and return prediction"""
    if request.method == "GET":  # Проверяем запрос
      return render_template('analise_page.html')

    if request.method == "POST":  # Проверяем запрос
      current_app.logger.info('Request image and analise this...')

      current_app.logger.info(request.files)
      img = request.files.get('img')  # Ищем наше изображение

      if img is None:  # Если изображения нет то возвращаем ошибку на страницу что изображения нет
        return render_template('analise_page.html', error='Not image uploaded')

      current_app.logger.info(img)
      current_app.logger.info(f'class {type(img)}')

      type_img = img.filename.split('.')[
        -1]  # Смотрим тип изображения и если он есть в указанных насройках пропускаем дальше
      if not check_type_img(type_img):
        return render_template('analise_page.html', error=f'Wrong type of image {type_img}')

      current_app.logger.info(f'Upload image "{img.filename}" with class "{type_img}"')

      class_img = check_class_img('TIRADS')  # Выбираем класс изображений для анализа и указания модели
      if class_img is None:
        return render_template('analise_page.html', error=f'Wrong class of image {class_img}')

      current_app.logger.info('Starting preprocess image...')

      size = (
      class_img['input_shape'][0], class_img['input_shape'][1])  # Выбираем размер до которого сжимаем наше изображение
      img = convert_bit2img(img.read())  # Переводим наше изображение из бит формата в массив numpy
      current_app.logger.info(f'size = {size}')
      img = preprocess_img(img, size)  # Обрабатываем изображение

      current_app.logger.info('Starting analise image...')
      pred_class, pred_softmax = analize_img(img, class_img['model_path'])  # Загружаем изображение и модель для анализа

      current_app.logger.info(f'Return on web-client predictions:  {pred_class}, {pred_softmax}')
      current_app.logger.info('Ending.')

      return render_template('analise_page.html', result=True, result_class=pred_class,
                             result_distribution=pred_softmax)  # Выводим результаты на страницу