import unittest
from app.models import Task
from tests import BaseTestCase
from tests.utils.user import save_user_to_db

class TestTaskModel(BaseTestCase):
    """ Test that task model is ok """

    def setUp(self):
        """ Setting up the test class  """
        super().setUp()
        self.data = {
            "title":"prueba",
            "description":"prueba",
            "user_id": 1
        }
    
    def task_exist(self):
      

if __name__ == "__main__":
    unittest.main()