"""
/mon, /unmon 폴더에서 파일명 parsing하여 파일 로드
"""

from pathlib import Path
import numpy as np
import pandas as pd

def load_cell_sequences(ts_dir: Path, is_mon: bool):
    ts_dir = Path(ts_dir)
    seqs, labels, names = [], [], []
    rows_all = []  # 모든 (t, d, s, label, file) row 저장
    names = []

    for cell_path in sorted(ts_dir.glob("*.cell")):
        stem = cell_path.stem

        # 불필요한 파일 제외
        if "join" in stem:  # join 사용 X
            continue

        if "split" not in stem: # split 아닌 파일 있으면 사용 X
            continue

        # label 부여
        if is_mon:  # mon 파일 형식: i-0_split_0.cell (i가 사이트 종류)
            site_prefix = stem.split('_')[0]  # "3-1"
            site_id = int(site_prefix.split('-')[0])
            label = site_id
        else:   # unmon 파일 형식: 0_split_0.cell (사이트 종류 X)
            label = 95

        # 데이터 body 읽어오기
        rows = []
        with cell_path.open("r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                t, d, s = parts[:3]

                # row-level label
                rows_all.append({
                    "t": float(t),
                    "d": int(d),
                    "s": float(s),
                    "label": label,
                    "file": stem
                })

    return pd.DataFrame(rows_all)

def load_one_cell(path):
    rows = []
    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            t, d, s = parts[:3]
            rows.append([float(t), int(d), float(s)])
    return np.array(rows, dtype=np.float32)
