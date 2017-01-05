FROM python:2.7-alpine

WORKDIR /glare

RUN pip install flask requests gunicorn gevent supervisor && \
    echo_supervisord_conf > ./supervisor.conf

ADD supervisor_glare.conf main.py ./
RUN cat supervisor_glare.conf >> ./supervisor.conf

EXPOSE 80
CMD ["supervisord", "-c", "./supervisor.conf"]
