import os
import wave
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime

router = APIRouter(prefix="/meeting")

BASE_STORAGE = "src/storage"


def get_meeting_folder(meeting_id: str) -> str:
    return os.path.join(BASE_STORAGE, meeting_id)


def ensure_storage():
    os.makedirs(BASE_STORAGE, exist_ok=True)


def get_next_chunk_index(folder: str) -> int:
    existing = [
        f for f in os.listdir(folder) if f.startswith("chunk_") and f.endswith(".wav")
    ]

    if not existing:
        return 1

    indexes = [int(f.replace("chunk_", "").replace(".wav", "")) for f in existing]
    return max(indexes) + 1


def merge_wav_files(folder: str, output_path: str):
    chunk_files = sorted(
        [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.startswith("chunk_") and f.endswith(".wav")
        ],
        key=lambda x: int(x.split("_")[-1].replace(".wav", "")),
    )

    if not chunk_files:
        raise Exception("No chunks found")

    with wave.open(chunk_files[0], "rb") as wf:
        params = wf.getparams()

    with wave.open(output_path, "wb") as output:
        output.setparams(params)

        for chunk in chunk_files:
            with wave.open(chunk, "rb") as wf:
                output.writeframes(wf.readframes(wf.getnframes()))


@router.post("/start")
async def start_meeting(meeting_id: str = Form(...)):
    ensure_storage()

    folder = get_meeting_folder(meeting_id)

    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.makedirs(folder)

    return {
        "status": "started",
        "meeting_id": meeting_id,
        "created_at": datetime.utcnow(),
    }


@router.post("/chunk")
async def upload_chunk(meeting_id: str = Form(...), file: UploadFile = File(...)):
    folder = get_meeting_folder(meeting_id)

    if not os.path.exists(folder):
        raise HTTPException(status_code=400, detail="Meeting not started")

    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files allowed")

    chunk_index = get_next_chunk_index(folder)
    file_path = os.path.join(folder, f"chunk_{chunk_index}.wav")

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    with open(file_path, "wb") as f:
        f.write(content)

    return {"status": "chunk_received", "chunk_index": chunk_index}


@router.post("/stop")
async def stop_meeting(meeting_id: str = Form(...)):
    folder = get_meeting_folder(meeting_id)

    if not os.path.exists(folder):
        raise HTTPException(status_code=400, detail="Meeting not found")

    output_path = os.path.join(folder, "final.wav")

    try:
        merge_wav_files(folder, output_path)

        return {
            "status": "stopped",
            "meeting_id": meeting_id,
            "final_file": output_path,
            "message": "Audio merged successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
