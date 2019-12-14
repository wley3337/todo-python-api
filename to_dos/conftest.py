import pytest
import os


import pdb

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
    db.cur.execute('DELETE FROM users')
    db.cur.execute('DELETE FROM lists')
    db.cur.execute('DELETE FROM to_dos')
    db.con.commit()
    # create test user
    db.cur.execute('INSERT INTO users(first_name, last_name, username, password_digest, created_at, updated_at) VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *',
                   ('testFirstName', 'testLastName', 'test123', "1"))
    db.con.commit()

    def fin():
            # cleanup db and close db connection
        db.cur.execute('DELETE FROM users')
        db.cur.execute('DELETE FROM lists')
        db.cur.execute('DELETE FROM to_dos')
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


@pytest.fixture(scope="module")
def list_1_for_tests(db_setup, user_for_test):
    """
    Creates a list with two To Dos for testing
    """
    heading = "test_1_heading"
    display_order = 0
    db_setup.cur.execute(
        """
        INSERT INTO lists(user_id, heading, display_order, created_at, updated_at) VALUES(%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *
        """, (user_for_test["id"], heading, display_order,)
    )
    db_setup.con.commit()
    db_setup.cur.execute(
        """
            SELECT row_to_json(L) 
                FROM( SELECT id, heading, display_order FROM lists WHERE heading = %s LIMIT 1)
            L
        """, (heading,)
    )

    test_list_json = db_setup.cur.fetchone()[0]
    return test_list_json


@pytest.fixture(scope="module")
def list_2_for_tests(db_setup, user_for_test):
    """
    Creates a list with two To Dos for testing
    """
    heading = "test_2_heading"
    display_order = 0
    db_setup.cur.execute(
        """
        INSERT INTO lists(user_id, heading, display_order, created_at, updated_at) VALUES(%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *
        """, (user_for_test["id"], heading, display_order,)
    )
    db_setup.con.commit()
    db_setup.cur.execute(
        """
            SELECT row_to_json(L) 
                FROM( SELECT id, heading, display_order FROM lists WHERE heading = %s LIMIT 1)
            L
        """, (heading,)
    )

    test_list_json = db_setup.cur.fetchone()[0]
    return test_list_json


@pytest.fixture(scope="module")
def to_do_1_for_tests(db_setup, list_1_for_tests):
    """
    Creates a list with two To Dos for testing
    """
    list_id = list_1_for_tests["id"]
    title = "toDoTest1Title"
    desc = "toDoTest1Desc"

    db_setup.cur.execute(
        """
        INSERT INTO to_dos(list_id, title, description, due, created_at, updated_at) VALUES(%s, %s, %s, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *
        """, (list_id, title, desc)
    )
    db_setup.con.commit()
    db_setup.cur.execute(
        """
            SELECT row_to_json(t) 
                FROM( SELECT id, list_id, title, description, due FROM to_dos WHERE title = %s LIMIT 1)
            t
        """, (title,)
    )

    test_to_do_json = db_setup.cur.fetchone()[0]
    return test_to_do_json


@pytest.fixture(scope="module")
def to_do_2_for_tests(db_setup, list_1_for_tests):
    """
    Creates a list with two To Dos for testing
    """
    list_id = list_1_for_tests["id"]
    title = "toDoTest2Title"
    desc = "toDoTest2Desc"

    db_setup.cur.execute(
        """
        INSERT INTO to_dos(list_id, title, description, due, created_at, updated_at) VALUES(%s, %s, %s, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *
        """, (list_id, title, desc)
    )
    db_setup.con.commit()
    db_setup.cur.execute(
        """
            SELECT row_to_json(t) 
                FROM( SELECT id, list_id, title, description, due FROM to_dos WHERE title = %s LIMIT 1)
            t
        """, (title,)
    )

    test_to_do_json = db_setup.cur.fetchone()[0]
    return test_to_do_json


@pytest.fixture(scope="module")
def to_do_3_for_tests(db_setup, list_2_for_tests):
    """
    Creates a list with two To Dos for testing
    """
    list_id = list_2_for_tests["id"]
    title = "toDoTest3Title"
    desc = "toDoTest3Desc"

    db_setup.cur.execute(
        """
        INSERT INTO to_dos(list_id, title, description, due, created_at, updated_at) VALUES(%s, %s, %s, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *
        """, (list_id, title, desc)
    )
    db_setup.con.commit()
    db_setup.cur.execute(
        """
            SELECT row_to_json(t) 
                FROM( SELECT id, list_id, title, description, due FROM to_dos WHERE title = %s LIMIT 1)
            t
        """, (title,)
    )


@pytest.fixture(scope="module")
def to_do_delete_for_tests(db_setup, list_1_for_tests):
    """
    Creates a list with two To Dos for testing
    """
    list_id = list_1_for_tests["id"]
    title = "toDoTestDeleteTitle"
    desc = "toDoTestDeleteDesc"

    db_setup.cur.execute(
        """
        INSERT INTO to_dos(list_id, title, description, due, created_at, updated_at) VALUES(%s, %s, %s, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *
        """, (list_id, title, desc)
    )
    db_setup.con.commit()
    db_setup.cur.execute(
        """
            SELECT row_to_json(t) 
                FROM( SELECT id, list_id, title, description, due FROM to_dos WHERE title = %s LIMIT 1)
            t
        """, (title,)
    )

    test_to_do_json = db_setup.cur.fetchone()[0]
    return test_to_do_json
