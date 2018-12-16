from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
while True:
    data = open('Hashtags.txt', 'r').read()
    @app.route('/count', methods=['GET'])

    def get_count():
        return data
    if __name__ == '__main__':
        app.run(debug=True)
