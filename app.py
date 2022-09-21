from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, redirect, request, url_for
import os
import jwt
import hashlib

app = Flask(__name__)

from pymongo import MongoClient
import certifi

client = MongoClient(
    'mongodb+srv://joongo_world:QhPRl58WsHjuGxRV@cluster0.amhacid.mongodb.net/?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())

db = client.joongo_world
SECRET_KEY = 'SPARTA'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('mainpage.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return render_template('mainpage.html')
    except jwt.exceptions.DecodeError:
        return render_template('mainpage.html')


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('sign_in.html', msg=msg)


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/register')
def register():
    return render_template('sign_up.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


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
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})

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
                'user': userinfo['nick'],
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
