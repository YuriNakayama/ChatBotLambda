from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    response = make_response(jsonify({'message': 'Hello, World!'}))
    response.headers['Content-Type'] = 'application/json'
    return response

def lambda_handler(event, context):
    return app
