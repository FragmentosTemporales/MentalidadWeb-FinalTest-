FROM python:3.9

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends
RUN apt-get install -y netcat-openbsd

WORKDIR /usr/src/app

COPY ./requirements-dev.txt /usr/src/app/requirements-dev.txt
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements-dev.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/
RUN chmod 755 /usr/src/app/entrypoint.sh

# run entrypoint
ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]