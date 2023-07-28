import json
import unittest
from flask_jwt_extended import create_access_token
from app.models import User
from app.messages import (
    ERR_EXISTING_USER,
    ERR_WRONG_USER_PASS,
    SUC_USER_UPDATED,
    SUC_NEW_USER,
)
from app.schemas import UserSchema
from tests import BaseTestCase
from tests.utils.user import save_user_to_db


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class TestUserEndpoint(BaseTestCase):
    """Test that users endpoints works fine"""

    def setUp(self):
        super().setUp()
        self.data = {
            "username": "test",
            "email": "example@example.com",
            "password": "12345",
            "is_disabled": False,
        }
        self.data2 = {
            "username": "test2",
        }

        self.user = save_user_to_db(self.data)
        self.token = create_access_token(self.user.email)

    def test_create_user_endpoint_ok(self):
        """Test creating new user is ok"""
        payload = json.dumps(
            {
                "username": "Fernando",
                "email": "testing2@gmail.com",
                "password": "DataEngineerLead",
                "is_disabled": False,
            }
        )
        response = self.client.post(
            "/api/register",
            headers={
                "Content-Type": "application/json",
            },
            data=payload,
        )
        user = User.find_by_email("testing2@gmail.com")
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json, SUC_NEW_USER)
        self.assertIsInstance(user, User)

    def test_create_user_endpoint_fail(self):
        """Test creating new user fail"""
        payload = json.dumps(
            {
                "username": self.data.get("username"),
                "email": self.data.get("email"),
                "password": self.data.get("password"),
            }
        )
        response = self.client.post(
            "/api/register",
            headers={
                "Content-Type": "application/json",
            },
            data=payload,
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json, ERR_EXISTING_USER)

    def test_login_user_endpoint_ok(self):
        """Test login user is ok"""
        payload = json.dumps(
            {"email": self.data.get("email"),
             "password": self.data.get("password")}
        )
        response = self.client.post(
            "/api/login",
            headers={
                "Content-Type": "application/json",
            },
            data=payload,
        )
        self.assertEqual(200, response.status_code)

    def test_login_user_endpoint_fail(self):
        """Test login user fail"""
        payload = json.dumps({"email": self.data.get("email"),
                              "password": "estanoes"})
        response = self.client.post(
            "/api/login",
            headers={
                "Content-Type": "application/json",
            },
            data=payload,
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json, ERR_WRONG_USER_PASS)

    def test_get_user_endpoint_ok(self):
        """Test get user is ok"""
        id = self.user.id
        response = self.client.get("/user/{}".format(id))
        self.assertEqual(200, response.status_code)

    def test_get_user_restx_ok(self):
        """Test get user is ok"""
        response = self.client.get(
            "/api/user",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token),
            },
        )
        self.assertEqual(200, response.status_code)

    def test_get_user_restx_fail(self):
        """Test get user failed"""
        response = self.client.get(
            "/api/user", headers={"Content-Type": "application/json"}
        )
        self.assertEqual(401, response.status_code)

    def test_update_user_restx_ok(self):
        """Test update user ok"""
        res = self.client.put(
            "/api/user",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token),
            },
            data=json.dumps(self.data2),
        )
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.json, SUC_USER_UPDATED)

    def test_update_user_restx_fail(self):
        """Test update user fail"""
        res = self.client.put(
            "/api/user",
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(self.data2),
        )
        self.assertEqual(401, res.status_code)

    def test_disable_user_restx_ok(self):
        """Test disabled user ok"""
        res = self.client.delete(
            "/api/user",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token),
            },
        )
        self.assertEqual(204, res.status_code)

    def test_disable_user_restx_fail(self):
        """Test disabled user ok"""
        res = self.client.delete(
            "/api/user",
            headers={
                "Content-Type": "application/json",
            },
        )
        print(res)
        self.assertEqual(401, res.status_code)


if __name__ == "__main__":
    unittest.main()
