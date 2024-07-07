from models.movie import Movie as MovieModel
from schemas.movie import Movie
from fastapi.responses import JSONResponse

class MovieService():
    def __init__(self,db):
        self.db = db
    
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self,id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result

    def get_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).first()
        return result

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def modify_movie(self,id, movie: Movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not result:
            return  JSONResponse(status_code=200,content={"message": "No se ha encontrado la pelicula"})
        if movie.id: 
            result.id = movie.id
        if movie.name:
            result.name = movie.name
        if movie.rating:
            result.rating = movie.rating
        if movie.category:
            result.category = movie.category
        
        self.db.commit()
        return 
        
    
    def delete_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return
    

            