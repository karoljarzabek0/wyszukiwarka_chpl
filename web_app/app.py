from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import torch
from sentence_transformers import SentenceTransformer
import json
import os
from .roberta import model

# Initialize app
app = Flask(__name__)
# Allow specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://192.168.0.113:5001",   
            "http://127.0.0.1:5001",
            "http://127.0.0.1:8000",
            "http://192.168.0.113:8000",
            "http://192.168.0.97:8000",
            "https://leki.karoljarzabek.pl"     # production
        ]
    }
})
# Load environment variables
load_dotenv()

# Import routes AFTER app, model, and kody_atc are defined
from .routes_api import api_bp
from .routes_fronend import frontend_bp

# Register Blueprints
app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(frontend_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
