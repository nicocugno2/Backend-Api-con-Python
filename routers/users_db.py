from fastapi import APIRouter, HTTPException, status
from db.models.users import User
from db.schemas.user import *
from db.client import db_client
from bson import ObjectId


# Para iniciar base de datos local "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath="c:\data\db"


router = APIRouter(prefix="/userdb",
                tags=["userdb"],
                responses={404: {"message": "No se ha encontrado"}})


def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Error":"No se ha encontrado el usuario---"}





@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())



@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Query
@router.get("/")
async def user(id: str):
    return search_user(("_id", ObjectId(id)))

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    if type(search_user("mail", user.mail)) == User:
        raise HTTPException(
            status_code=204, detail="El usuario ya existe")
        

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return{"error": "No se ha actualizado el usuario."}

    return search_user("_id", ObjectId(user.id))



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha eliminado el usuario"}

    
        
        
