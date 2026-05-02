import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def winsorize_df(df: pd.DataFrame, p: float = 0.01) -> pd.DataFrame:
    """Row-wise winsorize by quantile."""
    lo = df.quantile(p, axis=1)
    hi = df.quantile(1 - p, axis=1)
    return df.clip(lo, hi, axis=0)


def zscore_df(df: pd.DataFrame) -> pd.DataFrame:
    """Row-wise z-score."""
    return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)


def calc_turnover(w: pd.DataFrame) -> pd.Series:
    """0.5 * sum |w_t - w_{t-1}|"""
    return 0.5 * w.diff().abs().sum(axis=1).fillna(0.0)


def perf_stats(r: pd.Series) -> dict:
    r = r.dropna()
    ann_ret = (1 + r.mean()) ** 252 - 1
    ann_vol = r.std(ddof=0) * np.sqrt(252)
    sharpe = ann_ret / ann_vol if ann_vol > 0 else np.nan

    nav = (1 + r).cumprod()
    dd = 1 - nav / nav.cummax()
    maxdd = dd.max()
    return {
        "ann_ret": ann_ret,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "maxdd": maxdd,
        "nav": nav,
        "dd": dd
    }


def main():
    # ===== 1) Data =====
    tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "JPM", "XOM", "JNJ", "PG"]
    start, end = "2016-01-01", "2025-01-01"

    px = yf.download(tickers, start=start, end=end, auto_adjust=True)["Close"].dropna(how="all")
    ret = px.pct_change().dropna()

    # ===== 2) Signals =====
    # Momentum: 12-1 month (252d lookback, skip last 21d)
    mom = (px.shift(21) / px.shift(252)) - 1
    mom = mom.reindex(ret.index)

    # Quality proxy: low volatility (63d), negative vol => higher score for lower vol
    vol_63 = ret.rolling(63).std()
    quality = -vol_63

    # Cross-sectional cleaning
    mom_cs = zscore_df(winsorize_df(mom))
    q_cs = zscore_df(winsorize_df(quality))

    signal = 0.5 * mom_cs + 0.5 * q_cs
    signal = signal.dropna(how="all")

    # ===== 3) IC (next-day) =====
    fwd = ret.shift(-1).reindex(signal.index)
    ic = signal.corrwith(fwd, axis=1)  # one IC per day
    print(f"IC mean={ic.mean():.4f}, IC IR={ic.mean()/ic.std(ddof=0):.2f}")

    # ===== 4) Portfolio: top 20% equal-weight =====
    rank = signal.rank(axis=1, pct=True, ascending=False)
    w = (rank >= 0.8).astype(float)
    w = w.div(w.sum(axis=1), axis=0).fillna(0.0)

    # avoid look-ahead: trade on next day
    w_lag = w.shift(1).fillna(0.0)

    # ===== 5) Transaction costs =====
    to = calc_turnover(w_lag)
    cost_bps = 20
    cost = (cost_bps / 10000.0) * to

    # ===== 6) Backtest =====
    gross = (w_lag * ret).sum(axis=1).reindex(cost.index)
    net = gross - cost

    stats = perf_stats(net)
    print(f"AnnRet={stats['ann_ret']:.2%}, AnnVol={stats['ann_vol']:.2%}, Sharpe={stats['sharpe']:.2f}, MaxDD={stats['maxdd']:.2%}")
    print(f"Avg Turnover={to.mean():.2%}")

    # ===== 7) Save plots to reports/ =====
    stats["nav"].plot(title="NAV (Net)")
    plt.tight_layout()
    plt.savefig("reports/nav.png", dpi=200)
    plt.close()

    ic.rolling(63).mean().plot(title="Rolling 63D IC")
    plt.tight_layout()
    plt.savefig("reports/rolling_ic.png", dpi=200)
    plt.close()

    print("Saved: reports/nav.png and reports/rolling_ic.png")


if __name__ == "__main__":
    main()