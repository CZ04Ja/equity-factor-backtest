# Machine Learning for Finance Coursework: Close-to-Open Equity Strategy

This is a public-safe project note for my Machine Learning for Finance coursework exploration. It summarises the research idea, methodology, current results, and next directions without uploading raw coursework data.

## Project Idea

The project studies a US large-cap close-to-open overnight trading strategy. The portfolio enters positions at the day-`t` close and exits at the day-`t+1` open. The aim is not simply to predict returns, but to build a costed, capacity-aware, borrow-aware, and point-in-time machine-learning pipeline.

The main research question is:

> Can cross-sectional ML signals improve overnight return selection after realistic trading costs, borrow costs, and liquidity constraints?

## Current Champion Strategy

The current champion is an expanding-window volatility-scaled alpha model.

Core target:

```text
target = overnight_next / (vol20 / sqrt(252))
```

This asks the model to focus on risk-adjusted overnight opportunity rather than raw high-volatility moves.

Portfolio construction:

- Daily long-short close-to-open strategy.
- Top/bottom 3% cross-sectional baskets.
- Dollar-neutral portfolio.
- Equal weights within each side.
- 5% ADV20 participation cap.
- Commission, auction slippage, and tiered borrow costs included.
- Expanding-window training with no future data in each scored year.

## Headline Result

At 250M AUM over the 2010-2024 development window:

| Metric | Result |
|---|---:|
| Net annual return | 7.31% |
| Net annual volatility | 4.97% |
| Net Sharpe | 1.445 |
| Max drawdown | -10.19% |

The result is developed under a fixed cutoff of `2024-12-31`; no 2025+ data is used for model selection.

## Aggressive ML Extension

I also tested a more aggressive ML challenger by blending the transparent expanding-window signal with ridge and elastic-net ranked-feature alphas:

```text
blend_score = 0.60 * expanding_score
            + 0.25 * ridge_score
            + 0.15 * elastic_net_score
```

Champion-challenger summary at 250M AUM:

| Strategy | Validation 2019-2022 Sharpe | Holdout 2023-2024 Sharpe | Full 2010-2024 Sharpe | Max drawdown |
|---|---:|---:|---:|---:|
| Expanding champion | 2.279 | 0.620 | 1.445 | -10.19% |
| Ridge challenger | 1.523 | 1.027 | 1.239 | -12.73% |
| Elastic-net challenger | 1.572 | 0.900 | 1.258 | -11.89% |
| 60/25/15 blend | 1.979 | 0.804 | 1.383 | -10.19% |

The blend improves 2023-2024 internal holdout Sharpe versus the champion, but it does not beat the champion on validation Sharpe or full-period Sharpe. Therefore, the transparent expanding-window model remains the final promoted strategy, while the blended model is kept as a promising next research direction.

## What I Learned

The main lesson is that better predictive diagnostics do not automatically imply better tradable portfolio performance. Ridge and elastic net improve information coefficient and holdout survival, but direct promotion weakens costed portfolio Sharpe. A good ML trading strategy needs model quality, point-in-time discipline, cost awareness, capacity control, and robust validation design.

## Next Directions

- Tune blend weights using only design and validation periods.
- Keep 2023-2024 frozen as internal holdout.
- Test ridge/elastic-net signals as risk overlays instead of direct score blends.
- Expand stress-window analysis around 2018, 2020 Q1, and 2022.
- Improve explainability through feature-group ablation and signal decomposition.

## Reproducibility Note

The raw coursework data is not included in this public note. Reproduction requires the original course-provided data files placed under a local `data/` directory.

