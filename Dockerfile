FROM python:3.9.15-alpine3.17
# FROM python:3.8.2-slim-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /flexyweb
COPY . .
RUN pip install --upgrade pip --no-cache-dir
# RUN apt-get update

RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

# RUN apt-get update && apt-get install -y lsb-release && apt-get clean all
# RUN apk add --update python python-dev py-pip build-base
RUN pip3 install weasyprint


# EXPOSE 8000


RUN pip install -r req.txt --no-cache-dir
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "flexyweb.wsgi:application","--bind" "0.0.0.0:8000"]
