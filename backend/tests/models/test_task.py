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

    "filtrar id, tareas de usuario, borrar tareas, "

if __name__ == "__main__":
    unittest.main()