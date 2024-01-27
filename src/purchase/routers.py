from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from src.database import db
from src.purchase.models import user_purchase
from src.user.models import master_user
from src.product.models import master_product
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.purchase.schema import UserPurchaseSchemaIn
from pyfa_converter import PyFaDepends
from uuid import UUID
from sqlalchemy.sql import select

router = APIRouter(
    tags=["purchase"],
    prefix="/purchase"
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/",response_class=HTMLResponse)
async def purchase_show_page(request: Request):
    query = select([user_purchase.c.id,user_purchase.c.ratings,master_user.c.id,master_user.c.name,master_product.c.id,master_product.c.product_name]).select_from(master_user.join(user_purchase, master_user.c.id == user_purchase.c.user_id).join(master_product, master_product.c.id == user_purchase.c.product_id))
    result = await db.fetch_all(query)
    return templates.TemplateResponse("view_purchase/index.html",{"request":request,"result":result})

@router.get("/add",response_class=HTMLResponse)
async def purchase_add_page(request: Request):
    query = master_user.select()
    user_result = await db.fetch_all(query)
    query = master_product.select()
    product_result = await db.fetch_all(query)

    return templates.TemplateResponse("view_purchase/add.html",{"request":request,"user_result":user_result,"product_result":product_result})

@router.post("/add")
async def purchase_add(request: Request, purchase_data=PyFaDepends(model=UserPurchaseSchemaIn,_type=Form)):
    query = user_purchase.insert().values(**purchase_data.dict())
    await db.execute(query)
    response = RedirectResponse(request.url_for("purchase_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.get("/edit/{id}",response_class=HTMLResponse)
async def purchase_edit_page(request: Request, id:UUID):
    query = user_purchase.select().where(user_purchase.c.id==id)
    result = await db.fetch_one(query)
    query = master_user.select()
    user_result = await db.fetch_all(query)
    query = master_product.select()
    product_result = await db.fetch_all(query)
    return templates.TemplateResponse("view_purchase/edit.html",{"request":request,"result":result,"user_result":user_result,"product_result":product_result})

@router.post("/edit/{id}")
async def purchase_edit(request:Request,id:UUID,purchase_data=PyFaDepends(model=UserPurchaseSchemaIn,_type=Form)):
    query = user_purchase.update().where(user_purchase.c.id==id).values(**purchase_data.dict())
    await db.execute(query)
    response = RedirectResponse(request.url_for("purchase_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response

@router.post("/delete/{id}")
async def purchase_delete(request: Request, id: UUID):
    query = user_purchase.delete().where(user_purchase.c.id == id)
    await db.execute(query)
    response = RedirectResponse(request.url_for("purchase_show_page"))
    response.status_code = status.HTTP_303_SEE_OTHER
    return response
