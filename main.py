from fastapi import FastAPI
from BackEnd.couponfinder.routes.coupons import coupons_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import Form, HTTPException, status, Cookie, Depends, Response, Request
from BackEnd.users.models.UserModel import User, registered_users, hash_password
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
import bcrypt

app = FastAPI()
client = MongoClient('mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/')
db = client.dealscover
app.include_router(coupons_router)

templates = Jinja2Templates(directory="path_to_your_templates")


def get_current_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    user = users_collection.find_one({"token": token})
    if not user:
        raise HTTPException(status_code=403, detail="Invalid authentication")
    return user

@app.get("/")
async def view_index():
    return FileResponse("./FrontEnd/couponfinder/index.html")

# Mount the static directory for general static files
app.mount("/couponfinder", StaticFiles(directory="FrontEnd/couponfinder"), name="couponfinder")

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

client = MongoClient('mongodb+srv://admin:dealscover1@dealscovercluster.bxpq8ph.mongodb.net/')
db = client.dealscover
users_collection = db.users
@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...), admin: str = Form(...)):
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    admin_status = 'Y' if admin == "yes" else 'N'  # Only mark as admin if explicitly chosen "yes"
    token = ''

    user_document = {
        "username": username,
        "password": hashed_password,
        "email": email,
        "admin": admin_status,
        "token": token
    }
    # Inserting the user document into the collection
    users_collection.insert_one(user_document)
    
    # Redirect to the login page after successful registration
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


# @app.get("/login")
# async def get_login():
#     return FileResponse("./FrontEnd/login/index.html")

@app.get("/")
async def view_index(request: Request, token: str = Cookie(None)):
    user = get_current_user(token) if token else None
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


users_collection = db.users
import secrets

@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        token = secrets.token_urlsafe(16)
        users_collection.update_one({"username": username}, {"$set": {"token": token}})
        response.set_cookie(key="token", value=token, httponly=True, samesite='Lax', secure=True)
        return RedirectResponse(url="/?login=success", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")


@app.get("/protected-route")
async def protected_route(user=Depends(get_current_user)):
    return {"message": f"Welcome {user['username']}!"}

@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


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


