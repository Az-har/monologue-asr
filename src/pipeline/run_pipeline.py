import subprocess
import time
import httpx

from tqdm import tqdm

from src.preprocess.audio_cleaner import AudioCleaner
from src.asr.transcriber import WhisperTranscriber
from src.utils.writer import save_transcript
from src.utils.logger import setup_logger
from src.utils.text_cleaner import clean_transcript
from src.llm.cleaner import clean_with_llm
from src.config.settings import INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR, USE_LLM


# Global logger (IMPORTANT: only initialize once)
logger = setup_logger()


# ============================
# LLM CONTROL
# ============================

def start_llm():
    """Start Ollama container."""
    try:
        subprocess.run(
            ["docker", "compose", "up", "-d", "llm"],
            cwd="docker",
            check=True
        )
        logger.info("LLM container started")

    except Exception as e:
        logger.error(f"Failed to start LLM container: {str(e)}")


def wait_for_llm(timeout=60):
    """Wait until Ollama API is ready."""
    start = time.time()

    while time.time() - start < timeout:
        try:
            res = httpx.get("http://localhost:11434")
            if res.status_code == 200:
                logger.info("LLM is ready")
                return True
        except Exception:
            pass

        time.sleep(2)

    return False


def stop_llm():
    """Stop and remove Ollama container."""
    try:
        subprocess.run(
            ["docker", "compose", "stop", "llm"],
            cwd="docker",
            check=True
        )

        subprocess.run(
            ["docker", "compose", "rm", "-f", "llm"],
            cwd="docker",
            check=True
        )

        logger.info("LLM container stopped and removed")

    except Exception as e:
        logger.error(f"Error stopping LLM container: {str(e)}")


# ============================
# MAIN PIPELINE
# ============================

def run_pipeline():

    cleaner = AudioCleaner(PROCESSED_DIR)
    transcriber = WhisperTranscriber()

    files = list(INPUT_DIR.glob("*"))

    if not files:
        logger.info("No audio files found.")
        return

    # Start LLM if enabled
    if USE_LLM:
        start_llm()

        if not wait_for_llm():
            logger.error("LLM failed to start. Continuing without LLM.")
    
    try:
        for audio_file in tqdm(files, desc="Processing audio"):

            output_file = OUTPUT_DIR / (audio_file.stem + ".txt")

            if output_file.exists():
                logger.info(f"Skipping already processed file: {audio_file.name}")
                continue

            try:
                logger.info(f"Processing {audio_file.name}")

                # Step 1: Convert audio
                wav_file = cleaner.convert_to_wav(audio_file)
                logger.info(f"Converted to WAV: {wav_file}")

                # Step 2: Whisper transcription
                text = transcriber.transcribe(wav_file)

                # Step 3: Basic cleaning
                text = clean_transcript(text)

                # Step 4: LLM cleanup (optional)
                if USE_LLM:
                    text = clean_with_llm(text)

                # Step 5: Save output
                save_transcript(text, output_file)

                logger.info(f"Transcript saved: {output_file}")

            except Exception as e:
                logger.error(f"Failed processing {audio_file.name}: {str(e)}")

    finally:
        if USE_LLM:
            stop_llm()


# ============================
# ENTRY POINT
# ============================

if __name__ == "__main__":
    run_pipeline()