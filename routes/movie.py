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

routerMovie = APIRouter()

class Movie(BaseModel):
     id: Optional[int] = None
     title:str 
     overview: str 
     year:int 
     rating: float
     categoria:str
movies = []

class BearerJWT(HTTPBearer):
     async def __call__(self, request: Request):
          auth = await super().__call__(request)
          data = validateToken(auth.credentials)
          if data['email'] != 'gcruz@geotecnologias.com':
               raise HTTPException(status_code=403, detail='Bad Credentials')

@routerMovie.get('/api/movies',tags=["Movies"])
def get_movies():
    db = Session()
    data = db.query(ModelView).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get('/api/movies/{id}', tags=['Movies'])
def get_movie(id: str):
    
    db = Session()
    data = db.query(ModelView).filter(ModelView.id==id).first()

    if not data:
         return JSONResponse(status_code=404, content={'message': 'Recurso no encontrado'})
    # for item in movies:
    #     if item["imdbID"] == id:
    #         return item
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.get('/api/movies/',tags=["Movies"])
def get_movies_category(categoria: str):
    db = Session()
    data = db.query(ModelView).filter(ModelView.categoria==categoria).all()
    return JSONResponse(content=jsonable_encoder(data))




@routerMovie.post('/api/movies', tags=["Movies"], dependencies=[Depends(BearerJWT())])
def create_movie(movie:Movie):
    db = Session()
    newMovie = ModelView(**movie.dict())
    db.add(newMovie)
    db.commit()
    #movies.append(movie)
    return JSONResponse(content={'message': 'Se ha ingresado una nueva pelicula'})

@routerMovie.put('/api/movies/{id}', tags=["Movies"] )
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

@routerMovie.delete('/api/movies/{id}', tags=["Movies"] ) 
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
