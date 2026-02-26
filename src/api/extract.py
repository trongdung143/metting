from fastapi import APIRouter

router = APIRouter()


@router.post("/extract")
async def extract(metting_id: str):
    return
