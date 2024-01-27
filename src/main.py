import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import RedirectResponse
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from src.config import WEB_PORT
from fastapi.staticfiles import StaticFiles
from src.database import db
from fastapi.templating import Jinja2Templates
from src.user.routers import router as user_router
from src.product.routers import router as product_router
from src.interactions.routers import router as interactions_router
from src.purchase.routers import router as purchase_router
from src.recsys.routers import router as recsys_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.mount("/templates", StaticFiles(directory="src/templates"), name="templates")

templates = Jinja2Templates(directory="src/templates")

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()




app.include_router(user_router)
app.include_router(product_router)
app.include_router(interactions_router)
app.include_router(purchase_router)
app.include_router(recsys_router)

@app.get("/")
async def redirect():
    response = RedirectResponse(url='/user/')
    return response


if __name__ == "__main__":
    uvicorn.run("main:app",port=WEB_PORT,log_level="info",reload=True,host="0.0.0.0")

