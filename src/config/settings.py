from pathlib import Path

# Model configuration
MODEL_SIZE = "large-v2"   # dev machine
# MODEL_SIZE = "tiny"  # desktop machine

# Folder structure
DATA_DIR = Path("data")

INPUT_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

# Logging
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "pipeline.log"

# LLM Configuration
USE_LLM = True  # Toggle for enabling LLM cleanup
LLM_ENDPOINT = "http://localhost:11434/api/generate"  # Ollama API endpoint
LLM_MODEL = "llama3:8b"  # Model name
LLM_MAX_TOKENS = 4096
LLM_TEMPERATURE = 0.3

