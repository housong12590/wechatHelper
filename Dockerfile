FROM python:3.6-alpine

COPY . /project

WORKDIR /project

RUN cd /project \
    && pip install -r requirements.txt -i https://pypi.doubanio.com/simple\
    && pip install gunicorn \
    && chmod +x docker-entrypoint.sh

EXPOSE 5000


ENTRYPOINT ["./docker-entrypoint.sh"]


