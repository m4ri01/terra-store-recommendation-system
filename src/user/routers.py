from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from src.database import db
from src.user.models import master_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.user.schema import UserSchemaIn
from pyfa_converter import PyFaDepends
from uuid import UUID

router = APIRouter(
    tags=["user"],
    prefix="/user"
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/",response_class=HTMLResponse)
async def user_show_page(request: Request):
    query = master_user.select()
    result = await db.fetch_all(query)
    return templates.TemplateResponse("view_user/index.html",{"request":request,"result":result})

@router.get("/add",response_class=HTMLResponse)
async def user_add_page(request: Request):
    return templates.TemplateResponse("view_user/add.html",{"request":request})

@router.post("/add")
async def user_add(request: Request, user_data=PyFaDepends(model=UserSchemaIn,_type=Form) ):
    query = master_user.insert().values(**user_data.dict())
    await db.execute(query)
    response = RedirectResponse(request.url_for("user_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response
    
@router.get("/edit/{id}",response_class=HTMLResponse)
async def user_edit_page(request: Request,id: UUID):
    query = master_user.select().where(master_user.c.id == id)
    result = await db.fetch_one(query)
    return templates.TemplateResponse("view_user/edit.html",{"request":request,"result":result})

@router.post("/edit/{id}")
async def user_edit(request: Request,id: UUID, user_data=PyFaDepends(model=UserSchemaIn,_type=Form) ):
    query = master_user.update().where(master_user.c.id == id).values(**user_data.dict())
    await db.execute(query)
    response = RedirectResponse(request.url_for("user_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.post("/delete/{id}")
async def user_delete(request: Request,id: UUID):
    query = master_user.delete().where(master_user.c.id == id)
    await db.execute(query)
    response = RedirectResponse(request.url_for("user_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response