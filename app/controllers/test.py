from flask import jsonify
from flask_restful import Resource
from transformers import AutoModelForCausalLM, AutoTokenizer
# from modelscope import AutoModelForCausalLM as MAutoModelForCausalLM, AutoTokenizer as MAutoTokenizer
# from modelscope import GenerationConfig

DEFAULT_CKPT_PATH = 'Qwen/Qwen-7B-Chat'


class Test(Resource):
    def get(self):
        #  Global Module
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_CKPT_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            DEFAULT_CKPT_PATH,
            device_map="auto",
            trust_remote_code=True
        ).eval()

        response, history = model.chat(tokenizer, "你好", history=None)
        print(response)

        return jsonify({'Message': response})

    def post(self):
        #  Chinese Module
        # tokenizer = MAutoTokenizer.from_pretrained(DEFAULT_CKPT_PATH, trust_remote_code=True)
        # model = MAutoModelForCausalLM.from_pretrained(DEFAULT_CKPT_PATH, device_map="auto",
        #                                              trust_remote_code=True).eval()
        # model.generation_config = GenerationConfig.from_pretrained(DEFAULT_CKPT_PATH,
        #                                                            trust_remote_code=True)  # 可指定不同的生成长度、top_p等相关超参
        #
        # response, history = model.chat(tokenizer, "你好", history=None)
        # print(response)
        # return jsonify({'Message': response})
        pass