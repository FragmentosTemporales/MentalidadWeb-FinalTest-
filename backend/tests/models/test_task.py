import unittest
from app.models import Task
from tests import BaseTestCase
from tests.utils.task import save_task_to_db

class TestTaskModel(BaseTestCase):
    """ Test that task model is ok """

    def setUp(self):
        """ Setting up the test class  """
        super().setUp()
        self.data = {
            "task":"prueba",
            "description":"prueba",
            "is_completed": False,
            "user_id": 1
        }
        self.data2 = {
            "task":"prueba2",
            "description":"prueba2",
            "is_completed": False,
            "user_id": 1
        }
        self.data3 = {
            "task":"prueba3",
            "description":"prueba3",
            "is_completed": False,
            "user_id": 2
        }
        self.params = {
            "task":"prueba2",
            "description":"prueba2",
            "is_completed": True,
            "user_id": 1
        }
    
    def test_create_task(self):
        """ Test create task is success """
        task = save_task_to_db(self.data)
        self.assertIsNotNone(task.id)
        for key in self.data.keys():
            self.assertEqual(
                getattr(task, key), self.data.get(key, None) 
            )

    def test_update_succes(self):
        """ Test update task is succes """
        task = save_task_to_db(self.data)
        task.update(**self.params)
        for key in self.params.keys():
            self.assertEqual(getattr(task, key), self.params[key])

    def test_delete_from_database_success(self):
        """ Test deleting task from db is success """
        task = save_task_to_db(self.data)
        id = task.id
        task.delete_from_db()
        deleted_task = Task.find_by_id(id)
        self.assertIsNone(deleted_task)
    
    def test_find_by_id_succes(self):
        saved_task = save_task_to_db(self.data)
        task = Task.find_by_id(saved_task.id)
        self.assertIsInstance(task, Task)
        self.assertEquals(task, saved_task)

    def test_find_by_id_none(self):
        task = Task.find_by_id(0)
        self.assertIsNone(task)

    def test_find_user_task_by_user_id(self):
        task = save_task_to_db(self.data)
        save_task_to_db(self.data2)
        user = task.user_id
        task_list = Task.find_all_by_user_id(user)
        self.assertEquals(len(task_list), 2)


if __name__ == "__main__":
    unittest.main()