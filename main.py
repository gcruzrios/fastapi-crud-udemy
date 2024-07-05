from fastapi import Depends, FastAPI,Body, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from user_jwt import createToken, validateToken


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



class User(BaseModel):
     #username:str
     email: str
     password:str


class Movie(BaseModel):
     id: Optional[str] = None
     Title:str 
     Genre: str 
     Year:int 
     Country: str

movies = [
  {
    "Title": "They Shall Not Grow Old",
    "Year": 2018,
    "Rated": "R",
    "Released": "01 Feb 2019",
    "Runtime": "99 min",
    "Genre": "Documentary, History, War",
    "Director": "Peter Jackson",
    "Writer": "Peter Jackson",
    "Actors": "Mark Kermode, Peter Jackson",
    "Plot": "A documentary about World War I with never-before-seen footage to commemorate the centennial of the end of the war.",
    "Language": "English",
    "Country": "UK, New Zealand",
    "Awards": "Nominated for 1 BAFTA Film Award. Another 4 wins & 10 nominations.",
    "Poster": "https://m.media-amazon.com/images/M/MV5BZWI3ZThmYzUtNDJhOC00ZWY4LThiNmMtZDgxNjE3Yzk4NDU1XkEyXkFqcGdeQXVyNTk5Nzg1NjQ@._V1_SX300.jpg",
    "Ratings": [
      {
        "Source": "Internet Movie Database",
        "Value": "8.3/10"
      },
      {
        "Source": "Rotten Tomatoes",
        "Value": "100%"
      },
      {
        "Source": "Metacritic",
        "Value": "91/100"
      }
    ],
    "Metascore": 91,
    "imdbRating": 8.3,
    "imdbVotes": "21,722",
    "imdbID": "tt7905466",
    "Type": "movie",
    "DVD": "N/A",
    "BoxOffice": "N/A",
    "Production": "Warner Bros. Pictures",
    "Response": "True"
  },
  {
    "Title": "Parasite",
    "Year": 2019,
    "Rated": "R",
    "Released": "08 Nov 2019",
    "Runtime": "132 min",
    "Genre": "Comedy, Drama, Thriller",
    "Director": "Bong Joon Ho",
    "Writer": "Bong Joon Ho (story), Bong Joon Ho (screenplay), Bong Joon Ho (story by), Jin Won Han (screenplay)",
    "Actors": "Kang-ho Song, Sun-kyun Lee, Yeo-jeong Jo, Woo-sik Choi",
    "Plot": "All unemployed, Ki-taek and his family take peculiar interest in the wealthy and glamorous Parks, as they ingratiate themselves into their lives and get entangled in an unexpected incident.",
    "Language": "Korean, English",
    "Country": "South Korea",
    "Awards": "Won 1 Golden Globe. Another 119 wins & 179 nominations.",
    "Poster": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg",
    "Ratings": [
      {
        "Source": "Internet Movie Database",
        "Value": "8.6/10"
      },
      {
        "Source": "Rotten Tomatoes",
        "Value": "99%"
      },
      {
        "Source": "Metacritic",
        "Value": "96/100"
      }
    ],
    "Metascore": 96,
    "imdbRating": 8.6,
    "imdbVotes": "128,604",
    "imdbID": "tt6751668",
    "Type": "movie",
    "DVD": "14 Jan 2020",
    "BoxOffice": "N/A",
    "Production": "NEON",
    "Response": "True"
  },
  
]

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
    return movies

@app.get('/api/movies/{id}', tags=['Movies'])
def get_movie(id: str):
    for item in movies:
        if item["imdbID"] == id:
            return item
    return []    

@app.get('/api/movies/',tags=["Movies"])
def get_movies_category(genre: str):
    return genre


@app.post('/api/movies', tags=["Movies"], dependencies=[Depends(BearerJWT())])
def create_movie(movie:Movie):
    movies.append(movie)
    return JSONResponse(content={'message': 'Se ha ingresado una nueva pelicula'})

@app.put('/api/movies/{id}', tags=["Movies"] )
def update_movie(id: str, movie: Movie):
    for item in movies:
            if item["imdbID"] == id:
                item['Title'] = movie.Title,
                item['Genre'] = movie.Genre,
                item['Year'] = Movie.Year,
                item['Country'] = Movie.Country
                
                return item
    return []   

@app.delete('/api/movies/{id}', tags=["Movies"] ) 
def delete_movie(id:str):
     for item in movies:
            if item["imdbID"] == id:
                movies.remove(item)
                return movies