from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/fishwish")
async def fishwish():
    return FileResponse("pages/fishwish.html")