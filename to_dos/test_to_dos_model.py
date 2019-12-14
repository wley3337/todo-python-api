import pdb
import os
import pytest

from to_dos import to_dos_model

# NOTE: need to add a conf file for tests


class TestToDosModel:
    def test_delete_to_do_by_id(self, db_setup, to_do_delete_for_tests):
        """
        Test to check if a todo is properly deleted
        """
        deleted_id = to_do_delete_for_tests["id"]
        deleted_to_do_id_json = to_dos_model.delete_to_do_by_id(deleted_id)
        db_setup.cur.execute(
            """
                SELECT * FROM to_dos WHERE id = %s
            """, (deleted_id,)
        )
        results = db_setup.cur.fetchall()
        assert len(results) == 0
        assert deleted_to_do_id_json["toDoId"] == deleted_id

    def test_serialize_to_do(self, db_setup):
        """
        Test that the shape: {"id": to_do["id"], "listId": to_do["list_id"], "description": to_do["description"], "due": to_do["due"]} is returned
        """

        pass

    def test_get_to_dos_by_list_id(self, db_setup):
        """
        Test that you can get all the toDos associated with a single list
        """

        pass

    def test_get_all_to_dos(self, db_setup):
        """
        Test should return all toDos currently in DB. 
        """

        pass
