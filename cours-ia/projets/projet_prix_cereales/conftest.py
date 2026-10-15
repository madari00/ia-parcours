"""Rend le dossier du projet importable par pytest (from app.main import app)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
