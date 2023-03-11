from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()

# Const
ACCESS_TOKEN_DURATION = 1
ALGORITHM = "HS256"
SECRET = 'bed7bd913bc43e615279109e8a408211f20e4a13f6e22f39c8e0d9a2a8bff1da'


# Encryption
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

# user
class User(BaseModel):
    name: str
    username: str
    mail: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "nicocugno": {
    "name": "Nicolas Cugno",
    "username": "nicocugno",
    "mail": "nicocugno2@gmial.com",
    "disabled": False,
    "password": "$2a$12$cpQKKjkBXH3Qk8Lo8xjMhOb/zP3m7cTDiZF./u95GNZvfuMoxG/GO"
    },
    
    "nicocugno2": {
    "name": "Nicolas Cugno 2",
    "username": "nicocugno2",
    "mail": "nicocugno22@gmial.com",
    "disabled": True,
    "password": "$2a$12$zOHIoaDnB/dn6Q1u2DCkuOBOSHYj2Tnr1MzG/WQZUP2CBG7G7bofS"
    }
}

# @ defs
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Criterios d dependencia

async def auth_user(token:str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Credenciales de autenticacion invalidas",
                    headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)
    


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario inactivo")
    
    return user



# @app
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña no es correcta")

    access_token = {"sub":user.username,
                    "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) }

    return{"access_token": jwt.encode(access_token,SECRET ,algorithm = ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user










