from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from src.database import db
from src.product.models import master_product
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.product.schema import ProductSchemaIn
from pyfa_converter import PyFaDepends
from uuid import UUID

router = APIRouter(
    tags=["product"],
    prefix="/product"
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/",response_class=HTMLResponse)
async def product_show_page(request: Request):
    query = master_product.select()
    result = await db.fetch_all(query)
    return templates.TemplateResponse("view_product/index.html",{"request":request,"result":result})

@router.get("/add",response_class=HTMLResponse)
async def product_add_page(request: Request):
    return templates.TemplateResponse("view_product/add.html",{"request":request})

@router.post("/add")
async def product_add(request: Request, user_data=PyFaDepends(model=ProductSchemaIn,_type=Form) ):
    query = master_product.insert().values(**user_data.dict())
    print(query)
    await db.execute(query)
    response = RedirectResponse(request.url_for("product_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.get("/edit/{id}",response_class=HTMLResponse)
async def product_edit_page(request: Request,id: UUID):
    query = master_product.select().where(master_product.c.id == id)
    result = await db.fetch_one(query)
    return templates.TemplateResponse("view_product/edit.html",{"request":request,"result":result})

@router.post("/edit/{id}")
async def product_edit(request: Request,id: UUID, user_data=PyFaDepends(model=ProductSchemaIn,_type=Form) ):
    query = master_product.update().where(master_product.c.id == id).values(**user_data.dict())
    await db.execute(query)
    response = RedirectResponse(request.url_for("product_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.post("/delete/{id}")
async def product_delete(request: Request,id: UUID):
    query = master_product.delete().where(master_product.c.id == id)
    await db.execute(query)
    response = RedirectResponse(request.url_for("product_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response
