from models.users import Users as UsersModel
from schemas.user import User
from fastapi.responses import JSONResponse

class UserService():
    def __init__(self,db):
        self.db = db
        
    def get_users(self):
        result = self.db.query(UsersModel).all()
        return result
    
    
    def register_user(self, user: User):
        result = self.db.query(UsersModel).filter(UsersModel.email == user.email).first()
        if result:
           return result
        
        try:
            new_user = UsersModel(**user.model_dump())
        except Exception as e:
            return JSONResponse(content={"message":"No se ha podido crear el usuario"})

        self.db.add(new_user)
        self.db.commit()
        return 
    
    
    def delete_user(self, user: User):
        result = self.db.query(UsersModel).filter(UsersModel.email == user.email).first()
        if result:
            if not result.password == user.password:
                return {"message": "Contraseña incorrecta"}
            self.db.delete(result)
            self.db.commit()
            return 1
        return {"message":"User no encontrado o contraseña incorrecta"}
        
        
        
    