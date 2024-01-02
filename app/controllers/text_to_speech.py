from flask_restful import Resource
from flask import jsonify, request
from app.vallex.generate import audio_generate
import os


class Text2Speech(Resource):
    def post(self):
        req = request.get_json()
        text_prompt = req['text']
        voice_type = req['voice_type']

        
        audio_path = './audios/vallex_generation.wav'
        if os.path.exists(audio_path):
            print('# deleting exisitng audio file')
            os.remove(audio_path)

        audio_generate(text_prompt, "./audios/vallex_generation.wav", voice_type)
