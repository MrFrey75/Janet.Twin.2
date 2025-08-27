# Janet Twin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-teal.svg)
[![Docs](https://img.shields.io/badge/docs-available-brightgreen.svg)](docs/)

---

A long-term project to build a useful, opinionated, **learning** personal assistant.  
The goal is a small, reliable core that can grow new skills without turning into a spaghetti monster.

---

## 📌 Why This Exists

### Goals
- Learn from user tasks and history to improve over time (safe, inspectable learning).
- Prioritize **local-first** execution; cloud integrations are optional.
- Modular skill expansion via Python plugins.
- Clear data ownership with simple export options (no lock-in).
- Minimal, developer-friendly workflow with low overhead.

### Non-Goals
- Being a universal, one-size-fits-all system.

---

## 🚀 Quick Start (Development)

### Requirements
- Python 3.10+
- SQLite (default dev DB)

### Setup & Run
```bash
# clone the repository
git clone https://github.com/MrFrey75/Janet.Twin.2.git
cd Janet.Twin

# create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements-dev.txt

# if needed
chmod +x ./scripts/dev.sh

# optional: reset local dev database
./scripts/dev.sh reset-db

# run the app
python -m janet_twin
```

### Testing & Linting
```bash
# run tests
pytest

# run style checks
black --check src tests
flake8 src tests
mypy src
```

---

## 📂 Project Structure

```
JanetTwin/
├─ data/           # local databases, seeds, etc.
├─ docs/           # documentation (see index above)
├─ src/            # application source (src/janet_twin/ package)
├─tests/           # test suite
├─ scripts/        # dev scripts (dev.sh)
├─ LICENSE
├─ pyproject.toml  # packaging and entrypoint
├─ requirements.txt       # runtime deps
├─ requirements-dev.txt   # dev deps
├─ .env            # not tracked in github
├─ secrets.txt     # not tracked in github
└─ README.md
```

---

## 📖 Additional Info

- **Docs:** `docs/README.md` is the main index.  
- **Database reset:** `./scripts/dev.sh reset-db`  
- **Entry point:** `python -m janet_twin` or `janet-twin` after `pip install -e .`  
- **Plugin API:** see `docs/README.md` section "Plugin API".
