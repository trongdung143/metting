import whisperx
import gc
from whisperx.diarize import DiarizationPipeline
from src.setup import HUGGINGFACE_HUB_TOKEN


class ModelLoader:
    def __init__(self, device, batch_size, compute_type):
        self.device = device
        self.batch_size = batch_size
        self.compute_type = compute_type
        self.transcribe_model = None
        self.diarization_pipeline = None

        self._load_transcribe_model()
        self._load_diarization_pipeline()

    def _load_transcribe_model(self):
        print("Loading model...")
        transcribe_model = whisperx.load_model(
            "large-v2", device=self.device, compute_type=self.compute_type
        )
        self.transcribe_model = transcribe_model
        print("Model loaded.")

    def _load_diarization_pipeline(self):
        print("Loading diarization pipeline...")
        diarization_pipeline = DiarizationPipeline(
            token=HUGGINGFACE_HUB_TOKEN, device=self.device
        )
        self.diarization_pipeline = diarization_pipeline
        print("Diarization pipeline loaded.")

    def load_align_model(self, language_code):
        print("Loading align model...")
        model_a, metadata = whisperx.load_align_model(
            language_code=language_code, device=self.device
        )
        print("Align model loaded.")
        return model_a, metadata

    def get_transcribe_model(self):
        if self.transcribe_model is None:
            self._load_transcribe_model()
        return self.transcribe_model

    def get_diarization_pipeline(self):
        if self.diarization_pipeline is None:
            self._load_diarization_pipeline()
        return self.diarization_pipeline


# device = "cuda"
# audio_file = "src/test/data/test.wav"
# batch_size = 16
# compute_type = "float16"
