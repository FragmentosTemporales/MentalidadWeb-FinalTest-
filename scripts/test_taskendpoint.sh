#!/bin/sh
echo "---------------------------------------------"
echo "|       Testeando Task endpoints                 |"
echo "---------------------------------------------"
docker-compose run --rm backend sh -c "python manage.py test --test_name=endpoints.test_task.TestTaskEndpoint"