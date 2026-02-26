from src.services.transcription_service import TranscriptionService
from src.services.diarization_service import DiarizationService
from src.services.alignment_service import AlignmentService
from src.model.load_model import ModelLoader
import whisperx


class MeetingPipeline:
    def __init__(self, model_loader: ModelLoader):
        self.model_loader = model_loader
        self.transcription_service = TranscriptionService(model_loader)
        self.diarization_service = DiarizationService(model_loader)

    def process_meeting(self, audio_path):
        audio = whisperx.load_audio(audio_path)
        # Step 1: Transcribe the audio
        result_transcribe = self.transcription_service.transcribe(audio)
        # Step 2: Align the transcription
        result_align = AlignmentService(self.model_loader).align(
            audio, result_transcribe
        )
        # Step 3: Diarize the audio
        result_diarization = self.diarization_service.diarize(audio, result_align)
        cleaned = []
        for seg in result_diarization.get("segments", []):
            cleaned.append(
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip(),
                    "speaker": seg.get("speaker"),
                }
            )

        return cleaned
