from flask import Flask
import hydrator

app = Flask(__name__)

@app.route('/')
def index():
    return hydrator.load_files('input-example.txt', 'params-example.txt')