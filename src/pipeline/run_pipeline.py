from pathlib import Path
from tqdm import tqdm

from src.preprocess.audio_cleaner import AudioCleaner
from src.asr.transcriber import WhisperTranscriber
from src.utils.writer import save_transcript


INPUT_DIR = Path("data/input")
PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/output")


def run_pipeline():

    cleaner = AudioCleaner(PROCESSED_DIR)
    transcriber = WhisperTranscriber()

    files = list(INPUT_DIR.glob("*"))

    if not files:
        print("No audio files found in data/input")
        return

    for audio_file in tqdm(files, desc="Processing audio"):

        output_file = OUTPUT_DIR / (audio_file.stem + ".txt")

        # Skip already processed files
        if output_file.exists():
            print("Skipping (already processed):", audio_file.name)
            continue

        print("\nProcessing:", audio_file.name)

        # Convert audio
        wav_file = cleaner.convert_to_wav(audio_file)

        print("Converted to:", wav_file.name)

        # Transcribe
        text = transcriber.transcribe(wav_file)

        # Save transcript
        save_transcript(text, output_file)

        print("Transcript saved:", output_file)


if __name__ == "__main__":
    run_pipeline()