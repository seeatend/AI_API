from flask_restful import Api

from app.controllers.generate_video import GenerateVideo
from app.controllers.qwen_14b_chat import QWEN14BCHAT
from app.controllers.test import Test
from app.main.errors import errors

# Flask API Configuration
api = Api(
    catch_all_404s=False,
    errors=errors,
    prefix='/api'
)
api.add_resource(QWEN14BCHAT, '/qwen_14b_chat')
api.add_resource(Test, '/test')
api.add_resource(GenerateVideo, '/generate_video')


