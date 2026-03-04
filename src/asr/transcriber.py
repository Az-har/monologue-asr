from faster_whisper import WhisperModel
from pathlib import Path
from src.config.settings import MODEL_SIZE

class WhisperTranscriber:

    def __init__(self, model_size=MODEL_SIZE):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_path: str):

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(audio_path)

        segments, info = self.model.transcribe(
            str(audio_path),
            beam_size=1,
            vad_filter=True
        )

        text = []

        for seg in segments:
            text.append(seg.text.strip())

        return " ".join(text)