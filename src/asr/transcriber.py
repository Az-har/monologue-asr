from faster_whisper import WhisperModel
from pathlib import Path


class WhisperTranscriber:
    """
    Simple wrapper around faster-whisper.
    """

    def __init__(self, model_size="large-v2"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe an audio file and return text.
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(f"{audio_path} not found")

        segments, info = self.model.transcribe(
            str(audio_path),
            beam_size=5,
            vad_filter=True
        )

        text = []

        for segment in segments:
            text.append(segment.text.strip())

        return " ".join(text)