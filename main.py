from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
        return "holaaaa!"

@app.get("/url")
async def url():
        return {"url_curso":"https://mouredev.com/python"} 