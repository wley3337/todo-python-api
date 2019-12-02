from db import db_connection
# import datetime
# # t = datetime.datetime(2012, 2, 23, 0, 0)
# # t.strftime('%m/%d/%Y')


def get_users_lists_by_user_id(user_id):
    db = db_connection.DBConnection()
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


def serialize_list(list):
    """shape: {'id': 7, 'user_id': 1, 'heading': 'New list 3', 'display_order': 0, 'created_at': '2019-11-19T16:08:10.440681', 'updated_at': '2019-11-19T16:08:10.440681'}"""
    list_id = list["id"]
    return {"id": list_id, "heading": list["heading"], "toDos": []}
