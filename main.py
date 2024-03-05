from fastapi import FastAPI
from coupons import coupons_router  # Importing from the correct module
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.include_router(coupons_router)

@app.get("/")
async def view_index():
    return FileResponse("./static/index.html")

app.mount("/", StaticFiles(directory="static"), name="static")
