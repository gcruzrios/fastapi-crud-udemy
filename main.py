from fastapi import Depends, FastAPI,Body, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from user_jwt import createToken, validateToken
from bd.database import Session, engine, Base
from models.movie import Movie as ModelView
from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Api en primeros pasos",
    version="0.0.1",
)

class BearerJWT(HTTPBearer):
     async def __call__(self, request: Request):
          auth = await super().__call__(request)
          data = validateToken(auth.credentials)
          if data['email'] != 'gcruz@geotecnologias.com':
               raise HTTPException(status_code=403, detail='Bad Credentials')
          #return auth

Base.metadata.create_all(bind=engine)

class User(BaseModel):
     #username:str
     email: str
     password:str


class Movie(BaseModel):
     id: Optional[int] = None
     title:str 
     overview: str 
     year:int 
     rating: float
     categoria:str
movies = []

@app.get('/', tags=["Inicio"])
def read_root():
    return {'message':'Hello world'}

@app.post('/login', tags=["Auth"])
def login(user:User):
     if user.email == 'gcruz@geotecnologias.com' and user.password =='123456':
         token: str = createToken(user.dict())
         print(token)
     return token

@app.get('/api/movies',tags=["Movies"])
def get_movies():
    db = Session()
    data = db.query(ModelView).all()
    return JSONResponse(content=jsonable_encoder(data))

@app.get('/api/movies/{id}', tags=['Movies'])
def get_movie(id: str):
    
    db = Session()
    data = db.query(ModelView).filter(ModelView.id==id).first()

    if not data:
         return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    # for item in movies:
    #     if item["imdbID"] == id:
    #         return item
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@app.get('/api/movies/',tags=["Movies"])
def get_movies_category(categoria: str):
    db = Session()
    data = db.query(ModelView).filter(ModelView.categoria==categoria).all()
    return JSONResponse(content=jsonable_encoder(data))




@app.post('/api/movies', tags=["Movies"], dependencies=[Depends(BearerJWT())])
def create_movie(movie:Movie):
    db = Session()
    newMovie = ModelView(**movie.dict())
    db.add(newMovie)
    db.commit()
    #movies.append(movie)
    return JSONResponse(content={'message': 'Se ha ingresado una nueva pelicula'})

@app.put('/api/movies/{id}', tags=["Movies"] )
def update_movie(id: str, movie: Movie):
    db = Session()
    data = db.query(ModelView).filter(ModelView.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.categoria = movie.categoria
    db.commit()
    return JSONResponse(content={'message': 'Se ha actualizado una pelicula'})  

@app.delete('/api/movies/{id}', tags=["Movies"] ) 
def delete_movie(id:str):
    #for item in movies:
    #    if item["imdbID"] == id:
    #       movies.remove(item)
    #       return movies
    db = Session()
    data = db.query(ModelView).filter(ModelView.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message': 'Se ha eliminado una pelicula'})  
