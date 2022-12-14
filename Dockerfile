# python:3.9의 이미지로 부터
FROM python:3.10
# 제작자 및 author 기입
LABEL maintainer="tkdqja9812@gmail.com"

# 해당 디렉토리에 있는 모든 하위항목들을 '/app/server`로 복사한다
COPY . /app/server

# image의 directory로 이동하고
WORKDIR /app/server

# 필요한 의존성 file들 설치
RUN pip3 install -r requirements.txt

# container가 구동되면 실행
ENTRYPOINT ["python", "app.py"]