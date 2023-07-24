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
        self.data2 = {
            "username": "test2",
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
        """ Test login user is ok """
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
        self.assertEqual(200, response.status_code)

    def test_login_user_endpoint_fail(self):
        """ Test login user fail """
        save_user_to_db(self.data)
        payload = json.dumps({
            "email": "example@example.com",
            "password": "estanoes"
        })
        response = self.client.post(
            "/login",
            headers={
                "Content-Type": "application/json",
            },
            data=payload
        )
        #print(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json["error"],"El usuario o la contraseña son incorrectos")

    def test_get_user_endpoint_ok(self):
        """ Test get user is ok """
        user = save_user_to_db(self.data)
        id = user.id
        response = self.client.get(
            "/user/" + str(id),
        )
        self.assertEqual(200, response.status_code)

    def test_get_user_endpoint_fail(self):
        """ Test get user fail """
        user = self.data
        id = 9999
        response = self.client.get(
            "/user/" + str(id),
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json["error"], "Usuario no encontrado")

    def test_update_user_endpoint_ok(self):
        """ Test update user ok """
        user = save_user_to_db(self.data)
        id = user.id
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
        data = json.loads(response.data)
        token = data.get("token")
        res = self.client.put(
            "/userlist/" + str(id),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            data=json.dumps(self.data2)
        )
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.json["message"], "Usuario actualizado")

    def test_disable_user_endpoint_ok(self):
        """ Test disabled user ok """
        user = save_user_to_db(self.data)
        id = user.id
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
        data = json.loads(response.data)
        token = data.get("token")
        res = self.client.delete(
            "/userlist/" + str(id),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
        )
        self.assertEqual(204, res.status_code)
        self.assertEqual(res.data, b"")

    def test_disable_user_endpoint_fail(self):
        """ Test disabled user fail """
        user = save_user_to_db(self.data)
        id = user.id
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
        data = json.loads(response.data)
        token = data.get("token")
        res = self.client.delete(
            "/userlist/9999",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
        )
        print(res.data)
        self.assertEqual(404, res.status_code)
        self.assertEqual(res.json["error"], "Usuario no encontrado")


if __name__ == '__main__':
    unittest.main()