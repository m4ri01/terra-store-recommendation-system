from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from src.database import db
from src.user.models import master_user
from src.purchase.models import user_purchase
from src.product.models import master_product
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.recsys.schema import RecsysPredictIn
from pyfa_converter import PyFaDepends
from uuid import UUID
from sqlalchemy.sql import select
import surprise
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset
import pandas as pd
import numpy as np

router = APIRouter(
    tags=["recommender_system"],
    prefix="/recsys"
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/predict/{id}",response_class=HTMLResponse)
async def recsys_predict(request: Request,id: UUID):
    pred,algo = surprise.dump.load("src/static/assets/models/models.dump")
    query = master_product.select().with_only_columns([master_product.c.id])
    result = await db.fetch_all(query)
    
    product_id = [str(r['id']) for r in result]
    product_id = np.array(product_id)

    query = user_purchase.select().where(user_purchase.c.user_id==id)
    result = await db.fetch_all(query)
    product_purchased = [str(r['product_id']) for r in result]
    product_purchased = np.array(product_purchased)
    product_not_purchased = np.setdiff1d(product_id,product_purchased)
    test_set = [[id,product,0] for product in product_not_purchased]
    predictions = algo.test(test_set)
    pred_ratings = np.array([pred.est for pred in predictions])
    index_max = (-pred_ratings).argsort()[:10]
    product_result = []
    ratings = []
    for i in index_max:
        product_result.append(product_not_purchased[i])
        ratings.append(pred_ratings[i])
    query = master_product.select().where(master_product.c.id.in_(product_result))
    result = await db.fetch_all(query)
    modified_product_result = [None for _ in range(10)]
    product_result = np.array(product_result)
    for i,r in enumerate(result):
        product_dict = dict(r)
        product_id = product_dict['id']
        idx = np.argwhere(product_result==str(product_id))[0][0]
        product_dict['est_ratings'] = np.round(ratings[idx],2)
        modified_product_result[i] = product_dict
    query = master_user.select().where(master_user.c.id==id)
    user_result = await db.fetch_one(query)
    return templates.TemplateResponse("view_recsys/predict.html",{"request":request,"result":modified_product_result,"user_result":user_result})


@router.get("/train",response_class=HTMLResponse)
async def recsys_train(request:Request):
    reader = Reader()
    query = user_purchase.select()
    result = await db.fetch_all(query)
    df_result = []
    for r in result:
        df_result.append((r['user_id'],r['product_id'],r['ratings']))
    df = pd.DataFrame(df_result,columns=['user_id','product_id','ratings'])
    data = Dataset.load_from_df(df[['user_id','product_id','ratings']],reader)
    trainset, testset = train_test_split(data, test_size=.2)
    algo = SVD()
    predictions = algo.fit(trainset).test(testset)
    mae = accuracy.mae(predictions)
    rmse = accuracy.rmse(predictions)
    surprise.dump.dump("src/static/assets/models/models.dump", algo=algo)
    result = {"mae":mae,"rmse":rmse}
    return templates.TemplateResponse("view_recsys/train.html",{"request":request,"result":result})

