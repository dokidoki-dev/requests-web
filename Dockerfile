FROM python:3.7
RUN mkdir -p /var/www
COPY . /var/www
WORKDIR /var/www
RUN pip install --upgrade pip && pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]