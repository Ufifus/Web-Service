from flask import Flask

from REST_API import analise, check_device
import logging


app = Flask(__name__, static_url_path='')
app.register_blueprint(analise)
app.logger.name = 'NN_REST_flask'


if __name__ == '__main__':
    logging.basicConfig(filename='INFO.log', level=logging.DEBUG)
    app.logger.info('-----------------')
    app.logger.info('Starting...')
    app.logger.info(f'{check_device()}')
    app.run(debug=True)


