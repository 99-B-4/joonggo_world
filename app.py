from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, redirect, request
from bson.objectid import ObjectId
import os
import jwt
import hashlib
app = Flask(__name__)


# #########################################################
# 메인 페이지 로드
# #########################################################
# import certifi
# client = MongoClient(
#     'mongodb+srv://joongo_world:QhPRl58WsHjuGxRV@cluster0.amhacid.mongodb.net/?retryWrites=true&w=majority',
#     tlsCAFile=certifi.where())

# 서버용 DB설정
client = MongoClient('localhost', 27017, username="test", password="test")

db = client.joonggo_world
SECRET_KEY = 'JOONGGO_WORLD'


# #########################################################
# 페이지 로드
# #########################################################
@app.route('/')
def home():
    # 토큰값 쿠키에서 받아오기
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
    return render_template('login.html', msg=msg)


# #########################################################
# Login API
# #########################################################
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['username_give']
    pw_receive = request.form['password_give']

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


# #########################################################
# 회원가입 API
# #########################################################
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['username_give']
    pw_receive = request.form['password_give']
    nickname_receive = request.form['username_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


# #########################################################
# 회원가입 id 중복체크 API
# #########################################################
@app.route('/api/register/check_dup', methods=['POST'])
def check_dup():
   username_receive = request.form['username_give']
   exists = bool(db.user.find_one({'id': username_receive}))
   return jsonify({'result': 'success', 'exists': exists})


# #########################################################
# 게시글 불러오기 API
# #########################################################
@app.route('/api/postlist', methods=['GET'])
def api_postlist():
    posts = list(db.posts.find(
        {},
        {"_id": {"$toString": "$_id"}, "title": 1, "img": 1, "user": 1,  "contact": 1, "amount": 1, "content": 1})
    )
    return jsonify({'all_posts': posts})


# #########################################################
# 게시글 검색 API
# #########################################################
@app.route('/api/postlist/<search_val>', methods=['GET'])
def api_postfind(search_val):
    posts = list(db.posts.find(
        {'title': {'$regex': search_val}},
        {"_id": {"$toString": "$_id"}, "title": 1, "img": 1, "user": 1,  "contact": 1, "amount": 1, "content": 1})
    )
    return jsonify({'all_posts': posts})


# #########################################################
# 상세 페이지 API
# #########################################################
@app.route('/api/postdetail/<postid>', methods=['GET'])
def api_post(postid):
    post = list(db.posts.find({'_id': ObjectId(postid)}, {"_id": 0}))
    return jsonify({'all_posts': post})


# #########################################################
# 게시글 작성 API
# #########################################################
@app.route('/api/newpost', methods=['POST'])
def api_newpost():
    if request.method == 'POST':
        # 토큰에서 추출한 키값으로 유저명 가져오기
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})

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