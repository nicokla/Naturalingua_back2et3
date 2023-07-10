FROM python:3.9

RUN apt-get update
RUN apt-get install -y vim gcc libffi-dev musl-dev
RUN apt-get install -y python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
RUN apt-get install -y ffmpeg

WORKDIR /opt/app

# App non-root user
ENV GROUP=app
ENV USER=flask
ENV UID=12345
ENV GID=23456
RUN addgroup --gid "$GID" "$GROUP" \
  && adduser --uid "$UID" \
    --disabled-password \
    --gecos "" \
    --ingroup "$GROUP" \
    "$USER"

# Switch to the non-root user
RUN mkdir -p /home/flask/mytmp
RUN chown $USER /home/flask/mytmp

USER "$USER"
ENV PATH="/home/$USER/.local/bin:${PATH}"

# Copy requirements file to our container, install, and remove
# files to we don't need to reduce the container size
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --no-warn-script-location \
    --user \
    -r requirements.txt \
  && find "/home/$USER/.local" \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' +

# Copy app to container (with privileges to non-root user)
COPY --chown=$USER:$GROUP ./ ./

# RUN mkdir ./mytmp
# COPY --chown=$USER:$GROUP ../worker/mytmp ./mytmp

WORKDIR /opt/app
