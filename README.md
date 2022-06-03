
### Services:

# mongodb as databse  
# fastAPI as backend  
# mongo-express as admin view for mongo  



One thing with sharable resoucess is to keep single instance for database.
We have few options:   
 - we can use Depends to our controllers/views and inject db-client-session into lower layers
 - request.state (to keep)


or we can make global or we can just ContentVars to store threaded separated instance. 

Singleton as Motor database client is just to prevent accidently creating new instance we need to ensure that in one thread we will have only one instance.


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

# What is missing?

 For more complex applications FastAPI router is more convinient way to route api calls.
 Conifg we can store all of hardcoded settings in some config file or pass values as environment

## Layers (concept)

### endpoints
Framework related interface

### use_case
Our busniess logic is concentrated here, we can thing of it as a one-to-one with our stories use cases. That part should be fully framework, database agnostic. 
We need to give a db_adapter to be used (right now it is mongo but it can be easly changed to any ohter) and our db_client comming from application layer. 
It is okay to have few use_cases for one domain, each of them can have different adapter for example: what if we want to recieve file, parse - store context in database and send it to s3 bucket - that sounds like two use_cases (aka busniess logic) 


### repo.py
Database adapter (mongo in that case) it translates busniess logic into database queries. We need to pass db_client into it.
Each repo class can be suited for usecase for example: RepoMongoConnect RepoMongoRegister it give us more felxibility when we are dealing with fat-classes.


### entities
Because we are using Bsjon database mongodb we can safely use Pydantic as our models otherwise some ORM would be needed to do whole verification and validation on database level - afterall we would like to have guranace that rows in database do not have some trash. 
Pydantic should not be part of validation process. But for that use case fill fit fine.

### services:
Packages, modules that can be a installable packege - something that can serve some independet logic from our busniess logic functionality.


### utilites:


### Tests
  
  
```bash
pipenv install --dev
cd app
pytest .
```