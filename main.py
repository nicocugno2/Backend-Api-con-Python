from fastapi import FastAPI
from routers import users, products
from fastapi.staticfiles import StaticFiles



#Para iniciar el server: uvicorn main:app --reload

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(products.router)
app.mount("/static", StaticFiles(directory="statics"), name="static")

@app.get("/")
async def root():
        return "HI FastAPI!"

@app.get("/url")
async def mail():
        return {"mail":"nicocugno2@gmail.com"} 