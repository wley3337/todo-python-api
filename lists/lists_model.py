from config.db.db_connection import DBConnection
from to_dos import to_dos_model
from config.db.db_connection import DBConnection


# export interface ListSchemaType{
#     id: string
#     user_id: number
#     heading: string
#     display_order: number
#     created_at: Date
#     updated_at: Date
# }
# 'INSERT INTO lists(user_id, heading, display_order, created_at, updated_at) VALUES(%s, %s, %i, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *',


class List:
    def __init__(self, user_id, heading):
        self.user_id = user_id
        self.heading = heading
        self.display_order = 0
        self.errors = {"messages": []}
        self.status_code = 200

    def save(self):
        """
        Attempts to save list. If a list does not save, it returns False with status code of 500 and DataBase Error added to error messages, if successful returns True, code of 201
        """
        self.save_to_db()
        if hasattr(self, 'id'):
            self.status_code = 201
            return True
        else:
            self.errors['messages'].append("DataBase Error, Please Try again")
            self.status_code = 500
            return False

    def save_to_db(self):
        """
        Saves list to db
        'INSERT INTO lists(user_id, heading, display_order, created_at, updated_at) VALUES(%s, %s, %i, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING row_to_json(lists)' 
        """
        db = DBConnection()
        db.cur.execute(
            """
            INSERT INTO lists(user_id, heading, display_order, created_at, updated_at) VALUES(%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING row_to_json(lists)
            """, (self.user_id, self.heading, self.display_order)
        )
        db.con.commit()
        new_list = db.cur.fetchone()[0]
        self.id = new_list["id"]
        db.close()

    def to_json(self):
        """
        Returns a serialized list for React Front End
        """
        return serialize_list_by_id(self.id)


def get_list_by_id(list_id):
    db = DBConnection()
    # returns a tuple with a dict index 0 with columns as keys
    db.cur.execute(
        """SELECT row_to_json(lists) FROM lists WHERE id = %s""", (list_id,))
    list = db.cur.fetchone()[0]
    db.close()
    return list


def get_users_lists_by_user_id(user_id):
    db = DBConnection()
    # returns a tuple with a dict index 0 with columns as keys
    db.cur.execute(
        """SELECT row_to_json(lists) FROM lists WHERE user_id = %s""", (user_id,))
    lists = db.cur.fetchall()
    db.close()
    if len(lists) == 0:
        return []
    user_lists = []
    for list in lists:
        # accounts for dict in position 0
        user_lists.append(serialize_list(list[0]))
    return user_lists


def serialize_list_by_id(list_id):
    """
    Returns a serialzed list by list id
    """
    db_list = get_list_by_id(list_id)
    return serialize_list(db_list)


def serialize_list(list):
    """list shape: {'id': 7, 'user_id': 1, 'heading': 'New list 3', 'display_order': 0, 'created_at': '2019-11-19T16:08:10.440681', 'updated_at': '2019-11-19T16:08:10.440681'}"""
    list_id = list["id"]
    to_dos = to_dos_model.get_to_dos_by_list_id(list_id)
    return {"id": list_id, "heading": list["heading"], "toDos": to_dos}


def delete_list_by_id(list_id):
    db = DBConnection()
    db.cur.execute(
        """
        DELETE FROM lists WHERE id = %s RETURNING * 
        """, (list_id,)
    )
    db.con.commit()
