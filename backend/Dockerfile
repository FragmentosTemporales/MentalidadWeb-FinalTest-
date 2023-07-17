#Utilizamos python con alpine
FROM python:3.9-alpine

#instalamos y actualizamos python y pip
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

#establecemos el directorio de trabajo    
WORKDIR /src/app

#establecemos variables de entorno
ENV FLASK_APP index.py
ENV FLASK_RUN_HOST 0.0.0.0

#para mejorar respuesta de sqlalchemy
RUN apk add --no-cache gcc musl-dev linux-headers

#copiamos requirements.txt
COPY requirements.txt requirements.txt

#instalamos requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt

COPY . .

CMD ["flask", "run"]