# Dealscover
![updatepic](https://github.com/plovanpete/dealscoverCS3980project/assets/145849883/0eca74f9-8f0d-450c-a51a-fde6e2597b9b)

## Collaborators:
**Payton Lovan** - Mainly works on the main function of the app, integrating the Google Maps API with the restaurants and coupons of the app.

**Connor Stomp** - Mainly works on the Discreet Hidden Menu, the sub-domain of the app, allowing recipes that can be made from restaurants

**Henry Krain** - Mainly works on the authentication and login of the app.


A work in progress application where you find deals/coupons near you and post them!
The only thing that is functioning right now is the CouponFinder page. The rest are a Work in Progress! (WIP)

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
Also, if the website tends to not load, while you run the uvicorn, just edit any part of the backend code, save, and then undo what you changed.
This should fix the long loading freeze if it happens.

## Descriptions of main:
**main.py**: The file that allows the server to run and sets up static files so that we can import other modules or files from different compartments.

#### _Inside the Frontend Folder_:

It is compartmentalized into different folders for the files it needs
There is:
**couponfinder** - has the views folder which is just the index.html to see the webpage & logic folder which helps connect frontend to backend using CRUD operations.
**login** - As of now, only has the testing webpage.
**register** - Only has the webpage, and has a form to fill out!
**secretmenu** - WIP, has two folders, logic and views. Logic contains WIP code that is used to connect to the backend. (Trying to figure out how to use Google Cloud Service for images)
**users** - As of now, only has the testing webpage.

#### _Inside the BackendFolder_:
It is compartmentalized into different folders for the type it needs.
There is:
**couponfinder** - contains pydantic models for coupons in models folder; routes which is the endpoint APIs for backend, using the CRUD operations.
**gcs_imageuploading** - Does not work; was planning on using Google Cloud Services (GCS) to upload an image and then post it with the recipes. *(Currently WIP)*
**restaurants** - contains the pydantic models for restaurants in models folder; also contains routes, which is the endpoint APIs for backend and uses CRUD operations.
**secretmenu** - WIP, contains the pydantic models for recipes in models folder; also contains routes, which creates the endpoint APIs for backend and uses CRUD operations 
(Does not work; trying to implement GCS with it)
**users** - Only contains the UserModel; which is used to create the pydantic models of the user.

## Roadmap:
The document and outline can be found here for final project:
https://docs.google.com/document/d/1uGfQXSzGdjfWUUzGYpOBJLe7kYVDbonJf0ftApabEuU/edit?usp=sharing


