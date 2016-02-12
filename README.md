# proj6-mongo
Simple list of dated memos kept in MongoDB database

## What is here

A simple Flask app that displays all the dated memos it finds in a MongoDB database.
There is also a 'scaffolding' program, db_trial.py, for inserting a couple records into the database 
and printing them out.  Get db_trial.py working before you try making your flask app work. 

## What you'll add 

The user should be able to add dated memos, either from the same index page or from a separate page. 
Memos should be displayed in date order. 
The user should be able to delete memos. 

## Setting up

The most difficult, or at least frustrating, part is setting up the MongoDB database.  Use mongoctl on ix to create
your database.  On your own computer, 'mongod' is the program that starts the database process.  In either place, 
'mongo' is a shell that allows you to interact with the database through a sort of command line interface.  Javascript is 
the shell language of MongoDB. 

You will need to create an administrative user for your database, and a non-administrative user with readWrite access to a
'memos' database.  Note that MongoDB on ix is version 2.4, while your computer probably has version 3.x.  The procedures for
adding a user are somewhat different between versions. 

In Python, the pymongo API works with both versions of MongoDB, so it's only the initial setup where you have to be 
careful to use the right version-specific commands. 

