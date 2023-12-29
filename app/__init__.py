import logging
import os

from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from app import main
from app.main.api import api
from app.main.logging import LOGGING_CONFIG

# Flask App Initialization
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(main.settings[os.environ.get('APPLICATION_ENV', 'default')])

# Logs Initialization
console = logging.getLogger('console')

# Flask API Initialization
api.init_app(app)

@app.route('/videos/<string:key>/<path:filename>')
def video_static(key, filename):
    root_dir = os.path.dirname(os.getcwd())
    sadtalker = os.path.join('AI_API/' + app.config['VIDEOS_FOLDER'] + '/' + key)
    try:
        return send_from_directory(os.path.join(root_dir, sadtalker), filename)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, threaded=True)
