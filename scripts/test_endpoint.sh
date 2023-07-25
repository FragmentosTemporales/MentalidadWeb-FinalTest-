#!/bin/sh
echo "---------------------------------------------"
echo "|       Testeando endpoints                 |"
echo "---------------------------------------------"
docker-compose run --rm backend sh -c "python manage.py test --test_name=endpoints.test_user.TestUserEndpoint"