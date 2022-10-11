FROM python:3.10-slim
WORKDIR /app
RUN  apt-get update && apt-get install -y python3-pip libpq-dev python3-dev
COPY requirements.txt ./
COPY wheels /wheels
RUN /usr/bin/python3 -m pip install --no-cache -r requirements.txt && \
    /usr/bin/python3 -m pip install --no-cache /wheels/*

COPY app/ ./

CMD ["/usr/bin/python3", \
     "-m", "gunicorn", \
     "--pythonpath", "/usr/bin/python3", \
     "--limit-request-field_size", "134217728", \
     "--workers", "2", \
     "--bind", "0.0.0.0:80", \
     "wsgi:wsgi_app"]
