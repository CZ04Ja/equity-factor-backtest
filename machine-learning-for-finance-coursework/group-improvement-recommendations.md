# Group Coursework Improvement Recommendations

Review date: 2026-06-05  
Repository state reviewed: local branch `codex/aggressive-ml-blend`, commit `79fc169`  
Verification: `.venv/bin/python -m pytest -q` -> `15 passed in 18.75s`

## Current Position

The project is already in a strong submission-ready state. The current champion is the expanding-window volatility-scaled close-to-open strategy:

- 250M AUM net annual return: about `7.31%`
- 250M AUM net volatility: about `4.97%`
- 250M AUM net Sharpe: about `1.445`
- Max drawdown: about `-10.19%`
- Full-period IC mean: about `0.0289`, IC t-stat about `9.93`

The new aggressive ML blend challenger is useful but should stay as a research extension rather than the final promoted strategy:

```text
blend_score = 0.60 * expanding_score + 0.25 * ridge_score + 0.15 * elastic_net_score
```

It improves 2023-2024 internal holdout Sharpe from `0.620` to `0.804`, but full-period Sharpe falls from `1.445` to `1.383`, and validation Sharpe falls from `2.279` to `1.979`. This is a good critical-thinking result: aggressive ML improves some out-of-period robustness, but the final report should not overclaim it.

## Highest-Impact Improvements For The Final Group Report

### 1. Make The Methodology Story Tighter

The report should lead with the research discipline:

1. Define the trade: close day `t`, open day `t+1`, one overnight hold.
2. Define the target: `overnight_next / (vol20 / sqrt(252))`.
3. Explain the expanding-window design: each scored year trains only on earlier data.
4. Explain the portfolio: top/bottom 3%, dollar-neutral, equal-weighted sides, 5% ADV20 cap.
5. Explain all costs: commission, auction slippage, borrow tiers.
6. Explain model selection: validation 2019-2022, internal holdout 2023-2024, no holdout tuning.

This order is easier for markers to audit than starting with model names.

### 2. Turn The Aggressive ML Result Into A Strength

Do not write "ridge/elastic net failed." Write:

- Ridge and elastic net improve IC and holdout survival.
- Direct promotion weakens costed portfolio Sharpe.
- The blend partially transfers their robustness while preserving the champion's drawdown.
- Because full-period and validation Sharpe still fall, the group keeps the transparent champion.

This sounds mature: the group tested innovation, but did not cherry-pick.

### 3. Add A Clear Champion-Challenger Table In The Report Body

Recommended table:

| Strategy | Validation Sharpe | Holdout Sharpe | Full Sharpe | Max DD | Decision |
|---|---:|---:|---:|---:|---|
| Expanding champion | 2.279 | 0.620 | 1.445 | -10.19% | Final |
| Ridge | 1.523 | 1.027 | 1.239 | -12.73% | Not promoted |
| Elastic net | 1.572 | 0.900 | 1.258 | -11.89% | Not promoted |
| 60/25/15 blend | 1.979 | 0.804 | 1.383 | -10.19% | Extension |

The report should explicitly say that 2023-2024 was not used for weight tuning.

### 4. Improve The Robustness Section

The current evidence is good, but the final report can make it more marker-friendly by grouping robustness into:

- Time robustness: design / validation / internal holdout.
- Cost robustness: gross Sharpe versus net Sharpe, commission/slippage/borrow drag.
- Capacity robustness: 50M / 250M / 1B AUM comparison.
- Stress robustness: late 2018, 2020 Q1, 2022 drawdown windows.
- Feature robustness: feature ablation and IC stability.

This makes the strategy look less like a single Sharpe-ratio exercise.

### 5. Be More Explicit About Weaknesses

The final report should proactively disclose:

- 2023-2024 holdout Sharpe is positive but much lower than 2019-2022 validation.
- Full-period performance is materially reduced at 1B AUM because capacity constraints bind.
- The borrow-cost proxy is useful but not a true broker locate feed.
- Ridge/elastic net are less transparent than the champion.
- No 2025-2026 results should be used for tuning.

This critical thinking can improve credibility.

### 6. Improve Reproducibility Notes

Current README records `PYTHON=/opt/anaconda3/bin/python3`, but that path is machine-specific and was not available in this environment. A more portable command block should be added:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
PYTHON=.venv/bin/python make reproduce
```

Also mention that raw coursework data is required under `data/` and is intentionally not committed to GitHub.

## Suggested Short Team Chat Update

我们现在的作业成果其实已经很完整：主策略是 expanding-window + volatility-scaled target，250M AUM full-period net Sharpe 约 1.445，max drawdown 约 -10.19%。我们新增的 aggressive ML blend 用 expanding/ridge/elastic net 按 60/25/15 混合，确实把 2023-2024 holdout Sharpe 从 0.620 提高到 0.804，但 validation 和 full-period Sharpe 没有超过 champion，所以 final 还是保留 transparent expanding champion。报告里可以把这个写成优点：我们尝试了更激进 ML，但最后按 validation、holdout、drawdown、cost、capacity 综合判断，没有只为了创新分盲目换模型。

## Recommended Next Work

1. Add the champion-challenger table directly to the final report.
2. Add one paragraph explaining why the blend is an extension rather than final.
3. Make README reproduction commands environment-neutral.
4. Add one figure/table for stress windows if page budget allows.
5. Add a short limitations paragraph on borrow proxy, capacity, and lower holdout Sharpe.

