# PROJECT UPDATES

---

## Initial State

- Base ASR pipeline implemented
- Dockerized execution
- Whisper + preprocessing + cleaning working

---

## [2026-03-21]

### Added
- src/llm/cleaner.py - LLM cleanup module for improving transcript grammar and readability

### Modified
- src/config/settings.py - Added LLM configuration settings (endpoint, model, toggle, max_tokens, temperature)
- src/pipeline/run_pipeline.py - Integrated LLM cleanup step after text cleaning, made optional via config flag

### Reason
- To enhance transcript quality by using local LLM for grammar and readability improvements while preserving timestamps and meaning

---

## [2026-03-21]

### Added
- docker/docker-compose.yml - Docker Compose configuration for ephemeral Ollama LLM service

### Modified
- src/pipeline/run_pipeline.py - Added LLM container lifecycle management (start/stop) using subprocess and docker compose
- src/llm/cleaner.py - Updated to use Ollama HTTP API instead of OpenAI-compatible endpoint
- src/config/settings.py - Updated LLM settings to use Ollama endpoint and model

### Reason
- To implement ephemeral LLM system that runs only during pipeline execution using Docker and Ollama

---

## [2026-03-22]

### Modified
- src/pipeline/run_pipeline.py - Changed LLM container stop command from 'docker compose down' to 'docker compose rm -f llm'

### Reason
- To specifically remove the LLM container forcefully instead of stopping all services