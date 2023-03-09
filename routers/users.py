from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

#Para iniciar el server: uvicorn users:app --reload
router = APIRouter()


# objeto User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Funcion que busca al usuario y lo retorna
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"No se ha encontrado el usuario---"}


# Lista de usuario
users_list = [User(id= 1, name="nico", surname="cugno", url="https://nico.dev", age=19),
            User(id= 2, name="jere", surname="fernancdez", url="https://gedge.dev", age=54),
            User(id= 3, name="francisco", surname="parmigiani", url="https://pancho.dev", age=19)]


@router.get("/users")
async def users():
    return users_list


# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Query
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)

@router.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
        
    else:
        users_list.append(user)
        return user


@router.put("/user/", status_code=201)
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user
    if not found:
        raise HTTPException(status_code=404, detail='No se ha actualizado/encontrado el usuario')
    
# Funcion para eliminar usuario

@router.delete("/user/{id}", status_code=200)
async def user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {'El usuario se ha eliminado correctamente'}
        
        
# {"id" : 1, "name": "nico", "surname": "cugno", 
# "mail": "nicocugno2@gmail.com", "age": 19}