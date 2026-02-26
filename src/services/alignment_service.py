from src.model.load_model import ModelLoader
import whisperx


class AlignmentService:
    def __init__(self, model_loader: ModelLoader):
        self.model_loader = model_loader

    def align(self, audio, result_transcribe) -> str:
        model_a, metadata = self.model_loader.load_align_model(
            language_code=result_transcribe["language"]
        )
        result = whisperx.align(
            result_transcribe["segments"],
            model_a,
            metadata,
            audio,
            self.model_loader.device,
            return_char_alignments=False,
        )
        return result
