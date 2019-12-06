# Python (Flask with Docker) backend for a ToDo app

Docker setup and some of the API structure from [here](https://www.youtube.com/watch?v=4T5Gnrmzjak)

[ SQL reference to prevent SQL Injection in Python ](https://realpython.com/prevent-python-sql-injection/)
[Good Video on using pytest](https://www.youtube.com/watch?v=etosV2IWBF0)
[In depth video on how pytest works](https://www.youtube.com/watch?v=LX2ksGYXJ80)

issues: JWT decode is not working correctly once token is sent to front and then sent back.

## Setup

- clone repo
  **_Create `env.py` file_**

  ```
  import os
  os.environ["FLASK_ENV"] = "TEST, DEV, or PROD"
  os.environ["SECRET_KEY"] = "KEY_AS_STRING"
  os.environ["DB_DATABASE_DEV"]= "NAME_OF_YOUR_DEV_DB"
  os.environ["DB_DATABASE_TEST"]= "NAME_OF_YOUR_TEST_DB"
  # change for production
  os.environ["DB_DATABASE_PROD"]= "NAME_OF_YOUR_PROD_DB"
  ```

  **_For Docker_**

  - run `docker-compose build`
  - run `docker-compose up`
  - main entry point is `server.py`

  **_For Local DB_**

  - `source venv/bin/activate` for venv
  - run `python server.py`

## Dependencies:

- flask
- flask_restful [docs](https://flask-restful.readthedocs.io/en/latest/)
- flask-cors [docs](https://pypi.org/project/Flask-Cors/)
- psycopg2 [docs](http://initd.org/psycopg/docs/) -- If you're having trouble installing this try: `pip install psycopg2-binary`
- jwcrypto [docs](https://jwcrypto.readthedocs.io/en/latest/)
- bcrypt [docs](https://pypi.org/project/bcrypt/)
- marshmallow

**_Testing_**

- pytest [docs](https://docs.pytest.org/en/latest/)

## Structure of API

<strong>Routes: </strong>

- POST `/create-user`
  - <strong>USERNAME is unique</strong>
  - create new user with { user: {:firstName, :lastName, :username, :password } }
  - returns:
  ```
  {
    success: true/false,
      if true -->
      {
     user: { :firstName, :lastName, :username, lists: [ :id, :heading, :toDos [ :id, :listId, :title, :description, :due ] ] },
     token: JWT token
     }
      if false --> errors: [ 'of error message strings' ]
    }
  ```
- POST `/login` - login user with { user: { :username, :password } } - returns:

  ````
  {
  success: true/false,
   if true -->
  {
   user: {
  :firstName, :lastName, :username, lists: [ :id, :heading, :toDos [ :id, :listId, :title, :description, :due ] ]
  },
  token: JWT token
  }

        if false --> errors: { messages: ['Wrong Username or Password'] }
      }
      ```

  <strong>- JWT Auth Routes -</strong>
  ````

<strong>Must have: <span>&nbsp;&nbsp;</span> `"authorization": "Bearer *token*"`</strong>

- GET `/users/show`

  - auto login route for user with JWT Token
  - returns:

  ```
  {
    success: true or false,
    if true -->
      user: { :firstName, :lastName, :username, lists: [ :id, :heading, :toDos [ :id, :listId, :title, :description, :due ] ] }

    if false --> errors: [ 'Wrong Username or Password' ]
  }
  ```

- POST `/lists`

  - create new list with {list: { :heading } }
  - returns:

  ```
  {
    success: true or false,
    if true -->
      lists: [ :id, :heading, :toDos [ :id, :listId, :title, :description, :due ] ]

    if false --> errors: [ messages: [ 'error message strings' ] ]
  }
  ```

- DELETE `/lists/:id`

  - destroy list with {list: { :id } } and destroy all dependents
  - returns:

  ```
  {
    success: true or false,
    if true -->
      lists: [ :id, :heading, :toDos [ :id, :listId, :title, :description, :due ] ]

    if false --> errors: [ messages: [ 'List was not destroyed' ] ]
  }
  ```

- POST `/to_dos`

  - creates a todo with { todo: { :listId, :title, :description?, :due? } }
  - returns:

  ```
  {
    success: true or false,
    if true -->
      toDo: { :id, :listId, :title, :description, :due }
    if false --> errors: [ messages: [ 'error message strings' ] ]
  }
  ```

- DELETE `/to_dos/:id`
  - destroys a toDo with { todo: { :listId, :title, :description?, :due? }
  - returns:
  ```
  {
    success: true or false,
    if true -->
      toDoId: deleted toDo's id,
      toDoListId: deleted toDo's list_id
    if false --> errors: [ messages: [ 'ToDo was not deleted' ] ]
  }
  ```
