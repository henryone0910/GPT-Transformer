import openai
import os
from flask import Flask, redirect, render_template, request, url_for, jsonify
from dotenv import load_dotenv, find_dotenv, set_key

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

last_conv = []
last_conv.append(
    {'role': 'system', 'content': "you are a super rude assisstant."})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        checkAPI = request.form.get('api_key')
        if (checkAPI):
            openai.api_key = request.form['api_key']
            dotenv_file = find_dotenv()
            set_key(dotenv_file, "OPENAI_API_KEY", request.form['api_key'])
            print('key: ', request.form['api_key'])
            return "API Key Updated", 200

        try:
            version = request.form['version']
            prompt = request.form['prompt']

            question = {}
            question['role'] = 'user'
            question['content'] = prompt
            last_conv.append(question)

            answer = generate_response(last_conv, version)
        except Exception as e:
            print("Error:", e)
            answer = {'content': str(e)}
            return jsonify(answer), 401

        return jsonify(answer), 200

    result = {'role': 'assisstant'}
    result['content'] = request.args.get('result')
    return render_template('index.html', result=result)

def generate_response(last_conv, version):
    response = openai.ChatCompletion.create(
        model=version,
        messages=last_conv,
        temperature=.6
    )
    answer = {}
    answer['role'] = response['choices'][0]['message']['role']
    answer['content'] = response['choices'][0]['message']['content'].replace('\n', '<br>')
    last_conv.append(answer)
    return answer


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
