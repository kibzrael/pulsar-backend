FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y software-properties-common
# RUN add-apt-repository ppa:savoury1/ffmpeg4
# RUN add-apt-repository ppa:deadsnakes/ppa -y
# RUN rm -rf /var/lib/apt/lists/*
# RUN apt clean
RUN apt-get update
RUN apt-get install -y ffmpeg


# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
# RUN apt install python3.9 -y
# RUN which python
# RUN python --version
RUN apt-get -y install python3-pip
RUN pip install virtualenv

RUN virtualenv /env -p python3

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
RUN pip install --upgrade pip
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add the application source code.
ADD . /app

WORKDIR /app
# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
EXPOSE 8080

CMD gunicorn -w 5 --keep-alive 120 -t 120 --graceful-timeout 120 -k gthread --threads 3 -b :8080 main:app
# CMD ["gunicorn", "--bind", ":80", "--workers", "3", "pulse.wsgi:application"]