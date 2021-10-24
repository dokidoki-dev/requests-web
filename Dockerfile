FROM python:3.7
COPY . /requests-web
RUN mkdir -p /var/www
WORKDIR /var/www
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]