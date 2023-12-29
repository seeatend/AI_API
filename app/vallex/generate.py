from flask_restful import Resource
from flask import jsonify, request
from app.vallex.utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav


# from IPython.display import Audio

def audio_generate(text: str, audio_path: str, voice_type: str):
    print(text)

    # download and load all models
    preload_models()

    voice = 'zh2en_tts_3' if voice_type == 'male' else 'zh2en_tts_1'
    audio_array = generate_audio(text, voice)

    # save audio to disk
    # write_wav("./audios/vallex_generation.wav", SAMPLE_RATE, audio_array)
    write_wav(audio_path, SAMPLE_RATE, audio_array)

    # play text in notebook
    # Audio(audio_array, rate=SAMPLE_RATE)
