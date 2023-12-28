from flask_restful import Resource
from flask import jsonify, request
from app.vallex.utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav


# from IPython.display import Audio

class Text2Speech(Resource):
    def post(self):
        req = request.get_json()
        text_prompt = req['text']
        print(text_prompt)

        # download and load all models
        preload_models()

        audio_array = generate_audio(text_prompt)

        # save audio to disk
        write_wav("./app/vallex/results/vallex_generation.wav", SAMPLE_RATE, audio_array)

        # play text in notebook
        # Audio(audio_array, rate=SAMPLE_RATE)
