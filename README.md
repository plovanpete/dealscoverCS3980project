# Dealscover
![updatepic](https://github.com/plovanpete/dealscoverCS3980project/assets/145849883/0eca74f9-8f0d-450c-a51a-fde6e2597b9b)


A work in progress application where you find deals/coupons near you and post them!

## Instructions to start it and load it:
First, you'll want to create a virtual environment. Do so by using this command:
```
python -m venv venv
```
Do this command after you created your venv *(Only for Windows)*:
```
./venv/Scripts/activate  
```

Afterwards, install the requirements needed: 
```
pip install -r requirements.txt
```

You'll then have to connect to MongoDB. Start up MongoDB Compass and connect to the server. 
The URI to connect to MongoDB will be commented in the submission page, so that you can start up the database on your own.

Then, start up the actual backend server with this:
```
uvicorn main:app --reload
```

Connect to the localhost and feel free to take a look around afterwards! The login data for users is in the database if you want to check those out too.

## Descriptions of main:
**main.py**: The file that allows the server to run.

#### _Inside the Frontend Folder_:

It is compartmentalized into different folders for the type it needs.
couponfinder has the logics for restaurants as it is part of the main functionality to get coupons.

### _Inside the BackendFolder_:
It is compartmentalized into different folders for the type it needs.
restaurants has the backend logic for restaurants as it gets the things from the database.

## Roadmap:
The document and outline can be found here for final project:
https://docs.google.com/document/d/1uGfQXSzGdjfWUUzGYpOBJLe7kYVDbonJf0ftApabEuU/edit?usp=sharing
