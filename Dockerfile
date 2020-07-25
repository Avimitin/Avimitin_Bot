FROM python:3.8.2
MAINTAINER avimitin avimitin@gmail.com
ADD ./
COPY Bot2.py /code/
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD ["python3","Bot2.py"]
