FROM python:3.8.2
LABEL maintainer="avimitin<avimitin@gmail.com>"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/usr/src/app/config"]

CMD ["python3", "Bot2.py"]
