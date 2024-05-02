from fastapi import FastAPI
from BackEnd.couponfinder.routes.coupons import coupons_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Form, HTTPException, status
from BackEnd.users.models.UserModel import User, registered_users, hash_password
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from fastapi.responses import JSONResponse, HTMLResponse
import bcrypt
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to MongoDB
client = MongoClient('mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/')
db = client.userDB
coupon_collection = db.couponordeal

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(coupons_router)

@app.get("/")
async def view_index():
    logging.info('Accessed index page')
    return FileResponse("./FrontEnd/couponfinder/index.html")

# Mount the static directory for general static files
app.mount("/couponfinder", StaticFiles(directory="FrontEnd/couponfinder"), name="couponfinder")

# Secret Menu Page
@app.get("/dealscreetmenu/")
async def view_secrets():
    logging.info('Accessed Secret menu page')
    return FileResponse("./FrontEnd/secretmenu/index.html")

@app.get("/dealscreetmenu/", response_class=JSONResponse)
async def view_secrets():
    logging.info('Accessed Secret menu page')
    deals = coupon_collection.find()
    deals_list = [{"title": deal.get("title", ""), "description": deal.get("description", "")} for deal in deals]
    return deals_list



# User page 
@app.get("/users/")
async def view_secrets():
    return FileResponse("./FrontEnd/users/index.html")


@app.get("/register")
async def get_register():
    return FileResponse("./FrontEnd/register/index.html")


@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    logging.info(f'Registered new user: {username}')
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
    logging.info(f'{username} Attempted login')
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


