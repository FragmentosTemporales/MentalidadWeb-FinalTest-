import json
import unittest
from flask_jwt_extended import create_access_token
from app.models import Task
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
        payload = json.dumps({
            "task": "titulo",
            "description": "descripcion",
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
        print("response", response)
        # self.assertEqual(201, response.status_code)
        # self.assertEqual(self.data.task,  )


if __name__ == '__main__':
    unittest.main()