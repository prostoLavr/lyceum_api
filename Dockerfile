FROM python:3.11-slim
RUN  apt-get update && apt-get install -y libpq-dev build-essential libpcre3 libpcre3-dev
RUN groupadd --gid 2000 node \
  && useradd --uid 2000 --gid node --shell /bin/bash --create-home node
WORKDIR /app
COPY requirements.txt ./
COPY wheels /wheels
RUN python3 -m pip install --no-cache -r requirements.txt && \
    python3 -m pip install --no-cache /wheels/*

COPY ./app/ ./app/
COPY ./wsgi.py ./

CMD ["uwsgi", \ 
     "--http", ":80", \
     "--wsgi-file", "wsgi.py", \
     "--callable", "wsgi_app", \
     "--master", "--processes", "2", \
     "--threads", "1", \
     "--uid", "2000"]

