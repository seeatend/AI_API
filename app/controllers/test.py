from flask import jsonify
from flask_restful import Resource
from transformers import AutoModelForCausalLM, AutoTokenizer
# from modelscope import AutoModelForCausalLM as MAutoModelForCausalLM, AutoTokenizer as MAutoTokenizer
# from modelscope import GenerationConfig

DEFAULT_CKPT_PATH = 'Qwen/Qwen-14B-Chat'


class Test(Resource):
    def get(self):
        # #  Global Module
        # tokenizer = AutoTokenizer.from_pretrained(DEFAULT_CKPT_PATH, trust_remote_code=True)
        # model = AutoModelForCausalLM.from_pretrained(
        #     DEFAULT_CKPT_PATH,
        #     device_map="auto",
        #     trust_remote_code=True
        # ).eval()
        #
        # response, history = model.chat(tokenizer, "你好", history=None)
        # print(response)
        #
        return jsonify({'answer': 'test'})

    def post(self):
        # #  Global Module
        # tokenizer = AutoTokenizer.from_pretrained(DEFAULT_CKPT_PATH, trust_remote_code=True)
        # model = AutoModelForCausalLM.from_pretrained(
        #     DEFAULT_CKPT_PATH,
        #     device_map="auto",
        #     trust_remote_code=True
        # ).eval()
        #
        # response, history = model.chat(tokenizer, "你好", history=None)
        # print(response)
        #
        return jsonify({'answer': 'test'})