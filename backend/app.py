from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from routes import api

app = Flask(__name__)
CORS(app)
Swagger(app, template={
    "info": {
        "title": "SmartSeat API",
        "description": "Smart Seat Allocation Platform API",
        "version": "1.0.0"
    }
})
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
