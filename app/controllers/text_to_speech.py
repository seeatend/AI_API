from flask_restful import Resource
from flask import jsonify, request
from app.vallex.generate import audio_generate


class Text2Speech(Resource):
    def post(self):
        req = request.get_json()
        text_prompt = req['text']
        voice_type = req['voice_type']

        audio_generate(text_prompt, "./audios/vallex_generation.wav", voice_type)
