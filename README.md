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

## Frontend

- **couponfinder**:
  - views folder contains the index.html to view the webpage
  - logic folder has files that helps connect frontend to backend using CRUD operations

- **login**:
  - Only has the testing webpage

- **register**:
  - Only has the webpage with a form to fill out

- **secretmenu**:
  - WIP
  - Contains two folders: logic and views
  - Logic folder contains code to connect to the backend
  - Trying to figure out how to use Google Cloud Service for images, does not work for now.

- **users**:
  - Only has the testing webpage

## Backend

- **couponfinder**:
  - Contains pydantic models for coupons in models folder
  - Routes are the endpoint APIs for backend, using CRUD operations

- **gcs_imageuploading**:
  - Does not work; planned to use Google Cloud Services (GCS) to upload an image and post it with the recipes
  - Currently WIP

- **restaurants**:
  - Contains pydantic models for restaurants in models folder
  - Routes are the endpoint APIs for backend and use CRUD operations

- **secretmenu**:
  - WIP
  - Contains pydantic models for recipes in models folder
  - Routes create the endpoint APIs for backend and use CRUD operations
  - Trying to implement GCS with it

- **users**:
  - Only contains the UserModel used to create the pydantic models of the user


## Roadmap:
The document and outline can be found here for final project:
https://docs.google.com/document/d/1uGfQXSzGdjfWUUzGYpOBJLe7kYVDbonJf0ftApabEuU/edit?usp=sharing


