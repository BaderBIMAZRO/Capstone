# Casting Agency 
* This website responsible for creating movies and managing and assigning actors to those movies and implemented role base authentication from auth0 which add permissions for certain users.

## dependencies
```

- urllib3
- SQLAlchemy
- CORS
- functools
- pylint
- python-jose-cryptodome

```


### Dependencies
* After running loacl environment install requirements.txt  
```bash
$pip install -r requirements.txt
``` 

### Database Setup
* createdb CA  and in terminal run:
```bash
$psql CA < CA_test.psql 
```

### Running the server
* In the terminal run:
```bash
$export FLASK_APP=app.py

$flask run --reload
```
## Documentation
The Casting Agency has role based access control listed below:
* Assistant permissions:
- `get:movies`
- `get:actors`

* Director can view and patch movie and delete add actor
- `get:movies`
- `get:actors`
- `patch:movies`
- `patch:actors`
- `delete:actors`
- `post:actors`

* Producer has all permissions 

### Based_url
```http
http://127.0.0.1:5000/
```
### GET /movies - GET / actors
* When curl any of the endpoints above you will get response with data of movie or actor

```bash
$curl http://127.0.0.1:5000/movies

```
* Expected response

```json
{
    "movies": [
       
        {
            "id": 20,
            "rate": 3.0,
            "release_date": "Fri, 15 May 2020 23:00:00 GMT",
            "title": "Zack and Miri"
        },
        {
            "id": 21,
            "rate": 2.0,
            "release_date": "Fri, 15 May 2020 23:00:00 GMT",
            "title": "Youth in Revolt"
        },
        {
            "id": 22,
            "rate": 4.0,
            "release_date": "Fri, 15 May 2020 23:00:00 GMT",
            "title": "You Will Meet a Tall Dark Stranger"
        }
    ],
    "success": true
}

```
* curl actors example 
```bash
$curl http://127.0.0.1:5000/actors

```
* Expected response
```json
{
    "actors": [
        {
            "age": 20,
            "gender": "M",
            "id": 4,
            "name": "Muhammed"
        },
        {
            "age": 30,
            "gender": "M",
            "id": 10,
            "name": "Khalid"
        },
        {
            "age": 36,
            "gender": "M",
            "id": 13,
            "name": "Tom"
        }
    ],
    "success": true
}

```

### POST /movies - POST / actors

* This is an example of posting movie and actor
```bash
$curl --request POST \
--url http://127.0.0.1:5000/movies \
--header 'authorization: Bearer Your_token' \
--header 'content-type: application/json' -d '{"title": "curlPost", "rate": "5", "release_date": "2020-08-15T23:00:00.000Z"}' 

$curl --request POST \
--url http://127.0.0.1:5000/actors \
--header 'authorization: Bearer Your_token' \
--header 'content-type: application/json' -d '{"name": "Muhammed" , "age": 20, "gender": "M" }' 
```

* The expected response will be all data including the new posted one.

### DELETE /actors -  DELETE /movies
* Detete example in termainal.

```bash
$curl --request DELETE http://127.0.0.1:5000/movies/13 \
--header 'authorization: Bearer Your_token' 

$curl --request DELETE http://127.0.0.1:5000/actors/4 \
--header 'authorization: Bearer Your_token' 

```
* Response 
```json
# movies
$ {"id":"The movie with id:13 has been deleted","success":true}

# actors
$ {"id":"The actor with id:4 has been deleted","success":true}

```


### PATCH /actors - PATCH /movies
* Example of patch movie
```bash
$curl --request PATCH \
--url http://127.0.0.1:5000/movies/14 \
--header 'authorization: Bearer Your_token' \
--header 'content-type: application/json' -d '{"title": "curlPatch"}' 

```
* Patch response

```json
$ { "id":"movie with the id:14 has been updated", "success":true}
```
## Testing 
To run tests use the following commands in terminal.

- `dropdb CA_test`
- `createdb CA_test`
- `psql CA_test < CA_test.psql`
- `python test_app.py`



## Postman Testing
* Using postman for testing move postman json file with the following command in terminal: 
- ` mv capstone-fsnd-postman-collection_v1.json ../`
* Include JWT token to each role. 
* Import json file above in postman.
* Right-clicking the collection then run postman tests


