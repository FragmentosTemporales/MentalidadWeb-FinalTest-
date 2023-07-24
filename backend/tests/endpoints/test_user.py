import json
import unittest
from app.models import User
from app.schemas import UserSchema
from tests import BaseTestCase


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class TestUserEndpoint(BaseTestCase):
    """ Test that users endpoints works fine """

    def setUp(self):
        super().setUp()
        self.data = {
            "username": "test",
            "email": "example@example.com",
            "password": "12345",
            "is_disabled": False
        }

    def test_create_user_endpoint_ok(self):
        """ Test creating new user is ok """
        payload = json.dumps({
            "username": "Fernando",
            "email": "testing2@gmail.com",
            "password": "DataEngineerLead",
            "is_disabled": False
        })
        response = self.client.post(
            "/register",
            headers={
                "Content-Type": "application/json",
            },
            data=payload
        )
        print(response.json)
        user = User.find_by_email("testing2@gmail.com")
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json["message"], "Usuario guardado")
        self.assertIsInstance(user, User)

        
if __name__ == '__main__':
    unittest.main()