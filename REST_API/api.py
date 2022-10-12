from . import convert_res2json, convert_json2img, check_type_img, analize_img, preprocess_img
from .configs import type_images
from flask import Blueprint, current_app, jsonify, request


analise = Blueprint('analise', __name__)


@analise.route('/analize/get_types', methods=['GET'])
def get_types():
    """Response all types of available models"""
    keys = [key for key in type_images.keys()]
    if len(keys) == 0:
        return jsonify({'error': 'Not available models'}), 404
    return jsonify({'keys': keys}), 200


@analise.route('/analize/<type_img>/<name>', methods=['POST'])
def request_img(type_img, name):
    """Request json byte code image and decoding this with cv2"""
    current_app.logger.info(f'Upload image {name} with class {type_img}')
    if not request.json:
        current_app.logger.warn('Doesnt exist image')
        return jsonify({'Not exist any image'}), 404
    else:
        current_app.logger.info(f'Type model {type_img}')
        class_img = check_type_img(type_img)
        if not class_img:
            current_app.logger.warn(f'Doesnt exist class {type_img}')
            return jsonify({'error': 'This type doesnt allow'}), 404

        current_app.logger.info('Starting preprocess image...')
        img = request.json['img_json']
        img = convert_json2img(img)
        size = (class_img['input_shape'][0], class_img['input_shape'][1])
        img = preprocess_img(img, size)

        current_app.logger.info('Starting analise image...')
        pred_class, pred_softmax = analize_img(img, class_img['model_path'])
        pred_class, pred_softmax = convert_res2json(pred_class, pred_softmax)

        current_app.logger.info(f'Return on web-client predictions:  {pred_class}, {pred_softmax}')
        current_app.logger.info('Ending.')
        return jsonify({'Done': True, 'pred_class': pred_class, 'pred_softmax': pred_softmax}), 200