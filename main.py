from fastapi import FastAPI
from coupons import coupons_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Form, HTTPException, status
from UserModel import User, registered_users, hash_password
from fastapi.responses import RedirectResponse


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
