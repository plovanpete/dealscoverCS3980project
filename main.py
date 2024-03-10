from fastapi import FastAPI
from coupons import coupons_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.include_router(coupons_router)

@app.get("/")
async def view_index():
    return FileResponse("./FrontEnd/index.html")

app.mount("/", StaticFiles(directory="FrontEnd"), name="static")
