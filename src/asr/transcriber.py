from faster_whisper import WhisperModel
from pathlib import Path
from src.config.settings import MODEL_SIZE


class WhisperTranscriber:

    def __init__(self):

        self.model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_path):

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(audio_path)

        segments, info = self.model.transcribe(
            str(audio_path),
            task="translate",
            beam_size=3,
            vad_filter=True,
            condition_on_previous_text=False,
            temperature=0.0
        )

        paragraphs = []
        buffer = ""
        prev_end = 0

        for seg in segments:

            gap = seg.start - prev_end

            if gap > 1.5 and buffer:
                paragraphs.append(buffer.strip())
                buffer = ""

            timestamp = f"[{int(seg.start//60):02d}:{int(seg.start%60):02d}]"

            buffer += f"{timestamp} {seg.text.strip()} "

            prev_end = seg.end

        if buffer:
            paragraphs.append(buffer.strip())

        return "\n\n".join(paragraphs)