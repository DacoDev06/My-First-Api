from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import Session
from models.users import Users as UsersModel
from middlewares.jwt_bearer import JWTBearer
from utils.jwt_manager import create_token
from services.user import UserService
from schemas.user import User

user_router = APIRouter()
    
@user_router.get('/Users',tags=["auth"], dependencies=[Depends(JWTBearer)])
async def get_users():
    db = Session()
    result = UserService(db).get_users()
    if not result:
        return JSONResponse(status_code=404,content={"message":"No hay registros de Usuarios"})
    return JSONResponse(content=jsonable_encoder(result),status_code=200)
    


@user_router.post('/Users/register', tags=["auth"])
async def register(user: User):
    db = Session()
    user.token = create_token(user.model_dump())
    result = UserService(db).register_user(user)
    if result:
            return JSONResponse(content={"message":"El correo ya esta en uso!"}, status_code=403)
       
    return JSONResponse(status_code=201, content={"message":"Usuario creado con exito","token":user.token})
    

@user_router.post('/Users/login', tags=["auth"])
async def login(user: User):
    db = Session()
    result = db.query(UsersModel).filter(UsersModel.email == user.email and UsersModel.password==user.password).first()
    if not result:
        return JSONResponse(status_code=404,content={"message":"Usuario o contraseña incorrectos"})
    return JSONResponse(status_code=200,content={"message":"Inicio de sesion correcto","token":result.token})

@user_router.delete('/Users/delete', tags = ["auth"])
def delete_user(user: User):
    db = Session()
    result = UserService(db).delete_user(user)
    if type(result)==dict:
        return JSONResponse(status_code=404,content=result)
    return JSONResponse(status_code=201,content={"message":"Se ha eliminado el usurio"})
    