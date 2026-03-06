from tqdm import tqdm

from src.preprocess.audio_cleaner import AudioCleaner
from src.asr.transcriber import WhisperTranscriber
from src.utils.writer import save_transcript
from src.utils.logger import setup_logger

from src.config.settings import INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR


def run_pipeline():

    logger = setup_logger()

    cleaner = AudioCleaner(PROCESSED_DIR)
    transcriber = WhisperTranscriber()

    files = list(INPUT_DIR.glob("*"))

    if not files:
        logger.info("No audio files found.")
        return

    for audio_file in tqdm(files, desc="Processing audio"):

        output_file = OUTPUT_DIR / (audio_file.stem + ".txt")

        if output_file.exists():
            logger.info(f"Skipping already processed file: {audio_file.name}")
            continue

        try:

            logger.info(f"Processing {audio_file.name}")

            wav_file = cleaner.convert_to_wav(audio_file)

            logger.info(f"Converted to WAV: {wav_file}")

            text = transcriber.transcribe(wav_file)

            save_transcript(text, output_file)

            logger.info(f"Transcript saved: {output_file}")

        except Exception as e:

            logger.error(f"Failed processing {audio_file.name}: {str(e)}")


if __name__ == "__main__":
    run_pipeline()