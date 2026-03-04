from src.asr.transcriber import WhisperTranscriber
from pathlib import Path


INPUT_DIR = Path("data/input")


def main():

    files = list(INPUT_DIR.glob("*"))

    if not files:
        print("No audio files found")
        return

    transcriber = WhisperTranscriber()

    for audio in files:

        print(f"\nProcessing: {audio.name}")

        text = transcriber.transcribe(audio)

        print("\nTranscript:\n")
        print(text)


if __name__ == "__main__":
    main()