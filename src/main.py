from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from src.api import transcribe, meeting
from src.model.load_model import ModelLoader


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading AI models...")
    app.state.model_loader = ModelLoader(
        device="cpu", batch_size=16, compute_type="int8"
    )
    print("Models loaded.")
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)

BLOCKED_KEYWORDS = ["wget", "chmod", "rm", ";", "curl", "tftp", "ftpget"]


@app.middleware("http")
async def block_malicious_requests(request: Request, call_next):
    try:
        raw_url = str(request.url)
        if any(
            keyword in raw_url.lower()
            for keyword in ["wget", "curl", "sh ", "rm ", "chmod"]
        ):
            return JSONResponse(
                status_code=403,
                content={"detail": "Blocked request due to potential security risk."},
            )
        response = await call_next(request)
        return response
    except Exception:
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error."}
        )


app.include_router(transcribe.router)
app.include_router(meeting.router)
