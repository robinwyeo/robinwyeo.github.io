---
title: "A stock factor scoring & analyst aggregation dashboard"
date: 2026-05-30
tags:
  - finance
  - factor investing
  - quantitative
  - streamlit
  - python
permalink: /data-science/financial-tools/
header:
  teaser: /images/data-science/financial-tools/title.png
---

![Stock metrics dashboard](/images/data-science/financial-tools/title.png)

I've always found stock screeners a little unsatisfying: most of them hand you a single number — a P/E ratio, an analyst rating — and ask you to trust it. What I actually wanted was a tool that showed me *why* a company looks attractive (or doesn't), grounded in the kinds of factors that decades of empirical finance research have shown actually matter. So I built one.

This little dashboard scores a stock across a broad set of factors — value, momentum, quality, low volatility, financial strength, and more — and ranks each one cross-sectionally against the S&P 500 universe. It then pairs that with aggregated Wall Street analyst recommendations, price targets, and implied upside. The headline output is a single **composite score from 0–100**, but the whole point is that you can open it up and see exactly which factors are driving it.

Under the hood it's a [Streamlit](https://streamlit.io/) app written in Python ([source on GitHub](https://github.com/robinwyeo/financial-tools)), pulling market data from `yfinance`. Rather than just describe it, I've embedded the live dashboard right here so you can poke at it yourself.

## Try it

<iframe
  src="https://robinwyeo-stock-metrics.streamlit.app/?embed=true"
  title="Stock factor scoring & analyst aggregation dashboard"
  style="width: 100%; height: 900px; border: 1px solid #e1e1e1; border-radius: 6px;"
  loading="lazy"
  allow="clipboard-write">
</iframe>

<p style="text-align: center; margin-top: 0.75em;">
  <a href="https://robinwyeo-stock-metrics.streamlit.app" target="_blank" rel="noopener">
    Open the full dashboard in a new tab &rarr;
  </a>
</p>

> The app runs on Streamlit Community Cloud's free tier, so if it has been idle it may take ~30 seconds to wake up on first load. For the best experience (especially on mobile) use the "open in a new tab" link above.

## How to use it

1. **Enter a ticker** (e.g. `AAPL`, `MSFT`, `NVDA`) to pull its factor scorecard, analyst consensus, price targets, and implied upside.
2. **Read the composite score** — a 0–100 blend of the factor ranks. `70+` is the default "good buy" bar in the model.
3. **Drill into the factors** — each factor shows the stock's percentile rank versus the universe, with plain-language help text explaining what it measures.
4. **Check the price history** chart over ranges from one month to all-time.
5. **ETFs** are supported too, with basic fund info (no factor scoring, since factors are company-level).

## What's under the hood

The model goes well beyond a single P/E ratio. The factor families include:

- **Value** and **GARP** (Peter Lynch's PEG idea) — am I paying a reasonable price for the earnings/growth?
- **Momentum (12-1)** — trailing 12-month return excluding the most recent month.
- **Quality / Profitability** and **Capital Efficiency (ROIC)** — how good is the business itself?
- **Financial Strength (Piotroski F-Score)**, **Balance Sheet Strength**, and **Distress Risk (Altman Z)** — how durable is it?
- **Low Volatility**, **Investment (asset growth)**, **Earnings Revisions**, **Earnings Quality (accruals)**, **Shareholder Yield**, **Graham Number Value**, and **Downside Protection**.

Each metric is computed cross-sectionally — i.e. as a **percentile rank against the S&P 500 universe** (sector-adjusted when enabled) — so a score answers "how does this compare to peers?" rather than relying on an arbitrary absolute threshold. The analyst layer aggregates published recommendations into a consensus label and compares the average 12-month price target to today's price to get implied upside.

A companion GitHub Actions job refreshes the universe snapshot daily and can email alerts for watchlist names that clear the good-buy threshold, but that piece runs server-side and isn't part of this embedded dashboard.

## Caveats

This is a personal research tool, **not investment advice**. Factor scores and analyst targets are noisy, backward-looking inputs, and the model can be wrong. Data comes from a free third-party source and may be delayed or occasionally incomplete.
