"""Commonly used filesystem paths."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CORPUS_DIR = BASE_DIR / "corpus"
STRUCTURED_DIR = CORPUS_DIR / "structured"
UNSTRUCTURED_DIRS = [
    CORPUS_DIR / "kb",
    CORPUS_DIR / "policies",
    CORPUS_DIR / "runbooks",
    CORPUS_DIR / "macros",
]


def iter_pdf_paths() -> list[Path]:
    """Return all PDF files under the corpus tree."""
    return sorted(CORPUS_DIR.glob("**/*.pdf"))
