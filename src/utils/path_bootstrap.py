import sys
from pathlib import Path


def ensure_src_on_path():
    """
    Ensure the project's src/ directory is on sys.path.
    Safe replacement for sys.path.append("..").
    """
    current = Path(__file__).resolve()

    for parent in current.parents:
        src_dir = parent / "src"
        if src_dir.exists():
            src_path = str(src_dir)
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            return

    raise RuntimeError("Could not locate src/ directory for imports")