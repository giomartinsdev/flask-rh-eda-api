from flask import Flask
from infrastructure.web.api_config import api
from infrastructure.web.user_controller import ns_user

app = Flask(__name__)

@app.route('/health')
def health_check():
    return {
        "status_code": "ok",
        "code": 200,
        "data": "healthy"
    }

api.init_app(app)
api.add_namespace(ns_user)