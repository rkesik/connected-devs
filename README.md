
# Concept
In general we want to have separate busniess case layer (use_case) which can utilize different
adapters / repo to operate and expose business logic to our endpoints.

                       +------------------+
                       |    use case      |
                       +------------------+
                                |
             +------------------+---------------------+
             |                  |                     |
             V                  V                     V
    +-----------------+ +------------------+ +-------------------+
    |   GuthubRepo    | |   TwitterRepo    | |     MongoRepo     |
    +-----------------+ +------------------+ +-------------------+
            ^                     ^                    ^
            |                     |                    |
    ===========+=====================+====================+================
            |                     |                    |
    +--------------------+ +--------------------+ +--------------------+
    |   TwitterClient    | | GithubClinet       | |   MongoClient      |
    +--------------------+ +--------------------+ +--------------------+


## App
Ideally endpoints(views) should be thin as much as possible - and manage a control flow for REST api. 
For example if we would like to expose the same logic via commandline interface we need to just use our use_case layer.
```bash 
/interfaces/
    /api/views.py
    /cmd/cli/py
```   


## Usecases

Usecase should be configurable with db_handler because we want to have controll over db session to better   utilize db connections beloging to one thread.

### Repos and adapters
Repos - are jsut a addpater to external / internal services to mainly get data
In case of MongoRepo ->a s you might notice my intention was to create MongoRepo addapter configurable with  mongo_client that give us posibility to exchange client and keep MongoRepo with the same logic. Client need to be a one instance only to share same connection.  
  
```bash
# usecase.py
class UseCase:
    adapter = MongoRepo(clinet=current_mongo_driver)
    adapter.connect()
    adapter.select()

```

### entities
Because we are using Bsjon database mongodb we can safely use Pydantic as our models otherwise some ORM would be needed to do whole verification and validation on database level - afterall we would like to have guranace that rows in database do not have some trash. 
Pydantic should not be part of validation process. But for that use case fill fit fine.


# What is missing?

Please visit code and look for #TODOs with comments for specifc places

* For sure it would be nice to run code base against `mypy`, `black` `pylint` to have 
* ofc we ened to ensure proper docstrings for public class interfaces


# How to play?

notice: you need to have pipenv
  
```bash
docker compose up --build
```
visit on your browser: 
```
http://localhost:8000
```


### Tests
  
  
```bash
pipenv install --dev
cd app
pytest .
```