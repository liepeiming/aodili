FROM aodili_container

WORKDIR /www/mysite
COPY . /www/mysite

CMD ["python", "task.py"]
