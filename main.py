from fastapi import FastAPI, Body, Query, Path, Cookie, Header
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


# Cookies and Headers

@app.get("/items")
async def read_items(cookie_id: str | None = Cookie(None),
                    accept_encoding: str | None = Header(None),
                    sec_ch_ua: str | None = Header(None),
                    user_agent: str | None = Header(None),
                    token: list[str] | None = Header(None)):
        return {"cookie_id": cookie_id,
                "Accept-Encoding": accept_encoding,
                "sec-ch-ua": sec_ch_ua, 
                "User-Agent": user_agent,
                "Token-Values": token}