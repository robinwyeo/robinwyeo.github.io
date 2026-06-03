---
title: "A financial analysis dashboard for evaluating stocks "
date: 2026-02-12
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

I built this dashboard to better understand investment fundamentals and as a tool to evalaute US stocks before considering a purchase. Some background reading I found informative when deciding on what tools to include in this dashboard include Benjamin Graham's [The Intelligent Investor](https://www.goodreads.com/book/show/106835.The_Intelligent_Investor), Howard Mark's [The Most Important Thing: Uncommon Sense for the Thoughtful Investor](https://www.goodreads.com/book/show/10454418-the-most-important-thing), and Peter Lynch's [One Up on Wall Street](https://www.goodreads.com/book/show/762462.One_Up_On_Wall_Street).

Give it any ticker and it scores the company across **15 research-backed factors**, ranks each against the S&P 500, blends them into a single **0–100 composite score**, rates whether the current price looks like a **bargain**, and layers on aggregated Wall Street analyst views. It's a [Streamlit](https://streamlit.io/) app written in Python (see my [GitHub repo](https://github.com/robinwyeo/financial-tools) for source code) using market data from `yfinance`. I've embedded it below so you can try it yourself (though it works slightly better in full screen).

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

### Composite Score

A single **relative 0–100** number that blends all available factor ranks into one verdict. A `90` means the stock looks better than ~90% of the S&P 500 once every factor is added together as a weighted sum. Unlike the bargain score, the composite score is a **relative** rank — it does not, by itself, say whether today's price is cheap.

### Factor Scorecard

The scorecard lays out all **15 factors** in four categories: **Valuation**, **Quality/Profitability**, **Financial Health**, and **Market/Sentiment**. Each factor is computed cross-sectionally as a **percentile rank against the S&P 500** (sector-adjusted where possible), so a score answers "how does this stack up against other companies in the S&P500?" rather than leaning on an arbitrary absolute cutoff. Each row shows a percentile rank bar and color-coded dot: <span style="color:#e74c3c">**red (0–30, weak)**</span>, <span style="color:#f1c40f">**yellow (31–70, middling)**</span>, <span style="color:#2ecc71">**green (71–100, strong)**</span>. Factors without enough data show **N/A** in gray.

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

### Bargain Score

Sitting next to the composite gauge, the **Bargain Score** answers a different question: *is the stock priced like a deal right now?*. It is an **absolute 0–100** score built from fixed thresholds (not a percentile vs the S&P 500), so higher always means more of a bargain. The model blends five inputs, reweighting over whichever are available:

- **Margin of safety** — how far the price sits below Benjamin Graham's intrinsic-value estimate.
- **Discount from all-time high** — how much the stock has pulled back from its peak.
- **Discount from 52-week high** — shorter-term drawdown from the yearly peak.
- **RSI oversold** — whether recent selling has pushed the 14-day RSI into oversold territory.
- **Analyst upside** — how far the consensus price target sits above today's price.

The label summarizes the score: **Bargain** (≥ 50), **Fair** (26–49), or **Expensive** (&lt; 25).

### Good-buy signal

The dashboard flags a name as a rough **"good buy"** only when **all** of these pass (and the analyst consensus is not Sell):

| Criterion | Threshold |
| :--- | :--- |
| Composite | ≥ 50 |
| Analyst upside | ≥ 15% |
| Bargain | ≥ 50 |

A strong business on factors alone is not enough if the price is stretched; conversely, a deep discount does not qualify if fundamentals or analyst targets do not clear the bar.

### Analyst Consensus

The analyst layer aggregates published Wall Street ratings into a single **consensus label** (Buy / Hold / Sell), shows the **low, mean, and high 12-month price targets**, and computes **implied upside** — how far that target sits above or below today's price. Implied upside feeds both the Bargain Score and the good-buy check (≥ 15%).

## Caveats

This is a personal research tool, **not investment advice**. Factor scores and analyst targets are noisy, backward-looking inputs, and the model can be wrong. Data comes from a free third-party source and may be delayed or occasionally incomplete.
