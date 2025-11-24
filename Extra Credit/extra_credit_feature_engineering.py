"""
Data loader로 로드한 t, d, r raw 데이터로 feature 추출
"""

import numpy as np

# 기본 param
DEFAULT_N = 100
DEFAULT_T = 5.0


def compute_basic_features(seq):
    """
    전체 구간 기반 feature
    :param seq: numpy array (Tx3), columns = t, d, s
    :return: features
    """
    t = seq[:, 0]
    d = seq[:, 1]
    s = seq[:, 2]

    # duration
    duration = t[-1] - t[0] if len(t) > 1 else 0.0

    # in/out 분리
    in_mask = (d < 0)
    out_mask = (d > 0)

    in_sizes = s[in_mask]
    out_sizes = s[out_mask]

    # ipt
    if len(t) > 1:
        ipt = np.diff(t)
    else:
        ipt = np.array([0.0])

    return {
        "all_total_packets": len(seq),
        "all_num_in": np.sum(in_mask),
        "all_num_out": np.sum(out_mask),
        "all_incoming_ratio": np.sum(in_mask) / len(seq) if len(seq) > 0 else 0.0,
        "all_duration": duration,
        "all_pkts_per_sec": len(seq) / duration if duration > 0 else 0.0,

        # IPT stats
        "all_ipt_mean": float(np.mean(ipt)),
        "all_ipt_std": float(np.std(ipt)),
        "all_ipt_max": float(np.max(ipt)),
        "all_ipt_q75": float(np.percentile(ipt, 75)),

        # Packet size stats
        "all_in_size_mean": float(np.mean(in_sizes)) if len(in_sizes) else 0.0,
        "all_in_size_std": float(np.std(in_sizes)) if len(in_sizes) else 0.0,
        "all_in_size_max": float(np.max(in_sizes)) if len(in_sizes) else 0.0,

        "all_out_size_mean": float(np.mean(out_sizes)) if len(out_sizes) else 0.0,
        "all_out_size_std": float(np.std(out_sizes)) if len(out_sizes) else 0.0,
        "all_out_size_max": float(np.max(out_sizes)) if len(out_sizes) else 0.0,
    }


def compute_burst_features(seq):
    """
    전체 burst feature
    """
    d = seq[:, 1]
    if len(d) < 2:
        return {
            "all_burst_count": 0,
            "all_burst_mean": 0.0,
            "all_burst_std": 0.0,
            "all_burst_max": 0,
        }

    bursts = []
    cur_len = 1

    for i in range(1, len(d)):
        if d[i] == d[i-1]:
            cur_len += 1
        else:
            bursts.append(cur_len)
            cur_len = 1
    bursts.append(cur_len)
    bursts = np.array(bursts)

    return {
        "all_burst_count": len(bursts),
        "all_burst_mean": float(np.mean(bursts)),
        "all_burst_std": float(np.std(bursts)),
        "all_burst_max": int(np.max(bursts)),
    }


def compute_firstK_features(seq, K):
    """
    처음 K개 packet 기반 feature (first50, firstN, first30 공통)
    """
    if len(seq) < K:
        sub = seq
    else:
        sub = seq[:K]

    t = sub[:, 0]
    d = sub[:, 1]
    s = sub[:, 2]

    in_mask = (d < 0)
    out_mask = (d > 0)

    # IPT
    if len(t) > 1:
        ipt = np.diff(t)
    else:
        ipt = np.array([0.0])

    # burst count
    burst_cnt = 0
    if len(d) > 1:
        for i in range(1, len(d)):
            if d[i] != d[i - 1]:
                burst_cnt += 1

    return {
        "in_ratio": np.sum(in_mask) / len(sub) if len(sub) else 0.0,
        "out_ratio": np.sum(out_mask) / len(sub) if len(sub) else 0.0,

        "ipt_mean": float(np.mean(ipt)),
        "ipt_std": float(np.std(ipt)),

        "in_size_mean": float(np.mean(s[in_mask])) if np.sum(in_mask) else 0.0,
        "in_size_std": float(np.std(s[in_mask])) if np.sum(in_mask) else 0.0,

        "out_size_mean": float(np.mean(s[out_mask])) if np.sum(out_mask) else 0.0,
        "out_size_std": float(np.std(s[out_mask])) if np.sum(out_mask) else 0.0,

        "burst_count": burst_cnt,
    }


def compute_firstT_features(seq, T):
    """
    처음 T초 동안 feature
    """
    t = seq[:, 0]
    end_time = t[0] + T
    sub = seq[t <= end_time]

    if len(sub) == 0:
        return {
            "firstT_packets": 0,
            "firstT_in_ratio": 0.0,
            "firstT_out_ratio": 0.0,
            "firstT_ipt_mean": 0.0,
            "firstT_ipt_std": 0.0,
        }

    return {
        "firstT_packets": len(sub),
        "firstT_in_ratio": np.sum(sub[:, 1] < 0) / len(sub),
        "firstT_out_ratio": np.sum(sub[:, 1] > 0) / len(sub),
        "firstT_ipt_mean": float(np.mean(np.diff(sub[:, 0]))) if len(sub) > 1 else 0.0,
        "firstT_ipt_std": float(np.std(np.diff(sub[:, 0]))) if len(sub) > 1 else 0.0,
    }


def compute_first_in_response(seq):
    """
    서버 첫 수신 패킷까지 latency 측정
    """
    t = seq[:, 0]
    d = seq[:, 1]

    idx = np.where(d < 0)[0]  # 첫 in packet index
    if len(idx) == 0:
        return {
            "firstin_time": 0.0,
            "firstin_pkts_before": len(seq),
        }

    first_idx = idx[0]
    return {
        "firstin_time": t[first_idx] - t[0],
        "firstin_pkts_before": first_idx,
    }


def compute_direction_timing_firstN(seq, N):
    """
    초반 N개에서 in/out IPT 별도로 계산
    """
    sub = seq[:N] if len(seq) >= N else seq
    t = sub[:, 0]
    d = sub[:, 1]

    in_times = t[d < 0]
    out_times = t[d > 0]

    if len(in_times) > 1:
        ipt_in = np.diff(in_times)
    else:
        ipt_in = np.array([0.0])

    if len(out_times) > 1:
        ipt_out = np.diff(out_times)
    else:
        ipt_out = np.array([0.0])

    return {
        "firstN_ipt_in_mean": float(np.mean(ipt_in)),
        "firstN_ipt_out_mean": float(np.mean(ipt_out)),
    }


def extract_all_features(seq, N=DEFAULT_N, T=DEFAULT_T):
    """
    최종 45개 feature 모두 생성
    """
    feats = {}
    feats.update(compute_basic_features(seq))
    feats.update(compute_burst_features(seq))

    f50 = compute_firstK_features(seq, 50)
    for k, v in f50.items():
        feats[f"first50_{k}"] = v

    fN = compute_firstK_features(seq, N)
    for k, v in fN.items():
        feats[f"firstN_{k}"] = v

    feats.update(compute_direction_timing_firstN(seq, N))

    feats.update(compute_firstT_features(seq, T))

    f30 = compute_firstK_features(seq, 30)
    feats["first30_in_ratio"] = f30["in_ratio"]
    feats["first30_out_ratio"] = f30["out_ratio"]

    feats.update(compute_first_in_response(seq))

    return feats
