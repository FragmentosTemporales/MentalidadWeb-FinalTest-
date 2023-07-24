import unittest
from app.models import User
from tests import BaseTestCase
from tests.utils.user import save_user_to_db


class TestUserModel(BaseTestCase):
    """ Test that user model is ok """

    def setUp(self):
        """ Setting up the test class  """
        super().setUp()
        self.data = {
            "username": "test",
            "email": "example@example.com",
            "password": "12345",
            "is_disabled": False
        }
        self.data2 = {
            "username": "Testing",
            "email": "example2@example.com",
            "password": "12345",
            "is_disabled": False
        }
        self.data3 = {
            "username": "Testing",
            "email": "example2@example.com",
            "password": "12345",
            "is_disabled": False
        }
        self.data_email_upper = {
            "username": "test",
            "email": "EMAIL@EXAMPLE.COM",
            "password": "12345",
            "is_disabled": False
        }
        self.params = {
            "username": "testing 2",
            "email": "test@test.com",
            "is_disabled": True
        }

    def test_string_representation(self):
        """ Test string representation of user model """
        password = self.data.get("password", None)
        user = User(**self.data)
        user.set_password(password)
        self.assertEqual(str(user), "<User 'NotSaved: {}'>".format(
            user.username))
        user.save_to_db()
        self.assertEqual(str(user), "<User '#{}: {}'>".format(
            user.id, user.username))

    def test_create_success(self):
        """ Test create user is success """
        user = save_user_to_db(self.data)
        self.assertIsNotNone(user.id)
        for key in self.data.keys():
            if key != "password":
                self.assertEqual(
                    getattr(user, key), self.data.get(key, None))
        self.assertTrue(user.check_password(self.data.get("password", None)))

    def test_create_user_fails_because_email_already_taken(self):
        """ Test create user fails because email already taken """
        save_user_to_db(self.data)
        with self.assertRaises(ValueError) as context:
            user = User(**self.data)
            user.save_to_db()
        self.assertTrue(
            "El correo electrónico se encuentra tomado por otro usuario."
            in str(context.exception)
        )

    def test_email_normalized(self):
        """ Test user email is normalized after save into db """
        user = save_user_to_db(self.data_email_upper)
        user_saved = User.find_by_email(user.email)
        self.assertEquals(
            user_saved.email, self.data_email_upper["email"].lower())

    def test_update_success(self):
        """ Test update user is success """
        user = save_user_to_db(self.data)
        user.update(**self.params)
        for key in self.params.keys():
            self.assertEqual(getattr(user, key), self.params[key])

    def test_update_user_fails_because_email_duplicated(self):
        """ Test user update fails because already exists in db """
        save_user_to_db(self.data)
        new_user = save_user_to_db(self.data2)
        with self.assertRaises(ValueError) as context:
            new_user.update(**self.data)
        self.assertTrue(
            "El correo electrónico se encuentra tomado por otro usuario."
            in str(context.exception))

    def test_find_by_id_success(self):
        """ Test finding user by id is success """
        saved_user = save_user_to_db(self.data)
        user = User.find_by_id(saved_user.id)
        self.assertIsInstance(user, User)
        self.assertEquals(user, saved_user)

    def test_find_by_id_none(self):
        """ Test finding user by id returns none """
        user = User.find_by_id(9999)
        self.assertIsNone(user)

    def test_find_by_email_success(self):
        """ Test finding user by email is success """
        saved_user = save_user_to_db(self.data)
        user = User.find_by_email(saved_user.email)
        self.assertIsInstance(user, User)
        self.assertEquals(user, saved_user)

    def test_find_by_email_none(self):
        """ Test finding user by email returns None """
        user = User.find_by_email("testing1234@1234.xyz")
        self.assertIsNone(user)

    def test_delete_from_database_success(self):
        """ Test deleting user from db is success """
        user = save_user_to_db(self.data)
        id = user.id
        user.delete_from_db()
        deleted_user = User.find_by_id(id)
        self.assertIsNone(deleted_user)


if __name__ == "__main__":
    unittest.main()
