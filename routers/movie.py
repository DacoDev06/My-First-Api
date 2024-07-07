from fastapi import APIRouter , Depends, Query
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import  List
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie



movie_router = APIRouter()


# @app.get('/file-response',response_class=FileResponse)
# def get_file():
#     file_path : str = "C:/Users/User/Desktop/EYE.jpg"
#     return FileResponse(path=file_path,filename="EYE.jpg",media_type="JPG")


@movie_router.get('/movies',tags=["movies"], status_code=200, response_model=List[Movie], dependencies=[Depends(JWTBearer)])
async def get_movies():
    db = Session()
    result = MovieService(db).get_movies()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No hay registros"})
    
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}',tags=["movies"],response_model=Movie,status_code=200)
async def get_movie(id: int) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"No encontrado"})
    return JSONResponse(content=jsonable_encoder(result),status_code=200)

@movie_router.get('/movies/', tags=["movies"],status_code=200)
async def get_movie_by_category(category: str = Query(max_length=1000,min_length=5)):
    db = Session()
    result = MovieService(db).get_by_category(category)
    if not result:
        return JSONResponse(status_code=404,content={"message":"No se ha encontrado esa categoria"})

    # data = [movie for movie in movies if movie["category"]==category]
    return JSONResponse(status_code=200,content=jsonable_encoder(result))



@movie_router.post('/movies', tags = ["movies"],status_code=201,response_model=Movie)
async def create_movie(movie: Movie):
    db = Session()
    MovieService(db).create_movie(movie)
    # db.refresh(new_movie) #para que es?
    return JSONResponse(status_code=201,content={"message": "Se ha creado la pelicula"})

@movie_router.put("/movies/{id}",tags = ["movies"], response_model= dict,status_code=200)
async def modify_movie(id:int, movie: Movie):
    db = Session()
    MovieService(db).modify_movie(id, movie)
    
    
    # for item in movies:
    #     if item["id"] == id:
    #         item["name"] = movie.name
    #         item["rating"] = movie.rating
    #         item["category"] = movie.category
    #         return item
    return  JSONResponse(status_code=200,content={"message": "Se ha modificado la pelicula"})

@movie_router.delete("/movies/{id}", tags = ["movies"], response_model=dict, status_code=200)
async def delete_movie(id: int):
    db = Session()
    MovieService(db).delete_movie(id)
    # if not result:
    #     return JSONResponse(status_code=404,content={"message":"No se encontro pelicula con el id"})
    return JSONResponse(status_code=201,content={"message":f"Se ha eliminado la pelicula de id {id}"})

    # for movie in movies:
    #     if movie["id"] == id:
    #         movies.remove(movie)
    #         return  JSONResponse(status_code=200,content={"message": "Se ha eliminado la pelicula"})
    # return JSONResponse(status_code=400,content={"message":"[]"})