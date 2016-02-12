"""
Configuration of 'memos' Flask app. 
Edit to fit development or deployment environment.

"""

### Flask settings
PORT=5000        # The port I run Flask on
DEBUG = True     # Set to False on ix

### MongoDB settings
MONGO_PORT=27017 #  Probably best to use the same port as you use on ix

### The following are for a Mongo user you create for accessing your
### memos database.  It should not be the same as your database administrator
### account. 
MONGO_PW = "remember"  
MONGO_USER = "peasant"
MONGO_URL = "mongodb://{}:{}@localhost:{}/memos".format(MONGO_USER,MONGO_PW,MONGO_PORT)

