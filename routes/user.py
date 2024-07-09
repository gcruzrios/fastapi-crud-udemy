from fastapi import Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
from user_jwt import createToken, validateToken
from sqlalchemy.orm import Session
from bd.database import SessionLocal, engine, Base
from auth.auth_bearer import JWTBearer
from models.movie import Movie as ModelView
from models.user import User,TokenTable
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from utils import create_access_token,verify_password,get_hashed_password
import schemas


routerUser = APIRouter()

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



@routerUser.post("/register", tags=["Auth"])
def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password =get_hashed_password(user.password)
    print(encrypted_password)
    new_user = User(username=user.username, email=user.email, password=encrypted_password )
    print(new_user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}


# @routerUser.post('/login', tags=["Auth"])
# def login(user:User):
#      if user.email == 'gcruz@geotecnologias.com' and user.password =='123456':
#          token: str = createToken(user.dict())
#          print(token)
#      return token

@routerUser.post('/login' ,tags=["Auth"],response_model=schemas.TokenSchema)
def login(request: schemas.requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access=create_access_token(user.username)
   
    token_db = TokenTable(user_id=user.id,  access_token=access,  status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access
    }


@routerUser.get('/getusers', tags=["Auth"],dependencies=[Depends(JWTBearer())])
#@routerUser.get('/getusers', tags=["Auth"])
def getusers(session: Session = Depends(get_session)):
#def getusers(session: Session = Depends(get_session)):
    user = session.query(User).all()
    return user
