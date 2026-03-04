import subprocess
from pathlib import Path


class AudioCleaner:
    """
    Converts audio/video files into Whisper-friendly WAV format.
    """

    def __init__(self, output_dir="data/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert_to_wav(self, input_file):

        input_file = Path(input_file)

        output_file = self.output_dir / (input_file.stem + ".wav")

        command = [
            "ffmpeg",
            "-y",
            "-i", str(input_file),
            "-ac", "1",        # mono
            "-ar", "16000",    # 16kHz
            "-vn",
            str(output_file)
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return output_file