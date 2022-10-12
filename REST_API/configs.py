import os


base_dir = os.path.dirname(os.path.dirname(__file__))

dir_models = os.path.join(base_dir, 'models') # dir with models

if not os.path.exists(dir_models):
    os.mkdir(dir_models)

dir_images = os.path.join(base_dir, 'images') # dir with save images

if not os.path.exists(dir_images):
    os.mkdir(dir_images)


type_images = {
    'TIRADS': {
        'name_desease': 'TIRADS',
        'model_path': os.path.join(dir_models, 'TIRADS/Inception_80'),
        'input_shape': (300, 300, 3),
        'save_images': os.path.join(dir_images, 'TIRADS')
    }
}