import os
import pytest
from db import db_connection
from users import users_model
import env
# for mocking
# from unittest.mock import patch
#
# @patch('package.module.method',  new=method_to_call_instead) <---no invocation

# testing principle:
# Arrange
# Act
# Assert

# example of setup and tear down style
# db = None

# def setup_module(module):
#     # this sets up before running this test module (before action from rspec)
#     global db = "assign global a value"
#     return True


# def teardown_module(module):
#     # this is cleanup after tests are run (after action from rspec)
#     "close db connection here"
#     return True

# fixture method of testing
# scope module is file based
@pytest.fixture(scope="module")
def db_setup(request):
    """
    Test database setup
    """
    os.environ["FLASK_ENV"] = "TEST"
    db = db_connection.DBConnection()
    # create test user
    db.cur.execute('INSERT INTO users(first_name, last_name, username, password_digest, created_at, updated_at) VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *',
                   ('testFirstName', 'testLastName', 'test123', "1"))
    db.con.commit()

    def fin():
        # cleanup db and close db connection
        db.cur.execute('DELETE FROM users')
        db.con.commit()
        db.close()
    request.addfinalizer(fin)
    return db
    # or you can either clean up with this:
    # # setup step
    # yield db
    # # cleanup step
    # db.cur.execute('DELETE FROM users')
    # db.con.commit()
    # db.close()


@pytest.fixture(scope="module")
def user_for_test(db_setup):
    """
    Test Fixture for a test_user pulled from the database after creation
        shape: test_user = {
            "id": n, "first_name": 'testFirstName',
            "last_name": 'testLastName', "username": 'test123'
        }
    """
    db_setup.cur.execute(
        """
            SELECT row_to_json(u) 
                FROM( SELECT id, first_name, last_name, username FROM users WHERE username = %s LIMIT 1)
            u
            """, ("test123",))
    test_user = db_setup.cur.fetchone()[0]
    return test_user


"""USER MODEL tests"""


def test_get_user_by_username(db_setup):
    """
    Test able to get a user by username from database
    """
    user = users_model.get_user_by_username("test123")
    assert user["first_name"] == "testFirstName"


def test_all_users(db_setup):
    """
    Test return all users returns all users in DB
    """
    assert len(users_model.all_users()) == 1


def test_get_user_by_id(db_setup, user_for_test):
    """
    Test able to get a user by user['id']
    """
    user = users_model.get_user_by_id(user_for_test["id"])
    assert user["firstName"] == "testFirstName"


def test_serialize_user(db_setup):
    """
    Test correctly serializes a user pulled from the database
    """
    test_user = {"id": 1, "first_name": 'testFirstName',
                 "last_name": 'testLastName', "username": 'test123'}
    serialized_test_user = users_model.serialize_user(test_user)
    assert serialized_test_user["lists"] == []
    assert serialized_test_user["lastName"] == "testLastName"
