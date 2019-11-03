FROM python

WORKDIR /www/mysite
COPY requirements.txt /www/mysite/requirements.txt

RUN cd /www/mysite && \
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
