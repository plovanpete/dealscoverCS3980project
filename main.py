from fastapi import FastAPI
from coupons import coupons_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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


app.mount("/", StaticFiles(directory="FrontEnd/couponfinder"), name="coupons")
app.mount("/dealscreetmenu/", StaticFiles(directory="FrontEnd/secretmenu"), name = "secret")
app.mount("/users/", StaticFiles(directory="FrontEnd/users"), name = "users")
@app.get("/login/")
async def view_login():
    return FileResponse("./FrontEnd/users/index.html")

app.mount("/", StaticFiles(directory="FrontEnd/couponfinder"), name="coupons")
app.mount("/dealscreetmenu/", StaticFiles(directory="FrontEnd/secretmenu"), name = "secret")
app.mount("/users/", StaticFiles(directory="FrontEnd/users"), name = "users")
app.mount("/login/", StaticFiles(directory="FrontEnd/login"), name = "login")
