# Step 1 select default OS image
FROM alpine


# # Step 2 tell what you want to do

RUN echo "**** install Python ****" && \
    apk add py-pip --no-cache python && \
    if [ ! -e /usr/bin/python ]; then ln -sf python /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip /usr/bin/pip ; fi

# # Step 3 Configure a software
# # Defining working directory
WORKDIR /app

# # Copy everything which is present in my docker directory to working (/app)
COPY /requirements.txt /app

RUN pip install -r requirements.txt

RUN pip install flask-cors

COPY ["app.py", "/app"]

# Exposing an internal port
EXPOSE 5003


# Step 4 set default commands
# These are permanent commands i.e even if user will provide come commands those will be considered as argunemts of this command
ENTRYPOINT [ "python3" ]

# These commands will be replaced if user provides any command by himself
CMD ["app.py"]

