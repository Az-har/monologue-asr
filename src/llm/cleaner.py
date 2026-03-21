import httpx
from src.config.settings import LLM_ENDPOINT, LLM_MODEL
from src.utils.logger import setup_logger

logger = setup_logger()


def clean_with_llm(text):
    """
    Clean transcript using local Ollama LLM.
    Falls back safely if anything fails.
    """

    prompt = f"""
You are a transcript cleaner.

STRICT RULES:
- Preserve ALL timestamps exactly as they appear ([MM:SS])
- Do NOT remove or modify timestamps
- Do NOT add new information
- Do NOT hallucinate or guess missing words
- Fix grammar and sentence flow
- Convert spoken language into clear written English
- Remove filler words ONLY if redundant
- Keep paragraph structure intact

Transcript:
{text}

Return ONLY the cleaned transcript.
"""

    try:
        payload = {
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }

        response = httpx.post(LLM_ENDPOINT, json=payload, timeout=60.0)
        response.raise_for_status()

        result = response.json()

        cleaned_text = result.get("response", "").strip()

        if not cleaned_text:
            raise ValueError("Empty LLM response")

        logger.info("LLM cleanup successful")

        return cleaned_text

    except Exception as e:
        logger.error(f"LLM cleanup failed: {str(e)}. Using original text.")
        return text