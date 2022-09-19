from flask import Flask, render_template
import os
app = Flask(__name__)

from pymongo import MongoClient
import certifi
client = MongoClient(os.environ.get("MONGO"),tlsCAFile=certifi.where())
db = client.dbsparta_test


@app.route('/')
def home():
   return render_template('index.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)