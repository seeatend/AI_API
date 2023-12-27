from flask import jsonify
from flask_restful import Resource
from transformers import AutoModelForCausalLM, AutoTokenizer
# from modelscope import AutoModelForCausalLM as MAutoModelForCausalLM, AutoTokenizer as MAutoTokenizer
# from modelscope import GenerationConfig
from flask import jsonify, request

DEFAULT_CKPT_PATH = 'Qwen/Qwen-7B-Chat'


class QWEN14BCHAT(Resource):
    def post(self):
        req = request.get_json()
        question = req['question']
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_CKPT_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            DEFAULT_CKPT_PATH,
            device_map="auto",
            trust_remote_code=True
        ).eval()

        response, history = model.chat(tokenizer, question, history=None)
        print(response)
        print('history = ', history)

        return jsonify({'answer': response})
