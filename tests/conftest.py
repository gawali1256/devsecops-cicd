import os
import sys
from pathlib import Path

TEST_DB_PATH = Path("./test_app.db")
if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB_PATH.resolve()}")
