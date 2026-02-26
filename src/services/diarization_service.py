from src.model.load_model import ModelLoader
import whisperx


class DiarizationService:
    def __init__(self, model_loader: ModelLoader):
        self.model_loader = model_loader

    def diarize(self, audio, result_align) -> str:
        pipeline = self.model_loader.get_diarization_pipeline()
        diarize_segments = pipeline(audio)
        result = whisperx.assign_word_speakers(diarize_segments, result_align)
        return result
