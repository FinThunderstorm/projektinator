import re
from uuid import uuid4
import unittest
from entities.user import User
from utils.helpers import get_test_user


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = get_test_user()

    def test_init_user_with_id(self):
        user = User(self.user["username"],
                    self.user["user_role"],
                    self.user["password_hash"],
                    self.user["firstname"],
                    self.user["lastname"],
                    self.user["email"],
                    self.user["profile_image"],
                    self.user["user_id"])
        self.assertEqual(user.username, self.user["username"])
        self.assertEqual(user.user_role, self.user["user_role"])
        self.assertEqual(user.password_hash, self.user["password_hash"])
        self.assertEqual(user.firstname, self.user["firstname"])
        self.assertEqual(user.lastname, self.user["lastname"])
        self.assertEqual(user.email, self.user["email"])
        self.assertEqual(user.profile_image, self.user["profile_image"])
        self.assertEqual(user.user_id, self.user["user_id"])
        self.assertRegex(
            user.user_id, r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$')

    def test_init_user_without_id(self):
        user = User(self.user["username"],
                    self.user["user_role"],
                    self.user["password_hash"],
                    self.user["firstname"],
                    self.user["lastname"],
                    self.user["email"],
                    self.user["profile_image"])
        self.assertEqual(user.username, self.user["username"])
        self.assertEqual(user.user_role, self.user["user_role"])
        self.assertEqual(user.password_hash, self.user["password_hash"])
        self.assertEqual(user.firstname, self.user["firstname"])
        self.assertEqual(user.lastname, self.user["lastname"])
        self.assertEqual(user.email, self.user["email"])
        self.assertEqual(user.profile_image, self.user["profile_image"])
        self.assertRegex(
            user.user_id, r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$')

    def test_init_user_with_default_image(self):
        user = User(self.user["username"],
                    self.user["user_role"],
                    self.user["password_hash"],
                    self.user["firstname"],
                    self.user["lastname"],
                    self.user["email"],
                    None,
                    self.user["user_id"])
        self.assertEqual(user.username, self.user["username"])
        self.assertEqual(user.user_role, self.user["user_role"])
        self.assertEqual(user.password_hash, self.user["password_hash"])
        self.assertEqual(user.firstname, self.user["firstname"])
        self.assertEqual(user.lastname, self.user["lastname"])
        self.assertEqual(user.email, self.user["email"])
        self.assertEqual(user.profile_image, "defaultimage")
        self.assertEqual(user.user_id, self.user["user_id"])
        self.assertRegex(
            user.user_id, r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$")
