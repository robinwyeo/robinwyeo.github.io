---
title: "A financial analysis dashboard for evaluating stocks "
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

I built this dashboard to understand the metrics behind a stock before buying, and to keep that data in one place. Quick disclaimer: I'm not a professional financial analyst and this isn't investment advice.

Give it any ticker and it scores the company across **15 research-backed factors**, ranks each against the S&P 500, blends them into a single **0–100 composite score**, and layers on aggregated Wall Street analyst views. It's a [Streamlit](https://streamlit.io/) app written in Python (see my [GitHub repo](https://github.com/robinwyeo/financial-tools) for source code) using market data from `yfinance`. I've embedded it below so you can try it yourself.

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

## How to read it

Everything in the dashboard is normalized to be **relative**. Each factor is computed cross-sectionally as a **percentile rank against the S&P 500** (sector-adjusted where possible), so a score answers "how does this stack up against other companies in the S&P500?" rather than leaning on an arbitrary absolute cutoff. Across the board, **higher always means more favorable** — the tool flips "bad-direction" metrics so that green is always good.

### Composite Score

A single **0–100** number that blends all available factor ranks into one verdict. A `90` means the stock looks better than ~90% of the S&P 500 once every factor is weighed together. The model treats **composite ≥ 60 and implied upside ≥ 15%** as its rough "good buy" bar.

### Factor Scorecard

The scorecard lays out all **15 factors** in four categories (two columns in the UI). Each row shows a percentile rank bar and color-coded dot: <span style="color:#e74c3c">**red (0–30, weak)**</span>, <span style="color:#f1c40f">**yellow (31–70, middling)**</span>, <span style="color:#2ecc71">**green (71–100, strong)**</span>. Factors without enough data show **N/A** in gray.

**Valuation — am I paying a sensible price?**
- **Value** — earnings, book-value, and cash-flow multiples vs peers.
- **GARP** — Peter Lynch's PEG idea; growth relative to what you pay for it.
- **Graham Number Value** — Benjamin Graham's classic value checks.
- **Shareholder Yield** — dividends plus net buybacks as a share of market cap.

**Quality & Profitability — is the business actually good?**
- **Quality / Profitability** — margins and returns on assets and equity.
- **Capital Efficiency (ROIC)** — operating profit earned per dollar of invested capital.
- **Earnings Quality (Accruals)** — how much of reported profit is backed by real cash.

**Financial Health — can it survive and deploy capital wisely?**
- **Financial Strength (Piotroski F-Score)** — a 9-point profitability, leverage, and liquidity checklist.
- **Balance Sheet Strength** — cash cushion vs debt load.
- **Distress Risk (Altman Z)** — the classic 5-ratio bankruptcy-risk model.
- **Investment (Asset Growth)** — rewards disciplined rather than empire-building asset growth.

**Market & Sentiment — how is the stock behaving in the market?**
- **Momentum (12-1)** — trailing 12-month return, excluding the most recent month.
- **Earnings Revisions** — whether analyst estimates are trending up or down.
- **Low Volatility** — how steady the price has been.
- **Downside Protection** — severity of past drawdowns and bad-day moves (Howard Marks–style).

### Analyst Consensus

The analyst layer aggregates published Wall Street ratings into a single **consensus label** (Buy / Hold / Sell), shows the **average 12-month price target**, and computes **implied upside** — how far that target sits above or below today's price.

## Caveats

This is a personal research tool, **not investment advice**. Factor scores and analyst targets are noisy, backward-looking inputs, and the model can be wrong. Data comes from a free third-party source and may be delayed or occasionally incomplete.
