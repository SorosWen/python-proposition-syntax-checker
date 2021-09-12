from flask import Flask, send_from_directory
import os 

app = Flask(__name__)

@app.route('/')
def index(): 
    return "<p> it works <\p>"