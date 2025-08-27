import os
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils.formatter import (
    list_audios,
    find_latest_best_model,
    merge_and_split_metadata,
)


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


def test_merge_and_split_metadata(tmp_path):
    train_csv = tmp_path / "metadata_train.csv"
    eval_csv = tmp_path / "metadata_eval.csv"

    pd.DataFrame(
        [
            {"audio_file": "wavs/a.wav", "text": "a", "speaker_name": "spk"},
            {"audio_file": "wavs/b.wav", "text": "b", "speaker_name": "spk"},
        ]
    ).to_csv(train_csv, sep="|", index=False)
    eval_csv.touch()

    existing_train = pd.DataFrame(
        [{"audio_file": "wavs/c.wav", "text": "c", "speaker_name": "spk"}]
    )
    existing_eval = pd.DataFrame(
        [{"audio_file": "wavs/d.wav", "text": "d", "speaker_name": "spk"}]
    )

    merge_and_split_metadata(
        str(train_csv), str(eval_csv), existing_train, existing_eval, 0.5
    )

    final_train = pd.read_csv(train_csv, sep="|")
    final_eval = pd.read_csv(eval_csv, sep="|")

    assert "wavs/d.wav" in final_eval["audio_file"].tolist()
    assert set(final_train["audio_file"]).isdisjoint(
        set(final_eval["audio_file"])
    )
