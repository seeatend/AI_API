from flask_restful import Api

from app.controllers.generate_video import GenerateVideo
from app.controllers.qwen_7b_chat import Qwen7bChat
from app.controllers.text_to_speech import Text2Speech
from app.controllers.test import Test
from app.main.errors import errors

# Flask API Configuration
api = Api(
    catch_all_404s=False,
    errors=errors,
    prefix='/api'
)
api.add_resource(Qwen7bChat, '/qwen_7b_chat')
api.add_resource(Test, '/test')
api.add_resource(GenerateVideo, '/generate_video')
api.add_resource(Text2Speech, '/text_to_speech')
