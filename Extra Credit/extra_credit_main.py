from pathlib import Path
import pandas as pd
import numpy as np
from extra_credit_data_loader import load_one_cell
from extra_credit_feature_engineering import extract_all_features

BASE = Path(r"C:/Users/rdh08/Desktop/ML")
mon_dir = BASE / "mon"
unmon_dir = BASE / "unmon"

out_path = "all_features.csv"
first = True

print("[INFO] Extracting features from .cell files...")

folders = [(mon_dir, True), (unmon_dir, False)]

for ts_dir, is_mon in folders:

    cell_files = sorted(ts_dir.glob("*.cell"))
    total = len(cell_files)

    for idx, cell_path in enumerate(cell_files, 1):

        stem = cell_path.stem

        # skip 조건
        if "join" in stem:
            continue
        if "split" not in stem:
            continue

        # label 결정
        if is_mon:
            site_prefix = stem.split('_')[0]   # "3-1"
            site_id = int(site_prefix.split('-')[0])
            label = site_id
        else:
            label = 95

        # 파일 로드
        seq = load_one_cell(cell_path)

        # 빈 파일 스킵
        if seq is None or len(seq) == 0:
            print(f"[SKIP] Empty file: {stem}")
            continue

        seq = np.asarray(seq, dtype=float)
        if seq.ndim != 2 or seq.shape[1] != 3:
            print(f"[SKIP] Invalid shape in {stem}: {seq.shape}")
            continue

        # feature 추출
        feats = extract_all_features(seq)
        feats["label"] = label

        # CSV에 append
        pd.DataFrame([feats]).to_csv(
            out_path,
            mode="w" if first else "a",
            header=first,
            index=False
        )
        first = False

        print(f"[INFO] {stem} ({idx}/{total}) processed", end="\r")

print("\n[INFO] ALL DONE.")
