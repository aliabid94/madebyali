from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/transformers")
async def transformers():
    return FileResponse("pages/transformers.html")
