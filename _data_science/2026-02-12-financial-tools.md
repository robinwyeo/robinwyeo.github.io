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

I built this dashboard to better understand investment fundamentals and as a tool to evalaute US stocks before considering a purchase. Some background reading I found informative when deciding on what metrics to include in this dashboard include Benjamin Graham's [The Intelligent Investor](https://www.goodreads.com/book/show/106835.The_Intelligent_Investor), Howard Mark's [The Most Important Thing: Uncommon Sense for the Thoughtful Investor](https://www.goodreads.com/book/show/10454418-the-most-important-thing), and Peter Lynch's [One Up on Wall Street](https://www.goodreads.com/book/show/762462.One_Up_On_Wall_Street).

Give it any ticker and it scores the company across **15 research-backed factors**, ranks each against the S&P 500, blends them into a single 0–100 composite score, rates whether the current price looks like a bargain, and layers on aggregated Wall Street analyst views. It's a [Streamlit](https://streamlit.io/) app written in Python (see my [GitHub repo](https://github.com/robinwyeo/financial-tools) for source code) using market data from `yfinance`. I've embedded it below so you can try it yourself (though it works slightly better in full screen).

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

A single **relative 0–100** number that blends all available factor ranks into one verdict. A `90` means the stock looks better than ~90% of the S&P 500 once every factor is added together as a weighted sum. Unlike the bargain score, the composite score is a relative rank — it does not, by itself, say whether today's price is cheap.

### Factor Scorecard

The scorecard lays out all 15 factors in four categories: **Valuation**, **Quality/Profitability**, **Financial Health**, and **Market/Sentiment**. Each factor is computed cross-sectionally as a **percentile rank against the S&P 500** (sector-adjusted where possible), so a score answers "how does this stack up against other companies in the S&P500?" rather than leaning on an arbitrary absolute cutoff. Each row shows a percentile rank bar and color-coded dot: <span style="color:#e74c3c">**red (0–30, weak)**</span>, <span style="color:#f1c40f">**yellow (31–70, middling)**</span>, <span style="color:#2ecc71">**green (71–100, strong)**</span>. Factors without enough data show **N/A** in gray.

**Valuation — am I paying a sensible price?**
- **Value** — earnings, book-value, and cash-flow multiples vs peers.

  $$\frac{P}{E}, \quad \frac{P}{B}, \quad \frac{P}{\text{FCF}}$$

- **GARP** — Peter Lynch's PEG idea; growth relative to what you pay for it.

  $$\text{PEG} = \frac{P/E}{\text{EPS Growth Rate (\%)}}$$

- **Graham Number Value** — Benjamin Graham's classic value checks.

  $$G = \sqrt{22.5 \times \text{EPS} \times \text{BVPS}}$$

- **Shareholder Yield** — dividends plus net buybacks as a share of market cap.

  $$\text{Shareholder Yield} = \frac{\text{Dividends} + \text{Net Buybacks}}{\text{Market Cap}}$$

**Quality & Profitability — is the business actually good?**
- **Quality / Profitability** — margins and returns on assets and equity.

  $$\text{ROE} = \frac{\text{Net Income}}{\text{Equity}}, \quad \text{ROA} = \frac{\text{Net Income}}{\text{Total Assets}}$$

- **Capital Efficiency (ROIC)** — operating profit earned per dollar of invested capital.

  $$\text{ROIC} = \frac{\text{NOPAT}}{\text{Invested Capital}}, \quad \text{NOPAT} = \text{EBIT} \times (1 - t)$$

- **Earnings Quality (Accruals)** — how much of reported profit is backed by real cash.

  $$\text{Accrual Ratio} = \frac{\text{Net Income} - \text{Operating Cash Flow}}{\text{Total Assets}}$$

**Financial Health — can it survive and deploy capital wisely?**
- **Financial Strength (Piotroski F-Score)** — a 9-point profitability, leverage, and liquidity checklist.

  $$F = \sum_{i=1}^{9} f_i, \quad f_i \in \{0,\,1\}$$

- **Balance Sheet Strength** — cash cushion vs debt load.

  $$\text{Current Ratio} = \frac{\text{Current Assets}}{\text{Current Liabilities}}, \quad \frac{D}{E} = \frac{\text{Total Debt}}{\text{Equity}}$$

- **Distress Risk (Altman Z)** — the classic 5-ratio bankruptcy-risk model.

  $$Z = 1.2\,X_1 + 1.4\,X_2 + 3.3\,X_3 + 0.6\,X_4 + 1.0\,X_5$$

  $$X_1 = \frac{\text{Working Capital}}{\text{Total Assets}},\quad X_2 = \frac{\text{Retained Earnings}}{\text{Total Assets}},\quad X_3 = \frac{\text{EBIT}}{\text{Total Assets}}$$

  $$X_4 = \frac{\text{Market Cap}}{\text{Total Liabilities}},\quad X_5 = \frac{\text{Revenue}}{\text{Total Assets}}$$

- **Investment (Asset Growth)** — rewards disciplined rather than empire-building asset growth.

  $$\text{Asset Growth} = \frac{\text{Total Assets}_t - \text{Total Assets}_{t-1}}{\text{Total Assets}_{t-1}}$$

**Market & Sentiment — how is the stock behaving in the market?**
- **Momentum (12-1)** — trailing 12-month return, excluding the most recent month.

  $$\text{Mom}_{12\text{-}1} = \frac{P_{t-1} - P_{t-12}}{P_{t-12}}$$

- **Earnings Revisions** — whether analyst estimates are trending up or down.

  $$\text{Revision} = \frac{\hat{E}_{\text{current}} - \hat{E}_{\text{prior}}}{\lvert\hat{E}_{\text{prior}}\rvert}$$

- **Low Volatility** — how steady the price has been.

  $$\sigma_{\text{annual}} = \sigma_{\text{daily}} \times \sqrt{252}$$

- **Downside Protection** — severity of past drawdowns and bad-day moves (Howard Marks–style).

  $$\text{MDD} = \max_{t}\!\left(\frac{P_{\text{peak},t} - P_t}{P_{\text{peak},t}}\right)$$

### Bargain Score

Sitting next to the composite gauge, the Bargain Score answers a different question: *is the stock priced like a deal right now?*. It is an **absolute 0–100** score built from fixed thresholds (not a percentile vs the S&P 500), so higher always means more of a bargain. The model blends five inputs, reweighting over whichever are available:

- **Margin of safety** — how far the price sits below Benjamin Graham's intrinsic-value estimate.

  $$G = \sqrt{22.5 \times \text{EPS} \times \text{BVPS}}, \quad \text{MoS} = \frac{G - P}{G}$$

- **Discount from all-time high** — how much the stock has pulled back from its peak.

  $$\text{ATH Discount} = \frac{P_{\text{ATH}} - P}{P_{\text{ATH}}}$$

- **Discount from 52-week high** — shorter-term drawdown from the yearly peak.

  $$\text{52W Discount} = \frac{P_{52\text{W}} - P}{P_{52\text{W}}}$$

- **RSI oversold** — whether recent selling has pushed the 14-day RSI into oversold territory.

  $$\text{RSI} = 100 - \frac{100}{1 + RS}, \quad RS = \frac{\overline{\text{Gain}}_{14}}{\overline{\text{Loss}}_{14}}$$

- **Analyst upside** — how far the consensus price target sits above today's price.

  $$\text{Upside} = \frac{P_{\text{target}} - P}{P}$$

The label summarizes the score: Bargain (≥ 50), Fair (26–49), or Expensive (&lt; 25).

### Good-buy signal

The dashboard flags a name as a rough **"good buy"** only when all of these pass (and the analyst consensus is not Sell):

| Criterion | Threshold |
| :--- | :--- |
| Composite | ≥ 50.9 |
| Analyst upside | ≥ 15% |
| Bargain | ≥ 43.2 |
| Consensus | Not Sell |

A strong business on factors alone is not enough if the price is stretched; conversely, a deep discount does not qualify if fundamentals or analyst targets do not clear the bar.

### How the weights and thresholds were set

The factor weights, bargain weights, and good-buy thresholds were not chosen by hand. A historical backtest on S&P 500 constituents from **2010–2026** uses SEC EDGAR point-in-time fundamentals and price history to replay a quarterly strategy: invest **$20k** equally across the **top 5** composite-ranked stocks each quarter, hold, and compare return on deployed capital against the same **$20k/quarter SPY** schedule.

**Factor weights** are tuned with **5-fold time-series cross-validation**. Each candidate weight set runs that DCA strategy independently in every fold; the winner is the one with the best `mean(excess ROI) − std(excess ROI)` across folds — rewarding consistency across regimes, not a lucky spike in one period. The current weights (momentum and low-volatility/downside-protection heavy) come from this search.

**Good-buy thresholds** are calibrated separately by bucketing composite and bargain scores against historical forward returns and picking cutoffs where excess return turns reliably positive. **Bargain weights** are tuned to maximize the rank correlation between the bargain score and next-quarter returns.

All live parameters are in [`config.yaml`](https://github.com/robinwyeo/financial-tools/blob/main/config.yaml); the dashboard sidebar shows the current values.

### Analyst Consensus

The analyst layer aggregates published Wall Street ratings into a single consensus label (Buy / Hold / Sell), shows the low, mean, and high 12-month price targets, and computes implied upside — how far that target sits above or below today's price. Implied upside feeds both the Bargain Score and the good-buy check (≥ 15%).

## Caveats

This is a personal research tool, not investment advice. Factor scores and analyst targets are noisy, backward-looking inputs, and the model can be wrong. Data comes from a free third-party source and may be delayed or occasionally incomplete.
