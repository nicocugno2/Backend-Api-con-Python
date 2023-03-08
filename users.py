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
        return {"Error":"No se ha encontrado el usuario"}




users_list = [User(id= 1, name="nico", surname="cugno", url="https://nico.dev", age=19),
            User(id= 2, name="jere", surname="fernancdez", url="https://gedge.dev", age=54),
            User(id= 3, name="francisco", surname="parmigiani", url="https://pancho.dev", age=19)]

# Funcion Get normal para mostrar los usuarios
@app.get("/users")
async def users():
    return users_list


# Funcion Get con Path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Funcion Get Query  
@app.get("/userquery/")
async def user(id: int):
    return search_user(id)

# Funcion para agregar un usuario

@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)
        return user

# Funcion para una parte del usuario

@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {'error': 'No se ha actualizado el usuario'}
    else:
        return user
    
# Funcion para eliminar usuario

@app.delete("/user/{id}")
async def user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {'El usuario se ha eliminado correctamente'}
