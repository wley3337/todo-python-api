import os
import pytest

from users import users_model
# for mocking
# from unittest.mock import patch
#
# @patch('package.module.method',  new=method_to_call_instead) <---no invocation

# testing principle:
# Arrange
# Act
# Assert

"""USER MODEL tests"""


class TestUserModels:
    def test_get_user_by_username(self, db_setup):
        """
        Test able to get a user by username from database
        """
        user = users_model.get_user_by_username("test123")
        assert user["first_name"] == "testFirstName"

    def test_all_users(self, db_setup):
        """
        Test return all users returns all users in DB
        """
        assert len(users_model.all_users()) == 1

    def test_get_user_by_id(self, db_setup, user_for_test):
        """
        Test able to get a user by user['id']
        """
        user = users_model.get_user_by_id(user_for_test["id"])
        assert user["firstName"] == "testFirstName"

    def test_serialize_user(self, db_setup):
        """
        Test correctly serializes a user pulled from the database
        """
        test_user = {"id": 1, "first_name": 'testFirstName',
                     "last_name": 'testLastName', "username": 'test123'}
        serialized_test_user = users_model.serialize_user(test_user)
        assert serialized_test_user["lists"] == []
        assert serialized_test_user["lastName"] == "testLastName"
