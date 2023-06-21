from flask import Flask
from route.route import route

app = Flask(__name__)

app.register_blueprint(route)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)