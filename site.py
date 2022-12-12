from flask import Flask, render_template


from FLASK_SITE import *
import logging


app = Flask(__name__, static_url_path='')
app.register_blueprint(analise)
app.logger.name = 'NN_flask'


@app.route('/', methods=['GET'])
def hall_page():
    return render_template('hall_page.html')


if __name__ == '__main__':
    logging.basicConfig(filename='INFO.log', level=logging.DEBUG)
    app.logger.info('-----------------')
    app.logger.info('Starting...')
    app.logger.info(f'{check_device()}')
    app.run(debug=True)