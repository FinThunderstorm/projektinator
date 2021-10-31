from repositories.user_repository import user_repository
import unittest


class TestTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.__user_repository = user_repository

    def test_works(self):
        user = self.__user_repository.new(
            'username', 1, 'password', 'firstname', 'lastname', 'email@email.email')
        self.assertEqual(user.username, 'username')
