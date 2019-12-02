from db import db_connection


def get_to_dos_by_list_id(list_id):
    db = db_connection.DBConnection()
    # returns a tuple with a dict index 0 with columns as keys
    db.cur.execute(
        """SELECT row_to_json(to_dos) FROM to_dos WHERE list_id = %s""", (list_id,)
    )
    db_to_dos = db.cur.fetchall()
    db.close()

    to_dos = []
    if len(db_to_dos) == 0:
        return []
    for to_do in db_to_dos:
        to_dos.append(serialize_to_do(to_do[0]))
    return to_dos


def serialize_to_do(to_do):
    """to_do shape: {'id': 32, 'list_id': 2, 'title': 'This is Second List ', 'description': '', 'due': '2019-11-19T00:00:00', 'created_at': '2019-11-19T16:04:48.881635', 'updated_at': '2019-11-19T16:04:48.881635'}"""
    print(to_do)
    return {"id": to_do["id"], "listId": to_do["list_id"], "description": to_do["description"], "due": to_do["due"]}


def get_all_to_dos():
    db = db_connection.DBConnection()
    # returns a tuple with a dict index 0 with columns as keys
    db.cur.execute(
        """SELECT row_to_json(to_dos) FROM to_dos"""
    )
    db_to_dos = db.cur.fetchall()
    db.close()
    to_dos = []
    if len(db_to_dos) == 0:
        return []
    for to_do in db_to_dos:
        to_dos.append(serialize_to_do(to_do[0]))
    return to_dos
