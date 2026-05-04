---
title: "Interactive exploration of the Central Limit Theorem"
date: 2024-12-15
tags:
  - Central Limit Theorem
permalink: /data-science/central-limit-theorem/
---

*Jupyter notebook exploring the Central Limit Theorem. On the website this is a static page; interactive sliders run only in the [notebook source](https://github.com/robinwyeo/robinwyeo.github.io/blob/master/_data_science/2024-12-15-central-limit-theorem.ipynb).*

---


# Diving into the Central Limit Theorem

My main reason in writing this script was to better understand the **Central Limit Therorem** (CLT) and to develop a better intuition about its implications.

The CLT is certainly my favorite theorem in all of probability theory and among my favorite theorems in mathematics. Loosely put, the CLT states that the sum of a large number of independent random variables is approximately normally distributed. As a consequence, the CLT helps explain the remarkable observation that the empirical frequencies of so many natural populations exhibit a normal (bell-shaped) curve.

I find it at once deceptively simple and extremely profound; its application allows us to probabilistically evaluate an absurd number of natural phenomena and it's worth diving into.

In this notebook we will:

1. State the theorem precisely and unpack its equation.
2. Run three progressively more exotic simulations that demonstrate the CLT in action.
3. Show a case where the CLT **fails**, to build intuition about its requirements.

Note: in writing this blog post I relied heavily on the excellent textbook **A First Course in Probability by Sheldon Ross** as well as my course notes from undergraduate and graduate probability classes (specifically MIT 18.440, Stanford STATS116, and Stanford STATS200)


---

## 1) Formal Statement of CLT

Let \(X_1, X_2, \dots, X_n\) be **independent and identically distributed** (i.i.d.) random variables drawn from *any* distribution with:

- finite mean \(\mu = E\text{[}X_{i}\text{]}\)
- finite variance \(\sigma^2 = \text{Var}(X_{i}) > 0\)

Define the sample mean:

$$
\bar{X}_n = \frac{X_1 + X_2 + \dots + X_n}{n} = \frac{1}{n}\sum_{i=1}^{n} X_i
$$

Then the CLT states that the **standardized** sample mean converges in distribution to a standard normal distribution:

$$\boxed{\frac{\bar{X}_n - \mu}{\sigma \, / \, \sqrt{n}} \;\xrightarrow{\;d\;}\; \mathcal{N}(0,\,1) \quad \text{as } n \to \infty}$$

That is, for \(-\infty < a < \infty\),

$$\boxed{
P\left(
    \frac{X_1 + \cdots + X_n - n\mu}{\sigma \sqrt{n}} \leq a
\right)
\;\longrightarrow\;
\frac{1}{\sqrt{2\pi}} \int_{-\infty}^{a} e^{-x^2/2} \, dx
\qquad \text{as } n \to \infty}
$$

### Key requirements

1. **Independence.** The probability of any outcome for one observation does not depend on the outcomes of the others.
2. **Finite variance.** If \(\sigma^2 = \infty\) (e.g. the Cauchy distribution), the CLT does not apply and sample means do *not* become normal.

Notice what is **not** required: the population does not need to be continuous, symmetric, unimodal, or anywhere close to normal. That generality is what makes the CLT so powerful.


In layman's terms, the above tells us that:

> *When you average enough independent observations, the distribution of that average is approximately normal — no matter how the original data was distributed.*


---

## Setup



```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from IPython.display import display, clear_output
import ipywidgets as widgets

np.random.seed(42)

sns.set_theme(style="whitegrid", font_scale=1.1)
PALETTE = sns.color_palette("mako", 6)

%matplotlib inline


def plot_clt_grid(
    sample_sizes,
    sample_fn,
    pop_mean,
    pop_std,
    num_trials=50_000,
    suptitle="",
    raw_label="Raw population",
):
    """Draw a grid of histograms showing sample-mean distributions for various n.

    Parameters
    ----------
    sample_sizes : list[int]
        Values of n to illustrate.
    sample_fn : callable(size) -> np.ndarray
        Function that draws `size` i.i.d. samples from the population.
    pop_mean, pop_std : float
        True population mean and standard deviation.
    num_trials : int
        How many sample means to compute for each n.
    suptitle : str
        Figure title.
    raw_label : str
        Label for the n=1 panel.
    """
    ncols = len(sample_sizes)
    fig, axes = plt.subplots(1, ncols, figsize=(5 * ncols, 4.5))
    if ncols == 1:
        axes = [axes]

    for ax, n, color in zip(axes, sample_sizes, PALETTE):
        means = np.array(
            [sample_fn(n).mean() for _ in range(num_trials)]
        )

        ax.hist(means, bins=60, density=True, alpha=0.65, color=color, edgecolor="white", linewidth=0.4)

        se = pop_std / np.sqrt(n)
        x = np.linspace(means.min(), means.max(), 300)
        ax.plot(x, stats.norm.pdf(x, pop_mean, se), "k--", lw=2, label="CLT normal")

        label = raw_label if n == 1 else f"n = {n}"
        ax.set_title(label, fontweight="bold")
        ax.set_xlabel("Sample mean")
        ax.set_ylabel("Density" if ax is axes[0] else "")
        ax.legend(fontsize=9)

    fig.suptitle(suptitle, fontsize=15, fontweight="bold", y=1.03)
    fig.tight_layout()
    plt.show()


def clt_interactive_plot(
    sample_fn,
    pop_mean,
    pop_std,
    suptitle="",
    raw_label="Raw population",
    num_trials=15_000,
    n_default=30,
    color_index=0,
):
    """Histogram of sample means with a slider for n in [1, 1000] (ipywidgets)."""
    out = widgets.Output(
        layout={
            "border": "1px solid #ddd",
            "max_height": "520px",
            "overflow": "auto",
        }
    )
    slider = widgets.IntSlider(
        value=min(max(int(n_default), 1), 1000),
        min=1,
        max=1000,
        step=1,
        continuous_update=False,
        description="Sample size n",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="480px"),
    )

    def redraw(n):
        means = np.array([sample_fn(n).mean() for _ in range(num_trials)])
        se = pop_std / np.sqrt(n)
        color = PALETTE[color_index % len(PALETTE)]
        with out:
            clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.hist(
                means,
                bins=60,
                density=True,
                alpha=0.65,
                color=color,
                edgecolor="white",
                linewidth=0.4,
            )
            x = np.linspace(means.min(), means.max(), 300)
            ax.plot(x, stats.norm.pdf(x, pop_mean, se), "k--", lw=2, label="CLT normal")
            label = raw_label if n == 1 else f"n = {n}"
            ax.set_title(label, fontweight="bold")
            ax.set_xlabel("Sample mean")
            ax.set_ylabel("Density")
            ax.legend(fontsize=9)
            if suptitle:
                fig.suptitle(suptitle, fontsize=14, fontweight="bold", y=1.02)
            fig.tight_layout()
            plt.show()
            plt.close(fig)

    def on_change(change):
        redraw(change["new"])

    slider.observe(on_change, names="value")
    display(widgets.VBox([slider, out]))
    redraw(slider.value)
```

---

## 2.1) Rolling dice (Discrete Uniform Distribution)

Let's start by imagining a probablistic experiment involving a fair 6-sided die. A single roll produces one of \(\{1,2,3,4,5,6\}\) with equal probability \(1/6\). This distribution is:

- **Discrete** (only six values)
- **Uniform**

The first and second population moments are:

$$\mu = \frac{1+2+3+4+5+6}{6} = 3.5$$

$$\sigma^2 = \frac{1}{6}\sum_{k=1}^{6}(k - 3.5)^2 = \frac{35}{12} \approx 2.917$$

So, this discrete uniform distribution has mean 3.5 and variance 2.917. The then CLT predicts that the distribution of \(\bar{X}_n\) (the mean of \(n\) rolls) will be approximately normal (with distribution \(\mathcal{N}(3.5,\; 2.917/n)\)) for large \(n\).

What's amazing about the CLT is that despite the fact that the value of a dice roll is given by a uniform distribution, the distribution of its **sample mean** (as n grows large) is normal!


### Simulation

Let's now plot a simulation of n repeated rolls of a six-sided die to develop some intuition about the Central Limit Theorem (CLT).
- We model rolling a die n times, and repeat this for many repeated trials (50,000 in this simulation).
- For each trial, we calculates the mean of n die rolls.
- We then visualize the distribution of these sample means as n changes, showing how it approaches a normal distribution as n gets larger.
- The interactive plot in the notebook lets you adjust \(n\) and watch the sample means transition from the original uniform distribution (\(n=1\)) to an increasingly bell-shaped (normal) curve for large \(n\).
- Below, static figures show representative behavior at several values of \(n\).



```python
die_mean = 3.5
die_std = np.sqrt(35 / 12)

clt_interactive_plot(
    sample_fn=lambda n: np.random.randint(1, 7, size=n),
    pop_mean=die_mean,
    pop_std=die_std,
    suptitle="CLT with Dice Rolls (Discrete Uniform)",
    raw_label="Single roll (n = 1)",
    n_default=30,
    color_index=0,
)
```

Another way to see the convergence is to overlay smooth kernel density estimates (KDEs) for several values of \(n\) on a single axis. This makes it easy to watch the distribution tighten and reshape itself into a bell curve.



```python
fig, ax = plt.subplots(figsize=(9, 5))

kde_ns = [1, 3, 10, 30]  # Removed n=2
colors = sns.color_palette("viridis", len(kde_ns))

for n, c in zip(kde_ns, colors):
    means = np.array([np.random.randint(1, 7, size=n).mean() for _ in range(80_000)])
    sns.kdeplot(means, ax=ax, color=c, lw=2.2, label=f"n = {n}", clip=(0.5, 6.5))

se_30 = die_std / np.sqrt(30)
x = np.linspace(1, 6, 300)
ax.plot(x, stats.norm.pdf(x, die_mean, se_30), "k--", lw=2, label="N(3.5, σ²/30)")

ax.set_title("KDE Overlay — Dice Sample Means Converging to Normal", fontweight="bold", fontsize=13)
ax.set_xlabel("Sample mean")
ax.set_ylabel("Density")
ax.legend(title="Sample size", fontsize=9, title_fontsize=10)
fig.tight_layout()
plt.show()
```


    
![png](/images/data-science/central-limit-theorem/2024-12-15-central-limit-theorem_10_0.png)
    


**What to notice:**

- At \(n = 1\) the histogram is flat — the raw uniform distribution.
- At \(n = 3\) the bell curve begins to appear though with clear discrete values (since its simply the convolution of 3 uniform distributions).
- At \(n = 10\) there is a recognizable bell curve shape though not perfectly normal.
- At \(n = 30\) the fit to the theoretical normal (dashed line) distribution is nearly perfect.

Because the die is symmetric, convergence is fast (as seen above with convergence occuring by \(n = 30\) ). In the next section we'll explore a distribution that is far from symmetric, and see how well the CLT handles that.


---

## 2.2) Customer Wait Times (Exponential Distribution)

For this next example, imagine you're measuring how long customers wait on a support hotline and want to probabilistically model wait time duration.

This is a classic example in many introductory statistics textbooks that can be modeled by an **exponential distribution**:

$$\boxed{f(x) = \lambda e^{- \lambda x}, \quad x \geq 0}$$

Thus, the cumulative distribution function F(a) of an exponential random variable is given by:

$$
F(a) = P(X \leq a) = \int_{0}^{a} \lambda e^{-\lambda x}\,dx = 1 - e^{-\lambda a}, \quad a \geq 0
$$

Exponential distributions have the following properties:

- **Continuous** (for \(x \geq 0\))
- **Heavily right-skewed** (most waits are short, but a few are very long - see PDF plot below)


To simplify things for an example below, let's set \(\lambda = 1\). Then the probability density function \(f(x)\) and cumulative distribution function \(F(a)\) simplify to:

$$f(x) = e^{-x}, \quad x \geq 0, \qquad \mu = 1, \qquad \sigma = 1$$

$$F(a) = 1 - e^{-a}, \quad a \geq 0$$

Now let's plot \(f(x)\) and \(F(a)\) for our exponential distribution with \(\lambda = 1\).



```python
x = np.linspace(0, 8, 500)
pdf = np.exp(-x)
cdf = 1 - np.exp(-x)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(x, pdf, color=PALETTE[1], label="PDF")
axes[0].set_title("Exponential PDF ($\\lambda=1$)")
axes[0].set_xlabel("x")
axes[0].set_ylabel("Density")
axes[0].grid(True, linestyle='--', alpha=0.6)
axes[0].legend()

axes[1].plot(x, cdf, color=PALETTE[2], label="CDF")
axes[1].set_title("Exponential CDF ($\\lambda=1$)")
axes[1].set_xlabel("x")
axes[1].set_ylabel("Cumulative Probability")
axes[1].grid(True, linestyle='--', alpha=0.6)
axes[1].legend()

plt.tight_layout()
plt.show()
```


    
![png](/images/data-science/central-limit-theorem/2024-12-15-central-limit-theorem_14_0.png)
    


Interpretation of the Plots:

- **Left Plot (PDF):** This shows the probability density function (PDF) of the exponential distribution with λ = 1. For continuous distributions, the PDF provides the relative probability that the random variable would be equal to at that point; note that the PDF of any exact value is always zero and that it's the *area under the curve* (equivalent to the CDF) over an interval that actually gives probabilities. For our exponential distribution, the high PDF value at low x values indicates that very short wait times are much more probable than long ones, but there exists a right-sided tail of long wait times with increasingly low probabilities.

- **Right Plot (CDF):** This shows the cumulative distribution function (CDF), representing the probability that a random wait time is less than or equal to a particular value x. The CDF starts at 0 and rises toward 1 as x increases, illustrating that as you allow for longer wait times, the probability of having observed your event increases, eventually approaching certainty.


### Simulation

Now that we've gone over the basics of exponential distributions, let's see how the CLT handles it!



```python
exp_mean = 1.0
exp_std = 1.0

clt_interactive_plot(
    sample_fn=lambda n: np.random.exponential(scale=1.0, size=n),
    pop_mean=exp_mean,
    pop_std=exp_std,
    suptitle="CLT with Exponential Distribution (Wait Times)",
    raw_label="Single draw (n = 1)",
    n_default=30,
    color_index=1,
)
```

Setting \(n=1\), we recapitulate the probability density function of the exponential distribution (which is obviously not normal). As we increase our sample size \(n\), the histogram looks increasingly like a normal bell curve which is shifted slightly to the left (due to the left-handed skew of exponential distributions). As \(n\) gets ioncreasingly large, the CLT demonstrates that the sample mean distrbituion does indeed converge to a standard normal curve.


### Normality checks

Now let's perform two different checks for normality at three different increasing values of \(n\):
- generating Q-Q plots
- fitting the empirical CDF to the normal CDF


First let's add **Q-Q plots** for \(n = 5\), \(n = 30\), and \(n = 100\) for a more empirical evaluation of whether these distributions at different \(n\) values are truly normal. Q-Q plots are used to assess if an empirical distribution matches a theoretical normal distribution (often used in science to evaluate if a particular stasticial significant test that requires normality, such as a t-test, is appropriate for a given dataset). If the distributions of the sample mean at \(n = 5\), \(n = 30\), and \(n = 100\) are truly normal, the points will lie on a straight line in the below Q-Q plots.



```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

for ax, n in zip(axes, [5, 30, 100]):
    means = np.array(
        [np.random.exponential(1.0, size=n).mean() for _ in range(50_000)]
    )
    stats.probplot(means, dist="norm", plot=ax)
    ax.set_title(f"Q-Q Plot (n = {n})", fontweight="bold")
    ax.get_lines()[0].set(markerfacecolor=PALETTE[2], markeredgecolor="white", markersize=3)
    ax.get_lines()[1].set(color="black", linestyle="--")

fig.suptitle("Normality Check for Exponential Sample Means", fontsize=14, fontweight="bold", y=1.03)
fig.tight_layout()
plt.show()
```


    
![png](/images/data-science/central-limit-theorem/2024-12-15-central-limit-theorem_21_0.png)
    


Now let's compare the empirical CDF of the sample means directly against the theoretical normal CDF. Where the two curves overlap, the CLT approximation is working well.



```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
ecdf_ns = [5, 30, 100]
colors_ecdf = sns.color_palette("mako", len(ecdf_ns))

for ax, n, color in zip(axes, ecdf_ns, colors_ecdf):
    means = np.sort(
        np.array([np.random.exponential(1.0, size=n).mean() for _ in range(50_000)])
    )
    ecdf_y = np.arange(1, len(means) + 1) / len(means)

    se = exp_std / np.sqrt(n)
    theory_y = stats.norm.cdf(means, exp_mean, se)

    ax.step(means, ecdf_y, color=color, lw=1.5, label="Empirical CDF")
    ax.plot(means, theory_y, "k--", lw=2, label="Normal CDF")
    ax.set_title(f"n = {n}", fontweight="bold")
    ax.set_xlabel("Sample mean")
    ax.set_ylabel("Cumulative probability" if ax is axes[0] else "")
    ax.legend(fontsize=9, loc="lower right")

fig.suptitle("Empirical vs. Theoretical Normal CDF — Exponential Means",
             fontsize=14, fontweight="bold", y=1.03)
fig.tight_layout()
plt.show()
```


    
![png](/images/data-science/central-limit-theorem/2024-12-15-central-limit-theorem_23_0.png)
    


**What to notice:**

- At \(n = 1\) the histogram is the raw exponential — a sharp spike near zero with a long right tail.
- At \(n = 5\) the skew is still visible but softening.
- At \(n = 30\) the histogram is convincingly bell-shaped, and the Q-Q plot is close to linear with only mild deviation in the tails.
- At \(n = 100\) the normal fit is excellent though the Q-Q plot still displays some mild deviation in the tails.

Because the exponential distribution has a skewness of 2, it takes a larger \(n\) to reach normality compared to the symmetric die. This is a general pattern: **the more skewed or heavy-tailed the population, the more samples you need for CLT to hold**.


---

## 2.3 A Custom Bimodal Mixture ("Weird" Distribution)

To really stress-test the CLT, let's construct a distribution that is deliberately weird — **bimodal, asymmetric, and with unequal spread in each mode**.

Define \(X\) as a mixture:

$$X \sim 0.3\;\mathcal{N}(-4,\, 1) \;+\; 0.7\;\mathcal{N}(5,\, 4)$$

### Deriving the population moments

For a mixture \(X = \begin{cases} Y_1 & \text{with prob } p \\ Y_2 & \text{with prob } 1-p \end{cases}\) where \(p = 0.3\), \(Y_1 \sim \mathcal{N}(\mu_1, \sigma_1^2)\), \(Y_2 \sim \mathcal{N}(\mu_2, \sigma_2^2)\):

We can calculate the mean and variance as follows:

$$\mu = p\,\mu_1 + (1-p)\,\mu_2 = 0.3(-4) + 0.7(5) = -1.2 + 3.5 = 2.3$$

$$\sigma^2 = \underbrace{p\,\sigma_1^2 + (1-p)\,\sigma_2^2}_{\text{within-component}} + \underbrace{p(1-p)(\mu_1 - \mu_2)^2}_{\text{between-component}} = 0.3(1) + 0.7(4) + 0.3 \times 0.7 \times (-4-5)^2 = 0.3 + 2.8 + 17.01 = 20.11$$

Even though this is a weird-looking bimodal distrubution we've built, recall from the introduction that the only two key requirements for the CLT to hold are **independence** and **finite variance**, both of which are satisfied by our above constructed mixture.

Now let's see what this distribution looks like and convince ourselves that the CLT can still pull sample means toward a normal distrbution.



```python
P_MIX = 0.3
MU1, SIGMA1 = -4.0, 1.0
MU2, SIGMA2 = 5.0, 2.0

MIX_MEAN = P_MIX * MU1 + (1 - P_MIX) * MU2
MIX_VAR = P_MIX * SIGMA1**2 + (1 - P_MIX) * SIGMA2**2 + P_MIX * (1 - P_MIX) * (MU1 - MU2) ** 2
MIX_STD = np.sqrt(MIX_VAR)

print(f"Mixture mean  μ = {MIX_MEAN}")
print(f"Mixture var   σ² = {MIX_VAR}")
print(f"Mixture std   σ = {MIX_STD:.4f}")


def sample_mixture(n):
    """Draw n i.i.d. samples from the bimodal mixture."""
    component = np.random.binomial(1, 1 - P_MIX, size=n)
    return np.where(
        component,
        np.random.normal(MU2, SIGMA2, size=n),
        np.random.normal(MU1, SIGMA1, size=n),
    )
```

    Mixture mean  μ = 2.3
    Mixture var   σ² = 20.11
    Mixture std   σ = 4.4844



```python
x_grid = np.linspace(-10, 14, 500)
mixture_pdf = P_MIX * stats.norm.pdf(x_grid, MU1, SIGMA1) + (1 - P_MIX) * stats.norm.pdf(x_grid, MU2, SIGMA2)

fig, ax = plt.subplots(figsize=(8, 4))
ax.fill_between(x_grid, mixture_pdf, alpha=0.4, color=PALETTE[3])
ax.plot(x_grid, mixture_pdf, color=PALETTE[3], lw=2)
ax.axvline(MIX_MEAN, color="black", ls="--", lw=1.5, label=f"μ = {MIX_MEAN}")
ax.set_title("Bimodal Mixture Distribution", fontweight="bold", fontsize=13)
ax.set_xlabel("x")
ax.set_ylabel("Density")
ax.legend()
fig.tight_layout()
plt.show()
```


    
![png](/images/data-science/central-limit-theorem/2024-12-15-central-limit-theorem_27_0.png)
    


This is decidedly not bell-shaped — we've constructed a distribution with two humps of different heights and different widths.

Now let's take sample means.



```python
clt_interactive_plot(
    sample_fn=sample_mixture,
    pop_mean=MIX_MEAN,
    pop_std=MIX_STD,
    suptitle="CLT with the Bizarre Bimodal Mixture",
    raw_label="Single draw (n = 1)",
    n_default=30,
    color_index=2,
)
```

### Normality Check

Now let's introduce a new quantitative check for normality: the **Shapiro-Wilk test** which tests the null hypothesis that a sample comes from a normally distributed population. If the p-value is large (commonly above 0.05), we do not have enough evidence to reject normality, suggesting the data are consistent with a normal distribution. A small p-value indicates the data are unlikely to be normal.

Lety's use Python's *stats* package to calculate the Shapiro-Wilk test for increasing \(n\) below.



```python
np.random.seed(5)
print(f"{'n':>5}   {'Shapiro-Wilk p-value':>22}   Interpretation")
print("-" * 58)

for n in [2, 5, 10, 30, 50, 100, 250, 500]:
    means = np.array([sample_mixture(n).mean() for _ in range(5_000)])
    _, p_val = stats.shapiro(means)
    tag = "≈ normal" if p_val > 0.05 else "not yet normal"
    print(f"{n:>5}   {p_val:>22.6f}   {tag}")
```

        n     Shapiro-Wilk p-value   Interpretation
    ----------------------------------------------------------
        2                 0.000000   not yet normal
        5                 0.000000   not yet normal
       10                 0.000003   not yet normal
       30                 0.000011   not yet normal
       50                 0.008947   not yet normal
      100                 0.133341   ≈ normal
      250                 0.080117   ≈ normal
      500                 0.647815   ≈ normal


As you can see above, the Shapiro-Wilk test tells us that with increasing \(n\), the distribution of the sample mean does indeed become normal.


---

## 3) When the CLT Fails — The Cauchy Distribution

Everything above relied on the population having **finite variance**. What happens when that condition is violated?

The **Cauchy distribution** (equivalently, a \(t\)-distribution with 1 degree of freedom) has PDF:

$$f(x) = \frac{1}{\pi(1 + x^2)}$$

Its tails are so heavy that neither the mean nor the variance exist (\(E\text{[}|X|\text{]} = \infty\)). Remarkably, the distribution of the sample mean of \(n\) Cauchy draws is *itself* Cauchy — no matter how large \(n\) is!



```python
fig, axes = plt.subplots(1, 4, figsize=(20, 4.5))
cauchy_ns = [1, 10, 100, 1000]

for ax, n, color in zip(axes, cauchy_ns, PALETTE):
    means = np.array(
        [np.random.standard_cauchy(n).mean() for _ in range(50_000)]
    )
    trimmed = means[np.abs(means) < 20]  # trim for visibility
    ax.hist(trimmed, bins=120, density=True, alpha=0.65, color=color, edgecolor="white", linewidth=0.3)

    x = np.linspace(-20, 20, 500)
    # Plot Cauchy PDF
    ax.plot(x, stats.cauchy.pdf(x), "k--", lw=2, label="Cauchy PDF")
    # Plot Normal PDF with sample mean and std (red dashed)
    mean_trimmed = np.mean(trimmed)
    std_trimmed = np.std(trimmed)
    ax.plot(x, stats.norm.pdf(x, loc=mean_trimmed, scale=std_trimmed), color="red", linestyle="--", lw=2, label="Normal PDF")

    ax.set_title(f"n = {n}", fontweight="bold")
    ax.set_xlabel("Sample mean")
    ax.set_ylabel("Density" if ax is axes[0] else "")
    ax.set_xlim(-20, 20)
    ax.legend(fontsize=9)

fig.suptitle("Cauchy Sample Means — The CLT Does NOT Apply", fontsize=15, fontweight="bold", y=1.03)
fig.tight_layout()
plt.show()
```


    
![png](/images/data-science/central-limit-theorem/2024-12-15-central-limit-theorem_34_0.png)
    


**What to notice:**

- The histograms look essentially the same for \(n = 1\), \(n = 10\), \(n = 100\), and even \(n = 1000\).
- The (blue dashed) Cauchy distribution nicely fits every histogram and the distribution of the sample mean does **not** converge to the (red dashed) normal distribution as \(n\) grows.


---

## Conclusion

We tested the Central Limit Theorem against three very different distributions:

| Simulation | Distribution | Key property | Convergence speed |
|---|---|---|---|
| 1 | Discrete uniform (die) | Symmetric, discrete, flat | Fast (\(n \approx 5\) already looks normal) |
| 2 | Exponential | Continuous, heavily right-skewed | Moderate (\(n \approx 30\) needed) |
| 3 | Bimodal mixture | Two modes, asymmetric, wide | Moderate-to-slow (\(n \approx 30\text{–}50\)) |

In all three cases we see that the CLT holds: sample means became approximately normal as \(n\) grew. In contrast, simulating a Cauchy distribution (which violates the finite variance requirement of the CLT) showed us that its sample means never become normal no matter how large \(n\) gets.

### Practical implications

- **Confidence intervals** (\(\bar{x} \pm z^* \sigma / \sqrt{n}\)) work because the CLT guarantees that \(\bar{X}_n\) is approximately normal.
- **Hypothesis tests** (z-tests, t-tests for large \(n\)) rely on the same guarantee.
- **Polling and survey sampling**: the margin of error in an election poll is a direct application of the CLT.
- **A/B testing**: when you compare conversion rates between two groups, the CLT justifies using a normal approximation for the difference in proportions.

