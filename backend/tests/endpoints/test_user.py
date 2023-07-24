import json
import unittest
from app.models import User
from app.schemas import UserSchema
from tests import BaseTestCase
from tests.utils.user import save_user_to_db


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
        user = User.find_by_email("testing2@gmail.com")
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json["message"], "Usuario guardado")
        self.assertIsInstance(user, User)

    def test_create_user_endpoint_fail(self):
        """ Test creating new user fail"""
        save_user_to_db(self.data)
        payload = json.dumps({
            "username": "test",
            "email": "example@example.com",
            "password": "12345",
            "is_disabled": False
        })
        response = self.client.post(
            "/register",
            headers={
                "Content-Type": "application/json",
            },
            data=payload
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json["error"], "La cuenta ya existe o está deshabilitada.")

    def test_login_user_endpoint_ok(self):
        """ Test creating login user is ok """
        save_user_to_db(self.data)
        payload = json.dumps({
            "email": "example@example.com",
            "password": "12345"
        })
        response = self.client.post(
            "/login",
            headers={
                "Content-Type": "application/json",
            },
            data=payload
        )
        print(response.data)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()