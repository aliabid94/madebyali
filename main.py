from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fishwish import router as fishwish_router
from transformers import router as transformers_router
from slumberparty import router as slumberparty_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(fishwish_router)
app.include_router(transformers_router)
app.include_router(slumberparty_router)

@app.get("/")
async def home():
    return FileResponse("pages/index.html")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)