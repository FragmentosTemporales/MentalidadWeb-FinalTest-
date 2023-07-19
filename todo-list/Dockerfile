#Utilizamos la versión 14-slim de node
FROM node:14-slim

#Establecemos el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

#Copiamos el atchivo package.json para las dependencias
COPY package.json ./

#Una vez copiado el package.json ejecutamos npm install para las dependencias
RUN npm install

#Copiamos todo lo generado
COPY . .

#Exponemos el contenedor en el puerto 3000
EXPOSE 3000