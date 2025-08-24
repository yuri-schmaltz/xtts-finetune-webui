import os
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils.formatter import list_audios, find_latest_best_model


def test_list_audios(tmp_path):
    (tmp_path / "a.wav").write_bytes(b"data")
    (tmp_path / "b.mp3").write_bytes(b"data")
    (tmp_path / "c.txt").write_bytes(b"data")
    files = list(list_audios(str(tmp_path)))
    assert len(files) == 2
    assert any(f.endswith("a.wav") for f in files)
    assert any(f.endswith("b.mp3") for f in files)


def test_find_latest_best_model(tmp_path):
    d1 = tmp_path / "m1"
    d1.mkdir()
    f1 = d1 / "best_model.pth"
    f1.write_text("a")
    time.sleep(1)
    d2 = tmp_path / "m2"
    d2.mkdir()
    f2 = d2 / "best_model.pth"
    f2.write_text("b")
    result = find_latest_best_model(str(tmp_path))
    assert result == str(f2)
