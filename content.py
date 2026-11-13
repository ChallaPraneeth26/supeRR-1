"""Text and small tables transcribed from the SupeRR Selector Season 2 Round 1 report."""

SUMMARY_P1 = (
    "This report identifies the ten batters and ten bowlers who were most reliable under pressure in IPL and T20I "
    "matches between 2022 and 2026. The data contains deliveries and results but no measure of how difficult each ball "
    "was, so pressure is defined from the match situation: required run rate, wickets lost and overs remaining. Each "
    "player is compared with the league norm for the same situation and with his own normal performance. Players are "
    "ranked on rates and percentages, and only players with a meaningful number of pressure balls are eligible."
)
SUMMARY_P2 = (
    "Scores are built from percentile ranks. Where two players' scores are within 2.0 points, the player with more "
    "pressure balls ranks higher."
)
MAIN_FINDINGS = [
    "All ten batters scored faster under pressure than in normal play (strike-rate retention of 102% to 118%). "
    "Abhishek Sharma has the highest pressure strike rate (191.0), followed by Jos Buttler (177.3) and Yashasvi Jaiswal (175.3).",
    "All ten bowlers have a pressure economy below the league pressure economy of 9.82. Only four of them (Narine, "
    "Theekshana, Ngidi and Malinga) were also better under pressure than in their own normal overs. Sunil Narine's "
    "pressure economy is 6.80, and Jasprit Bumrah saves the most runs per over (2.13).",
    "The shortlist is stable: at least 9 of 10 names in each list stay in the top twelve under every alternative weighting tested.",
]
SUMMARY_P3 = (
    "Four placements differ from a purely mechanical reading of the scores. Three of them (Reeza Hendricks, Mohammad "
    "Rizwan and Tim Southee) involve analyst judgement, and one (Taskin Ahmed and Eshan Malinga) follows the "
    "near-equal rule. The Selection decisions page sets out the evidence for each so that they can be challenged."
)

FLOW = [
    ("Raw data", "IPL + T20I ball-by-ball"),
    ("Data cleaning", "rain, super overs, extras rules"),
    ("Match situation", "RRR, wickets, overs left"),
    ("Pressure flag", "batting and bowling rules"),
    ("Metrics", "pressure vs normal, vs league norm"),
    ("Eligibility", "minimum balls, innings, spells"),
    ("Percentile scoring", "weighted score out of 100"),
    ("Reliability checks", "alt. weights, format, period"),
    ("Final top 10", "near-equal rule + selection decisions"),
]

CLEANING = [
    ("1. Join files", "Ball-by-ball records joined to the matches file (result, rain revisions) by match_id and to the competitions file (IPL or T20I) by comp_id.", "833 matches: 392 IPL and 441 T20I"),
    ("2. Remove super overs", "All super-over deliveries dropped before any calculation.", "Super overs excluded"),
    ("3. Remove rain-affected matches", "Matches with revised targets or overs dropped, because the required run rate is not comparable.", "34 matches removed"),
    ("4. Apply counting rules", "Runs, balls and wickets counted as in the counting rules table so that every metric uses the same definitions.", "Applied to all metrics"),
]
COUNTING = [
    ("Batter runs", "Runs scored off the bat only. Byes and leg-byes are not credited to the batter."),
    ("Ball faced", "Every delivery except a wide. A no-ball counts as a ball faced."),
    ("Legal ball", "A delivery that is neither a wide nor a no-ball. Overs bowled = legal balls / 6."),
    ("Runs charged to a bowler", "Bat runs plus wides and no-balls. Byes and leg-byes are not charged."),
    ("Wicket credited to a bowler", "Excludes run-outs, retirements and obstruction."),
    ("Dot ball (batter)", "A ball faced on which the batter scored no bat runs. This includes balls where only byes or leg-byes were taken."),
    ("Dot ball (bowler)", "A legal ball on which no runs were charged to the bowler."),
]

BAT_PRESSURE_INTRO = (
    "Not every delivery in a T20 match carries the same pressure. I identified these situations from the match state "
    "at the moment each ball is bowled, using the conditions below. They are reasoned choices, not measured constants."
)
BAT_COND1 = [
    "The team is batting in the second innings.",
    "The first two overs have been completed (the ball is from the 3rd over onward).",
    "The required run rate is 9 or more runs per over.",
]
BAT_COND1_NOTE = (
    "Required run rate = (target - runs scored so far) / (balls remaining / 6). The target is the first-innings total "
    "(runs plus extras) plus one. I chose 9 because the league scoring rate is about 139.2 runs per 100 balls (roughly "
    "8.4 per over). A required rate of 9 or more means the batting side must score faster than the average pace to win."
)
BAT_COND2 = (
    "The batting team has lost 2 or more wickets in the previous 12 legal balls, in either innings. The window is the "
    "12 completed legal balls bowled immediately before the current delivery, within the same innings. Losing two "
    "wickets in a short spell changes what the incoming batter must do: rebuild the innings or keep attacking. It also "
    "covers first-innings pressure, which a chase-only rule would miss."
)
BOWL_COND1 = "Every delivery in overs 17 to 20, in either innings. Batters attack in these overs and the bowler has the least room for error, so one expensive over can decide a match."
BOWL_COND2 = [
    "The team is batting in the second innings.",
    "The delivery is bowled after the 10th over has been completed (from the first ball of the 11th over).",
    "The required run rate is between 7.5 and 14 runs per over.",
    "The batting team has lost 6 or fewer wickets.",
    "Runs are still needed, meaning the target has not yet been reached.",
]
BOWL_NOTE = (
    "This captures the stage of a chase when the result is genuinely open and the bowler can still change it. Every "
    "bowler is compared with the league norm for the same innings and over number, so a death-over specialist is not "
    "penalised for bowling in the hardest overs."
)

BAT_METRICS_TABLE = [
    ("Pressure strike rate (SR)", "100 x bat runs / balls faced, using pressure balls only", "Keeping the scoring rate up when it is hardest"),
    ("Normal SR", "The same formula on non-pressure balls", "The batter's own baseline"),
    ("SR retention %", "Pressure SR / Normal SR x 100", "Above 100 means faster under pressure than usual"),
    ("Dot-ball %", "100 x pressure balls with no bat runs / pressure balls faced", "Lower means less pressure is left on the batter"),
    ("Rotation %", "100 x pressure balls with 1, 2 or 3 bat runs / pressure balls faced", "Strike rotation under pressure"),
    ("Scores-after-dot %", "Of the pressure dot balls that are followed by another ball faced by the same batter in that innings, the share where that next ball scores at least 1 bat run", "How quickly the pressure is handed back to the bowler. It uses the batter's own next ball, so a strike change does not distort it"),
    ("Balls per dismissal", "Pressure balls faced / max(1, times dismissed on pressure balls)", "Avoids throwing the wicket away"),
    ("% innings at league SR", "100 x pressure innings with a pressure SR of 137.2 or more / pressure innings. A pressure innings is one with at least 6 pressure balls faced", "Consistency across matches"),
    ("% innings of 20+", "100 x innings with 20 or more bat runs / innings in which the batter faced at least 6 balls (whole innings, not only pressure balls)", "Basic scoring consistency"),
    ("Tough-chase team win %", "100 x tough chases won by the batter's team / tough chases. A tough chase is a second-innings match in which the batter faced at least 6 balls at a required rate of 9 or more", "Whether the pressure scoring helped win. It is weak evidence because it depends on teammates"),
]
BAT_METRICS_NOTES = [
    ("Balls per dismissal when there is no dismissal.", "To avoid dividing by zero, the number of dismissals is set to a minimum of 1. A batter who was never dismissed on a pressure ball therefore scores his total pressure balls faced. This does not affect the top 10: every selected batter was dismissed at least about 9 times on pressure balls (the lowest is Shashank Singh, 314 balls / 34.9). The minimum matters only for eligible players outside the top 10."),
    ("Why '% innings of 20+' uses whole innings.", "It is the one batting metric that is not limited to pressure balls, and that is deliberate. Pressure balls are only 31.8% of balls faced, so a 20-run threshold counted on pressure balls alone would be reached rarely and would mostly reflect how many pressure balls an innings happened to contain. The 20+ metric adds a basic check that a good pressure record sits on top of a reliable scoring base. Because it is not a pressure measure, it has the lowest weight in the model (5%)."),
]
BOWL_METRICS_TABLE = [
    ("Pressure overs", "Legal pressure balls / 6. Wides and no-balls add to runs charged but not to legal balls", "The denominator for every 'per over' metric"),
    ("Pressure economy", "Runs charged to the bowler on pressure balls / pressure overs", "The plain measure of run suppression"),
    ("Expected runs / wickets", "The baseline is the league mean runs charged (and wickets credited) per delivery for the same innings and over number, taken over all league deliveries. Expected runs and expected wickets are the sums of this baseline across the bowler's pressure deliveries", "A fair baseline for each phase of the innings"),
    ("Runs saved per over", "(Expected runs - runs charged) / pressure overs", "Run suppression against the situation"),
    ("Wickets above expected per over", "(Wickets credited - expected wickets) / pressure overs. Run-outs are excluded", "Forcing batter mistakes"),
    ("Pressure dot-ball %", "100 x legal pressure balls with no runs charged / legal pressure balls", "Builds pressure on the batter"),
    ("Boundary % conceded", "100 x pressure deliveries with a bat-scored four or six / all pressure deliveries (wides and no-balls included)", "Avoids releasing pressure"),
    ("Wides + no-balls per over", "(Wides + no-balls on pressure deliveries) / pressure overs", "Self-inflicted mistakes"),
    ("Pressure spell", "All of a bowler's pressure deliveries in one innings of one match, counted as a spell when there are at least 6 pressure balls", "The unit for the consistency metrics below"),
    ("% spells beating expected", "100 x pressure spells with runs charged at or below expected runs / pressure spells", "Consistency across matches"),
    ("% disaster spells", "100 x pressure spells with an economy of 14 or more / pressure spells", "Avoids collapses"),
    ("Resilience", "Runs saved per over on pressure balls - runs saved per over on non-pressure balls", "Better or worse than the bowler's own normal"),
    ("Pressure-spell team win %", "100 x matches won by the bowler's team / matches in which the bowler had a pressure spell", "Weak result signal"),
]
EXPECTED_NOTE = (
    "The baseline depends on two things only: the innings (first or second) and the over number (1 to 20). For each "
    "combination I take the league average runs charged per delivery and wickets credited per delivery, using every "
    "league delivery in that innings and over, not only pressure deliveries. For example, every delivery bowled in the "
    "18th over of a second innings is compared with the league average for the 18th over of second innings, whoever the "
    "bowler or batter and whatever the score. The baseline does not adjust for the required run rate, wickets in hand, "
    "the batter, the venue or the opposition. The pressure flag is what separates hard situations from easy ones, and "
    "the baseline only removes the effect of the phase of the innings."
)

SCORING_TEXT = [
    "The metrics are measured on different scales. A strike rate near 170 cannot be added to a dot-ball percentage near 28 or a count of balls per dismissal. To make them comparable, every metric is converted into a percentile among all eligible players.",
    "Percentile. A player's percentile on a metric is the share of eligible players whose value is equal to or worse than his, so the best player on a metric scores 1.0. For metrics where a lower value is better, the direction is reversed so that the lowest value scores 1.0. These are batter dot-ball %, bowler boundary % conceded, wides + no-balls per over, and % disaster spells. Bowler dot-ball % is the other way round: higher is better.",
    "Score. Each metric's percentile is multiplied by its weight, the results are added, and the total is multiplied by 100.",
]
WEIGHTS_NOTE = (
    "The weights are my judgement. I gave the most weight (20%) to the measure that speaks most directly to pressure: "
    "scoring speed for batters and run suppression for bowlers. Metrics that describe how a player gets there (dots, "
    "rotation, wickets, errors, consistency) carry 5% to 15%. Team results are capped at 10% because a win depends on teammates."
)
ELIGIBILITY = (
    "Batters need at least 300 balls faced, 250 pressure balls and 8 pressure innings (66 qualify). Bowlers need at "
    "least 300 balls, 200 pressure balls and 15 pressure spells (73 qualify). Players below these floors are excluded "
    "rather than adjusted, because their percentages are too uncertain."
)
CLOSE_SCORES = (
    "Scores within 2.0 points are treated as equal and are ordered by number of pressure balls, more balls first. I use "
    "this rule because performance shown over a larger sample is more trustworthy. Gaps larger than 2.0 points are "
    "decided by score. Where my final list departs from this rule, the departure is stated and explained on the "
    "Selection decisions page."
)
FAIR = [
    ("Sample size", "minimum pressure balls and pressure innings or spells. Among the top 10 in each list, pressure samples range from 210 to 596 balls. The six smallest (210 to 314 balls) are named on the Reliability page as the least certain."),
    ("Match context", "bowlers are judged against the league norm for the same innings and over; batters against the league pressure SR and their own normal SR. Rain-affected matches are removed."),
    ("IPL versus T20I", "every top-10 player is also shown split by format and by period (2022-24 against 2025-26), so one format or old form cannot carry a ranking unnoticed."),
]

BAT_NOTICE = {
    "7.1": "Every batter scores faster under pressure than normally. Abhishek Sharma's retention is only 102% because his normal strike rate is already 186.6. Kohli rotates strike most often (53.1% of balls) and Jaiswal least (37.6%).",
    "7.2": "Kohli has the highest score (89.9) but ranks second, because it is within 2.0 points of Buttler's (88.1) and Buttler has more pressure balls. Gill, Sudharsan, Jaiswal and de Kock (82.6 to 84.2) form another near-tie, ordered by pressure balls.",
    "7.3": "Gill, Sudharsan, Jaiswal and Shashank Singh have no T20I figure, so their evidence is IPL only. De Kock is the only batter with a large format gap (187 in T20Is, 138 in the IPL). Buttler, Kohli, Jaiswal, Abhishek Sharma and Samson are steady between periods.",
}
BOWL_NOTICE = {
    "8.1": "All ten bowlers are well under the league pressure economy of 9.82. Narine, Theekshana, Ngidi and Malinga are cheaper under pressure than in their own normal overs; Bumrah, Santner, Rashid Khan, Rauf, Hosein and Kuldeep are dearer.",
    "8.2": "Narine is clear in first place. Bumrah (82.7) and Santner (84.3) are within 2.0 points, so Bumrah's far larger sample (582 balls against 235) puts him third. Rashid Khan (81.5) and Ngidi (81.6) are a near-tie, ordered by pressure balls.",
    "8.3": "Narine has no T20I figure, and Rauf and Hosein have no IPL figure, so their evidence comes from one format. Seven of the ten bowlers (all except Narine, Ngidi and Kuldeep) were more expensive in 2025-26 than in 2022-24, and the rise is largest for Santner, Malinga and Theekshana.",
}

BAT_NARR = {
"Jos Buttler": "Buttler qualified on volume and speed. His pressure strike rate is 177.3 against 150.9 in normal play, from 490 pressure balls over 24 innings, and he matched the league pressure rate in 83.3% of those innings. The record holds in both competitions (186 in the IPL, 155 in T20Is) and both periods (180 and 175). His weaker points are balls per dismissal (23.3, well below Kohli's 35.8) and a team win rate of 40.9% in his 22 tough chases. His score is 1.8 points below Kohli's, which is inside the near-equal band, so his larger sample (490 balls against 429) places him first.",
"Virat Kohli": "Kohli has the highest batting score because he leads the metrics that measure staying in and keeping the scoreboard moving: 35.8 balls per dismissal, a 25.6% dot-ball rate, strike rotation on 53.1% of balls and a scoring ball after 77.1% of his dot balls. Each is the best of the ten. His pressure strike rate is 157.3 against 142.9 normally, and he is consistent across formats (158 in the IPL, 155 in T20Is) and periods (157 and 158). His team won 61.1% of his 18 tough chases. The limit is raw scoring speed: seven of the other nine batters have a higher pressure strike rate, and his T20I figure rests on only 51 balls. Because his score is only 1.8 points above Buttler's, the near-equal rule puts him second.",
"Shubman Gill": "Gill's pressure strike rate is 165.6 against 146.7 normally (retention 113%), with a 27.1% dot-ball rate and strike rotation of 50.8%. His team won 62.5% of the 16 tough chases in which he batted, the best of the ten, and he improved from 157 in 2022-24 to 179 in 2025-26 (170 balls). Two things hold him back. All of his pressure evidence is from the IPL, and he scores after a dot ball only 67.9% of the time, the lowest of the ten. He leads a four-way near-tie (scores 82.6 to 84.2) and is placed third on pressure balls (439).",
"Sai Sudharsan": "Sudharsan qualified through steady scoring: a pressure strike rate of 156.0 against 144.9 normally, strike rotation of 51.0%, a scoring ball after 72.1% of his dot balls and 32.3 balls per dismissal. He has improved sharply, from 134 in 2022-24 (below the league pressure rate of 137.2) to 170 in 2025-26 (254 balls). What limits him is a pressure strike rate that is the second lowest of the ten, team wins in only 47.1% of 17 tough chases, and IPL-only evidence. He sits in the same near-tie as Gill and ranks fourth on 420 pressure balls.",
"Quinton de Kock": "De Kock qualified on his ability to restart an innings: he scores on the next ball after 75.6% of his dot balls, second only to Kohli, and his pressure strike rate is 162.7 against 145.6 normally. His record is split by format. He scored at 187 in T20Is (180 balls) and 188 in 2025-26, but only 138 in the IPL (174 balls), barely above the league pressure rate. He also has the fewest pressure innings of the ten (14), and his team won 46.2% of 13 tough chases. In the four-way near-tie his 354 pressure balls place him fifth.",
"Yashasvi Jaiswal": "Jaiswal qualified on speed that he repeats from match to match. His pressure strike rate is 175.3 against 150.1 normally (retention 117%), and he matched the league pressure rate in 88.2% of his pressure innings, the best of the ten. His figures are steady across periods (175 and 176) but come entirely from the IPL (173 from 327 balls). The weakness is how he scores: the highest dot-ball rate of the ten (32.1%), the lowest strike rotation (37.6%) and 22.7 balls per dismissal. With the smallest sample in his near-tie band (340 balls), he ranks sixth.",
"Shreyas Iyer": "Iyer has the largest pressure sample of the ten batters (557 balls over 23 innings), which makes his the most reliable evidence in the group. He holds his scoring rate under pressure (155.7 against 153.0 normally), rotates strike on 51.7% of balls and scored at 211 in 73 knockout balls. Both formats are covered (IPL 162, T20I 137), and he improved from 143 in 2022-24 to 163 in 2025-26 (348 balls). The limit is that his pressure strike rate is the lowest of the ten and his T20I figure is close to the league pressure rate. His score is 0.7 above Abhishek Sharma's, a near-tie, and his larger sample gives him seventh place.",
"Abhishek Sharma": "Abhishek has the highest pressure strike rate of the ten at 191.0, from 433 balls in 25 innings (the most of any batter), and he matched the league pressure rate in 80.0% of them. He is stable across formats (196 in the IPL, 178 in T20Is) and rose from 178 in 2022-24 to 199 in 2025-26 (266 balls). His team won 57.9% of 19 tough chases. Retention is only 102% because he already scores at 186.6 in normal play: he does not speed up so much as stay fast. What holds him back is the shape of that scoring, with a 30.0% dot-ball rate, strike rotation of 39.7% and 20.6 balls per dismissal, all among the weaker figures in the group. He ranks eighth, just below Iyer.",
"Shashank Singh": "Shashank qualified on speed and survival: a pressure strike rate of 172.6 against 150.2 normally (retention 115%), a 27.4% dot-ball rate and 34.9 balls per dismissal, the second best of the ten. His consistency evidence is thinner than the others'. All of it comes from the IPL (314 balls, the smallest batting sample in the list), his strike rate fell from 182 in 2022-24 to 157 in 2025-26 (122 balls), he matched the league pressure rate in only 61.1% of pressure innings, and his team won 20.0% of his 15 tough chases. His score is 1.9 points below Abhishek Sharma's, so Abhishek's larger sample places him higher, and 3.4 points above Samson's. His selection over Mohammad Rizwan is a judgement decision explained on the Selection decisions page.",
"Sanju Samson": "Samson qualified on consistency. His pressure strike rate is 174.2 against 150.2 normally (retention 116%), it is stable across formats (172 in the IPL, 182 in T20Is) and periods (173 and 175), and he matched the league pressure rate in 80.0% of his pressure innings. He has the lowest score of the ten because of 20.0 balls per dismissal (the lowest), a 31.2% dot-ball rate (second highest) and a scoring ball after only 69.0% of dot balls (second lowest). His place in the list follows the decision on Reeza Hendricks on the Selection decisions page.",
}
BOWL_NARR = {
"Sunil Narine": "Narine has the best bowling score by a clear margin (89.1 against 86.6). His pressure economy is 6.80 against the league's 9.82, he saves 1.92 runs per over, he took 22 wickets, he beat expected runs in 76.7% of his spells (the best of the ten) and he bowls only 0.11 wides and no-balls per over. He is also improving, from 7.37 in 2022-24 to 5.83 in 2025-26 (103 balls). The weak points are a smaller sample (278 balls over 30 spells), evidence that is entirely from the IPL, and a team win rate of 50.0% in those spells. He is more than 2.0 points ahead of the next bowler, so no tie-break was needed.",
"Maheesh Theekshana": "Theekshana saves 1.90 runs per over and is cheaper under pressure (7.33) than in normal play (7.81). He bowled 52 pressure spells, took 31 wickets from 427 balls, had only 9.6% disaster spells and beat expected runs in 73.1% of spells. He has done it in both formats, though differently: 6.80 in T20Is (254 balls) against 8.12 in the IPL (173 balls). The concern is recent form, as his economy rose from 6.64 in 2022-24 to 8.93 in 2025-26 (129 balls). His score is 2.3 points above Santner's, so he is second on score alone.",
"Jasprit Bumrah": "Bumrah saves the most runs per over of the ten (2.13), took 40 wickets from 582 pressure balls and had the fewest disaster spells (5.1%). He is reliable in both formats (7.74 in the IPL, 6.95 in T20Is) and both periods (7.15 and 7.80). The caution is that his pressure economy (7.51) is higher than his normal economy (7.09), and his boundary rate (13.9%) is only mid-table. His score is 1.6 points below Santner's, but with far more pressure balls (582 against 235) the near-equal rule places him third.",
"Mitchell Santner": "Santner has the highest score in his near-tie group, built on results: he beat expected runs in 76.0% of his spells and his team won 68.0% of the 25 spells, the best of the ten. Against that, his pressure economy (7.86) is above his normal one (7.37), he bowls 0.31 wides and no-balls per over and 12.0% of his spells were disasters. His evidence is split between the IPL (7.54 from only 78 balls) and T20Is (8.03 from 157 balls), and his economy rose from 6.39 in 2022-24 to 9.45 in 2025-26 (113 balls). With only 235 pressure balls he is placed fourth, below Bumrah.",
"Rashid Khan": "Rashid has the largest pressure sample of any bowler (596 balls over 67 spells) and the most wickets (53), with just 0.06 wides and no-balls per over, and his team won 59.7% of those spells. His pressure economy (8.34) is well above his normal economy (7.13) and 17.9% of his spells were disasters, the highest of the ten, so his value lies in wickets rather than control. The split is large: 6.58 in T20Is (248 balls) against 9.59 in the IPL (348 balls), and 7.58 in 2022-24 against 9.76 in 2025-26 (206 balls). His score is 0.1 below Ngidi's, so the near-equal rule places him fifth on sample size.",
"Lungi Ngidi": "Ngidi is cheaper under pressure (8.48) than in normal play (9.13), saves 1.41 runs per over and has the second-highest dot-ball rate of the ten (37.0%). He improved from 9.55 in 2022-24 to 7.82 in 2025-26 (142 balls) and is similar in both formats (8.12 in the IPL, 8.77 in T20Is). The limits are that only 63.0% of his spells beat expected runs, he concedes 16.8% boundaries, his team won just 44.4% of 27 spells (the lowest of the ten) and his sample (230 balls) is among the smallest. He is sixth, behind Rashid Khan on sample size.",
"Haris Rauf": "Rauf took 40 wickets from 404 pressure balls and has the highest dot-ball rate of the ten (38.2%). His pressure economy (9.03) is below the league's 9.82 but above his own normal (8.45), and it rose from 8.60 to 9.97 in 2025-26 (127 balls). The weaknesses are the highest boundary rate of the ten (18.9%), 0.30 wides and no-balls per over, and evidence that is from T20Is only. His score is 2.4 points above Malinga's, so he is seventh on score.",
"Eshan Malinga": "Malinga is cheaper under pressure (8.66) than in normal play (9.27), saves 1.37 runs per over, took 24 wickets and beat expected runs in 73.3% of his spells. His results differ by format: 7.84 in the IPL (196 balls) against 10.26 in T20Is (100 balls), and his economy rose from 6.30 in 2022-24 to 9.27 in 2025-26 (235 balls). He gives away the most wides and no-balls of the ten (0.47 per over) and 13.3% of his spells were disasters. His score is 1.5 points below Hosein's, but with more pressure balls (296 against 210) the near-equal rule places him eighth.",
"Akeal Hosein": "Hosein's case rests on avoiding disasters: only 8.0% of his spells were disasters, second only to Bumrah, and 72.0% beat expected runs. His T20I economy is 7.92 (184 balls), though it rose from 6.82 to 8.97 in 2025-26 (115 balls). He is slightly dearer under pressure than normally (8.00 against 7.67), has the lowest dot-ball rate of the ten (30.6%), the fewest wickets (18) and the smallest sample (210 balls, T20Is only). He is ninth because his score is within 2.0 points of Malinga's, who has more pressure balls.",
"Kuldeep Yadav": "Kuldeep qualified on stability. His economy is almost identical across periods (8.59 and 8.61 over 200 balls in 2025-26) and acceptable in both formats (8.83 in the IPL, 7.77 in T20Is). He took 31 wickets from 404 balls and his team won 60.9% of his spells. He has the lowest score of the ten because he saves only 0.57 runs per over, beat expected runs in just 56.5% of spells (the lowest) and had 17.4% disaster spells. His place follows the decision on Tim Southee on the Selection decisions page.",
}

DECISIONS_INTRO = (
    "The final order is the score order with the near-equal rule, except for four notable decisions. Three of them are "
    "analyst judgement: I overrode the model, and I say so. One follows the stated rule and needs no override. I set them "
    "out so that an evaluator can see exactly where my judgement enters and can disagree with it."
)
DECISIONS_TABLE = [
    ("Reeza Hendricks", "Not selected (3rd batter by score, 86.5)", "Analyst judgement"),
    ("Mohammad Rizwan", "Not selected; Shashank Singh selected, although the tie-break favours Rizwan", "Analyst judgement (override of the tie-break)"),
    ("Tim Southee", "Not selected; Kuldeep Yadav selected (score gap of 5.6 points)", "Analyst judgement"),
    ("Taskin Ahmed", "Eshan Malinga ranks above him", "Follows the near-equal rule"),
]
DECISIONS = [
("Mohammad Rizwan and Shashank Singh (analyst judgement)", [
 "This is the decision that does not follow my stated rule, so I want to be direct about it. Rizwan's score was 77.1 and Shashank Singh's was 77.5, a gap of 0.4 points and well inside the 2.0-point band. Rizwan had more pressure balls (329 against 314), so applying the tie-break mechanically would have placed Rizwan ahead of Shashank. I did not apply it, and I selected Shashank. This is a manual override based on my judgement. It is not an outcome of the scoring model.",
 "My reason is that a 15-ball difference in sample size is small, while the difference in how the two bat under pressure is large. Rizwan's pressure strike rate of 145.9 is 44th of the 66 eligible batters. Shashank's is 172.6. For a list about reliability under pressure, I judged that gap to matter more than 15 extra balls. The cost is that Shashank's own evidence has weaknesses: all IPL, a fall from 182 to 157 across periods, and team wins in 20.0% of tough chases. A reader who prefers a strictly rule-based list could reasonably put Rizwan in his place."]),
("Reeza Hendricks (analyst judgement)", [
 "Hendricks scored 86.5, the third-highest among eligible batters, so leaving him out is also a manual override. His pressure strike rate is 173.2 against 128.8, which is excellent on paper. However, all 328 of his pressure balls are from T20Is, only 24 are from 2025-26 and none are from the IPL, and his team won 17% of his tough chases. The data therefore cannot show whether his record carries across formats or is recent.",
 "This is a statement about the evidence, not about his ability. The dataset does not show that his current ability is poor; it only cannot confirm that it is repeatable. I selected Sanju Samson instead, whose pressure strike rate is stable across the IPL, T20Is and both periods."]),
("Tim Southee (analyst judgement)", [
 "Southee scored 79.5, which is 5.6 points above Kuldeep Yadav's 73.9, so this too is an override and not a near-equal case. The data holds no pressure balls for Southee since 2025, and his IPL pressure economy is 10.15, above the league pressure economy of 9.82. Without recent evidence I could not confirm that his record still applies. Kuldeep's economy is almost the same in both periods (8.59 and 8.61) and acceptable in both formats (8.83 in the IPL, 7.77 in T20Is). The absence of recent pressure balls may have causes the data cannot explain, so this is a cautious choice based on missing evidence."]),
("Taskin Ahmed and Eshan Malinga (follows the near-equal rule)", [
 "Taskin's score was 77.9 and Malinga's was 76.4, a gap of 1.5 points, inside the near-equal band. Malinga had more pressure balls (296 against 282), so he ranks above Taskin under the stated rule. No override was involved. The rest of the evidence points the same way: Taskin beat expected runs in only 61% of his spells, against 73.3% for Malinga, and conceded about a run more per over under pressure than in normal play."]),
]
OTHER_EXCLUSIONS = [
    ("Phil Salt, Abrar Ahmed, Gudakesh Motie and Rasikh Salam", "excluded by the sample floor. Their pressure-ball counts are 243, 153, 177 and 172, below the 250 (batters) or 200 (bowlers) floor. Their percentages are strong but too uncertain to rank."),
    ("Wanindu Hasaranga and Varun Chakravarthy", "considered but not selected. Hasaranga beats expected runs in only 48.6% of his spells, and Chakravarthy has 26.8% disaster spells."),
]
LIMITATIONS = [
    ("Pressure is inferred, not observed.", "I only have match-state information, so a routine ball in a tight chase counts as pressure, while a hard ball in a quiet phase does not. This adds noise to individual figures. I have no evidence that it favours any player, but I cannot test that with this data."),
    ("The thresholds are my choices.", "A required rate of 9, a collapse of 2 wickets in 12 balls, and overs 17 to 20 are reasoned criteria, not universal definitions of pressure. Different cut-offs would change which balls count and could move players with small samples."),
    ("Opposition strength is not modelled.", "A pressure ball against a top attack counts the same as one against a weak one, so a player who faced easier opposition may look better than he is."),
    ("The bowling baseline is by innings and over only.", "Expected runs do not adjust for required run rate, wickets in hand, the batter or the venue, so a bowler who is given the hardest matchups within an over is not credited for them."),
    ("Pitch, weather and ground are not in the data.", "Dew, pitch behaviour and boundary size affect strike rates and economies, and the model cannot separate them from player skill."),
    ("IPL and T20I conditions differ.", "Several players have a record from one format only (Rauf and Hosein: T20Is; Shashank Singh, Gill, Sudharsan and Jaiswal: IPL). For them I cannot show that the record transfers, which is why format and period splits are shown beside every rank."),
    ("Samples are modest.", "The smallest top-10 samples (Hosein, Ngidi, Santner, Narine, Malinga and Shashank Singh, 210 to 314 pressure balls) could move a few places with a few more matches."),
    ("Team results depend on teammates.", "A win is not one player's doing, so team win percentages carry only 10% of the score and should be read as supporting evidence."),
    ("The weights are judgement.", "Percentiles avoid scale effects but cannot reward an exceptional value that sits just above the next player. Different weights could shift players with similar scores. I tested three alternatives, but the exact order within near-equal bands should not be treated as fixed."),
    ("The team shown is the most frequent team in the data.", "For a player who also plays for a country, this can be an IPL franchise."),
]
STABILITY_NOTE = (
    "The shortlist is stable: at least 9 of 10 names in each list survive every weighting. The exact order inside a list "
    "is less certain, especially within near-equal bands. These checks vary the weights only. I did not test alternative pressure thresholds."
)
REPRO = [
    ("Load and clean.", "Join the ball-by-ball records to the matches file (result, rain revisions) by match_id and to the competitions file (IPL or T20I) by comp_id. Drop super overs and the 34 rain-affected matches."),
    ("Build the match state for every delivery.", "Calculate cumulative runs, legal balls bowled and wickets lost before the delivery. For second innings, target = first-innings total (runs plus extras) + 1, balls remaining = 120 - legal balls bowled, and required rate = (target - runs) / (balls remaining / 6)."),
    ("Count recent wickets.", "For each delivery, count the wickets lost in the previous 12 completed legal balls of the same innings, not including the current ball."),
    ("Flag pressure.", "Apply the pressure rules to mark each delivery as a batting pressure ball and/or a bowling pressure ball."),
    ("Aggregate.", "For each striker and each bowler, add up runs, balls, dismissals, wickets and extras separately on pressure and non-pressure balls, using the counting rules."),
    ("Calculate expected values.", "For bowlers, build a league table of mean runs charged and mean wickets credited per delivery, indexed by innings (1 or 2) and over number (1 to 20), using all league deliveries. Expected runs and wickets are the sums of the matching table values over the bowler's pressure deliveries."),
    ("Calculate the metrics.", "Compute every metric (with dismissals set to at least 1 for balls per dismissal). Build pressure innings for batters and pressure spells for bowlers (one innings of one match each) for the consistency metrics."),
    ("Apply eligibility floors.", "Keep batters with 300 balls, 250 pressure balls and 8 pressure innings, and bowlers with 300 balls, 200 pressure balls and 15 pressure spells."),
    ("Score.", "Percentile-rank each metric among eligible players (reversing the lower-is-better metrics), multiply by the weights, add up and multiply by 100."),
    ("Order and decide.", "Order by score using the 2.0-point near-equal rule (more pressure balls first), then apply the selection decisions."),
    ("Check reliability.", "Re-score under the three alternative weightings and compare each top-10 player's format and period splits."),
]
CONCLUSION = (
    "The ranking rests on one idea: a player is reliable under pressure when he keeps performing at or above the league "
    "norm, and close to his own normal, in the situations where that is hardest. The batters stand out for holding or "
    "raising their scoring rate while limiting dot balls and wickets. The bowlers stand out for keeping runs well below "
    "the league pressure economy while avoiding damaging spells. The shortlist is stable under different weightings, and "
    "the places where I departed from the raw order are stated and argued on the Selection decisions page. The main "
    "caution is that pressure is inferred from match state and that several samples are modest, so positions inside "
    "near-equal bands should be read as close calls and not as measured differences."
)
