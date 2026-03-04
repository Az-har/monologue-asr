from src.preprocess.audio_cleaner import AudioCleaner
from pathlib import Path


INPUT_DIR = Path("data/input")


def main():

    cleaner = AudioCleaner()

    files = list(INPUT_DIR.glob("*"))

    if not files:
        print("No files found")
        return

    for f in files:

        print("Cleaning:", f.name)

        wav = cleaner.convert_to_wav(f)

        print("Created:", wav)


if __name__ == "__main__":
    main()