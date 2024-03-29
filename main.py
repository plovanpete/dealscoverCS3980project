from fastapi import FastAPI
from coupons import coupons_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Form, HTTPException
from UserModel import User, registered_users, hash_password



app = FastAPI()

app.include_router(coupons_router)

@app.get("/")
async def view_index():
    return FileResponse("./FrontEnd/couponfinder/index.html")

# Secret Menu Page
@app.get("/dealscreetmenu/")
async def view_secrets():
    return FileResponse("./FrontEnd/secretmenu/index.html")

# User page 
@app.get("/users/")
async def view_secrets():
    return FileResponse("./FrontEnd/users/index.html")

from fastapi.responses import FileResponse


@app.get("/register")
async def get_register():
    return FileResponse("./FrontEnd/register/index.html")


@app.get("/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    if username in registered_users:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(password)
    registered_users[username] = User(username=username, email=email, hashed_password=hashed_password)
    
    # Redirect or respond as needed
    return {"message": "User registered successfully"}


app.mount("/", StaticFiles(directory="FrontEnd/couponfinder"), name="coupons")
app.mount("/dealscreetmenu/", StaticFiles(directory="FrontEnd/secretmenu"), name = "secret")
app.mount("/users/", StaticFiles(directory="FrontEnd/users"), name = "users")

@app.get("/login/")
async def view_login():
    return FileResponse("./FrontEnd/login/index.html")

app.mount("/", StaticFiles(directory="FrontEnd/couponfinder"), name="coupons")
app.mount("/dealscreetmenu/", StaticFiles(directory="FrontEnd/secretmenu"), name = "secret")
app.mount("/users/", StaticFiles(directory="FrontEnd/users"), name = "users")
app.mount("/login/", StaticFiles(directory="FrontEnd/login"), name = "login")
