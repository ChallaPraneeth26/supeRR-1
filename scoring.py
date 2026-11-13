"""Scoring logic from Section 5 of the report. No Streamlit imports, so it can be tested on its own."""
from __future__ import annotations
import pandas as pd

# metric column -> (weight %, higher_is_better)
BAT_METRICS = {
    "p_sr": ("Pressure SR", 20, True),
    "p_dot": ("Dot-ball % (lower is better)", 15, False),
    "p_rec": ("Scores-after-dot %", 15, True),
    "p_bpd": ("Balls per dismissal", 15, True),
    "sr_retention": ("SR retention %", 10, True),
    "p_sr_hit": ("% innings at league SR", 10, True),
    "chase_win_pct": ("Tough-chase team win %", 10, True),
    "pct20": ("% innings of 20+", 5, True),
}
BOWL_METRICS = {
    "p_rsae": ("Runs saved per over", 20, True),
    "p_wae": ("Wickets above expected", 15, True),
    "good_pct": ("% spells beating expected", 15, True),
    "p_dot": ("Dot-ball %", 10, True),
    "p_bnd": ("Boundary % conceded (lower is better)", 10, False),
    "p_err": ("Wides + no-balls per over (lower is better)", 10, False),
    "win_pct": ("Team win % in spells", 10, True),
    "bad_pct": ("% disaster spells (lower is better)", 5, False),
    "res": ("Resilience vs own normal", 5, True),
}


def score(df: pd.DataFrame, metrics: dict, weights: dict | None = None) -> pd.Series:
    """100 x sum(percentile x weight). Percentile 1.0 = best on that metric."""
    w = {k: (weights[k] if weights else v[1]) for k, v in metrics.items()}
    total = sum(w.values())
    out = pd.Series(0.0, index=df.index)
    for k, (_, _, higher) in metrics.items():
        out += (w[k] / total) * df[k].rank(pct=True, ascending=higher)
    return 100 * out


def near_equal_order(df: pd.DataFrame, score_col: str = "new_score", tol: float = 2.0) -> pd.DataFrame:
    """Order by score, but treat scores within `tol` points (of the first score in a run) as level
    and put the player with more pressure balls first."""
    d = df.sort_values(score_col, ascending=False).reset_index(drop=True)
    order, i = [], 0
    while i < len(d):
        j = i
        while j + 1 < len(d) and d.loc[i, score_col] - d.loc[j + 1, score_col] <= tol:
            j += 1
        order += d.iloc[i : j + 1].sort_values("p_balls", ascending=False).index.tolist()
        i = j + 1
    return d.loc[order].reset_index(drop=True)


def pressure_flags(innings, legal_before, runs_so_far, wickets_lost, target, wickets_last12):
    """Section 3 rules for one delivery. Returns (batting_pressure, bowling_pressure, required_rate)."""
    over = legal_before // 6 + 1
    rrr = None
    need = 0
    if innings == 2:
        need = target - runs_so_far
        balls_left = max(120 - legal_before, 1)
        rrr = need / (balls_left / 6)
    hard_chase = innings == 2 and legal_before >= 12 and rrr is not None and rrr >= 9 and need > 0
    collapse = wickets_last12 >= 2
    death = over >= 17
    close_chase = (
        innings == 2 and legal_before >= 60 and rrr is not None and 7.5 <= rrr <= 14 and wickets_lost <= 6 and need > 0
    )
    return (hard_chase or collapse), (death or close_chase), rrr
