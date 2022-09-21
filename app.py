from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, request
import os

app = Flask(__name__)

from pymongo import MongoClient
import certifi

client = MongoClient('localhost', 27017, username="test", password="test")
db = client.joongo_world


@app.route('/')
def home():
    return render_template('mainpage.html')


# 게시글 불러오기 / 검색 API
@app.route('/api/postlist', methods=['GET'])
def api_postlist():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) != 0 and request.args.get('filter') != '':
        posts = list(db.posts.find({'title': {'$regex': request.args.get('filter')}}, {}))
        return jsonify({'all_posts': posts})

    posts = list(db.posts.find({}, {}))
    return jsonify({'all_posts': posts})


# 게시글 불러오기 / 검색 API
@app.route('/api/post', methods=['GET'])
def api_post():
    print(request.args.get('p_id'))
    post = list(db.posts.find({'_id': int(request.args.get('p_id'))}, {}))
    print(post)
    return jsonify({'all_posts': post})


# 게시글 작성 API
@app.route('/api/newpost', methods=['POST'])
def api_newpost():
    if request.method == 'POST':
        # 포스트 id값
        id = len(list(db.posts.find({}, {'_id': False, })))

        # POST방식으로 form data가져옴
        result = request.form

        # 업로드한 img 가져옴
        file = request.files['img']

        # 파일명 세팅
        extension = file.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{mytime}'
        save_to = os.path.join(app.root_path, 'static/image', f'{filename}.{extension}')
        file.save(save_to)

        # DB업로드
        db.posts.insert_one(
            {
                '_id': id,
                'title': result.get('title'),
                'img': f'{filename}.{extension}',
                'contact': result.get('contact'),
                'amount': result.get('amount'),
                'content': result.get('content'),
                'time': today,
            }
        )
        return redirect('/')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
