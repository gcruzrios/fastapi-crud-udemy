from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
from user_jwt import createToken, validateToken
from bd.database import engine, Base
from fastapi.encoders import jsonable_encoder
from routes.movie import routerMovie
from routes.user import routerUser
import os
app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Api en primeros pasos",
    version="0.0.1",
)
Base.metadata.create_all(bind=engine)

app.include_router(routerMovie)
app.include_router(routerUser)

          #return auth

@app.get('/', tags=["Inicio"])
def read_root():
    return {'message':'Hello world'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port) 


