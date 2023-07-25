import json
import unittest
from flask_jwt_extended import create_access_token
from app.models import Task, User
from app.schemas import TaskSchema
from tests import BaseTestCase
from tests.utils.task import save_task_to_db
from tests.utils.user import save_user_to_db

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class TestTaskEndpoint(BaseTestCase):
    """ Test that task endpoint works fine! """

    def setUp(self):
        """ Setting up the test class """
        super().setUp()
        self.data = {
            "task": "titulo",
            "description": "descripcion",
            "is_completed": False,
            "user_id": 1
        }
        self.data2 = {
            "task": "titulo",
            "description": "descripcion",
            "is_completed": False,
            "user_id": 2
        }
        self.params = {
            "username": "test",
            "email": "example@example.com",
            "password": "12345",
            "is_disabled": False
        }
        self.user = save_user_to_db(self.params)
        self.token = create_access_token(self.user.email)

    def test_task_created_suc(self):
        """ test task is created succesfully """
        payload = json.dumps(self.data)
        response = self.client.post(
            "/tasks",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            },
            data=payload
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json["message"],
                         "Tarea guardada exitósamente")

    def test_task_created_fail(self):
        """ test task is not created """
        payload = json.dumps({
            "task": "",
            "description": "",
            "is_completed": False,
            "user_id": 1
        })
        response = self.client.post(
            "/tasks",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            },
            data=payload
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json["error"], "El valor de Tarea no puede estar vacío")

    def test_get_tasks_suc(self):
        """ Test get tasks endpoint """
        id = 2
        save_task_to_db(self.data)
        save_task_to_db(self.data)
        save_task_to_db(self.data2)
        user2 = User.find_by_id(2)
        print(user2)
        response = self.client.get(
            "/tasklist/{}".format(id),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            },
        )
        data = response.json
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(data),2)


if __name__ == '__main__':
    unittest.main()
