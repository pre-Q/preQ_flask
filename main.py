import json
from flask import Flask, request, current_app
from collections import OrderedDict
from extract_keyword import get_keyword

app = Flask(__name__)


def api_response(status, message, data):
    return current_app.response_class(
        json.dumps(OrderedDict([('status', status), ('message', message), ('data', data)]),
                   indent=None), mimetype='application/json')


@app.route('/api/v1/keyword', methods=['POST'])
def post_keyword():
    try:
        application = request.get_json()['application']
        keyword_top5, soft_skills = get_keyword(application)
        return api_response(200, "키워드 추출 성공", {"keywordTop5": keyword_top5, "softSkills": soft_skills}), 200
    except Exception as e:
        print("Someting wrong!!", e)
        return api_response(500, "Internal Server Error", str(e)), 500



@app.route('/')
def health_check():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
