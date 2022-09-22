<h3 align="center"><b>미니프로젝트, 중고세상</b></h3>

<h4 align="center">📆 2022.09.19 ~ WIP</h4>
<br>

---

<h3><b>프로젝트 소개</b></h3>
일상에서 사용빈도가 낮은 물건들을 버리지 않고 같은 지역의 다른 사람에게 좋은 가격으로 거래할 수 있는 중고 거래 플랫폼입니다.
<br><br> 

---

<br>
<h3 align="center"><b>🛠 Tech Stack 🛠</b></h3>
<p align="center">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
<img src="https://img.shields.io/badge/jquery-0769AD?style=for-the-badge&logo=jquery&logoColor=white">
<img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
<img src="https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=aws&logoColor=white">
</br>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white">
<img src="https://img.shields.io/badge/Python-F80000?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Flask-4FC08D?style=for-the-badge&logo=Flask&logoColor=white">
<img src="https://img.shields.io/badge/MongoDB-61DAFB?style=for-the-badge&logo=MongoDB&logoColor=white">

---

<br>
<h3 align="center"><b>🏷 API Table 🏷</b></h3>
<table width="100%">
    <tr align="center">
	<td width="12%"><b>기능</b></td>
        <td width="5%"><b>Method</b></td>
        <td width="12%"><b>URL</b></td>
        <td width="30%"><b>Request</b></td>
        <td width="31%"><b>Response</b></td>
    </tr>
    <tr>
        <td width="12%">메인 페이지 로드</td>
        <td width="5%">GET</td>
        <td width="12%">/</td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">로그인 페이지 로드</td>
        <td width="5%">GET</td>
        <td width="12%">/login</td>
        <td width="30%"></td>
        <td width="31%"></td>
    </tr>
    <tr>
        <td width="12%">로그인</td>
        <td width="5%">POST</td>
        <td width="12%">/api/login</td>
        <td width="30%">{'id_receive': username_give, 'pw_receive': password_give}</td>
        <td width="31%">로그인 성공 - {'result': 'success', 'token': token}<br>로그인 실패 - {'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'}</td>
    </tr>
    <tr>
        <td width="12%">회원가입</td>
        <td width="5%">POST</td>
        <td width="12%">/register</td>
        <td width="30%">{'id_receive': username_give, 'pw_receive': password_give,  'nickname_receve': user_password}</td>
        <td width="31%">{'msg': '회원가입이 완료되었습니다.'}</td>
    </tr>
    <tr>
        <td width="12%">회원가입 id 중복체크</td>
        <td width="5%">POST</td>
        <td width="12%">/register/check_dup</td>
        <td width="30%">{'username_receive': username_give}</td>
        <td width="31%">중복 존재 - {'result': 'success', 'exists': True}<br>중복 미존재 - {'result': 'success', 'exists': False}</td>
    </tr>
    <tr>
        <td width="12%">게시글 불러오기</td>
        <td width="5%">GET</td>
        <td width="12%">/api/postlist</td>
        <td width="30%"></td>
        <td width="31%">'all_posts': posts</td>
    </tr>
    <tr>
        <td width="12%">게시글 검색</td>
        <td width="5%">GET</td>
        <td width="12%">/api/postlist/&lt;search_val&gt;</td>
        <td width="30%">search_val</td>
        <td width="31%">'all_posts': posts</td>
    </tr>
    <tr>
        <td width="12%">상세페이지</td>
        <td width="5%">GET</td>
        <td width="12%">/api/postdetail/&lt;postid&gt;</td>
        <td width="30%">postid</td>
        <td width="31%">'all_posts': posts</td>
    </tr>
    <tr>
        <td width="12%">상세페이지</td>
        <td width="5%">GET</td>
        <td width="12%">/api/newpost</td>
        <td width="30%">result=request.form</td>
        <td width="31%">'all_posts': posts</td>
    </tr>
</table>

<br>
