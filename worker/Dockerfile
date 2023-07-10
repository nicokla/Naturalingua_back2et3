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

RUN mkdir -p /home/flask/mytmp
RUN chown $USER:$GROUP /home/flask/mytmp

# Switch to the non-root user
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

# RUN python -m unidic download

# Copy app to container (with privileges to non-root user)
COPY --chown=$USER:$GROUP ./ ./

# RUN mkdir -p /home/flask/.fonts
# COPY --chown=$USER:$GROUP ./fonts /home/flask/.fonts
RUN mkdir -p /home/$USER/.local/share/fonts
RUN cp -r ./fonts /home/$USER/.local/share
RUN fc-cache -f -v

# CONTAINER_ID=$(docker ps -aqf "name=worker")
# docker cp ./worker/fonts/. $CONTAINER_ID:/home/flask/.local/share/fonts
# docker exec -u root -it $CONTAINER_ID sh -c "chown -R flask:app /home/flask/.local/share"
# docker exec -u root -it $CONTAINER_ID sh -c "ls -al /home/flask/.local/share/fonts"
# docker exec -it $CONTAINER_ID sh -c "fc-cache -f -v"


WORKDIR /opt/app/indic-trans
RUN  pip install \
    --no-cache-dir \
    --no-warn-script-location \
    --user \
    -r \
    ./requirements.txt
RUN python setup.py install --user
RUN cp -r ./indictrans/mappings "/home/$USER/.local/lib/python3.9/site-packages/indictrans/mappings"
RUN cp -r ./indictrans/models "/home/$USER/.local/lib/python3.9/site-packages/indictrans/models"

WORKDIR /opt/app

# RUN mkdir -p /home/flask/mytmp
# RUN chown $USER:$GROUP /home/flask/mytmp
