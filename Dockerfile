# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

# The Google App Engine python runtime is Debian Jessie with Python installed
# and various os-level packages to allow installation of popular Python
# libraries. The source is on github at:
#   https://github.com/GoogleCloudPlatform/python-docker
# FROM gcr.io/google_appengine/python
# FROM tiangolo/uwsgi-nginx:python3.8-alpine-2020-12-19
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:savoury1/ffmpeg4
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

# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
EXPOSE 8000
CMD cd app && gunicorn -w 5 --keep-alive 120 -t 120 --graceful-timeout 120 -k gthread --threads 3 -b :$PORT main:app
# CMD ["gunicorn", "--bind", ":80", "--workers", "3", "pulse.wsgi:application"]