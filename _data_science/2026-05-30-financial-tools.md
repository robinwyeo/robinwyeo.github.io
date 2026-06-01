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

I recently built a stock analysis dashboard and thought I'd host it on my website. Obvious disclaimer - I am not a professional financial analyst and really built this tool to help myself better understand the underlying metrics of stocks for personal investment, and to aggregate data in a central location.

The dashboard takes any ticker and scores it across a broad set of factors — **value**, **momentum**, **quality**, **low volatility**, **financial strength**, and more — then ranks each one against the rest of the S&P 500. Each factor is really just a question I'd want answered before buying: am I paying a sensible price (value)? Is the business actually any good (quality, ROIC)? How durable is it (balance sheet strength, Altman Z, Piotroski F-Score)? All of that gets blended into a single **composite score from 0–100** (the model treats `70+` as its rough "good buy" bar), and on top of the factors it pulls in aggregated Wall Street analyst ratings, average price targets, and the implied upside versus today's price.

Under the hood it's a [Streamlit](https://streamlit.io/) app written in Python ([source on GitHub](https://github.com/robinwyeo/financial-tools)), pulling market data from `yfinance`. Rather than just describe it, I've embedded the live dashboard right here so you can poke at it yourself.

## Try it

<div style="display: flex; align-items: center; gap: 0.6em; margin-bottom: 0.75em;">
  <label for="ticker-input" style="font-weight: 600; white-space: nowrap; font-size: 1em;">Ticker:</label>
  <input
    id="ticker-input"
    type="text"
    placeholder="e.g. AAPL"
    maxlength="10"
    style="padding: 0.45em 0.75em; border: 1px solid #ccc; border-radius: 4px; font-size: 1em; width: 120px; text-transform: uppercase; font-family: monospace;"
  />
  <button
    onclick="loadTicker()"
    style="padding: 0.45em 1.1em; background: #0066cc; color: #fff; border: none; border-radius: 4px; font-size: 1em; cursor: pointer;">
    Load
  </button>
</div>

<iframe
  id="stock-dashboard"
  src="https://robinwyeo-stock-metrics.streamlit.app/?embed=true"
  title="Stock factor scoring & analyst aggregation dashboard"
  style="width: 100%; height: 900px; border: 1px solid #e1e1e1; border-radius: 6px;"
  loading="lazy"
  allow="clipboard-write">
</iframe>

<script>
function loadTicker() {
  var t = document.getElementById('ticker-input').value.trim().toUpperCase();
  if (!t) return;
  document.getElementById('stock-dashboard').src =
    'https://robinwyeo-stock-metrics.streamlit.app/?embed=true&ticker=' + encodeURIComponent(t);
}
document.getElementById('ticker-input').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') loadTicker();
});
</script>

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
