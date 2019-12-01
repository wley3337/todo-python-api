# Python (Flask with Docker) backend for a ToDo app

Docker setup and some of the API structure from [here](https://www.youtube.com/watch?v=4T5Gnrmzjak)
## Setup 
* clone repo
***Create `env.py` file***
  ```
  import os
  
  os.environ["DB_DATABASE_DEV"]= "NAME_OF_YOUR_DEV_DB"
  os.environ["DB_DATABASE_TEST"]= "NAME_OF_YOUR_TEST_DB"
  # change for production
  os.environ["DB_DATABASE_PROD"]= "NAME_OF_YOUR_PROD_DB"
  ```
***For Docker***
* run `docker-compose build` 
* run `docker-compose up`
* main entry point is `server.py`

***For Local DB***
* run `python server.py`

## Dependencies: 
* flask
* flask_restful
* psycopg2
* marshmallow 

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
  - POST `/login` 
      - login user with { user: { :username, :password } }
      - returns: 
      ```
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
      - create new list  with  {list: { :heading } }
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
      - destroy list  with  {list: { :id } } and destroy all dependents
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