#!/bin/sh
echo "---------------------------------------------"
echo "|       Testeando nuestra super app          |"
echo "---------------------------------------------"
docker-compose run --rm backend sh -c "python manage.py test && flake8"