from fastapi import Request, HTTPException
from config.database import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.users import Users as UsersModel
from utils.jwt_manager import validate_token



class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        try: 
            auth = await super().__call__(request)
            data = validate_token(auth.credentials)
        except Exception as e:
            raise HTTPException(status_code=403,detail="Credenciales invalidas")
        db = Session()
        result = db.query(UsersModel).filter(UsersModel.email == data["email"] and UsersModel.password == data["password"]).first()
        if not result:
            raise HTTPException(status_code=403,detail="Credenciales invalidas")

