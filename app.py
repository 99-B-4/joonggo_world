from flask import Flask, render_template, jsonify
import os
app = Flask(__name__)

from pymongo import MongoClient
import certifi
client = MongoClient('mongodb+srv://joongo_world:QhPRl58WsHjuGxRV@cluster0.amhacid.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.joongo_world


@app.route('/')
def home():
   return render_template('mainpage.html')

# 개시글 불러오기
@app.route('/api/postlist', methods=['GET'])
def api_postlist():

    posts = list(db.posts.find({}, {'_id': False, }))
    print(posts)
    return jsonify({'all_posts': posts})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)