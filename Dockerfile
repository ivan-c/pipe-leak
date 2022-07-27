FROM python:3.9

WORKDIR /opt/app

# cache hack; very fragile
COPY requirements.txt ./
RUN pip install --requirement requirements.txt

COPY . .
ENV FLASK_APP=pipe_leak.wsgi:app \
    FLASK_ENV=development \
    PORT=8008

EXPOSE "${PORT}"

#CMD gunicorn --bind "0.0.0.0:${PORT:-8008}" ${FLASK_APP}
CMD flask run --host 0.0.0.0 --port ${PORT:-8008}
