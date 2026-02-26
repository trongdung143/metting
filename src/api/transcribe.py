from fastapi import APIRouter, Depends
from src.dependencies import get_model_loader
from src.services.meeting_pipeline import MeetingPipeline
from src.model.load_model import ModelLoader

router = APIRouter()


@router.post("/transcribe")
async def transcribe(
    audio_path: str, model_loader: ModelLoader = Depends(get_model_loader)
):
    service = MeetingPipeline(model_loader)
    result = service.process_meeting(audio_path)
    return result
