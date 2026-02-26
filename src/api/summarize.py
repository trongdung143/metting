from fastapi import APIRouter

router = APIRouter()


@router.post("/summarize")
async def summarize(metting_id: str):
    return
