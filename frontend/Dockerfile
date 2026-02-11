FROM python:3.11-slim

WORKDIR /app

# 필요한 파일들을 복사합니다.
COPY . .

# 의존성 패키지를 설치합니다.
RUN pip install -r requirements.txt

# Streamlit 기본 포트를 개방합니다.
EXPOSE 8501

# 파일명이 streamlit_app.py 이므로 이에 맞춰 실행 명령어를 수정합니다.
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]