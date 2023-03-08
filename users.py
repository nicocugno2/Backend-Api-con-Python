from fastapi import FastAPI
from pydantic import BaseModel


#Para iniciar el server: uvicorn users:app --reload
app = FastAPI()


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


@app.get("/users")
async def users():
    return users_list


# Path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Query
@app.get("/userquery/")
async def user(id: int):
    return search_user(id)

@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)


@app.put("/user/")
async def user(user: User):
    pass
