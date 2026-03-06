from pathlib import Path

# Model configuration
MODEL_SIZE = "tiny"   # dev machine
# MODEL_SIZE = "large-v2"  # desktop machine

# Folder structure
DATA_DIR = Path("data")

INPUT_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

# Logging
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "pipeline.log"