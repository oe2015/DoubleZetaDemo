from flask import Flask, request, jsonify
from langchain import HuggingFacePipeline
from transformers import AutoTokenizer, pipeline
import torch
import logging

app = Flask(__name__)

model_name = "deepset/roberta-base-squad2"

nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
QA_input = {
    'question': 'Why is model conversion important?',
    'context': 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
}
res = nlp(QA_input)
print(res)

@app.route("/generate", methods=["POST"])
def generate():
    input_data = request.json
    print(input_data)
    question = input_data["question"]
    business_info = input_data["context"]
    context = ". ".join([f"{key}: {value}" for key, value in business_info.items()]) + "."
    QA_input = {
        'question': question,
        'context': context
    }   
    response = nlp(QA_input)   
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)