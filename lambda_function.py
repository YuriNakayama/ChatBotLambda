from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})

def lambda_handler(event, context):
    return app
