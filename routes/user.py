from fastapi import Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
from user_jwt import createToken, validateToken
from bd.database import Session
from models.movie import Movie as ModelView
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerUser = APIRouter()

class User(BaseModel):
     #username:str
     email: str
     password:str

@routerUser.post('/login', tags=["Auth"])
def login(user:User):
     if user.email == 'gcruz@geotecnologias.com' and user.password =='123456':
         token: str = createToken(user.dict())
         print(token)
     return token
