#!/usr/bin/env bash
set -e

case "$1" in
  reset-db)
    echo "Resetting SQLite dev DB..."
    rm -f data/dev.db
    python -c "import sqlite3; sqlite3.connect('data/dev.db').close()"
    ;;
  install)
    echo "Installing dependencies..."
    pip install -r requirements-dev.txt
    ;;
  run)
    echo "Starting Janet Twin..."
    python -m janet_twin
    ;;
  *)
    echo "Usage: $0 {reset-db|install|run}"
    exit 1
    ;;
esac
