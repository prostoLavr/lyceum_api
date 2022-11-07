FROM python:3.10-slim
WORKDIR /test
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
COPY test.py ./
CMD ["python3", "-m", "pytest","--log-cli-level=DEBUG",  "--capture=tee-sys", "test.py"]

