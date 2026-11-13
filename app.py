import io
import json
from pathlib import Path

import pandas as pd
import streamlit as st

import content as C
from appdata import load_all
from scoring import BAT_METRICS, BOWL_METRICS, near_equal_order, pressure_flags, score

DATA = Path(__file__).parent / "data"
st.set_page_config(page_title="Players under pressure", page_icon="🏏", layout="wide")


@st.cache_data
def load():
    blob = load_all()
    csv = lambda name: pd.read_csv(io.StringIO(blob[name]))
    return csv("final_batters"), csv("final_bowlers"), csv("eligible_batters"), csv("eligible_bowlers"), json.loads(blob["league"]), json.loads(blob["sens"])


fb, fw, eb, ew, L, SENS = load()


# ------------------------------------------------------------------ helpers
def dash(x, fmt="{:.0f}"):
    return "-" if pd.isna(x) else fmt.format(x)


def split_cell(val, n, fmt="{:.0f}"):
    return "-" if pd.isna(val) else f"{fmt.format(val)} ({int(n)})"


def show_df(df):
    """Full-width table that works on both older and newer Streamlit versions."""
    try:
        st.dataframe(df, hide_index=True, width="stretch")
    except TypeError:
        st.dataframe(df, hide_index=True, use_container_width=True)


def table(rows, cols):
    show_df(pd.DataFrame(rows, columns=cols))


# -------------------------------------------------------------------- pages
def page_overview():
    st.title("🏏 Identifying the most reliable players under pressure")
    st.caption("SupeRR Selector Season 2, Round 1. IPL and T20I ball-by-ball records, 2022 to 2026.")
    a, b, c, d = st.columns(4)
    a.metric("Matches analysed", L["matches"], help=f"{L['ipl_matches']} IPL and {L['t20i_matches']} T20I")
    b.metric("Deliveries", f"{L['balls']:,}")
    c.metric("League pressure SR", L["bat_league_sr_press"], help=f"Overall league SR is {L['bat_league_sr']}")
    d.metric("League pressure economy", L["bowl_league_econ_press"], help=f"Overall league economy is {L['bowl_league_econ']}")
    st.subheader("Executive summary")
    st.write(C.SUMMARY_P1)
    st.write(C.SUMMARY_P2)
    st.subheader("Final top 10 batters and bowlers")
    n = pd.DataFrame(
        {
            "#": fb["rank"],
            "Top 10 batters": fb["player"],
            "Batter score": fb["score"].round(1),
            "Top 10 bowlers": fw["player"],
            "Bowler score": fw["score"].round(1),
        }
    )
    show_df(n)
    st.caption(
        "Rank is the final position in the list. Score is the weighted percentile score out of 100, so rank does not "
        "always follow score (see the near-equal rule and the Selection decisions page)."
    )
    st.subheader("Main findings")
    for f in C.MAIN_FINDINGS:
        st.markdown(f"- {f}")
    st.write(C.SUMMARY_P3)
    left, right = st.columns(2)
    with left:
        st.markdown("**Pressure vs normal strike rate**")
        st.bar_chart(fb.set_index("player")[["p_sr", "np_sr"]].rename(columns={"p_sr": "Pressure SR", "np_sr": "Normal SR"}))
    with right:
        st.markdown("**Pressure vs normal economy (lower is better)**")
        st.bar_chart(fw.set_index("player")[["econ", "np_econ"]].rename(columns={"econ": "Pressure economy", "np_econ": "Normal economy"}))


def page_data():
    st.title("Data and how pressure is defined")
    st.subheader("Analysis process")
    dot = ["digraph G { rankdir=LR; node [shape=box, style=rounded, fontname=Helvetica, fontsize=11, color=\"#1F4E78\"];"]
    for i, (t, s) in enumerate(C.FLOW):
        dot.append(f'n{i} [label="{t}\\n{s}"];')
        if i:
            dot.append(f"n{i-1} -> n{i};")
    dot.append("}")
    st.graphviz_chart("\n".join(dot))
    st.subheader("Data used and preparation")
    st.markdown(
        f"- **Ball-by-ball file:** about {L['balls']:,} deliveries from {L['matches']} matches ({L['ipl_matches']} IPL, {L['t20i_matches']} T20I), 2022 to November 2026. Super overs are excluded.\n"
        "- **Matches file:** result and winner, used for team win rates in pressure situations. 34 rain-affected matches (revised targets or overs) were removed because required run rates are not comparable.\n"
        "- **Competitions file:** separates IPL (T20) from T20I fixtures for the format-consistency checks. The team and playing-XI files were used for names only; every player in the ball-by-ball data played the match."
    )
    st.markdown("**Data-cleaning steps**")
    table(C.CLEANING, ["Step", "What was done", "Effect"])
    st.markdown("**Counting rules used throughout**")
    table(C.COUNTING, ["Item", "Rule"])

    st.subheader("How pressure is defined")
    st.write(C.BAT_PRESSURE_INTRO)
    t1, t2 = st.tabs(["Batting pressure", "Bowling pressure"])
    with t1:
        st.markdown("A ball faced is a batting pressure ball if **either** condition holds when the ball is bowled.")
        st.markdown("**Condition 1: hard chase.** All of the following apply:")
        for x in C.BAT_COND1:
            st.markdown(f"- {x}")
        st.write(C.BAT_COND1_NOTE)
        st.markdown("**Condition 2: batting collapse.** " + C.BAT_COND2)
        st.info(f"Together the two conditions cover {L['bat_press_share']}% of balls faced.")
    with t2:
        st.markdown("A delivery is a bowling pressure ball if **either** condition holds.")
        st.markdown("**Condition 1: death overs.** " + C.BOWL_COND1)
        st.markdown("**Condition 2: close chase.** All of the following apply:")
        for x in C.BOWL_COND2:
            st.markdown(f"- {x}")
        st.write(C.BOWL_NOTE)
        st.info(
            f"Together these cover {L['bowl_press_share']}% of deliveries. The league economy in these situations is "
            f"{L['bowl_league_econ_press']} runs per over, against {L['bowl_league_econ']} overall."
        )

    st.subheader("Try the pressure rules")
    st.caption("Enter a match situation to see whether the delivery counts as a pressure ball under the rules above.")
    c1, c2, c3 = st.columns(3)
    innings = c1.radio("Innings", [1, 2], horizontal=True)
    legal = c1.slider("Legal balls bowled so far", 0, 119, 60)
    runs = c2.number_input("Team runs so far", 0, 300, 80)
    wk = c2.number_input("Wickets lost", 0, 10, 3)
    last12 = c3.number_input("Wickets lost in the last 12 legal balls", 0, 10, 0)
    target = c3.number_input("Target (second innings only)", 1, 300, 170, disabled=(innings == 1))
    bat_p, bowl_p, rrr = pressure_flags(innings, legal, runs, wk, target if innings == 2 else None, last12)
    m1, m2, m3 = st.columns(3)
    m1.metric("Over", legal // 6 + 1)
    m2.metric("Required rate", "-" if rrr is None else f"{rrr:.2f}")
    m3.metric("Batting pressure ball", "Yes" if bat_p else "No")
    st.metric("Bowling pressure ball", "Yes" if bowl_p else "No")


def page_metrics():
    st.title("Metrics, formulas and scoring")
    st.subheader("Batting metrics")
    table(C.BAT_METRICS_TABLE, ["Metric", "Formula and denominator", "Why it matters"])
    for t, x in C.BAT_METRICS_NOTES:
        st.markdown(f"**{t}** {x}")
    st.subheader("Bowling metrics")
    table(C.BOWL_METRICS_TABLE, ["Metric", "Formula and denominator", "Why it matters"])
    st.markdown("**How expected runs and wickets are calculated.** " + C.EXPECTED_NOTE)
    st.latex(r"\text{Expected runs}=\sum E_{runs}(\text{innings},\text{over})\ \text{over the bowler's pressure deliveries}")
    st.latex(r"\text{Expected wickets}=\sum E_{wkts}(\text{innings},\text{over})\ \text{over the bowler's pressure deliveries}")

    st.subheader("Rating and scoring methodology")
    for p in C.SCORING_TEXT:
        st.write(p)
    st.latex(r"\text{Final score}=100\times\sum(\text{metric percentile}\times\text{metric weight})")
    left, right = st.columns(2)
    with left:
        st.markdown("**Batting weights**")
        table([(v[0], f"{v[1]}%") for v in BAT_METRICS.values()] + [("Total", "100%")], ["Batting metric", "Weight"])
    with right:
        st.markdown("**Bowling weights**")
        table([(v[0], f"{v[1]}%") for v in BOWL_METRICS.values()] + [("Total", "100%")], ["Bowling metric", "Weight"])
    st.write(C.WEIGHTS_NOTE)
    st.markdown("**Eligibility.** " + C.ELIGIBILITY)
    st.markdown("**Handling close scores.** " + C.CLOSE_SCORES)
    st.subheader("Keeping the comparison fair")
    for t, x in C.FAIR:
        st.markdown(f"- **{t}:** {x}")

    st.subheader("Re-weighting lab")
    st.caption(
        "Change the weights and see who would make the top 10. With the default weights this reproduces the published "
        "scores (exactly for batters, within 0.04 points for bowlers). The published lists also include the judgement "
        "decisions, so they can differ from a purely mechanical ranking."
    )
    kind = st.radio("Rank", ["Batters", "Bowlers"], horizontal=True, key="labkind")
    metrics, df, pub = (BAT_METRICS, eb, fb) if kind == "Batters" else (BOWL_METRICS, ew, fw)
    cols = st.columns(3)
    w = {}
    for i, (k, (label, default, _)) in enumerate(metrics.items()):
        w[k] = cols[i % 3].slider(label, 0, 40, default, key=f"w_{kind}_{k}")
    if sum(w.values()) == 0:
        st.warning("Set at least one weight above zero.")
        return
    use_rule = st.checkbox("Apply the 2-point near-equal rule (more pressure balls ranks first)", value=True)
    d = df.copy()
    d["new_score"] = score(d, metrics, w)
    d = near_equal_order(d) if use_rule else d.sort_values("new_score", ascending=False).reset_index(drop=True)
    pubrank = dict(zip(pub["player"], pub["rank"]))
    top = d.head(10).copy()
    out = pd.DataFrame(
        {
            "New rank": range(1, 11),
            "Player": top["player"].values,
            "New score": top["new_score"].round(1).values,
            "Pressure balls": top["p_balls"].astype(int).values,
            "Published rank": [pubrank.get(p, "-") for p in top["player"]],
        }
    )
    show_df(out)
    overlap = sum(p in pubrank for p in top["player"])
    st.metric("Names shared with the published top 10", f"{overlap} of 10")
    missing = [p for p in pub["player"] if p not in set(top["player"])]
    if missing:
        st.caption("Published players not in this top 10: " + ", ".join(missing))


def player_page(kind):
    bat = kind == "bat"
    df = fb if bat else fw
    N = C.BAT_NARR if bat else C.BOWL_NARR
    notice = C.BAT_NOTICE if bat else C.BOWL_NOTICE
    sec = "7" if bat else "8"
    st.title("Top 10 batters: results and analysis" if bat else "Top 10 bowlers: results and analysis")
    if bat:
        st.caption(f"League reference: pressure SR {L['bat_league_sr_press']}, overall SR {L['bat_league_sr']}. SR = strike rate; ret. = retention.")
        t1 = pd.DataFrame({"#": df["rank"], "Batter": df["player"], "Team (most frequent)": df["team"], "Press. balls": df["p_balls"],
                           "Press. inns": df["p_inns"], "Pressure SR": df["p_sr"].round(1), "Normal SR": df["np_sr"].round(1),
                           "SR ret. %": df["ret"].round(0).astype(int), "Dot %": df["dot"].round(1), "Rotation %": df["rot"].round(1)})
        t2 = pd.DataFrame({"#": df["rank"], "Batter": df["player"], "Scores after dot %": df["rec"].round(1), "Balls / dismissal": df["bpd"].round(1),
                           "% inns at league SR": df["hit"].round(1),
                           "Tough-chase team win % (n)": [f"{a:.1f} ({int(b)})" for a, b in zip(df["cwin"], df["cn"])],
                           "Score (0-100)": df["score"].round(1)})
        t3 = pd.DataFrame({"#": df["rank"], "Batter": df["player"],
                           "IPL": [split_cell(a, b) for a, b in zip(df["ipl"], df["ipl_n"])],
                           "T20I": [split_cell(a, b) for a, b in zip(df["t20i"], df["t20i_n"])],
                           "2022-24": [dash(x) for x in df["e"]],
                           "2025-26": [split_cell(a, b) for a, b in zip(df["l"], df["l_n"])],
                           "Overall": df["p_sr"].round(1)})
        cap3 = "A dash means fewer than 40 pressure balls in that split. Split values are rounded to the nearest whole number."
        chart = df.set_index("player")[["p_sr", "np_sr"]].rename(columns={"p_sr": "Pressure SR", "np_sr": "Normal SR"})
        chart_title = f"Pressure SR against normal SR for the top 10 batters (league pressure SR is {L['bat_league_sr_press']})"
    else:
        st.caption(f"League reference: pressure economy {L['bowl_league_econ_press']} runs per over, overall {L['bowl_league_econ']}.")
        t1 = pd.DataFrame({"#": df["rank"], "Bowler": df["player"], "Team (most frequent)": df["team"], "Press. balls": df["p_balls"],
                           "Spells": df["spells"], "Press. econ": df["econ"].round(2), "Normal econ": df["np_econ"].round(2),
                           "Press. wickets": df["wk"], "Runs saved / over": df["rsae"].round(2), "Dot %": df["dot"].round(1)})
        t2 = pd.DataFrame({"#": df["rank"], "Bowler": df["player"], "Boundary % conceded": df["bnd"].round(1),
                           "Wides + no-balls / over": df["err"].round(2), "% spells beating expected": df["good"].round(1),
                           "% disaster spells": df["bad"].round(1), "Team win % in spells": df["win"].round(1),
                           "Score (0-100)": df["score"].round(1)})
        t3 = pd.DataFrame({"#": df["rank"], "Bowler": df["player"],
                           "IPL": [split_cell(a, b, "{:.2f}") for a, b in zip(df["ipl"], df["ipl_n"])],
                           "T20I": [split_cell(a, b, "{:.2f}") for a, b in zip(df["t20i"], df["t20i_n"])],
                           "2022-24": [dash(x, "{:.2f}") for x in df["e"]],
                           "2025-26": [split_cell(a, b, "{:.2f}") for a, b in zip(df["l"], df["l_n"])],
                           "Overall": df["econ"].round(2)})
        cap3 = "A dash means fewer than 36 legal pressure balls in that split."
        chart = df.set_index("player")[["econ", "np_econ"]].rename(columns={"econ": "Pressure economy", "np_econ": "Normal economy"})
        chart_title = f"Pressure economy against normal economy for the top 10 bowlers (league pressure economy is {L['bowl_league_econ_press']}; lower is better)"

    st.markdown(f"**Table {sec}.1 Pressure volume, " + ("strike rate and shot profile**" if bat else "economy and wickets**"))
    show_df(t1)
    st.markdown("**What to notice.** " + notice[f"{sec}.1"])
    st.markdown(f"**Table {sec}.2 " + ("Consistency, result and final score**" if bat else "Control, consistency, result and final score**"))
    show_df(t2)
    st.markdown("**What to notice.** " + notice[f"{sec}.2"])
    st.markdown(f"**Table {sec}.3 Consistency across formats and periods (" + ("pressure SR" if bat else "pressure economy") + "; balls in brackets)**")
    show_df(t3)
    st.caption(cap3)
    st.markdown("**What to notice.** " + notice[f"{sec}.3"])
    st.markdown("**" + chart_title + "**")
    st.bar_chart(chart)

    st.subheader(f"{sec}.1 Why each {'batter' if bat else 'bowler'} is on the list and why this rank")
    names = [f"{int(r)}. {p}" for r, p in zip(df["rank"], df["player"])]
    pick = st.selectbox("Choose a player", names)
    row = df.iloc[names.index(pick)]
    st.markdown(f"### {row['player']}  (score {row['score']:.1f})")
    if bat:
        a, b, c, d = st.columns(4)
        a.metric("Pressure SR", f"{row['p_sr']:.1f}", f"{row['p_sr'] - row['np_sr']:+.1f} vs normal")
        b.metric("Dot %", f"{row['dot']:.1f}")
        c.metric("Balls / dismissal", f"{row['bpd']:.1f}")
        d.metric("Pressure balls", int(row["p_balls"]))
    else:
        a, b, c, d = st.columns(4)
        a.metric("Pressure economy", f"{row['econ']:.2f}", f"{row['econ'] - row['np_econ']:+.2f} vs normal", delta_color="inverse")
        b.metric("Runs saved / over", f"{row['rsae']:.2f}")
        c.metric("Pressure wickets", int(row["wk"]))
        d.metric("Pressure balls", int(row["p_balls"]))
    st.write(N[row["player"]])
    with st.expander("Show all ten write-ups"):
        for r, p in zip(df["rank"], df["player"]):
            st.markdown(f"**{int(r)}. {p}.** {N[p]}")


def page_decisions():
    st.title("Selection decisions and exclusions")
    st.write(C.DECISIONS_INTRO)
    st.markdown("**The four notable selection decisions**")
    table(C.DECISIONS_TABLE, ["Player", "Outcome", "Basis"])
    for title, paras in C.DECISIONS:
        st.subheader(title)
        for p in paras:
            st.write(p)
    st.subheader("Other exclusions")
    for t, x in C.OTHER_EXCLUSIONS:
        st.markdown(f"- **{t}:** {x}")


def page_reliability():
    st.title("Reliability checks and limitations")
    st.subheader("Stability checks")
    st.write(
        "To test whether the order depends on my chosen weights, all eligible players were re-scored under three "
        "alternative weightings. The table shows how many of the final ten remain in the top twelve."
    )
    rows = [(k, f"{v[0]} of 10", f"{v[1]} of 10", ", ".join(v[2] + v[3]) or "none") for k, v in SENS.items()]
    table(rows, ["Alternative weighting", "Batters kept", "Bowlers kept", "Dropped out of top 12"])
    st.write(C.STABILITY_NOTE)
    st.subheader("Limitations and how they affect the results")
    for t, x in C.LIMITATIONS:
        st.markdown(f"- **{t}** {x}")
    st.subheader("Steps to reproduce the analysis")
    for i, (t, x) in enumerate(C.REPRO, 1):
        st.markdown(f"{i}. **{t}** {x}")
    st.subheader("Conclusion")
    st.write(C.CONCLUSION)


def page_explore():
    st.title("Explore all eligible players")
    kind = st.radio("Players", ["Batters", "Bowlers"], horizontal=True)
    bat = kind == "Batters"
    d = (eb if bat else ew).copy()
    d["group"] = d["in_final"].map({True: "Top 10", False: "Other"})
    lo, hi = int(d.p_balls.min()), int(d.p_balls.max())
    mn = st.slider("Minimum pressure balls", lo, hi, lo, step=10)
    d = d[d.p_balls >= mn]
    q = st.text_input("Search by name")
    if q:
        d = d[d.player.str.contains(q, case=False, na=False)]
    if bat:
        keys = {"Score": "score", "Pressure SR": "p_sr", "Dot %": "p_dot", "Rotation %": "p_rot", "Scores after dot %": "p_rec", "Balls / dismissal": "p_bpd", "Pressure balls": "p_balls"}
        low_better = {"p_dot"}
        x, y = "p_dot", "p_sr"
        note = "Each dot is a batter. Top left (low dot %, high pressure SR) is best."
    else:
        keys = {"Score": "score", "Pressure economy": "p_econ", "Runs saved / over": "p_rsae", "Pressure wickets": "p_wk", "Dot %": "p_dot", "% spells beating expected": "good_pct", "Pressure balls": "p_balls"}
        low_better = {"p_econ"}
        x, y = "p_econ", "p_dot"
        note = "Each dot is a bowler. Bottom right is not what you want: look for low economy (left) and high dot % (top)."
    label = st.selectbox("Sort by", list(keys))
    col = keys[label]
    d = d.sort_values(col, ascending=(col in low_better))
    st.caption("Lower is better for " + label + "." if col in low_better else "Higher is better for " + label + ".")
    show_df(d.drop(columns=["group"]))
    if len(d):
        st.scatter_chart(d, x=x, y=y, size="p_balls", color="group")
        st.caption(note + " Colour marks the published top 10.")


def page_downloads():
    st.title("Downloads")
    st.write("The full report, with every formula, table and the reasoning behind each rank, plus the data behind this dashboard.")
    pdf = DATA / "SupeRR_Selector_Season_2_Round_1_Report.pdf"
    if pdf.exists():
        st.download_button("Download the report (PDF)", pdf.read_bytes(), pdf.name, "application/pdf")
    else:
        st.caption("The report PDF is not included in this deployment. Add it to a data folder next to app.py to show a download button here.")
    st.download_button("Final top 10 batters (CSV)", fb.drop(columns=["why_in", "why_rank"], errors="ignore").to_csv(index=False), "final_top10_batters.csv", "text/csv")
    st.download_button("Final top 10 bowlers (CSV)", fw.drop(columns=["why_in", "why_rank"], errors="ignore").to_csv(index=False), "final_top10_bowlers.csv", "text/csv")
    st.download_button("All eligible batters (CSV)", eb.to_csv(index=False), "eligible_batters.csv", "text/csv")
    st.download_button("All eligible bowlers (CSV)", ew.to_csv(index=False), "eligible_bowlers.csv", "text/csv")


PAGES = {
    "Overview": page_overview,
    "Data and pressure": page_data,
    "Metrics and scoring": page_metrics,
    "Top 10 batters": lambda: player_page("bat"),
    "Top 10 bowlers": lambda: player_page("bowl"),
    "Selection decisions": page_decisions,
    "Reliability and limits": page_reliability,
    "Explore players": page_explore,
    "Downloads": page_downloads,
}
st.sidebar.title("Players under pressure")
choice = st.sidebar.radio("Go to", list(PAGES))
st.sidebar.caption("SupeRR Selector Season 2, Round 1")
PAGES[choice]()
