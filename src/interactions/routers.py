from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from src.database import db
from src.interactions.models import user_interactions
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.interactions.schema import InteractionsSchemaIn
from src.user.models import master_user
from pyfa_converter import PyFaDepends
from uuid import UUID
from sqlalchemy.sql import select

router = APIRouter(
    tags=["interactions"],
    prefix="/interactions"
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/",response_class=HTMLResponse)
async def interactions_show_page(request: Request):
    query = select([user_interactions,master_user]).select_from(master_user.join(user_interactions, master_user.c.id == user_interactions.c.user_id))
    result = await db.fetch_all(query)
    return templates.TemplateResponse("view_interactions/index.html",{"request":request,"result":result})

@router.get("/add",response_class=HTMLResponse)
async def interactions_add_page(request: Request):
    query = master_user.select()
    result = await db.fetch_all(query)
    return templates.TemplateResponse("view_interactions/add.html",{"request":request,"result":result})

@router.post("/add")
async def interactions_add(request: Request, interactions_data=PyFaDepends(model=InteractionsSchemaIn,_type=Form) ):
    query = user_interactions.insert().values(**interactions_data.dict())
    await db.execute(query)
    response = RedirectResponse(request.url_for("interactions_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.get("/edit/{id}",response_class=HTMLResponse)
async def interactions_edit_page(request: Request,id: UUID):
    query = user_interactions.select().where(user_interactions.c.id == id)
    result = await db.fetch_one(query)
    query = master_user.select()
    user_result = await db.fetch_all(query)
    return templates.TemplateResponse("view_interactions/edit.html",{"request":request,"result":result,"user_result":user_result})

@router.post("/edit/{id}")
async def interactions_edit(request: Request,id: UUID, interactions_data=PyFaDepends(model=InteractionsSchemaIn,_type=Form) ):
    query = user_interactions.update().where(user_interactions.c.id == id).values(**interactions_data.dict())
    await db.execute(query)
    response = RedirectResponse(request.url_for("interactions_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.post("/delete/{id}")
async def interactions_delete(request: Request,id: UUID):
    query = user_interactions.delete().where(user_interactions.c.id == id)
    await db.execute(query)
    response = RedirectResponse(request.url_for("interactions_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response