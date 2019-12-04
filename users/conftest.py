import pytest
import os

import config.env
from config.db.db_connection import DBConnection

"""User TEST DB and TEST USER fixtures with commented notes about Pytest pattern options"""
# fixture method of testing
# scope module is file based
@pytest.fixture(scope="module")
def db_setup(request):
    """
    Test database setup
    """
    os.environ["FLASK_ENV"] = "TEST"
    db = DBConnection()
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

# """ Notes on setup and tear down process and options:
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
# @pytest.fixture(scope="module")
# def db_setup(request):
#     """
#     Test database setup
#     """
#     os.environ["FLASK_ENV"] = "TEST"
#     db = db_connection.DBConnection()
#     # create test user
#     db.cur.execute('INSERT INTO users(first_name, last_name, username, password_digest, created_at, updated_at) VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *',
#                    ('testFirstName', 'testLastName', 'test123', "1"))
#     db.con.commit()

#     def fin():
#         # cleanup db and close db connection
#         db.cur.execute('DELETE FROM users')
#         db.con.commit()
#         db.close()
#     request.addfinalizer(fin)
#     return db
#     # or you can either clean up with this:
#     # # setup step
#     # yield db
#     # # cleanup step
#     # db.cur.execute('DELETE FROM users')
#     # db.con.commit()
#     # db.close()


# @pytest.fixture(scope="module")
# def user_for_test(db_setup):
#     """
#     Test Fixture for a test_user pulled from the database after creation
#         shape: test_user = {
#             "id": n, "first_name": 'testFirstName',
#             "last_name": 'testLastName', "username": 'test123'
#         }
#     """
#     db_setup.cur.execute(
#         """
#             SELECT row_to_json(u)
#                 FROM( SELECT id, first_name, last_name, username FROM users WHERE username = %s LIMIT 1)
#             u
#             """, ("test123",))
#     test_user = db_setup.cur.fetchone()[0]
#     return test_user

# """
