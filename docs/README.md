# Janet Twin Documentation

Welcome to the official documentation for **Janet Twin**, a PyQt-based conversational GPT client.

---

## Quickstart

Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/MrFrey75/Janet.Twin.git
cd Janet.Twin
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m janet_twin
```

---

## Architecture Overview

- **Frontend:** PyQt6 GUI  
- **Core Engine:** GPT API client  
- **Plugin System:** Python modules under `src/janet_twin/plugins/`  
- **Persistence:** SQLite database (`data/dev.db`), can be reset with:

```bash
./scripts/dev.sh reset-db
```

---

## Data Model

- **User:** Stores session and conversation history  
- **Message:** Tracks role (`user` / `assistant`) and content  
- **Plugin:** Defines plugin name, version, and contract  

---

## Plugin API

Plugins are Python modules that must implement:

```python
def run(input: str) -> str:
    ...
```

- Declare plugins in `plugins.json`  
- Return plain text or structured JSON  
- Automatically discovered by the core engine  

---

## Development

- See `scripts/dev.sh` for common tasks:
  - `./scripts/dev.sh install` → install dependencies
  - `./scripts/dev.sh reset-db` → reset dev database
  - `./scripts/dev.sh run` → start the app

- **Testing & linting:** run `pytest` for tests, `flake8`, `black --check`, and `mypy` for style and type checks.  

---

## Contribution

See `CONTRIBUTING.md` for guidelines on submitting PRs, coding standards, and testing requirements.  

---

## License

MIT License — see `LICENSE` for details.