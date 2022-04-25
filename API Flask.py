# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 17:43:47 2022

@author: howar
"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
    
