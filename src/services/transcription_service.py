from src.model.load_model import ModelLoader


class TranscriptionService:
    def __init__(self, model_loader: ModelLoader):
        self.model_loader = model_loader

    def transcribe(self, audio) -> str:
        model = self.model_loader.get_transcribe_model()
        result = model.transcribe(audio, batch_size=self.model_loader.batch_size)
        return result
