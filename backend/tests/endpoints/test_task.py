import json
import unittest
from flask_jwt_extended import create_access_token
from app.schemas import TaskSchema
from app.messages import (
    ERR_TASK_EMPTY,
    ERR_TASK_NOT_FOUND,
    SUC_TASK_OK,
    SUC_TASK_UPDATED,
)
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
        self.params2 = {
            "username": "test",
            "email": "example2@example.com",
            "password": "12345",
            "is_disabled": False
        }
        self.user = save_user_to_db(self.params)
        self.user2 = save_user_to_db(self.params2)
        self.update = {
            "task": "titulo update",
            "description": "descripcion update",
            "is_completed": False,
            "user_id": self.user.id
        }
        self.data = {
            "task": "titulo",
            "description": "descripcion",
            "is_completed": False,
            "user_id": self.user.id
        }
        self.data2 = {
            "task": "titulo",
            "description": "descripcion",
            "is_completed": False,
            "user_id": 2
        }
        self.token = create_access_token(self.user.email)
        self.token2 = create_access_token(self.user2.email)

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
        self.assertEqual(response.json, SUC_TASK_OK)

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
        self.assertEqual(response.json, ERR_TASK_EMPTY)

    def test_get_tasks_suc(self):
        """ Test get tasks endpoint """
        save_task_to_db(self.data)
        save_task_to_db(self.data)
        save_task_to_db(self.data2)
        response = self.client.get(
            "/tasklist",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            },
        )
        data = response.json
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(data), 2)

    # TODO = revisar este caso
    def test_get_tasks_fail(self):
        """ Test get tasks endpoint """
        save_task_to_db(self.data)
        save_task_to_db(self.data)
        save_task_to_db(self.data2)
        response = self.client.get(
            "/tasklist",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer "
            },
        )
        self.assertEqual(422, response.status_code)

    def test_update_task_suc(self):
        """ Test endopoint update task ok"""
        task = save_task_to_db(self.data)
        response = self.client.put(
            "/task/{}".format(task.id),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            },
            data=json.dumps(self.update)
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, SUC_TASK_UPDATED)

    def test_update_task_fail(self):
        """ Test endopoint update task fail"""
        task = save_task_to_db(self.data)
        response = self.client.put(
            "/task/{}".format(task.id),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token2)
            },
            data=json.dumps(self.update)
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json, ERR_TASK_NOT_FOUND)

    def test_delete_task_suc(self):
        """ Test endopoint delete task ok"""
        task = save_task_to_db(self.data)
        response = self.client.delete(
            "/task/{}".format(task.id),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        self.assertEqual(204, response.status_code)

    def test_delete_task_fail(self):
        """ Test endopoint delete task fail"""
        task = save_task_to_db(self.data)
        response = self.client.delete(
            "/task/{}".format(task.id),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token2)
            }
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json, ERR_TASK_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
