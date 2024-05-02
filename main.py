from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from BackEnd.couponfinder.routes.coupons import coupons_router
from BackEnd.restaurants.routes.restaurants import restaurants_router
from BackEnd.restaurants.model.RestaurantModel import RestaurantRequest
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Form, HTTPException, status
from BackEnd.users.models.UserModel import User, registered_users, hash_password
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow requests from specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

    
#Gets MongoDB client sync.
'''client = MongoClient('mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/')
db = client.dealscover'''

# MongoDB connection URI
MONGO_URI = "mongodb://localhost:27017"
# Connect to MongoDB
client = MongoClient(MONGO_URI)
# Database
db = client["dealscover"]
# Collection
restaurants_collection = db["restaurants"]

app.include_router(coupons_router)
app.include_router(restaurants_router)

@app.get("/")
async def view_index():
    return FileResponse("./FrontEnd/couponfinder/views/index.html")

# Mount the static directory for general static files
app.mount("/couponfinder", StaticFiles(directory="FrontEnd/couponfinder"), name="couponfinder")
app.mount("/restaurants", StaticFiles(directory="FrontEnd/restaurants"), name="restaurants")

# FastAPI route to handle POST requests with restaurant data
@app.post("/restaurants/")
def create_restaurant(restaurant: RestaurantRequest):
    # Access the restaurant data sent from the client
    name = restaurant.name
    address = restaurant.address
    zipcode = restaurant.zipcode

    # Perform actions with the restaurant data (e.g., saving to a database)
    # Here, we'll just return the received data as confirmation
    return {"name": name, "address": address, "zipcode": zipcode}

# Secret Menu Page
@app.get("/dealscreetmenu/")
async def view_secrets():
    return FileResponse("./FrontEnd/secretmenu/index.html")

coupon_collection = db.couponordeal
@app.post("/dealscreetmenu/")
async def view_secrets(description: str = Form(...), title: str = Form(...)):
    deal = coupon_collection.find()
    # Pass the fetched data to your HTML template
    return {
        "description": description,
        "title": title
    }



# User page 
@app.get("/users/")
async def view_secrets():
    return FileResponse("./FrontEnd/users/index.html")


@app.get("/register")
async def get_register():
    return FileResponse("./FrontEnd/register/index.html")


@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    if username in registered_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = hash_password(password)
    registered_users[username] = User(username=username, email=email, hashed_password=hashed_password)
    
    # Redirect to the couponfinder index.html after successful registration
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/login")
async def get_login():
    return FileResponse("./FrontEnd/login/index.html")


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username != "expected_username" or password != "expected_password":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Redirect with a query parameter indicating a successful login
    return RedirectResponse(url="/couponfinder/?login=success", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/test")
def test():
    return {"message": "Test route is working"}

app.mount("/static", StaticFiles(directory="FrontEnd/static"), name="static")

# app.mount("/", StaticFiles(directory="FrontEnd/couponfinder"), name="coupons")
# app.mount("/dealscreetmenu/", StaticFiles(directory="FrontEnd/secretmenu"), name = "secret")
# app.mount("/users/", StaticFiles(directory="FrontEnd/users"), name = "users")
# app.mount("/login/", StaticFiles(directory="FrontEnd/login"), name = "login")



users_collection = db.users
@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...), admin: str = Form(...)):
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
   
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_document = {
        "username": username,
        "password": hashed_password,
        "email": email,
        "admin": 'Y' if admin else 'N'
    }
    # Inserting the user document into the collection
    users_collection.insert_one(user_document)
   
    # Redirect to the login page after successful registration
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


