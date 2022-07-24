from flask import Flask, request, jsonify
from predicition import make_prediction

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def hello_world():
    if str(request.args['Query']) == 'gates':
        result = make_prediction('img.jpeg')
    if str(request.args['Query']) == 'charlie':
        result = make_prediction('charlie.jpeg')
    d={}
    d['Query'] = str(result)
    return jsonify(d)


if __name__ == '__main__':
    app.run()