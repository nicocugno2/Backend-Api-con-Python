from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
    "password": "123456"
    },
    
    "nicocugno2": {
    "name": "Nicolas Cugno 2",
    "username": "nicocugno2",
    "mail": "nicocugno22@gmial.com",
    "disabled": True,
    "password": "789456"
    }
}

# Devuelve el user sin mostrar la contraseña
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# Devuelve todo el user
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# Dependencia
async def current_user(token: str= Depends(oauth2)):
    user =  search_user(token)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticacion invalidas",
                            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario inactivo")
    
    return user



@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña no es correcta")

    return{"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user









