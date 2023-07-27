#!/bin/s
echo "---------------------------------------------"
echo "|   Copiando Datos de Frontend a Backend     |"
echo "---------------------------------------------"

cp -r todo-list/build/static backend/app/static
cp todo-list/build/index.html backend/app/templates

echo "Datos copiados exitosamente."
