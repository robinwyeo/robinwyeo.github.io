---
title: "Exploring bird diversity with AviList"
date: 2026-05-12
tags:
  - AviList
  - ornithology
  - birds
  - taxonomy
  - conservation
permalink: /data-science/ebird-avilist/
header:
  teaser: /images/data-science/avilist/title.png
---

![AviList title image](/images/data-science/avilist/title.png)

{% raw %}
Bird taxonomy dates back to 1758 when Carl Linnaeus, the "father of modern taxonomy", recognized 554 species of birds in the tenth edition of *Systema Naturae*. Since then the birds (which in taxonomy are represented by the class *Ave*) have become, by far, the most thoroughly described and well-characterized taxonomic class on the planet with over 10,000 species described. Furthermore, there is good reason to believe that the current species count is vanishingly close to the true global count unlike the current counts for other terrestrial vertebrate groups - mammals (6495 sp), reptiles (11,440 sp), and amphibians (8301 sp) - which are known to be severely undercounted. Despite how well studied they are, there has not always been global consensus on how to classify the various species, genuses, and even orders of birds. Over the last 50 or so years, modern bird taxonomy has been simultaneously described by 4 comprehensive (yet often conflicting) checklists, the two most popular of which are the [Clements Checklist of Birds of the World](https://www.birds.cornell.edu/clementschecklist) (used by the Cornell Lab of Ornithology) and the [International Ornithological Community (IOC) World Bird List](https://www.worldbirdnames.org/new/). 

Back in 2018, ornithologists representing all the world's major zoogeographic regions convened at the International Ornithological Congress in Vancouver to consolidate modern bird taxonomy into a single harmonized list, and in July 2025, **[AviList](https://www.avilist.org/)** was released (see original publication in [Biodiversity and Conservation, 2025](https://link.springer.com/article/10.1007/s10531-025-03120-y)). With global consensus, the first release of the AviList contains **11,131 bird species across 2376 genera, 252 families, and 46 orders**.

![Indochinese-Roller](https://drive.google.com/thumbnail?id=1vL-BvdXWxK5bc5C8pzx6UcHow0oC93i-&sz=w1000)
<br>
_Photo I took of an Indochinese Roller (Coracias affinis) at Angkor Wat in 2024_

Having spent a good chunk of 2025 birding in Southeast Asia and South America, I was excited to dig into this new checklist when I returned from sabbatical and see what I could learn about bird taxonomy, evolution, geography, and conservation. So, I downloaded the [AviList v2025 checklist (11 Jun, extended)](https://www.avilist.org/checklist/v2025/) and decided to generate this data science writeup using Jupyter Notebook to better understand it.

Outline:
1. **History**
2. **Taxonomy**
3. **Evolution**
4. **Geography**
5. **Conservation**


## Setup, data preparation, and dataset overview

<details markdown="1" class="avilist-setup-code">
<summary>Setup code: imports, paths, and plotting defaults</summary>




```python
from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
import seaborn as sns

try:
    from IPython.display import HTML, display
except ImportError:
    display = print
    HTML = lambda x: x


def _repo_root() -> Path:
    p = Path.cwd().resolve()
    for cand in [p, *p.parents]:
        if not (cand / "requirements.txt").exists():
            continue
        if (cand / "python" / "birds_nb.py").is_file():
            return cand
        if (cand / "birds_nb.py").is_file():
            return cand
    return p


REPO_ROOT = _repo_root()
_py = REPO_ROOT / "python"
if (_py / "birds_nb.py").is_file():
    sys.path.insert(0, str(_py))

from birds_nb import (
    CONTINENT_DISPLAY,
    collapse_sunburst_genera_by_family,
    family_label,
    genus_label,
    order_label,
    sp_region_label,
    sunburst_panzoom_viewport,
)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
pd.set_option("display.max_columns", 40)
pd.set_option("display.width", 180)
pd.set_option("display.max_colwidth", 120)
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 110
plt.rcParams["savefig.dpi"] = 130

DATA_DIR = REPO_ROOT / "data" if (REPO_ROOT / "data").is_dir() else REPO_ROOT
AVILIST_XLSX = DATA_DIR / "AviList-v2025-11Jun-extended.xlsx"
LIFELIST_CSV = DATA_DIR / "RWY_ebird_world_life_list.csv"
CACHE = DATA_DIR / ".cache_avilist.pkl.gz"
for p in (AVILIST_XLSX, LIFELIST_CSV):
    assert p.exists(), f"Missing {p}"
print(f"AviList {AVILIST_XLSX.name} ({AVILIST_XLSX.stat().st_size/1e6:.1f} MB) | list {LIFELIST_CSV.name} ({LIFELIST_CSV.stat().st_size/1e3:.1f} KB)")
# Geography choropleth: set EBIRD_API_KEY (free) — https://ebird.org/api/keygen

```

    AviList AviList-v2025-11Jun-extended.xlsx (8.9 MB) | list RWY_ebird_world_life_list.csv (171.8 KB)


</details>


### Data loading and preparation

<details markdown="1" class="avilist-setup-code">
<summary>Setup code: load AviList and derive species tables</summary>




```python
from birds_nb import add_genus_common_example, continents_in, countries_in, load_avilist, regions_in

YEAR_RE = re.compile(r"(1[5-9]\d{2}|20\d{2})")

def _yr(v):
    if not isinstance(v, str):
        return np.nan
    m = YEAR_RE.search(v)
    return float(m[1]) if m else np.nan

# Load + derive all Step 1 working columns in one place.
df_all = load_avilist(AVILIST_XLSX, CACHE)
df_all["Description_year"] = df_all["Authority"].map(_yr)
df_all["Genus"] = df_all["Scientific_name"].astype(str).str.split().str[0]

iucn_order = ["LC", "NT", "VU", "EN", "CR", "EW", "EX", "DD", "NE"]
raw_iucn = df_all["IUCN_Red_List_Category"].fillna("NE").astype(str).str.strip()
raw_iucn = raw_iucn.str.replace(r"^CR.*", "CR", regex=True).where(raw_iucn.isin(iucn_order), "NE")
df_all["IUCN"] = pd.Categorical(raw_iucn, categories=iucn_order, ordered=True)

extinct_raw = df_all["Extinct_or_possibly_extinct"].astype(str).str.strip().str.lower()
df_all["is_extinct"] = extinct_raw.isin({"extinct", "possibly extinct", "yes", "true", "1"}) | df_all["IUCN"].isin(["EX", "EW"])

df_species = df_all[df_all["Taxon_rank"] == "species"].copy().reset_index(drop=True)
df_species = add_genus_common_example(df_species)
df_family = df_all[df_all["Taxon_rank"] == "family"].copy().reset_index(drop=True)
df_order = df_all[df_all["Taxon_rank"] == "order"].copy().reset_index(drop=True)

df_species["Range_continents"] = df_species["Range"].map(continents_in)
df_species["Range_regions"] = df_species["Range"].map(regions_in)
df_species["Range_countries"] = df_species["Range"].map(countries_in)
df_species["N_continents"] = df_species["Range_continents"].map(len)

parsed = (df_species["N_continents"] > 0).sum()
country_parsed = (df_species["Range_countries"].map(len) > 0).sum()
print(
    f"Loaded {len(df_all):,} rows | orders {len(df_order)} | families {len(df_family)} | "
    f"genera {df_species['Genus'].nunique():,} | species {len(df_species):,} | "
    f"continent parsed {parsed:,}/{len(df_species):,} | "
    f"country parsed {country_parsed:,}/{len(df_species):,}"
)

```

    Loaded 33,684 rows | orders 46 | families 252 | genera 2,376 | species 11,131 | continent parsed 5,726/11,131 | country parsed 5,163/11,131


</details>


<details markdown="1" class="avilist-setup-code">
<summary>Setup code: rank counts and dataset overview</summary>




```python
rank_counts = pd.Series({
    "Order": (df_all["Taxon_rank"] == "order").sum(),
    "Family": (df_all["Taxon_rank"] == "family").sum(),
    "Genus": df_species["Genus"].nunique(),
    "Species": (df_all["Taxon_rank"] == "species").sum(),
    "Subspecies": (df_all["Taxon_rank"] == "subspecies").sum(),
})
richest_families = (
    df_species.groupby(["Order", "Family", "Family_English_name"], dropna=False)
    .size().reset_index(name="n_species")
    .sort_values("n_species", ascending=False)
)
richest_orders = (
    df_species.groupby("Order").size()
    .reset_index(name="n_species")
    .sort_values("n_species", ascending=False).head(10)
)

```

</details>


## 1) History

In this section we're going to jump in and start exploring the AviList, starting with some history! One fun thing about the extended data version of AviList is that it has **tons** of metadata so we can ask questions like when and by whom were the most bird species described?

### When were these species described?

Based ont the plots below, the golden age of bird identification was the 19<sup>th</sup> century in which the number of identified birds worldwide exploded from ~2000 to ~10,000. Although the subsequent 20<sup>th</sup> and 21<sup>st</sup> centuries saw a rise in the popularity of recreational birding, the global species count would only rise another ~10% between 1900 and the present (supporting the view that there remain less and less undiscovered species).


```python
year_df = df_species.dropna(subset=["Description_year"]).copy()
year_df["decade"] = (year_df["Description_year"] // 10 * 10).astype(int)
counts = year_df["decade"].value_counts().sort_index()
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].bar(counts.index, counts.values, width=8, color="#3d7ea0")
axes[0].set(xlabel="decade", ylabel="# species described", title="Descriptions by decade")
axes[1].plot(counts.index, counts.cumsum(), lw=2, color="#d83333")
axes[1].set(xlabel="decade", ylabel="cumulative species count", title="Cumulative")
plt.tight_layout()
plt.show()

```


    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_14_0.png)
    


This is not to say that there remain no undiscovered bird species; I extracted the 5 latest species that wwere added to the AviList and printed them below. As you can see, ornithologists and recreational birders are still discovering new species (though interestingly all 5 of the latest discoveries were found in the Malay Archipelago).


```python
print("5 most recent:")
cols = ["Scientific_name", "English_name_AviList", "Family", "Description_year", "Authority"]
for geo in ("Region", "Regions", "Distribution", "Range", "Location", "Geography", "Countries"):
    if geo in year_df.columns:
        cols.append(geo)
        break


def abbrev_authority(x):
    if pd.isna(x):
        return x
    first = str(x).split(";")[0].strip()
    return f"{first} et al." if first else x


recent = year_df.sort_values("Description_year", ascending=False)[cols].head(5).copy()
recent["Authority"] = recent["Authority"].map(abbrev_authority)
recent["Description_year"] = pd.to_numeric(recent["Description_year"], errors="coerce").astype("Int64")
recent
```

    5 most recent:





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Scientific_name</th>
      <th>English_name_AviList</th>
      <th>Family</th>
      <th>Description_year</th>
      <th>Authority</th>
      <th>Range</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2164</th>
      <td>Caprimulgus ritae</td>
      <td>Timor Nightjar</td>
      <td>Caprimulgidae</td>
      <td>2024</td>
      <td>King, BF et al.</td>
      <td>Timor, Rote, and Wetar (eastern Lesser Sundas)</td>
    </tr>
    <tr>
      <th>8186</th>
      <td>Zosterops paruhbesar</td>
      <td>Wangi-wangi White-eye</td>
      <td>Zosteropidae</td>
      <td>2023</td>
      <td>Irham, M et al.</td>
      <td>Wangi-wangi, Wakatobi (Tukangbesi) Islands, off southeastern Sulawesi</td>
    </tr>
    <tr>
      <th>8169</th>
      <td>Zosterops meratusensis</td>
      <td>Meratus White-eye</td>
      <td>Zosteropidae</td>
      <td>2022</td>
      <td>Irham, M et al.</td>
      <td>Meratus Mountains, South Kalimantan, southeastern Borneo</td>
    </tr>
    <tr>
      <th>2836</th>
      <td>Otus bikegila</td>
      <td>Principe Scops Owl</td>
      <td>Strigidae</td>
      <td>2022</td>
      <td>Melo, M et al.</td>
      <td>Príncipe Island (Gulf of Guinea)</td>
    </tr>
    <tr>
      <th>9146</th>
      <td>Cyornis kadayangensis</td>
      <td>Meratus Blue Flycatcher</td>
      <td>Muscicapidae</td>
      <td>2022</td>
      <td>Irham, M et al.</td>
      <td>Meratus Mountains, South Kalimantan, southeastern Borneo</td>
    </tr>
  </tbody>
</table>
</div>



### Who were the most prolific discoverers?

Our old friend Car Linnaeus easily takes the top spot for discovering over 700 bird species; in fact Linnaeus described ~280 new species in 1758 alone. If you've ever gone birding, getting ~280 new lifers in a year is already pretty respectable so it's crazy to think that Linnaeus managed to **discover** ~280 previously unknown species in a year!


```python
from birds_nb import describer_name

df_species["Describer"] = df_species["Authority"].map(describer_name)
top_describers = df_species.query("Describer != ''")["Describer"].value_counts().head(20).iloc[::-1]
fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(top_describers.index, top_describers.values, color=sns.color_palette("mako", n_colors=20))
for i, v in enumerate(top_describers.values):
    ax.text(v + 2, i, str(int(v)), va="center", fontsize=8)
ax.set(xlabel="species described", title="Top discoverers")
plt.tight_layout()
plt.show()

```


    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_18_0.png)
    


A fun part of looking over this plot is recognizing the names of some of the explorers from birds Sara and I have seen. For example, although I know nothing about Coenraad Jacob Temminck the man (I had to google him to learn he was an 18<sup>th</sup> century Dutch zoologist), I do recognize the name from the Temminck's Sunbird _(Aethopyga temminckii)_ and Temminck's Babbler _(Pellorneum pyurogenys)_, both of which we saw in Borneo in 2025. As a side note, there's an ongoing movement advocating that these types of birds should be renamed to something more descriptive/anatomical instead of all being named after dead white European men... time will tell!

## 2) Taxonomy

Now let's jump into the bird list itself! To explore this yourself, you can visit this hyperlink **[AviList v2025 checklist (11 Jun, extended)](https://www.avilist.org/checklist/v2025/)** to download the ~33,000 row excel spreadsheet and take a look at the raw data.


```python
fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
bars = ax.bar(rank_counts.index, rank_counts.values, color="#4C78A8")
ax.set(title="AviList v2025 — Taxon Counts", xticklabels=rank_counts.index)
ax.tick_params(axis="x", rotation=35)
ax.grid(False)
for bar in bars:
    ax.annotate(f"{int(bar.get_height()):,}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", fontsize=10)
plt.show()
```


    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_21_0.png)
    


The newly harmonized AviList has **46 orders, 252 families, 2376 genuses, and 11,131 species**. Fun fact: the world's most prolific (and perhaps greatest?) birder, Peter Kaestner has a life list of 10,036 at the time of writing this and was [the first birder to cross the 10K threshold](https://www.aba.org/peter-kaestner-breaks-the-10000-bird-barrier/) on February 9, 2024; given that the ceiling is now set at 11,131 species, Kaestner has seen ~90.2% of all bird species since his first checklist in 1957 nearly 70 years ago.

### Species richness rankings

Just knowing how many species there are isn't particularly exciting, I want to use the AviList to gain a better understand of species diversity and distribution. So beloww we'll separate out the top Orders and Families by species count.


```python
order_labels = [order_label(o) for o in richest_orders["Order"]]

fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
sns.barplot(data=richest_orders, y=order_labels, x="n_species", ax=ax, color="#F58518")
ax.set_title("Top 10 Orders by Species Count")
ax.set_xlabel("Species")
ax.set_ylabel("")
plt.show()

```


    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_24_0.png)
    


As you can see above, the Passeriformes order **absolutely dominates** species count, accounting for ~60% of all global species. Birds of the order Passeriformes (from the Latin "sparrow-shaped") are more comonly known as passerines or perching birds, and include some North American favorites such as the American Robin _(Turdus migratorius)_, Northern Cardinal _(Cardinalis cardinalis)_, and Black-capped Chickadee _(Poecile atricapillus)_

A natural question follows: **why are there so many passerines**? For some reason, evolution has accelerated speciation of this Order and/or buffered these lineages against extinction. The dominance of the Passeriformes Order (an event referred to as "passerine superradiation") is a classic subject of study and debate in evolutionary biology; the truth behind their global diversity is likely to be some synergistic combination of the following leading hypotheses:
- the evolution of their extraordinatry vocal abilities created a complex and diverse set of mating criteria resulting in reproductive isolation thus accelerating speciation
- their morphological perching adaptation (anisodactyly) conferred a huge competitive advantage, allowing them to easily dwell and build their nests in trees thus minimizing predation
- that dispersion to the Wallacean islands in the Malay Archipelago (30-40 Ma) from where they evolved in Australia ~47 Ma provided frequent opportunity for speciation (similar to Darwin's finches)

So the next time a song sparrow is perching and singing a melody at your birdfeeder, take a moment to appreciate that these two adaptations were likely among the key reasons that perching songbirds dominate bird diversity!


```python
top_fam = richest_families.head(30).iloc[::-1]
fig, ax = plt.subplots(figsize=(10, 9))
ax.barh(top_fam["Family"] + "  (" + top_fam["Family_English_name"].fillna("") + ")", top_fam["n_species"], color=sns.color_palette("viridis", n_colors=30))
for i, v in enumerate(top_fam["n_species"]):
    ax.text(v + 5, i, str(int(v)), va="center", fontsize=8)
ax.set_xlabel("species count")
ax.set_title("Top 30 families")
plt.tight_layout()
plt.show()

```


    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_26_0.png)
    


I next looked at the top 30 bird families by species count which is not nearly as overwhelmed by a single category as bird orders. Interesting to see that Flycatchers (one of my favorite bird families) and Tanagers (another of my favorite bird families) are among the most numerous. Hummingbirds come as no surprise to anyone who has visited South America and seen the mind-boggling diversity of hummingbirds everywhere but there are some surprises in this list too like Thamnophilidae (Antbirds, Antshrikes, Antwrens, and Antvireos) ranking so high! Perhaps this just surprises me because of how frustratingly difficult these birds are to find in the wild.

### Genus size distribution

One taxonomic rung up from species are genera, and I was curious to ask whether most bird genera contain many different species or whether they only have a handful.


```python
gen_sizes = df_species.groupby("Genus").size().values
mono = (
    df_species.groupby(["Family", "Genus"]).size().reset_index(name="n").assign(monotypic=lambda d: d["n"] == 1)
    .groupby("Family").agg(n_genera=("Genus", "size"), n_mono=("monotypic", "sum")).assign(pct_mono=lambda d: d["n_mono"] / d["n_genera"] * 100)
    .query("n_genera >= 5").sort_values("pct_mono", ascending=False).head(15).iloc[::-1]
)
fe = df_family.set_index("Scientific_name")["Family_English_name"].to_dict()
fig, axes = plt.subplots(1, 2, figsize=(13, 4))
axes[0].hist(gen_sizes, bins=range(1, int(gen_sizes.max()) + 2), color="#3d7ea0")
axes[0].set(xlabel="species/genus", ylabel="genera", yscale="log", title="Genus sizes")
axes[1].barh([family_label(f, fe.get(f, "")) for f in mono.index], mono["pct_mono"], color="#d83333")
axes[1].set(xlabel="% monotypic genera", title="Monotypic-heavy families (≥5 genera)")
plt.tight_layout()
plt.show()

```


    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_29_0.png)
    


It turns out that most bird genera are tiny — and hundreds are monotypic (a single species). Interpreting what this means can be challenging: often it can be due to extreme specialization but it can also reflect sole survivors of a once diverse lineage (as in the case of vultures and the osprey) or even just be due to taxonomic splitting by modern ornithologists. On the other hand, there exist a handful of mega-genera (e.g. *Zosterops* white-eyes, *Myzomela* honeyeaters) that dominate the tail of the distribution. These mega-genera are often due to ther emergence of "general" evolutionary adaptations that confer an evolutionary advantage but are flexible enough to generalize to a great number of ecological niches.

### Interactive sunburst plot

Using an interactive **sunburst** plot gives us a nice way to explore the AviList: each ring is a finer rank (Order → Family → Genus), and wedge size corresponds to species count. Click a wedge to drill into that branch and click the center ring of the plot to jump back toward the full tree.

<details markdown="1" class="avilist-setup-code">
<summary>Show code — interactive sunburst</summary>




```python
sb_df = (
    df_species.groupby(["Order", "Family", "Genus"], dropna=False)
    .agg(n_species=("Scientific_name", "size"), Family_English_name=("Family_English_name", "first"), Genus_common_example=("Genus_common_example", "first"))
    .reset_index()
)
# Fewer sunburst sectors → lighter SVG; counts stay exact in aggregated "Other genera" wedges.
sb_df = collapse_sunburst_genera_by_family(sb_df, max_genera_per_family=40)
sb_df["Order_plot"] = sb_df["Order"].map(order_label)
sb_df["Family_plot"] = [family_label(f, e) for f, e in zip(sb_df["Family"], sb_df["Family_English_name"])]
sb_df["Genus_plot"] = [genus_label(g, h) for g, h in zip(sb_df["Genus"], sb_df["Genus_common_example"])]

fig = px.sunburst(
    sb_df,
    path=["Order_plot", "Family_plot", "Genus_plot"],
    values="n_species",
    color="Order",
    color_discrete_sequence=px.colors.qualitative.Bold,
    title="Sunburst Order→Family→Genus",
    width=560,
    height=560,
)

trace = fig.data[0]
id_to_parent = dict(zip(trace.ids, trace.parents))
id_to_label = dict(zip(trace.ids, trace.labels))

orders = []
families = []
genera = []

for node_id in trace.ids:
    parent_id = id_to_parent.get(node_id, "")
    if not parent_id:
        order_plot = id_to_label.get(node_id, "")
        family_plot = ""
        genus_plot = ""
    else:
        grandparent_id = id_to_parent.get(parent_id, "")
        if not grandparent_id:
            order_plot = id_to_label.get(parent_id, "")
            family_plot = id_to_label.get(node_id, "")
            genus_plot = ""
        else:
            order_plot = id_to_label.get(grandparent_id, "")
            family_plot = id_to_label.get(parent_id, "")
            genus_plot = id_to_label.get(node_id, "")

    orders.append(order_plot)
    families.append(family_plot)
    genera.append(genus_plot)

fig.update_traces(
    customdata=list(zip(orders, families, genera, fig.data[0].values)),
    hovertemplate=(
        "Order: %{customdata[0]}<br>"
        "Family: %{customdata[1]}<br>"
        "Genus: %{customdata[2]}<br>"
        "n_species: %{customdata[3]}"
        "<extra></extra>"
    ),
)

fig.update_layout(
    dragmode="pan",
    margin=dict(t=55, l=24, r=24, b=24),
    uirevision="sunburst-aves",
    # Disable layout tween on drill-down / restyle (snappier than Plotly's default ~500ms).
    transition=dict(duration=0, easing="linear"),
)
# responsive=True lets the graph div outgrow the pan-zoom frame, clipping the plot on static sites.
_cfg = {"scrollZoom": True, "displayModeBar": True, "doubleClick": "reset", "responsive": False}
SUNBURST_GD_ID = "sunburst-avilist"
fig_html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, config=_cfg, div_id=SUNBURST_GD_ID)

display(HTML(sunburst_panzoom_viewport(fig_html, SUNBURST_GD_ID, 560, 560)))

```





</details>

<div class="sunburst-panzoom-root" style="width:100%;display:flex;justify-content:center;align-items:center;box-sizing:border-box;padding:6px 0"><iframe src="/assets/data-science/avilist/figures/sunburst-avilist.html" style="width:min(900px,100%);height:980px;border:none;border-radius:8px;display:block;margin:1em auto;" loading="lazy"></iframe>
</div>


## 3) Evolution

### Some evolutionary context: birds in the Mesozoic era

Before we dive into the evolutionary relationships between modern bird lineages, let's step back and discuss a bit of background on how birds evolved in the first place (for further reading, please see these excellent reviews on which I based this summary: [Wu et al., 2025](https://academic.oup.com/nsr/article/12/7/nwaf238/8158921), [Field et al., 2025](https://royalsocietypublishing.org/rsbl/article/21/1/20240500/116002/Whence-the-birds-200-years-of-dinosaurs-avian), and [Claramunt & Cracraft, 2015](https://www.science.org/doi/10.1126/sciadv.1501005)). One of the most exciting recent insights in paleontology and ornithology is the discovery/confirmation that birds really are in fact **modern dinosaurs**; as Field et al. write, _"Among the most revolutionary insights emerging from 200 years of research on dinosaurs is that the clade Dinosauria is represented by approximately 11 000 living species of birds"_.

![Evolution timeline](/images/data-science/avilist/stiller_timeline.png)
<br>
_Source: Stiller et al., 2024_

I should mention that bird evolution is a highly debated and contentious field, and while there is, as of yet, no real consensus among experts, evidence over the last 30 years is starting to paint a clearer picture. During the Mesozoic era (252-66 Ma), also known as the "age of the dinosaurs", the skies were populated by a variety of winged and feathered creatures (such as _Enantiornithes_ and _Hesperornithiformes_) that we now understand to be "stem birds"; although morpholigcally similar to modern birds, these were in fact an evolutionary offshoot, and it was not until the end of this geologic period that "crown birds", scientifically known as **Neornithes** which encompass every known living bird today, began to emerge.

Evidence suggests that the most recent common ancestor of modern birds inhabited South America around 95 million years ago (Ma). Approximately 66 Ma, the Chicxulub asteroid impact triggered the Cretaceous-Paleogene (K-Pg) mass extinction wiping out ~75% of all plant and animal species on Earth, including all non-avian dinosaurs, flying pterosaurs, and the diverse "stem bird" lineages. However the ancestors of modern birds (ground-dwelling Neornithes) survived this mass extinction event and rapidly began diversifying to populate this post-extinction world, a period of time referred to as the "Big Bang of avian evolution". Birds used two main dispersion routes as they rapidly evolved and reclaimed the skies: reaching the Old World through North America, and reaching Australia and Zealandia through Antarctica.


### Evolutionary tree of modern bird species

Now that we have some evolutionary context, let's take a look at an evolutionary tree of all ~11,000 modern bird species! For once the extended AviList alone didn't have all the required metadata for my question so I derived the trees below from **OpenTree of Life** (synthesis v15), which integrates hundreds of published phylogenetic studies including the landmark [**Stiller et al. 2024**](https://www.nature.com/articles/s41586-024-07323-1) *Nature* paper on avian evolution — a whole-genome, time-calibrated phylogeny covering 363 species across 218/252 currently recognised bird families (92% of the total). OpenTree synthesises these studies into a consensus species tree of all ~70,000 living vertebrate lineages, from which I extracted the bird subtree.

Below I've generated an interactive evolutionary tree rendered with **[Phylocanvas.gl](https://phylocanvas.gl)**, a WebGL phylogenetic viewer. Use the mouse to **pan / zoom**, click a node to **expand / collapse** a clade, and hover over any leaf to see the full label. **Click any family leaf** to zoom in on that family and bring up a species-level cladogram (derived from OpenTree, coloured by genus). Use the **← Back to family tree** button to return to the full family view.


<div style="font-family:sans-serif;"><details style="background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:8px 14px;margin-bottom:6px;"><summary style="font-size:12px;font-weight:600;color:#24292f;cursor:pointer;">Legend — bird orders (click to expand)</summary><div style="padding-top:8px;line-height:1.9;"><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#6B4226;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Accipitriformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#74C69D;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Aegotheliformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#F72585;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Anseriformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#74B3CE;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Apodiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#2A9D8F;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Apterygiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#43AA8B;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Bucerotiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#84A98C;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Caprimulgiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#2B9348;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Cariamiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#F4A261;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Casuariiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#5C5C8A;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Cathartiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#AE2012;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Charadriiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#D62828;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Ciconiiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#A7754D;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Coliiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#D00000;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Columbiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#577590;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Coraciiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#8338EC;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Cuculiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#CA6702;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Eurypygiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#80B918;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Falconiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#E9C46A;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Galbuliformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#4CC9F0;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Galliformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#94D2BD;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Gaviiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#9B2226;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Gruiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#CE796B;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Leptosomiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#FFBE0B;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Mesitornithiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#3A86FF;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Musophagiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#2D6A4F;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Nyctibiiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#023E8A;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Opisthocomiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#FF006E;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Otidiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#FFBF69;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Passeriformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#FCBF49;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Pelecaniformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#EE9B00;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Phaethontiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#06D6A0;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Phoenicopteriformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#264653;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Piciformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#40916C;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Podargiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#FB8500;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Podicipediformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#005F73;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Procellariiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#FF9F1C;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Psittaciformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#38B000;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Pterocliformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#457B9D;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Rheiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#0A9396;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Sphenisciformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#52B788;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Steatornithiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#508CA4;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Strigiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#E63946;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Struthioniformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#F77F00;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Suliformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#6A4C93;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Tinamiformes</span></span><span style="display:inline-flex;align-items:center;margin:3px 10px 3px 0;"><span style="width:10px;height:10px;border-radius:50%;background:#C18C5D;flex-shrink:0;margin-right:5px;"></span><span style="font-size:10px;color:#24292f;">Trogoniformes</span></span></div></details><!-- phylocanvas-static-embed -->
<iframe srcdoc="&lt;!DOCTYPE html&gt;&lt;html&gt;&lt;head&gt;&lt;meta charset=&quot;utf-8&quot;&gt;&lt;style&gt;html,body{margin:0;padding:0;background:#ffffff;font-family:sans-serif;}&lt;/style&gt;&lt;/head&gt;&lt;body&gt;&lt;div style=&quot;display:flex;justify-content:space-between;align-items:center;padding:6px 10px;background:#f6f8fa;border:1px solid #d0d7de;border-bottom:none;border-radius:6px 6px 0 0;gap:10px;box-sizing:border-box;&quot;&gt;&lt;span id=&quot;avilist-fam-tree-dd-title&quot; style=&quot;font:13px/1.4 system-ui,Segoe UI,sans-serif;color:#24292f;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;&quot;&gt;All bird families (252) — click a family to see its species&lt;/span&gt;&lt;button id=&quot;avilist-fam-tree-dd-back&quot; hidden style=&quot;flex-shrink:0;padding:3px 10px;font-size:12px;cursor:pointer;border:1px solid #d0d7de;border-radius:5px;background:#fff;color:#24292f;&quot;&gt;← Back to family tree&lt;/button&gt;&lt;/div&gt;&lt;div id=&quot;avilist-fam-tree-fam-search-wrap&quot; class=&quot;phylo-family-picker&quot; style=&quot;font-family:system-ui,Segoe UI,sans-serif;margin:0 0 8px 0;position:relative;max-width:min(560px,96vw);&quot;&gt;&lt;label for=&quot;avilist-fam-tree-fam-search&quot; style=&quot;display:block;font-size:0.82rem;font-weight:600;color:#24292f;margin-bottom:4px;&quot;&gt;Family &lt;span style=&quot;font-weight:400;color:#57606a;&quot;&gt;(type to filter, ↑↓ Enter — &lt;span style=&quot;white-space:nowrap;&quot;&gt;All families&lt;/span&gt; / &lt;span style=&quot;white-space:nowrap;&quot;&gt;Undo&lt;/span&gt; buttons, &lt;span style=&quot;white-space:nowrap;&quot;&gt;⌘/Ctrl+Z&lt;/span&gt; undo)&lt;/span&gt;&lt;/label&gt;&lt;div style=&quot;display:flex;gap:8px;align-items:center;width:100%;&quot;&gt;&lt;div style=&quot;flex:1;min-width:0;position:relative;&quot;&gt;&lt;input id=&quot;avilist-fam-tree-fam-search&quot; type=&quot;text&quot; placeholder=&quot;e.g. Paridae, Thraupidae, Parrot…&quot; autocomplete=&quot;off&quot; spellcheck=&quot;false&quot; role=&quot;combobox&quot; aria-autocomplete=&quot;list&quot; aria-controls=&quot;avilist-fam-tree-fam-suggest&quot; aria-expanded=&quot;false&quot; style=&quot;width:100%;box-sizing:border-box;padding:8px 10px;border:1px solid #d0d7de;border-radius:6px;font-size:14px;outline:none;&quot; /&gt;&lt;div id=&quot;avilist-fam-tree-fam-suggest&quot; role=&quot;listbox&quot; aria-label=&quot;Family suggestions&quot; style=&quot;display:none;position:absolute;left:0;right:0;z-index:100;margin-top:4px;max-height:min(320px,42vh);overflow-y:auto;background:#fff;border:1px solid #d0d7de;border-radius:6px;box-shadow:0 12px 28px rgba(31,35,40,0.18);&quot;&gt;&lt;/div&gt;&lt;/div&gt;&lt;div style=&quot;display:flex;flex-direction:column;gap:5px;flex-shrink:0;&quot;&gt;&lt;button type=&quot;button&quot; id=&quot;avilist-fam-tree-fam-search-all&quot; aria-label=&quot;Show all families, clear highlight&quot; style=&quot;display:inline-flex;align-items:center;justify-content:center;padding:8px 11px;font-size:12px;font-weight:600;line-height:1.2;cursor:pointer;border:1px solid #d0d7de;border-radius:6px;background:#f6f8fa;color:#24292f;white-space:nowrap;font-family:inherit;box-sizing:border-box;&quot;&gt;All families&lt;/button&gt;&lt;button type=&quot;button&quot; id=&quot;avilist-fam-tree-fam-search-undo&quot; aria-label=&quot;Undo last family selection&quot; style=&quot;display:inline-flex;align-items:center;justify-content:center;padding:8px 11px;font-size:12px;font-weight:600;line-height:1.2;cursor:pointer;border:1px solid #d0d7de;border-radius:6px;background:#f6f8fa;color:#24292f;white-space:nowrap;font-family:inherit;box-sizing:border-box;background:#fff;&quot;&gt;Undo&lt;/button&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&lt;div id=&quot;avilist-fam-tree&quot; style=&quot;position:relative;width:100%;height:760px;&quot;&gt;&lt;div id=&quot;avilist-fam-tree-pc&quot; style=&quot;width:100%;height:100%;background:#ffffff;overflow:hidden;&quot;&gt;&lt;/div&gt;&lt;canvas id=&quot;avilist-fam-tree-path-overlay&quot; width=&quot;8&quot; height=&quot;8&quot; style=&quot;position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:3;&quot;&gt;&lt;/canvas&gt;&lt;/div&gt;&lt;script src=&quot;https://unpkg.com/@phylocanvas/phylocanvas.gl@1/dist/bundle.min.js&quot;&gt;&lt;/script&gt;&lt;script&gt;(function () {
  var CONTAINER_ID = &quot;avilist-fam-tree&quot;;
  var NEWICK;
  var META;
  var HEIGHT       = 760;
  var CDN          = &quot;https://unpkg.com/@phylocanvas/phylocanvas.gl@1/dist/bundle.min.js&quot;;
  var STROKE       = [42, 42, 42, 255];
  var FONT         = [26, 26, 26, 255];
  var LINE_W       = 1.75;
  var FAMILY_HOVER = true;
  var DRILLDOWN    = true;
  var DD_MODE      = &quot;fetch&quot;;
  var DD_URL_BASE  = &quot;/assets/data-science/avilist/phylogeny/subtrees/&quot;;
  var DD_SUBTREES  = null;
  var DD_FAM_TITLE = &quot;All bird families (252) \u2014 click a family to see its species&quot;;
  var DD_SP_TYPE   = window.phylocanvas ? window.phylocanvas.TreeTypes[&quot;Rectangular&quot;] : &quot;Rectangular&quot;;
  var FAMILY_SEARCH_ROWS = [{&quot;display&quot;:&quot;Acanthisittidae (New Zealand Wrens)&quot;,&quot;tip&quot;:&quot;Acanthisittidae&quot;},{&quot;display&quot;:&quot;Acanthizidae (Gerygones, Thornbills, Scrubwrens, and Allies)&quot;,&quot;tip&quot;:&quot;Acanthizidae&quot;},{&quot;display&quot;:&quot;Accipitridae (Kites, Old World Vultures, Eagles, and Hawks)&quot;,&quot;tip&quot;:&quot;Accipitridae&quot;},{&quot;display&quot;:&quot;Acrocephalidae (Reed Warblers and Allies)&quot;,&quot;tip&quot;:&quot;Acrocephalidae&quot;},{&quot;display&quot;:&quot;Aegithalidae (Tit-warblers, Bushtits, and Long-tailed Tit)&quot;,&quot;tip&quot;:&quot;Aegithalidae&quot;},{&quot;display&quot;:&quot;Aegithinidae (Ioras)&quot;,&quot;tip&quot;:&quot;Aegithinidae&quot;},{&quot;display&quot;:&quot;Aegothelidae (Owlet-nightjars)&quot;,&quot;tip&quot;:&quot;Aegothelidae&quot;},{&quot;display&quot;:&quot;Alaudidae (Larks)&quot;,&quot;tip&quot;:&quot;Alaudidae&quot;},{&quot;display&quot;:&quot;Alcedinidae (Kingfishers)&quot;,&quot;tip&quot;:&quot;Alcedinidae&quot;},{&quot;display&quot;:&quot;Alcidae (Auks, Puffins, and Murres)&quot;,&quot;tip&quot;:&quot;Alcidae&quot;},{&quot;display&quot;:&quot;Anatidae (Ducks, Swans, and Geese)&quot;,&quot;tip&quot;:&quot;Anatidae&quot;},{&quot;display&quot;:&quot;Anhimidae (Screamers)&quot;,&quot;tip&quot;:&quot;Anhimidae&quot;},{&quot;display&quot;:&quot;Anhingidae (Anhinga and Darters)&quot;,&quot;tip&quot;:&quot;Anhingidae&quot;},{&quot;display&quot;:&quot;Anseranatidae (Magpie Goose)&quot;,&quot;tip&quot;:&quot;Anseranatidae&quot;},{&quot;display&quot;:&quot;Apodidae (Swifts)&quot;,&quot;tip&quot;:&quot;Apodidae&quot;},{&quot;display&quot;:&quot;Apterygidae (Kiwis)&quot;,&quot;tip&quot;:&quot;Apterygidae&quot;},{&quot;display&quot;:&quot;Aramidae (Limpkin)&quot;,&quot;tip&quot;:&quot;Aramidae&quot;},{&quot;display&quot;:&quot;Ardeidae (Herons, Egrets, and Bitterns)&quot;,&quot;tip&quot;:&quot;Ardeidae&quot;},{&quot;display&quot;:&quot;Artamidae (Woodswallows, Bellmagpies, and Allies)&quot;,&quot;tip&quot;:&quot;Artamidae&quot;},{&quot;display&quot;:&quot;Atrichornithidae (Scrubbirds)&quot;,&quot;tip&quot;:&quot;Atrichornithidae&quot;},{&quot;display&quot;:&quot;Balaenicipitidae (Shoebill)&quot;,&quot;tip&quot;:&quot;Balaenicipitidae&quot;},{&quot;display&quot;:&quot;Bernieridae (Malagasy Warblers and Tetrakas)&quot;,&quot;tip&quot;:&quot;Bernieridae&quot;},{&quot;display&quot;:&quot;Bombycillidae (Waxwings)&quot;,&quot;tip&quot;:&quot;Bombycillidae&quot;},{&quot;display&quot;:&quot;Brachypteraciidae (Ground Rollers)&quot;,&quot;tip&quot;:&quot;Brachypteraciidae&quot;},{&quot;display&quot;:&quot;Bucconidae (Puffbirds)&quot;,&quot;tip&quot;:&quot;Bucconidae&quot;},{&quot;display&quot;:&quot;Bucerotidae (Hornbills)&quot;,&quot;tip&quot;:&quot;Bucerotidae&quot;},{&quot;display&quot;:&quot;Buphagidae (Oxpeckers)&quot;,&quot;tip&quot;:&quot;Buphagidae&quot;},{&quot;display&quot;:&quot;Burhinidae (Thick-knees and Stone-curlews)&quot;,&quot;tip&quot;:&quot;Burhinidae&quot;},{&quot;display&quot;:&quot;Cacatuidae (Cockatoos)&quot;,&quot;tip&quot;:&quot;Cacatuidae&quot;},{&quot;display&quot;:&quot;Calcariidae (Longspurs and Snow Buntings)&quot;,&quot;tip&quot;:&quot;Calcariidae&quot;},{&quot;display&quot;:&quot;Callaeidae (New Zealand Wattlebirds)&quot;,&quot;tip&quot;:&quot;Callaeidae&quot;},{&quot;display&quot;:&quot;Calyptomenidae (African and Green Broadbills)&quot;,&quot;tip&quot;:&quot;Calyptomenidae&quot;},{&quot;display&quot;:&quot;Calyptophilidae (Chat-tanagers)&quot;,&quot;tip&quot;:&quot;Calyptophilidae&quot;},{&quot;display&quot;:&quot;Campephagidae (Cuckooshrikes)&quot;,&quot;tip&quot;:&quot;Campephagidae&quot;},{&quot;display&quot;:&quot;Capitonidae (New World Barbets)&quot;,&quot;tip&quot;:&quot;Capitonidae&quot;},{&quot;display&quot;:&quot;Caprimulgidae (Nightjars and Nighthawks)&quot;,&quot;tip&quot;:&quot;Caprimulgidae&quot;},{&quot;display&quot;:&quot;Cardinalidae (Cardinals and Allies)&quot;,&quot;tip&quot;:&quot;Cardinalidae&quot;},{&quot;display&quot;:&quot;Cariamidae (Seriemas)&quot;,&quot;tip&quot;:&quot;Cariamidae&quot;},{&quot;display&quot;:&quot;Casuariidae (Emu and Cassowaries)&quot;,&quot;tip&quot;:&quot;Casuariidae&quot;},{&quot;display&quot;:&quot;Cathartidae (New World Vultures)&quot;,&quot;tip&quot;:&quot;Cathartidae&quot;},{&quot;display&quot;:&quot;Certhiidae (Treecreepers)&quot;,&quot;tip&quot;:&quot;Certhiidae&quot;},{&quot;display&quot;:&quot;Cettiidae (Bush Warblers and Allies)&quot;,&quot;tip&quot;:&quot;Cettiidae&quot;},{&quot;display&quot;:&quot;Chaetopidae (Rockjumpers)&quot;,&quot;tip&quot;:&quot;Chaetopidae&quot;},{&quot;display&quot;:&quot;Charadriidae (Plovers and Lapwings)&quot;,&quot;tip&quot;:&quot;Charadriidae&quot;},{&quot;display&quot;:&quot;Chionidae (Sheathbills)&quot;,&quot;tip&quot;:&quot;Chionidae&quot;},{&quot;display&quot;:&quot;Chloropseidae (Leafbirds)&quot;,&quot;tip&quot;:&quot;Chloropseidae&quot;},{&quot;display&quot;:&quot;Ciconiidae (Storks)&quot;,&quot;tip&quot;:&quot;Ciconiidae&quot;},{&quot;display&quot;:&quot;Cinclidae (Dippers)&quot;,&quot;tip&quot;:&quot;Cinclidae&quot;},{&quot;display&quot;:&quot;Cinclosomatidae (Jewel-babblers and Quail-thrushes)&quot;,&quot;tip&quot;:&quot;Cinclosomatidae&quot;},{&quot;display&quot;:&quot;Cisticolidae (Cisticolas and Allies)&quot;,&quot;tip&quot;:&quot;Cisticolidae&quot;},{&quot;display&quot;:&quot;Climacteridae (Australasian Treecreepers)&quot;,&quot;tip&quot;:&quot;Climacteridae&quot;},{&quot;display&quot;:&quot;Cnemophilidae (Satinbirds)&quot;,&quot;tip&quot;:&quot;Cnemophilidae&quot;},{&quot;display&quot;:&quot;Coliidae (Mousebirds)&quot;,&quot;tip&quot;:&quot;Coliidae&quot;},{&quot;display&quot;:&quot;Columbidae (Doves and Pigeons)&quot;,&quot;tip&quot;:&quot;Columbidae&quot;},{&quot;display&quot;:&quot;Conopophagidae (Gnateaters)&quot;,&quot;tip&quot;:&quot;Conopophagidae&quot;},{&quot;display&quot;:&quot;Coraciidae (Rollers)&quot;,&quot;tip&quot;:&quot;Coraciidae&quot;},{&quot;display&quot;:&quot;Corcoracidae (White-winged Chough and Apostlebird)&quot;,&quot;tip&quot;:&quot;Corcoracidae&quot;},{&quot;display&quot;:&quot;Corvidae (Crows, Jays, and Magpies)&quot;,&quot;tip&quot;:&quot;Corvidae&quot;},{&quot;display&quot;:&quot;Cotingidae (Cotingas)&quot;,&quot;tip&quot;:&quot;Cotingidae&quot;},{&quot;display&quot;:&quot;Cracidae (Guans, Curassows, and Chachalacas)&quot;,&quot;tip&quot;:&quot;Cracidae&quot;},{&quot;display&quot;:&quot;Cuculidae (Cuckoos)&quot;,&quot;tip&quot;:&quot;Cuculidae&quot;},{&quot;display&quot;:&quot;Dasyornithidae (Bristlebirds)&quot;,&quot;tip&quot;:&quot;Dasyornithidae&quot;},{&quot;display&quot;:&quot;Dicaeidae (Flowerpeckers)&quot;,&quot;tip&quot;:&quot;Dicaeidae&quot;},{&quot;display&quot;:&quot;Dicruridae (Drongos)&quot;,&quot;tip&quot;:&quot;Dicruridae&quot;},{&quot;display&quot;:&quot;Diomedeidae (Albatrosses)&quot;,&quot;tip&quot;:&quot;Diomedeidae&quot;},{&quot;display&quot;:&quot;Donacobiidae (Donacobius)&quot;,&quot;tip&quot;:&quot;Donacobiidae&quot;},{&quot;display&quot;:&quot;Dromadidae (Crab-Plover)&quot;,&quot;tip&quot;:&quot;Dromadidae&quot;},{&quot;display&quot;:&quot;Dulidae (Palmchat)&quot;,&quot;tip&quot;:&quot;Dulidae&quot;},{&quot;display&quot;:&quot;Elachuridae (Elachura)&quot;,&quot;tip&quot;:&quot;Elachuridae&quot;},{&quot;display&quot;:&quot;Emberizidae (Old World Buntings)&quot;,&quot;tip&quot;:&quot;Emberizidae&quot;},{&quot;display&quot;:&quot;Erythrocercidae (Yellow Flycatchers)&quot;,&quot;tip&quot;:&quot;Erythrocercidae&quot;},{&quot;display&quot;:&quot;Estrildidae (Munias, Parrotfinches, Waxbills, and Allies)&quot;,&quot;tip&quot;:&quot;Estrildidae&quot;},{&quot;display&quot;:&quot;Eulacestomatidae (Ploughbill)&quot;,&quot;tip&quot;:&quot;Eulacestomatidae&quot;},{&quot;display&quot;:&quot;Eupetidae (Rail-babbler)&quot;,&quot;tip&quot;:&quot;Eupetidae&quot;},{&quot;display&quot;:&quot;Eurylaimidae (Grauer&#x27;s Broadbill and Asian Broadbills)&quot;,&quot;tip&quot;:&quot;Eurylaimidae&quot;},{&quot;display&quot;:&quot;Eurypygidae (Sunbittern)&quot;,&quot;tip&quot;:&quot;Eurypygidae&quot;},{&quot;display&quot;:&quot;Falconidae (Falcons and Caracaras)&quot;,&quot;tip&quot;:&quot;Falconidae&quot;},{&quot;display&quot;:&quot;Falcunculidae (Shriketits)&quot;,&quot;tip&quot;:&quot;Falcunculidae&quot;},{&quot;display&quot;:&quot;Formicariidae (Antthrushes)&quot;,&quot;tip&quot;:&quot;Formicariidae&quot;},{&quot;display&quot;:&quot;Fregatidae (Frigatebirds)&quot;,&quot;tip&quot;:&quot;Fregatidae&quot;},{&quot;display&quot;:&quot;Fringillidae (Finches, Euphonias, and Allies)&quot;,&quot;tip&quot;:&quot;Fringillidae&quot;},{&quot;display&quot;:&quot;Furnariidae (Ovenbirds and Woodcreepers)&quot;,&quot;tip&quot;:&quot;Furnariidae&quot;},{&quot;display&quot;:&quot;Galbulidae (Jacamars)&quot;,&quot;tip&quot;:&quot;Galbulidae&quot;},{&quot;display&quot;:&quot;Gaviidae (Loons)&quot;,&quot;tip&quot;:&quot;Gaviidae&quot;},{&quot;display&quot;:&quot;Glareolidae (Coursers and Pratincoles)&quot;,&quot;tip&quot;:&quot;Glareolidae&quot;},{&quot;display&quot;:&quot;Grallariidae (Antpittas)&quot;,&quot;tip&quot;:&quot;Grallariidae&quot;},{&quot;display&quot;:&quot;Gruidae (Cranes)&quot;,&quot;tip&quot;:&quot;Gruidae&quot;},{&quot;display&quot;:&quot;Haematopodidae (Oystercatchers)&quot;,&quot;tip&quot;:&quot;Haematopodidae&quot;},{&quot;display&quot;:&quot;Heliornithidae (Finfoots)&quot;,&quot;tip&quot;:&quot;Heliornithidae&quot;},{&quot;display&quot;:&quot;Hemiprocnidae (Treeswifts)&quot;,&quot;tip&quot;:&quot;Hemiprocnidae&quot;},{&quot;display&quot;:&quot;Hirundinidae (Swallows)&quot;,&quot;tip&quot;:&quot;Hirundinidae&quot;},{&quot;display&quot;:&quot;Hydrobatidae (Northern Storm Petrels)&quot;,&quot;tip&quot;:&quot;Hydrobatidae&quot;},{&quot;display&quot;:&quot;Hyliidae (Hylias)&quot;,&quot;tip&quot;:&quot;Hyliidae&quot;},{&quot;display&quot;:&quot;Hyliotidae (Hyliotas)&quot;,&quot;tip&quot;:&quot;Hyliotidae&quot;},{&quot;display&quot;:&quot;Hylocitreidae (Hylocitrea)&quot;,&quot;tip&quot;:&quot;Hylocitreidae&quot;},{&quot;display&quot;:&quot;Hypocoliidae (Hypocolius)&quot;,&quot;tip&quot;:&quot;Hypocoliidae&quot;},{&quot;display&quot;:&quot;Ibidorhynchidae (Ibisbill)&quot;,&quot;tip&quot;:&quot;Ibidorhynchidae&quot;},{&quot;display&quot;:&quot;Icteridae (New World Blackbirds, Troupials, and Allies)&quot;,&quot;tip&quot;:&quot;Icteridae&quot;},{&quot;display&quot;:&quot;Ifritidae (Ifrit)&quot;,&quot;tip&quot;:&quot;Ifritidae&quot;},{&quot;display&quot;:&quot;Indicatoridae (Honeyguides)&quot;,&quot;tip&quot;:&quot;Indicatoridae&quot;},{&quot;display&quot;:&quot;Irenidae (Fairy-bluebirds)&quot;,&quot;tip&quot;:&quot;Irenidae&quot;},{&quot;display&quot;:&quot;Jacanidae (Jacanas)&quot;,&quot;tip&quot;:&quot;Jacanidae&quot;},{&quot;display&quot;:&quot;Laniidae (Shrikes)&quot;,&quot;tip&quot;:&quot;Laniidae&quot;},{&quot;display&quot;:&quot;Laridae (Skimmers, Noddies, Terns, and Gulls)&quot;,&quot;tip&quot;:&quot;Laridae&quot;},{&quot;display&quot;:&quot;Leiothrichidae (Laughingthrushes and Allies)&quot;,&quot;tip&quot;:&quot;Leiothrichidae&quot;},{&quot;display&quot;:&quot;Leptosomidae (Cuckoo-roller)&quot;,&quot;tip&quot;:&quot;Leptosomidae&quot;},{&quot;display&quot;:&quot;Locustellidae (Grasshopper Warblers, Grassbirds, and Allies)&quot;,&quot;tip&quot;:&quot;Locustellidae&quot;},{&quot;display&quot;:&quot;Lybiidae (African Barbets)&quot;,&quot;tip&quot;:&quot;Lybiidae&quot;},{&quot;display&quot;:&quot;Machaerirhynchidae (Boatbills)&quot;,&quot;tip&quot;:&quot;Machaerirhynchidae&quot;},{&quot;display&quot;:&quot;Macrosphenidae (Longbills, Crombecs, and Allies)&quot;,&quot;tip&quot;:&quot;Macrosphenidae&quot;},{&quot;display&quot;:&quot;Malaconotidae (Bushshrikes and Allies)&quot;,&quot;tip&quot;:&quot;Malaconotidae&quot;},{&quot;display&quot;:&quot;Maluridae (Grasswrens, Fairywrens, and Emu-wrens)&quot;,&quot;tip&quot;:&quot;Maluridae&quot;},{&quot;display&quot;:&quot;Megalaimidae (Asian Barbets)&quot;,&quot;tip&quot;:&quot;Megalaimidae&quot;},{&quot;display&quot;:&quot;Megapodiidae (Megapodes)&quot;,&quot;tip&quot;:&quot;Megapodiidae&quot;},{&quot;display&quot;:&quot;Melampittidae (Melampittas)&quot;,&quot;tip&quot;:&quot;Melampittidae&quot;},{&quot;display&quot;:&quot;Melanocharitidae (Longbills and Berrypeckers)&quot;,&quot;tip&quot;:&quot;Melanocharitidae&quot;},{&quot;display&quot;:&quot;Melanopareiidae (Crescentchests)&quot;,&quot;tip&quot;:&quot;Melanopareiidae&quot;},{&quot;display&quot;:&quot;Meliphagidae (Honeyeaters)&quot;,&quot;tip&quot;:&quot;Meliphagidae&quot;},{&quot;display&quot;:&quot;Menuridae (Lyrebirds)&quot;,&quot;tip&quot;:&quot;Menuridae&quot;},{&quot;display&quot;:&quot;Meropidae (Bee-eaters)&quot;,&quot;tip&quot;:&quot;Meropidae&quot;},{&quot;display&quot;:&quot;Mesitornithidae (Mesites)&quot;,&quot;tip&quot;:&quot;Mesitornithidae&quot;},{&quot;display&quot;:&quot;Mimidae (Mockingbirds and Thrashers)&quot;,&quot;tip&quot;:&quot;Mimidae&quot;},{&quot;display&quot;:&quot;Mitrospingidae (Mitrospingid Tanagers)&quot;,&quot;tip&quot;:&quot;Mitrospingidae&quot;},{&quot;display&quot;:&quot;Modulatricidae (Dapple-throat and Allies)&quot;,&quot;tip&quot;:&quot;Modulatricidae&quot;},{&quot;display&quot;:&quot;Mohoidae (Hawaiian Honeyeaters)&quot;,&quot;tip&quot;:&quot;Mohoidae&quot;},{&quot;display&quot;:&quot;Mohouidae (Whiteheads)&quot;,&quot;tip&quot;:&quot;Mohouidae&quot;},{&quot;display&quot;:&quot;Momotidae (Motmots)&quot;,&quot;tip&quot;:&quot;Momotidae&quot;},{&quot;display&quot;:&quot;Monarchidae (Monarch Flycatchers, Paradise Flycatchers, and Shrikebills)&quot;,&quot;tip&quot;:&quot;Monarchidae&quot;},{&quot;display&quot;:&quot;Motacillidae (Wagtails and Pipits)&quot;,&quot;tip&quot;:&quot;Motacillidae&quot;},{&quot;display&quot;:&quot;Muscicapidae (Chats, Old World Flycatchers, and Allies)&quot;,&quot;tip&quot;:&quot;Muscicapidae&quot;},{&quot;display&quot;:&quot;Musophagidae (Turacos)&quot;,&quot;tip&quot;:&quot;Musophagidae&quot;},{&quot;display&quot;:&quot;Nectariniidae (Spiderhunters and Sunbirds)&quot;,&quot;tip&quot;:&quot;Nectariniidae&quot;},{&quot;display&quot;:&quot;Neosittidae (Sittellas)&quot;,&quot;tip&quot;:&quot;Neosittidae&quot;},{&quot;display&quot;:&quot;Nesospingidae (Puerto Rican Tanager)&quot;,&quot;tip&quot;:&quot;Nesospingidae&quot;},{&quot;display&quot;:&quot;Nicatoridae (Nicators)&quot;,&quot;tip&quot;:&quot;Nicatoridae&quot;},{&quot;display&quot;:&quot;Notiomystidae (Stitchbird)&quot;,&quot;tip&quot;:&quot;Notiomystidae&quot;},{&quot;display&quot;:&quot;Numididae (Guineafowl)&quot;,&quot;tip&quot;:&quot;Numididae&quot;},{&quot;display&quot;:&quot;Nyctibiidae (Potoos)&quot;,&quot;tip&quot;:&quot;Nyctibiidae&quot;},{&quot;display&quot;:&quot;Oceanitidae (Southern Storm Petrels)&quot;,&quot;tip&quot;:&quot;Oceanitidae&quot;},{&quot;display&quot;:&quot;Odontophoridae (New World Quail)&quot;,&quot;tip&quot;:&quot;Odontophoridae&quot;},{&quot;display&quot;:&quot;Onychorhynchidae (Royal Flycatchers and Allies)&quot;,&quot;tip&quot;:&quot;Onychorhynchidae&quot;},{&quot;display&quot;:&quot;Opisthocomidae (Hoatzin)&quot;,&quot;tip&quot;:&quot;Opisthocomidae&quot;},{&quot;display&quot;:&quot;Oreoicidae (Australasian Bellbirds)&quot;,&quot;tip&quot;:&quot;Oreoicidae&quot;},{&quot;display&quot;:&quot;Oriolidae (Old World Orioles)&quot;,&quot;tip&quot;:&quot;Oriolidae&quot;},{&quot;display&quot;:&quot;Orthonychidae (Logrunner and Chowchilla)&quot;,&quot;tip&quot;:&quot;Orthonychidae&quot;},{&quot;display&quot;:&quot;Otididae (Bustards)&quot;,&quot;tip&quot;:&quot;Otididae&quot;},{&quot;display&quot;:&quot;Oxyruncidae (Sharpbill)&quot;,&quot;tip&quot;:&quot;Oxyruncidae&quot;},{&quot;display&quot;:&quot;Pachycephalidae (Whistlers and Allies)&quot;,&quot;tip&quot;:&quot;Pachycephalidae&quot;},{&quot;display&quot;:&quot;Pandionidae (Osprey)&quot;,&quot;tip&quot;:&quot;Pandionidae&quot;},{&quot;display&quot;:&quot;Panuridae (Reedling)&quot;,&quot;tip&quot;:&quot;Panuridae&quot;},{&quot;display&quot;:&quot;Paradisaeidae (Birds-of-paradise)&quot;,&quot;tip&quot;:&quot;Paradisaeidae&quot;},{&quot;display&quot;:&quot;Paradoxornithidae (Parrotbills and Allies)&quot;,&quot;tip&quot;:&quot;Paradoxornithidae&quot;},{&quot;display&quot;:&quot;Paramythiidae (Tit Berrypecker and Crested Berrypeckers)&quot;,&quot;tip&quot;:&quot;Paramythiidae&quot;},{&quot;display&quot;:&quot;Pardalotidae (Pardalotes)&quot;,&quot;tip&quot;:&quot;Pardalotidae&quot;},{&quot;display&quot;:&quot;Paridae (Tits, Chickadees, and Titmice)&quot;,&quot;tip&quot;:&quot;Paridae&quot;},{&quot;display&quot;:&quot;Parulidae (New World Warblers)&quot;,&quot;tip&quot;:&quot;Parulidae&quot;},{&quot;display&quot;:&quot;Passerellidae (New World Sparrows)&quot;,&quot;tip&quot;:&quot;Passerellidae&quot;},{&quot;display&quot;:&quot;Passeridae (Snowfinches and Old World Sparrows)&quot;,&quot;tip&quot;:&quot;Passeridae&quot;},{&quot;display&quot;:&quot;Pedionomidae (Plains-wanderer)&quot;,&quot;tip&quot;:&quot;Pedionomidae&quot;},{&quot;display&quot;:&quot;Pelecanidae (Pelicans)&quot;,&quot;tip&quot;:&quot;Pelecanidae&quot;},{&quot;display&quot;:&quot;Pellorneidae (Ground Babblers and Allies)&quot;,&quot;tip&quot;:&quot;Pellorneidae&quot;},{&quot;display&quot;:&quot;Petroicidae (Australasian Robins)&quot;,&quot;tip&quot;:&quot;Petroicidae&quot;},{&quot;display&quot;:&quot;Peucedramidae (Olive Warbler)&quot;,&quot;tip&quot;:&quot;Peucedramidae&quot;},{&quot;display&quot;:&quot;Phaenicophilidae (Hispaniolan Tanagers)&quot;,&quot;tip&quot;:&quot;Phaenicophilidae&quot;},{&quot;display&quot;:&quot;Phaethontidae (Tropicbirds)&quot;,&quot;tip&quot;:&quot;Phaethontidae&quot;},{&quot;display&quot;:&quot;Phalacrocoracidae (Cormorants and Shags)&quot;,&quot;tip&quot;:&quot;Phalacrocoracidae&quot;},{&quot;display&quot;:&quot;Phasianidae (Partridges, Pheasants, Grouse, and Allies)&quot;,&quot;tip&quot;:&quot;Phasianidae&quot;},{&quot;display&quot;:&quot;Philepittidae (Asities)&quot;,&quot;tip&quot;:&quot;Philepittidae&quot;},{&quot;display&quot;:&quot;Phoenicopteridae (Flamingos)&quot;,&quot;tip&quot;:&quot;Phoenicopteridae&quot;},{&quot;display&quot;:&quot;Phoeniculidae (Wood Hoopoes and Scimitarbills)&quot;,&quot;tip&quot;:&quot;Phoeniculidae&quot;},{&quot;display&quot;:&quot;Phylloscopidae (Leaf Warblers)&quot;,&quot;tip&quot;:&quot;Phylloscopidae&quot;},{&quot;display&quot;:&quot;Picathartidae (Rockfowl)&quot;,&quot;tip&quot;:&quot;Picathartidae&quot;},{&quot;display&quot;:&quot;Picidae (Woodpeckers)&quot;,&quot;tip&quot;:&quot;Picidae&quot;},{&quot;display&quot;:&quot;Pipridae (Manakins)&quot;,&quot;tip&quot;:&quot;Pipridae&quot;},{&quot;display&quot;:&quot;Pittidae (Pittas)&quot;,&quot;tip&quot;:&quot;Pittidae&quot;},{&quot;display&quot;:&quot;Pityriasidae (Bristlehead)&quot;,&quot;tip&quot;:&quot;Pityriasidae&quot;},{&quot;display&quot;:&quot;Platylophidae (Jayshrike)&quot;,&quot;tip&quot;:&quot;Platylophidae&quot;},{&quot;display&quot;:&quot;Platysteiridae (Wattle-eyes and Batises)&quot;,&quot;tip&quot;:&quot;Platysteiridae&quot;},{&quot;display&quot;:&quot;Ploceidae (Weavers and Allies)&quot;,&quot;tip&quot;:&quot;Ploceidae&quot;},{&quot;display&quot;:&quot;Pluvianellidae (Magellanic Plover)&quot;,&quot;tip&quot;:&quot;Pluvianellidae&quot;},{&quot;display&quot;:&quot;Pluvianidae (Egyptian Plover)&quot;,&quot;tip&quot;:&quot;Pluvianidae&quot;},{&quot;display&quot;:&quot;Pnoepygidae (Cupwings)&quot;,&quot;tip&quot;:&quot;Pnoepygidae&quot;},{&quot;display&quot;:&quot;Podargidae (Frogmouths)&quot;,&quot;tip&quot;:&quot;Podargidae&quot;},{&quot;display&quot;:&quot;Podicipedidae (Grebes)&quot;,&quot;tip&quot;:&quot;Podicipedidae&quot;},{&quot;display&quot;:&quot;Polioptilidae (Gnatwrens and Gnatcatchers)&quot;,&quot;tip&quot;:&quot;Polioptilidae&quot;},{&quot;display&quot;:&quot;Pomatostomidae (Australasian Babblers)&quot;,&quot;tip&quot;:&quot;Pomatostomidae&quot;},{&quot;display&quot;:&quot;Procellariidae (Petrels, Shearwaters, and Diving Petrels)&quot;,&quot;tip&quot;:&quot;Procellariidae&quot;},{&quot;display&quot;:&quot;Promeropidae (Sugarbirds)&quot;,&quot;tip&quot;:&quot;Promeropidae&quot;},{&quot;display&quot;:&quot;Prunellidae (Accentors)&quot;,&quot;tip&quot;:&quot;Prunellidae&quot;},{&quot;display&quot;:&quot;Psittacidae (African and New World Parrots)&quot;,&quot;tip&quot;:&quot;Psittacidae&quot;},{&quot;display&quot;:&quot;Psittaculidae (Old World Parrots)&quot;,&quot;tip&quot;:&quot;Psittaculidae&quot;},{&quot;display&quot;:&quot;Psophiidae (Trumpeters)&quot;,&quot;tip&quot;:&quot;Psophiidae&quot;},{&quot;display&quot;:&quot;Psophodidae (Whipbirds and Wedgebills)&quot;,&quot;tip&quot;:&quot;Psophodidae&quot;},{&quot;display&quot;:&quot;Pteroclidae (Sandgrouse)&quot;,&quot;tip&quot;:&quot;Pteroclidae&quot;},{&quot;display&quot;:&quot;Ptiliogonatidae (Silky-flycatchers)&quot;,&quot;tip&quot;:&quot;Ptiliogonatidae&quot;},{&quot;display&quot;:&quot;Ptilonorhynchidae (Bowerbirds)&quot;,&quot;tip&quot;:&quot;Ptilonorhynchidae&quot;},{&quot;display&quot;:&quot;Pycnonotidae (Bulbuls)&quot;,&quot;tip&quot;:&quot;Pycnonotidae&quot;},{&quot;display&quot;:&quot;Rallidae (Rails, Gallinules, and Coots)&quot;,&quot;tip&quot;:&quot;Rallidae&quot;},{&quot;display&quot;:&quot;Ramphastidae (Toucans)&quot;,&quot;tip&quot;:&quot;Ramphastidae&quot;},{&quot;display&quot;:&quot;Recurvirostridae (Stilts and Avocets)&quot;,&quot;tip&quot;:&quot;Recurvirostridae&quot;},{&quot;display&quot;:&quot;Regulidae (Kinglets)&quot;,&quot;tip&quot;:&quot;Regulidae&quot;},{&quot;display&quot;:&quot;Remizidae (Penduline Tits)&quot;,&quot;tip&quot;:&quot;Remizidae&quot;},{&quot;display&quot;:&quot;Rhagologidae (Berryhunter)&quot;,&quot;tip&quot;:&quot;Rhagologidae&quot;},{&quot;display&quot;:&quot;Rheidae (Rheas)&quot;,&quot;tip&quot;:&quot;Rheidae&quot;},{&quot;display&quot;:&quot;Rhinocryptidae (Tapaculos)&quot;,&quot;tip&quot;:&quot;Rhinocryptidae&quot;},{&quot;display&quot;:&quot;Rhipiduridae (Fantails and Silktails)&quot;,&quot;tip&quot;:&quot;Rhipiduridae&quot;},{&quot;display&quot;:&quot;Rhodinocichlidae (Thrush-tanager)&quot;,&quot;tip&quot;:&quot;Rhodinocichlidae&quot;},{&quot;display&quot;:&quot;Rhynochetidae (Kagu)&quot;,&quot;tip&quot;:&quot;Rhynochetidae&quot;},{&quot;display&quot;:&quot;Rostratulidae (Painted-Snipes)&quot;,&quot;tip&quot;:&quot;Rostratulidae&quot;},{&quot;display&quot;:&quot;Sagittariidae (Secretarybird)&quot;,&quot;tip&quot;:&quot;Sagittariidae&quot;},{&quot;display&quot;:&quot;Salpornithidae (Spotted Creepers)&quot;,&quot;tip&quot;:&quot;Salpornithidae&quot;},{&quot;display&quot;:&quot;Sapayoidae (Sapayoa)&quot;,&quot;tip&quot;:&quot;Sapayoidae&quot;},{&quot;display&quot;:&quot;Sarothruridae (Flufftails)&quot;,&quot;tip&quot;:&quot;Sarothruridae&quot;},{&quot;display&quot;:&quot;Scolopacidae (Sandpipers and Allies)&quot;,&quot;tip&quot;:&quot;Scolopacidae&quot;},{&quot;display&quot;:&quot;Scopidae (Hamerkop)&quot;,&quot;tip&quot;:&quot;Scopidae&quot;},{&quot;display&quot;:&quot;Semnornithidae (Prong-billed Barbet and Toucan Barbet)&quot;,&quot;tip&quot;:&quot;Semnornithidae&quot;},{&quot;display&quot;:&quot;Sittidae (Nuthatches)&quot;,&quot;tip&quot;:&quot;Sittidae&quot;},{&quot;display&quot;:&quot;Spheniscidae (Penguins)&quot;,&quot;tip&quot;:&quot;Spheniscidae&quot;},{&quot;display&quot;:&quot;Spindalidae (Spindalises)&quot;,&quot;tip&quot;:&quot;Spindalidae&quot;},{&quot;display&quot;:&quot;Steatornithidae (Oilbird)&quot;,&quot;tip&quot;:&quot;Steatornithidae&quot;},{&quot;display&quot;:&quot;Stenostiridae (Fairy Flycatchers)&quot;,&quot;tip&quot;:&quot;Stenostiridae&quot;},{&quot;display&quot;:&quot;Stercorariidae (Jaegers and Skuas)&quot;,&quot;tip&quot;:&quot;Stercorariidae&quot;},{&quot;display&quot;:&quot;Strigidae (Owls)&quot;,&quot;tip&quot;:&quot;Strigidae&quot;},{&quot;display&quot;:&quot;Strigopidae (New Zealand Parrots)&quot;,&quot;tip&quot;:&quot;Strigopidae&quot;},{&quot;display&quot;:&quot;Struthionidae (Ostriches)&quot;,&quot;tip&quot;:&quot;Struthionidae&quot;},{&quot;display&quot;:&quot;Sturnidae (Rhabdornis, Starlings, and Mynas)&quot;,&quot;tip&quot;:&quot;Sturnidae&quot;},{&quot;display&quot;:&quot;Sulidae (Boobies and Gannets)&quot;,&quot;tip&quot;:&quot;Sulidae&quot;},{&quot;display&quot;:&quot;Sylviidae (Sylviid Warblers and Allies)&quot;,&quot;tip&quot;:&quot;Sylviidae&quot;},{&quot;display&quot;:&quot;Teretistridae (Cuban Warblers)&quot;,&quot;tip&quot;:&quot;Teretistridae&quot;},{&quot;display&quot;:&quot;Thamnophilidae (Antbirds, Antshrikes, Antwrens, and Antvireos)&quot;,&quot;tip&quot;:&quot;Thamnophilidae&quot;},{&quot;display&quot;:&quot;Thinocoridae (Seedsnipes)&quot;,&quot;tip&quot;:&quot;Thinocoridae&quot;},{&quot;display&quot;:&quot;Thraupidae (Tanagers and Allies)&quot;,&quot;tip&quot;:&quot;Thraupidae&quot;},{&quot;display&quot;:&quot;Threskiornithidae (Ibises and Spoonbills)&quot;,&quot;tip&quot;:&quot;Threskiornithidae&quot;},{&quot;display&quot;:&quot;Tichodromidae (Wallcreeper)&quot;,&quot;tip&quot;:&quot;Tichodromidae&quot;},{&quot;display&quot;:&quot;Timaliidae (Tree Babblers, Scimitar Babblers, and Allies)&quot;,&quot;tip&quot;:&quot;Timaliidae&quot;},{&quot;display&quot;:&quot;Tinamidae (Tinamous)&quot;,&quot;tip&quot;:&quot;Tinamidae&quot;},{&quot;display&quot;:&quot;Tityridae (Tityras, Becards, and Allies)&quot;,&quot;tip&quot;:&quot;Tityridae&quot;},{&quot;display&quot;:&quot;Todidae (Todies)&quot;,&quot;tip&quot;:&quot;Todidae&quot;},{&quot;display&quot;:&quot;Trochilidae (Hummingbirds)&quot;,&quot;tip&quot;:&quot;Trochilidae&quot;},{&quot;display&quot;:&quot;Troglodytidae (Wrens)&quot;,&quot;tip&quot;:&quot;Troglodytidae&quot;},{&quot;display&quot;:&quot;Trogonidae (Trogons)&quot;,&quot;tip&quot;:&quot;Trogonidae&quot;},{&quot;display&quot;:&quot;Turdidae (Thrushes and Allies)&quot;,&quot;tip&quot;:&quot;Turdidae&quot;},{&quot;display&quot;:&quot;Turnicidae (Buttonquail)&quot;,&quot;tip&quot;:&quot;Turnicidae&quot;},{&quot;display&quot;:&quot;Tyrannidae (Tyrant Flycatchers and Allies)&quot;,&quot;tip&quot;:&quot;Tyrannidae&quot;},{&quot;display&quot;:&quot;Tytonidae (Bay Owls and Barn Owls)&quot;,&quot;tip&quot;:&quot;Tytonidae&quot;},{&quot;display&quot;:&quot;Upupidae (Hoopoes)&quot;,&quot;tip&quot;:&quot;Upupidae&quot;},{&quot;display&quot;:&quot;Urocynchramidae (Przevalski&#x27;s Finch)&quot;,&quot;tip&quot;:&quot;Urocynchramidae&quot;},{&quot;display&quot;:&quot;Vangidae (Vangas, Helmetshrikes, and Allies)&quot;,&quot;tip&quot;:&quot;Vangidae&quot;},{&quot;display&quot;:&quot;Viduidae (Whydahs and Indigobirds)&quot;,&quot;tip&quot;:&quot;Viduidae&quot;},{&quot;display&quot;:&quot;Vireonidae (Shrike-babblers, Erpornis, and Vireos)&quot;,&quot;tip&quot;:&quot;Vireonidae&quot;},{&quot;display&quot;:&quot;Zeledoniidae (Wrenthrush)&quot;,&quot;tip&quot;:&quot;Zeledoniidae&quot;},{&quot;display&quot;:&quot;Zosteropidae (White-eyes, Yuhinas, and Allies)&quot;,&quot;tip&quot;:&quot;Zosteropidae&quot;}];

  
  var _currentTree  = null;
  var _inFamilyMode = true;
  var _activeMeta   = META;
  var _container    = null;
  var _outerWrap    = null;
  var DEF_HI_COL    = [60, 115, 131, 255];
  var DEF_HALO_W    = 4;
  var DEF_HALO_R    = 12;
  var _pathTimer    = null;
  var _pathNodes    = [];
  var _familyPayload = null;
  
  var _lastAppliedFamilyTip = &quot;&quot;;
  var _famNavHistory = [];

  function buildStyles(meta) {
    var s = {};
    Object.keys(meta).forEach(function (tip) {
      var m = meta[tip];
      var style = {
        fillColour:   m.color || &quot;#aaaaaa&quot;,
        strokeColour: m.color || &quot;#aaaaaa&quot;,
        shape: &quot;circle&quot;,
        size:  5,
        label: (m.label !== undefined &amp;&amp; m.label !== null &amp;&amp; m.label !== &quot;&quot;) ? m.label : tip,
      };
      s[tip] = style;
      
      var us = tip.replace(/ /g, &quot;_&quot;);
      if (us !== tip) s[us] = style;
    });
    return s;
  }

  function _metaRowForLeaf(key) {
    if (!key) return null;
    if (_activeMeta[key]) return _activeMeta[key];
    var spaced = key.replace(/_/g, &quot; &quot;);
    if (spaced !== key &amp;&amp; _activeMeta[spaced]) return _activeMeta[spaced];
    return null;
  }

  
  var _tipEl = null;
  function _ensureTip() {
    if (_tipEl) return _tipEl;
    _tipEl = document.createElement(&quot;div&quot;);
    _tipEl.setAttribute(&quot;data-phylo-tip&quot;, &quot;1&quot;);
    _tipEl.style.cssText = [
      &quot;position:fixed&quot;,&quot;z-index:99999&quot;,&quot;pointer-events:none&quot;,&quot;display:none&quot;,
      &quot;max-width:min(380px,94vw)&quot;,&quot;padding:9px 11px&quot;,
      &quot;font:12px/1.5 system-ui,Segoe UI,sans-serif&quot;,&quot;color:#24292f&quot;,
      &quot;background:#fff&quot;,&quot;border:1px solid #d0d7de&quot;,&quot;border-radius:7px&quot;,
      &quot;box-shadow:0 6px 18px rgba(31,35,40,.18)&quot;,&quot;white-space:pre-wrap&quot;,
      &quot;word-break:break-word&quot;
    ].join(&quot;;&quot;);
    document.body.appendChild(_tipEl);
    return _tipEl;
  }
  function _hideTip() {
    if (_tipEl) { _tipEl.style.display = &quot;none&quot;; _tipEl.textContent = &quot;&quot;; }
  }
  function _showTip(txt, ev) {
    var tip = _ensureTip();
    tip.textContent = txt;
    tip.style.display = &quot;block&quot;;
    var pad = 12, w = tip.offsetWidth, h = tip.offsetHeight;
    tip.style.left = Math.max(6, Math.min(ev.clientX + pad, window.innerWidth  - w - 6)) + &quot;px&quot;;
    tip.style.top  = Math.max(6, Math.min(ev.clientY + pad, window.innerHeight - h - 6)) + &quot;px&quot;;
  }

  
  var _hoverBound = false;
  function _onHoverMove(ev) {
    var canvas = _container &amp;&amp; _container.querySelector(&quot;canvas&quot;);
    if (!canvas || !_currentTree || !_currentTree.deck) { _hideTip(); return; }
    var r = canvas.getBoundingClientRect();
    var x = ev.clientX - r.left, y = ev.clientY - r.top;
    if (x &lt; 0 || y &lt; 0 || x &gt; r.width || y &gt; r.height) { _hideTip(); return; }
    var node = null;
    try {
      var picked = _currentTree.deck.pickObject({ x: x, y: y });
      if (picked &amp;&amp; typeof _currentTree.pickNodeFromLayer === &quot;function&quot;)
        node = _currentTree.pickNodeFromLayer(picked);
    } catch (e) { _hideTip(); return; }
    if (!node || !node.isLeaf) { _hideTip(); return; }
    var key = node.label || node.id;
    var row = _metaRowForLeaf(key);
    if (!row || !row.tooltip) { _hideTip(); return; }
    _showTip(row.tooltip, ev);
  }
  function _bindHover(container) {
    if (_hoverBound) return;
    _hoverBound = true;
    _ensureTip();
    container.addEventListener(&quot;pointerleave&quot;, _hideTip);
    container.addEventListener(&quot;pointermove&quot;,  _onHoverMove);
  }

  
  var _resizeBound = false;
  function _onResize() {
    if (!_currentTree) return;
    var el = _sizeTargetEl();
    if (!el) return;
    _currentTree.setProps({ size: { width: containerWidth(el), height: HEIGHT } });
    if (DRILLDOWN) {
      _resizePathOverlay();
      _drawPathOverlay();
    }
  }
  function _bindResize(container) {
    if (_resizeBound) return;
    _resizeBound = true;
    window.addEventListener(&quot;resize&quot;, _onResize);
    if (typeof ResizeObserver !== &quot;undefined&quot;) {
      new ResizeObserver(_onResize).observe(container);
    }
  }

  
  var _ddBound    = false;
  var _ddPtrStart = null;
  function _bindDrilldown(container) {
    if (_ddBound) return;
    _ddBound = true;
    container.addEventListener(&quot;pointerdown&quot;, function (ev) {
      _ddPtrStart = { x: ev.clientX, y: ev.clientY };
      _hideTip();
    });
    container.addEventListener(&quot;pointerup&quot;, function (ev) {
      if (!DRILLDOWN || !_inFamilyMode || !_ddPtrStart) { _ddPtrStart = null; return; }
      var dx = ev.clientX - _ddPtrStart.x;
      var dy = ev.clientY - _ddPtrStart.y;
      _ddPtrStart = null;
      if (dx * dx + dy * dy &gt; 64) return;   
      if (!_currentTree || !_currentTree.deck) return;
      var canvas = container.querySelector(&quot;canvas&quot;);
      if (!canvas) return;
      var r  = canvas.getBoundingClientRect();
      var cx = ev.clientX - r.left, cy = ev.clientY - r.top;
      var node = null;
      try {
        var picked = _currentTree.deck.pickObject({ x: cx, y: cy });
        if (picked &amp;&amp; typeof _currentTree.pickNodeFromLayer === &quot;function&quot;)
          node = _currentTree.pickNodeFromLayer(picked);
      } catch (e) { return; }
      if (!node || !node.isLeaf) return;
      var family = node.label || node.id;
      if (!family) return;
      _enterFamily(family);
    });
  }

  
  var _famSearchBound = false;
  function _sizeTargetEl() {
    return (DRILLDOWN &amp;&amp; _outerWrap) ? _outerWrap : _container;
  }
  function _pathOverlay() {
    return document.getElementById(CONTAINER_ID + &quot;-path-overlay&quot;);
  }
  function _stopPathTimer() {
    if (_pathTimer) { clearInterval(_pathTimer); _pathTimer = null; }
  }
  function _clearPathOverlay() {
    var c = _pathOverlay();
    if (!c) return;
    var ctx = c.getContext(&quot;2d&quot;);
    if (ctx) ctx.clearRect(0, 0, c.width, c.height);
  }
  function _resizePathOverlay() {
    var c = _pathOverlay();
    if (!c || !_outerWrap) return;
    var r = _outerWrap.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    var w = Math.max(1, Math.floor(r.width * dpr));
    var h = Math.max(1, Math.floor(r.height * dpr));
    if (c.width !== w || c.height !== h) {
      c.width = w;
      c.height = h;
    }
    c.style.width = &quot;100%&quot;;
    c.style.height = &quot;100%&quot;;
  }
  function _projectPhylo(tree, node) {
    if (!tree || typeof tree.projectPoint !== &quot;function&quot; || !node) return null;
    try {
      var p = tree.projectPoint([node.x, node.y]);
      return (p &amp;&amp; p.length &gt;= 2) ? [p[0], p[1]] : null;
    } catch (e) { return null; }
  }
  function _projectPhyloXY(tree, x, y) {
    if (!tree || typeof tree.projectPoint !== &quot;function&quot;) return null;
    try {
      var p = tree.projectPoint([x, y]);
      return (p &amp;&amp; p.length &gt;= 2) ? [p[0], p[1]] : null;
    } catch (e2) { return null; }
  }
  function _shortAngleDelta(a0, a1) {
    var d = a1 - a0;
    while (d &gt; Math.PI) d -= 2 * Math.PI;
    while (d &lt; -Math.PI) d += 2 * Math.PI;
    return d;
  }
  function _dedupePts2D(pts, eps) {
    eps = eps || 0.45;
    var out = [];
    for (var i = 0; i &lt; pts.length; i++) {
      var q = pts[i];
      if (!q) continue;
      if (!out.length) { out.push(q); continue; }
      var p = out[out.length - 1];
      if (Math.hypot(q[0] - p[0], q[1] - p[1]) &gt; eps) out.push(q);
    }
    return out;
  }
  
  function _treeTypeIs(name) {
    var TT = window.phylocanvas &amp;&amp; window.phylocanvas.TreeTypes;
    var tt = null;
    try {
      if (_currentTree &amp;&amp; _currentTree.props &amp;&amp; _currentTree.props.type != null)
        tt = _currentTree.props.type;
      else if (_currentTree &amp;&amp; _currentTree.getTreeType)
        tt = _currentTree.getTreeType();
    } catch (e0) {}
    if (tt == null) return false;
    if (TT) {
      if (name === &quot;Circular&quot;   &amp;&amp; tt === TT.Circular) return true;
      if (name === &quot;Rectangular&quot; &amp;&amp; tt === TT.Rectangular) return true;
      if (name === &quot;Hierarchical&quot; &amp;&amp; tt === TT.Hierarchical) return true;
      if (name === &quot;Radial&quot;     &amp;&amp; tt === TT.Radial) return true;
      if (name === &quot;Diagonal&quot;   &amp;&amp; tt === TT.Diagonal) return true;
    }
    var codes = { Circular: &quot;cr&quot;, Rectangular: &quot;rc&quot;, Hierarchical: &quot;hr&quot;, Radial: &quot;rd&quot;, Diagonal: &quot;dg&quot; };
    return tt === codes[name];
  }
  function _nodeAngleRad(n, rx, ry) {
    if (!n) return null;
    if (n.angle != null &amp;&amp; isFinite(n.angle)) return n.angle;
    if (rx == null || ry == null) return null;
    return Math.atan2(n.y - ry, n.x - rx);
  }
  
  function _circInnerJunction(n, p, rx, ry) {
    var ix = n.cx, iy = n.cy;
    if (ix != null &amp;&amp; iy != null &amp;&amp; isFinite(ix) &amp;&amp; isFinite(iy)) {
      if (Math.hypot(ix - rx, iy - ry) &gt; 1e-4) return [ix, iy];
    }
    var na = _nodeAngleRad(n, rx, ry);
    if (!p || na == null) return null;
    var pr = Math.hypot(p.x - rx, p.y - ry);
    if (pr &lt; 1e-4) return [rx, ry];
    return [rx + pr * Math.cos(na), ry + pr * Math.sin(na)];
  }
  
  function _worldPathAlongBranches(chain) {
    if (!chain || chain.length &lt; 2)
      return chain &amp;&amp; chain.length ? [[chain[0].x, chain[0].y]] : [];
    var g = null;
    try {
      if (_currentTree &amp;&amp; _currentTree.getGraphAfterLayout)
        g = _currentTree.getGraphAfterLayout();
    } catch (e1) { g = null; }
    var root = g &amp;&amp; g.root;
    var rx = root ? root.x : 0, ry = root ? root.y : 0;

    if (_treeTypeIs(&quot;Rectangular&quot;)) {
      var pr = [];
      for (var ir = 1; ir &lt; chain.length; ir++) {
        var pa = chain[ir - 1], ch = chain[ir];
        if (!pr.length) pr.push([pa.x, pa.y]);
        pr.push([pa.x, ch.y]);
        pr.push([ch.x, ch.y]);
      }
      return _dedupePts2D(pr, 0.35);
    }

    if (_treeTypeIs(&quot;Hierarchical&quot;)) {
      var ph = [];
      for (var ih = 1; ih &lt; chain.length; ih++) {
        var pap = chain[ih - 1], chh = chain[ih];
        if (!ph.length) ph.push([pap.x, pap.y]);
        ph.push([chh.x, pap.y]);
        ph.push([chh.x, chh.y]);
      }
      return _dedupePts2D(ph, 0.35);
    }

    if (_treeTypeIs(&quot;Circular&quot;) &amp;&amp; root) {
      var leaf = chain[chain.length - 1];
      var acc = [];
      var n = leaf;
      while (n.parent) {
        var p = n.parent;
        acc.push([n.x, n.y]);
        var ij = _circInnerJunction(n, p, rx, ry);
        if (!ij) { n = p; continue; }
        var ix = ij[0], iy = ij[1];
        var innerR = Math.hypot(ix - rx, iy - ry);
        if (innerR &gt; 1e-4) {
          acc.push([ix, iy]);
          var prx = p.x - rx, pry = p.y - ry;
          var a0 = Math.atan2(iy - ry, ix - rx);
          var pa = _nodeAngleRad(p, rx, ry);
          var a1 = (Math.abs(prx) + Math.abs(pry) &lt; 1e-4)
            ? a0
            : (pa != null ? pa : Math.atan2(pry, prx));
          var d = _shortAngleDelta(a0, a1);
          if (Math.abs(d) &gt; 2e-3) {
            var segs = Math.max(10, Math.min(96, Math.ceil(Math.abs(d) / (Math.PI / 32))));
            for (var s = 1; s &lt;= segs; s++) {
              var t = s / segs;
              var a = a0 + d * t;
              acc.push([rx + innerR * Math.cos(a), ry + innerR * Math.sin(a)]);
            }
          }
        }
        n = p;
      }
      acc.reverse();
      return _dedupePts2D(acc, 0.12);
    }

    if (_treeTypeIs(&quot;Radial&quot;) || _treeTypeIs(&quot;Diagonal&quot;)) {
      var pr2 = [];
      for (var ir2 = 0; ir2 &lt; chain.length; ir2++) {
        var nd = chain[ir2];
        pr2.push([nd.x, nd.y]);
      }
      return _dedupePts2D(pr2, 0.2);
    }

    return _dedupePts2D(
      chain.map(function (n) { return [n.x, n.y]; }),
      0.2
    );
  }
  function _drawPathOverlay() {
    var c = _pathOverlay();
    if (!c || !_currentTree || !_pathNodes.length) return;
    var ctx = c.getContext(&quot;2d&quot;);
    if (!ctx) return;
    var dpr = window.devicePixelRatio || 1;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, c.width / dpr, c.height / dpr);
    ctx.lineCap = &quot;round&quot;;
    ctx.lineJoin = &quot;round&quot;;
    ctx.strokeStyle = &quot;#000&quot;;
    ctx.lineWidth = 4;
    var wPts = _worldPathAlongBranches(_pathNodes);
    ctx.beginPath();
    var first = true;
    for (var i = 0; i &lt; wPts.length; i++) {
      var ppt = _projectPhyloXY(_currentTree, wPts[i][0], wPts[i][1]);
      if (!ppt) continue;
      if (first) { ctx.moveTo(ppt[0], ppt[1]); first = false; }
      else ctx.lineTo(ppt[0], ppt[1]);
    }
    if (!first) ctx.stroke();
  }
  function _startPathTimer() {
    _stopPathTimer();
    if (!DRILLDOWN || !_pathNodes.length) return;
    _pathTimer = setInterval(function () { _drawPathOverlay(); }, 120);
  }
  function _clearFamilyPathHighlight() {
    _stopPathTimer();
    _pathNodes = [];
    _clearPathOverlay();
    if (_currentTree &amp;&amp; typeof _currentTree.setProps === &quot;function&quot;) {
      try {
        _currentTree.setProps({
          selectedIds: [],
          highlightColour: DEF_HI_COL,
          haloWidth: DEF_HALO_W,
          haloRadius: DEF_HALO_R,
        });
      } catch (e) {}
    }
  }
  function _findLeafNodeForTip(tip) {
    if (!_currentTree || !tip) return null;
    
    
    var g = null;
    try {
      if (typeof _currentTree.getGraphAfterLayout === &quot;function&quot;)
        g = _currentTree.getGraphAfterLayout();
    } catch (e1) { g = null; }
    if (!g || !g.leaves) return null;
    var want = String(tip).trim();
    var wantLo = want.toLowerCase();
    var wantUs = want.replace(/ /g, &quot;_&quot;);
    var wantUsLo = wantUs.toLowerCase();
    for (var i = 0; i &lt; g.leaves.length; i++) {
      var L = g.leaves[i];
      if (!L) continue;
      var lab = L.label != null ? String(L.label) : &quot;&quot;;
      var labUs = lab.replace(/ /g, &quot;_&quot;);
      if (lab === want || labUs === wantUs) return L;
      if (lab.toLowerCase() === wantLo || labUs.toLowerCase() === wantUsLo) return L;
    }
    return null;
  }
  function _chainRootToLeaf(leaf) {
    var ch = [];
    for (var n = leaf; n; n = n.parent) ch.push(n);
    ch.reverse();
    return ch;
  }
  function _applyFamilyTip(tip) {
    if (!DRILLDOWN || !_inFamilyMode) return;
    _clearFamilyPathHighlight();
    if (!tip) {
      _lastAppliedFamilyTip = &quot;&quot;;
      return;
    }
    if (!_currentTree) {
      _lastAppliedFamilyTip = &quot;&quot;;
      return;
    }
    var leaf = _findLeafNodeForTip(tip);
    if (!leaf) {
      _lastAppliedFamilyTip = &quot;&quot;;
      return;
    }
    _pathNodes = _chainRootToLeaf(leaf);
    _resizePathOverlay();
    _drawPathOverlay();
    _startPathTimer();
    try {
      _currentTree.setProps({
        selectedIds: [leaf.id],
        highlightColour: [0, 0, 0, 255],
        haloWidth: 6,
        haloRadius: 16,
      });
    } catch (e) {}
    _lastAppliedFamilyTip = String(tip).trim();
  }
  function _bindFamilySearch() {
    if (!DRILLDOWN || _famSearchBound) return;
    _famSearchBound = true;
    var ALL_KEY = &quot;All families&quot;;
    var input = document.getElementById(CONTAINER_ID + &quot;-fam-search&quot;);
    var panel = document.getElementById(CONTAINER_ID + &quot;-fam-suggest&quot;);
    if (!input || !panel) return;
    var btnAll = document.getElementById(CONTAINER_ID + &quot;-fam-search-all&quot;);
    var btnUndo = document.getElementById(CONTAINER_ID + &quot;-fam-search-undo&quot;);

    var payload = {};
    payload[ALL_KEY] = &quot;&quot;;
    for (var i = 0; i &lt; FAMILY_SEARCH_ROWS.length; i++) {
      var row = FAMILY_SEARCH_ROWS[i];
      if (row &amp;&amp; row.display) payload[row.display] = row.tip || &quot;&quot;;
    }
    var LABELS = Object.keys(payload);

    function escapeHtml(s) {
      var d = document.createElement(&quot;div&quot;);
      d.textContent = s;
      return d.innerHTML;
    }
    function highlight(label, qt) {
      if (!qt) return escapeHtml(label);
      var ll = label.toLowerCase();
      var ql = qt.toLowerCase();
      var ii = ll.indexOf(ql);
      if (ii &lt; 0) return escapeHtml(label);
      return escapeHtml(label.slice(0, ii))
        + &#x27;&lt;mark style=&quot;background:#fff8c5;padding:0 1px;border-radius:2px;&quot;&gt;&#x27;
        + escapeHtml(label.slice(ii, ii + qt.length)) + &quot;&lt;/mark&gt;&quot;
        + escapeHtml(label.slice(ii + qt.length));
    }
    function buildVisible(q) {
      var qt = q.trim().toLowerCase();
      if (!qt) {
        var rest = LABELS.filter(function (l) { return l !== ALL_KEY; })
          .sort(function (a, b) { return a.localeCompare(b); });
        return { rows: [ALL_KEY].concat(rest.slice(0, 22)), more: Math.max(0, rest.length - 22) };
      }
      var hit = LABELS.filter(function (l) { return l.toLowerCase().indexOf(qt) &gt;= 0; });
      hit.sort(function (a, b) {
        var ca = a.toLowerCase().indexOf(qt);
        var cb = b.toLowerCase().indexOf(qt);
        if (ca !== cb) return ca - cb;
        return a.localeCompare(b);
      });
      return { rows: hit.slice(0, 80), more: Math.max(0, hit.length - 80) };
    }
    var FAM_HIST_MAX = 24;
    function rememberNavState() {
      _famNavHistory.push({ v: input.value, tip: _lastAppliedFamilyTip });
      if (_famNavHistory.length &gt; FAM_HIST_MAX) _famNavHistory.shift();
    }
    function syncUndoButton() {
      if (btnUndo) btnUndo.disabled = !_famNavHistory.length;
    }
    function undoFamilySearchSelection() {
      if (!_famNavHistory.length) return;
      var prev = _famNavHistory.pop();
      input.value = prev.v != null ? prev.v : &quot;&quot;;
      _applyFamilyTip(prev.tip || &quot;&quot;);
      closePanel();
      syncUndoButton();
    }
    function applyByLabel(lbl) {
      if (!(lbl in payload)) return;
      var tip = payload[lbl];
      _applyFamilyTip(tip);
    }
    function selectAndApply(lbl) {
      if (!(lbl in payload)) return;
      var newTip = payload[lbl] != null ? String(payload[lbl]).trim() : &quot;&quot;;
      if (input.value === lbl &amp;&amp; _lastAppliedFamilyTip === newTip) {
        panel.style.display = &quot;none&quot;;
        input.setAttribute(&quot;aria-expanded&quot;, &quot;false&quot;);
        return;
      }
      rememberNavState();
      input.value = lbl;
      applyByLabel(lbl);
      panel.style.display = &quot;none&quot;;
      input.setAttribute(&quot;aria-expanded&quot;, &quot;false&quot;);
      syncUndoButton();
    }
    var visible = [];
    var activeIdx = -1;
    function renderList() {
      var q = input.value;
      var qt = q.trim();
      var built = buildVisible(q);
      visible = built.rows;
      activeIdx = -1;
      var html = &quot;&quot;;
      for (var idx = 0; idx &lt; visible.length; idx++) {
        var lbl = visible[idx];
        html +=
          &#x27;&lt;div role=&quot;option&quot; tabindex=&quot;-1&quot; class=&quot;phylo-suggest-row&quot; data-idx=&quot;&#x27; + idx + &#x27;&quot; &#x27;
          + &#x27;style=&quot;padding:8px 10px;cursor:pointer;font-size:13px;color:#24292f;&#x27;
          + &#x27;border-bottom:1px solid #f0f3f6;&quot;&gt;&#x27; + highlight(lbl, qt) + &quot;&lt;/div&gt;&quot;;
      }
      if (built.more &gt; 0) {
        html += &#x27;&lt;div style=&quot;padding:7px 10px;font-size:11px;color:#57606a;border-top:1px solid #eaeef2;&quot;&gt;&#x27;
          + (qt ? (&quot;…&quot; + built.more + &quot; more matches — refine your search&quot;)
                 : (&quot;…and &quot; + built.more + &quot; more families — keep typing to search&quot;))
          + &quot;&lt;/div&gt;&quot;;
      }
      panel.innerHTML = html;
      Array.prototype.forEach.call(panel.querySelectorAll(&quot;.phylo-suggest-row&quot;), function (el) {
        el.addEventListener(&quot;mousedown&quot;, function (ev) {
          ev.preventDefault();
          var i = parseInt(el.getAttribute(&quot;data-idx&quot;), 10);
          if (i &gt;= 0 &amp;&amp; visible[i]) selectAndApply(visible[i]);
        });
      });
    }
    function openPanel() {
      renderList();
      panel.style.display = &quot;block&quot;;
      input.setAttribute(&quot;aria-expanded&quot;, &quot;true&quot;);
    }
    function closePanel() {
      panel.style.display = &quot;none&quot;;
      input.setAttribute(&quot;aria-expanded&quot;, &quot;false&quot;);
    }

    input.addEventListener(&quot;focus&quot;, function () { openPanel(); });
    input.addEventListener(&quot;input&quot;, function () { openPanel(); });
    input.addEventListener(&quot;keydown&quot;, function (ev) {
      if ((ev.ctrlKey || ev.metaKey) &amp;&amp; String(ev.key).toLowerCase() === &quot;z&quot; &amp;&amp; !ev.shiftKey) {
        if (_famNavHistory.length &gt; 0) {
          ev.preventDefault();
          undoFamilySearchSelection();
        }
        return;
      }
      if (ev.key === &quot;Backspace&quot; &amp;&amp; input.value === &quot;&quot; &amp;&amp; !ev.repeat) {
        if (_famNavHistory.length &gt; 0) {
          ev.preventDefault();
          undoFamilySearchSelection();
        }
        return;
      }
      if (panel.style.display !== &quot;none&quot; &amp;&amp; (ev.key === &quot;ArrowDown&quot; || ev.key === &quot;ArrowUp&quot;)) {
        ev.preventDefault();
        if (!visible.length) return;
        if (activeIdx &lt; 0) activeIdx = 0;
        else if (ev.key === &quot;ArrowDown&quot;) activeIdx = (activeIdx + 1) % visible.length;
        else activeIdx = (activeIdx - 1 + visible.length) % visible.length;
        var rows = panel.querySelectorAll(&quot;.phylo-suggest-row&quot;);
        for (var r = 0; r &lt; rows.length; r++) {
          rows[r].style.background = (r === activeIdx) ? &quot;#f6f8ff&quot; : &quot;#fff&quot;;
        }
      } else if (ev.key === &quot;Enter&quot;) {
        if (panel.style.display !== &quot;none&quot; &amp;&amp; activeIdx &gt;= 0 &amp;&amp; visible[activeIdx]) {
          ev.preventDefault();
          selectAndApply(visible[activeIdx]);
        } else {
          var q = input.value.trim();
          var built = buildVisible(q);
          if (built.rows.length === 1) {
            ev.preventDefault();
            selectAndApply(built.rows[0]);
          } else if (q &amp;&amp; built.rows.length &gt; 0) {
            
            ev.preventDefault();
            selectAndApply(built.rows[0]);
          }
        }
      } else if (ev.key === &quot;Escape&quot;) {
        closePanel();
      }
    });
    document.addEventListener(&quot;click&quot;, function (ev) {
      var wrap = input.closest(&quot;.phylo-family-picker&quot;);
      if (wrap &amp;&amp; !wrap.contains(ev.target)) closePanel();
    });
    if (btnAll) {
      btnAll.addEventListener(&quot;click&quot;, function () { selectAndApply(ALL_KEY); });
    }
    if (btnUndo) {
      btnUndo.addEventListener(&quot;click&quot;, function () { undoFamilySearchSelection(); });
    }
    syncUndoButton();
    _familyPayload = payload;
  }

  function containerWidth(el) {
    var w = el.clientWidth || el.offsetWidth || 0;
    if (w &lt; 32) w = el.getBoundingClientRect().width || 0;
    if (w &lt; 32) w = window.innerWidth || 0;
    
    return Math.max(w, 280);
  }

  
  
  
  function whenSized(el, cb, tries) {
    tries = tries || 0;
    var w = el.clientWidth || el.offsetWidth || 0;
    
    if (w &lt; 32) {
      var iw = window.innerWidth || 0;
      if (iw &gt;= 32) w = Math.min(Math.max(400, iw - 24), 920);
    }
    if (w &gt;= 32) { cb(w); return; }
    if (tries &gt; 60) { cb(containerWidth(el)); return; }
    requestAnimationFrame(function () { whenSized(el, cb, tries + 1); });
  }

  
  function _makeTree(newick, meta, treeType, showLeafLabels) {
    return new window.phylocanvas.PhylocanvasGL(_container, {
      size:               { width: containerWidth(_sizeTargetEl()), height: HEIGHT },
      source:             newick,
      type:               window.phylocanvas.TreeTypes[treeType],
      strokeColour:       STROKE,
      fontColour:         FONT,
      lineWidth:          LINE_W,
      showLabels:         true,
      showLeafLabels:     showLeafLabels,
      alignLabels:        true,
      showInternalLabels: false,
      showBranchLengths:  false,
      interactive:        true,
      styles:             buildStyles(meta),
    });
  }

  
  function _enterFamily(family) {
    _clearFamilyPathHighlight();
    _famNavHistory.length = 0;
    var ubDrill = document.getElementById(CONTAINER_ID + &quot;-fam-search-undo&quot;);
    if (ubDrill) ubDrill.disabled = true;
    var fw0 = document.getElementById(CONTAINER_ID + &quot;-fam-search-wrap&quot;);
    if (fw0) fw0.style.display = &quot;none&quot;;
    function _go(payload) {
      if (!payload || !payload.newick) return;
      try { _currentTree.destroy(); } catch (e) {}
      _activeMeta  = payload.meta || {};
      _currentTree = _makeTree(payload.newick, _activeMeta, DD_SP_TYPE, true);
      _inFamilyMode = false;
      var titleEl = document.getElementById(CONTAINER_ID + &quot;-dd-title&quot;);
      if (titleEl) {
        var nSp = payload.n_species || 0, nGe = payload.n_genera || 0;
        titleEl.textContent = family + &quot; — &quot; + nSp + &quot; species | &quot; + nGe + &quot; genera&quot;;
      }
      var backEl = document.getElementById(CONTAINER_ID + &quot;-dd-back&quot;);
      if (backEl) backEl.hidden = false;
      _hideTip();
      _resizePathOverlay();
    }
    if (DD_MODE === &quot;inline&quot;) {
      _go(DD_SUBTREES ? (DD_SUBTREES[family] || null) : null);
    } else if (DD_MODE === &quot;fetch&quot; &amp;&amp; DD_URL_BASE) {
      fetch(DD_URL_BASE + encodeURIComponent(family) + &quot;.json&quot;)
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(_go)
        .catch(function () {});
    }
  }

  
  function _enterFamilyTree() {
    try { _currentTree.destroy(); } catch (e) {}
    _activeMeta  = META;
    _currentTree = _makeTree(NEWICK, META, &quot;Circular&quot;, !FAMILY_HOVER);
    _inFamilyMode = true;
    var titleEl = document.getElementById(CONTAINER_ID + &quot;-dd-title&quot;);
    if (titleEl) titleEl.textContent = DD_FAM_TITLE;
    var backEl = document.getElementById(CONTAINER_ID + &quot;-dd-back&quot;);
    if (backEl) backEl.hidden = true;
    _hideTip();
    var fw1 = document.getElementById(CONTAINER_ID + &quot;-fam-search-wrap&quot;);
    if (fw1) fw1.style.display = &quot;block&quot;;
    _clearFamilyPathHighlight();
    _resizePathOverlay();
    var inp = document.getElementById(CONTAINER_ID + &quot;-fam-search&quot;);
    if (inp &amp;&amp; inp.value.trim() &amp;&amp; _familyPayload) {
      var v = inp.value.trim();
      if (Object.prototype.hasOwnProperty.call(_familyPayload, v))
        _applyFamilyTip(_familyPayload[v]);
    }
  }

  
  function renderTree() {
    try {
      if (DRILLDOWN) {
        _outerWrap = document.getElementById(CONTAINER_ID);
        _container = document.getElementById(CONTAINER_ID + &quot;-pc&quot;);
        if (!_outerWrap || !_container) {
          console.error(&quot;[phylo] Missing drilldown tree mount:&quot;, CONTAINER_ID);
          return;
        }
      } else {
        _outerWrap = null;
        _container = document.getElementById(CONTAINER_ID);
        if (!_container) {
          console.error(&quot;[phylo] Missing container:&quot;, CONTAINER_ID);
          return;
        }
      }
      
      
      if (DRILLDOWN) {
        _bindFamilySearch();
      }
      if (!window.phylocanvas || !window.phylocanvas.PhylocanvasGL) {
        console.error(&quot;[phylo] Phylocanvas.gl not loaded&quot;);
        return;
      }
      
      DD_SP_TYPE = window.phylocanvas.TreeTypes[&quot;Rectangular&quot;] || &quot;Rectangular&quot;;
      whenSized(_sizeTargetEl(), function () {
        _activeMeta  = META;
        _currentTree = _makeTree(NEWICK, META, &quot;Circular&quot;, !FAMILY_HOVER);
        _inFamilyMode = true;
        _bindResize(_sizeTargetEl());
        if (FAMILY_HOVER || DRILLDOWN) _bindHover(_container);
        if (DRILLDOWN) {
          _bindDrilldown(_container);
          var backEl = document.getElementById(CONTAINER_ID + &quot;-dd-back&quot;);
          if (backEl) {
            backEl.addEventListener(&quot;click&quot;, function () { _enterFamilyTree(); });
          }
          _resizePathOverlay();
        }
      });
    } catch (err) {
      console.error(&quot;[phylo] Phylocanvas render error:&quot;, err);
    }
  }

  function loadAndRender() {
    if (window.phylocanvas &amp;&amp; window.phylocanvas.PhylocanvasGL) {
      setTimeout(renderTree, 0);
      return;
    }
    var tag = document.querySelector(&#x27;script[data-phylocanvas-loader=&quot;true&quot;]&#x27;);
    if (!tag) {
      tag = document.createElement(&quot;script&quot;);
      tag.src = CDN;
      tag.async = true;
      tag.setAttribute(&quot;data-phylocanvas-loader&quot;, &quot;true&quot;);
      (document.head || document.documentElement).appendChild(tag);
      tag.addEventListener(&quot;load&quot;, function () { setTimeout(renderTree, 0); }, { once: true });
      tag.addEventListener(&quot;error&quot;, function () {
        console.error(&quot;[phylo] Failed to load Phylocanvas.gl from&quot;, CDN);
      });
      return;
    }
    var n = 0;
    var poll = setInterval(function () {
      if (window.phylocanvas &amp;&amp; window.phylocanvas.PhylocanvasGL) {
        clearInterval(poll);
        renderTree();
      } else if (++n &gt; 200) {
        clearInterval(poll);
        console.error(&quot;[phylo] Timeout waiting for Phylocanvas.gl&quot;);
      }
    }, 50);
  }

  Promise.all([
    fetch(&quot;/assets/data-science/avilist/phylogeny/family_tree.nwk&quot;).then(function(r){return r.text();}),
    fetch(&quot;/assets/data-science/avilist/phylogeny/family_meta.json&quot;).then(function(r){return r.json();})
  ]).then(function(res){
    NEWICK = res[0];
    META   = res[1];
    if (document.readyState === &quot;loading&quot;) {
      document.addEventListener(&quot;DOMContentLoaded&quot;, loadAndRender, { once: true });
    } else {
      setTimeout(loadAndRender, 0);
    }
  }).catch(function(err){
    console.error(&quot;[phylo] Failed to load tree data:&quot;, err);
  });
})();&lt;/script&gt;&lt;/body&gt;&lt;/html&gt;" sandbox="allow-scripts allow-same-origin" scrolling="no" style="width:100%;min-width:280px;height:985px;border:none;border-radius:8px;border:1px solid #d0d7de;background:#ffffff;display:block;"></iframe></div>


    [phylo] Using cached family tree (family_tree.nwk)
    [phylo] Using cached family subtrees (252 families in subtrees/)
    [phylo] Loaded 252 family subtrees for inline mode





So what can we learn from this evolutionary tree? As with our previous visualizations, the first glaring takeaway is that most bird families are passerines (light yellow nodes) but unlike the prior bar plots and sunburst plots we can now also see that passerines have evolved relatively recently compared to other bird families (scientific evidence confirms they evolved in Australia ~47 Ma). So what about the most ancestral birds? How did evolution branch and branch to eventually come up with passerines?

Let's take a look at the first evolutionary branches from the common bird ancestor: we find that the most "ancient" bird families include ostriches, tinamous, and rheas which fits in with the modern paleontological consensus that the most recent common ancestor of birds that survived the K-Pg extinction were ground-dwelling. We then see the emergence of ducks, geese, and swans as well as gamebirds (pheasants, quails, turkey). Continuing in evolutionary time we see branching to produce seabirds and shorebirds (as well as _Strisores_ such as the nightjars, potoos, hummingbirds, and swifts) and then kingfishers, woodpeckers, owls, birds of prey, and parrots before coming to the evolutionary branching that created _Passeriformes_ that now account for 60% of bird species.

The above whirlwind tour through evolutionary time obviously left out tons of interesting birds so explore the evolutionary tree for yourself to see what you can learn (for example, I had no idea that grebes were most closely related to flamingoes!).

## 4) Geography

### World map by species count

Having visualized the evolutionary relationship between modern bird lineages, I was interested to see if we could plot the **geographic distribution** of birds worldwide. So I built a choropleth of species richness per **ISO country**, using the [eBird API 2.0](https://documenter.getpostman.com/view/664302/S1ENwy59) and then merged the results with AviList's nomenclature.

Below, you can see each country colored by species richness and then use ther search bar to narrow the results to your favorite bird family to see how certain bird lineages are restricted to specific geographic areas.

<details markdown="1" class="avilist-setup-code">
<summary>Show code — choropleth &amp; family picker</summary>




```python
import json
import os
import importlib

import plotly.graph_objects as go

from birds_nb import COUNTRY_KEYWORDS, ISO3_TO_NAME

import ebird_spatial
importlib.reload(ebird_spatial)
from ebird_spatial import build_choropleth_country_mat

EBIRD_CACHE = DATA_DIR / ".cache_ebird"
_api_key = os.environ.get("EBIRD_API_KEY", "").strip()
all_iso = sorted(COUNTRY_KEYWORDS.keys())
_ebird = build_choropleth_country_mat(
    df_species,
    all_iso,
    _api_key,
    EBIRD_CACHE,
    force_refresh=False,
)
country_mat = _ebird["country_mat"]
totals = _ebird["totals_matched"].reindex(all_iso, fill_value=0)
totals_raw = _ebird["totals_ebird_raw"].reindex(all_iso, fill_value=0)
country_names = [ISO3_TO_NAME.get(iso, iso) for iso in all_iso]

print(
    "[eBird choropleth] ISO3 without ISO-2 map:",
    len(_ebird["iso3_missing_iso2"]),
    "| API/network failures:",
    len(_ebird["iso3_fetch_failed"]),
)
print(
    "  eBird codes not in taxonomy table:",
    f'{_ebird["n_codes_unmatched_taxonomy"]:,}',
    "| on list but not in AviList (binomial):",
    f'{_ebird["n_codes_unmatched_avilist"]:,}',
)
print(
    "  eBird list × country dropped (not in AviList Range_countries when parsed):",
    f'{_ebird.get("n_pairs_range_filtered", 0):,}',
)
if _ebird["iso3_missing_iso2"][:5]:
    print("  no ISO-2 (sample):", _ebird["iso3_missing_iso2"][:8])
if _ebird["iso3_fetch_failed"][:5]:
    print("  fetch failed (sample):", _ebird["iso3_fetch_failed"][:8])

fe = df_family.set_index("Scientific_name")["Family_English_name"].to_dict()


def _z_for(family: str):
    if family not in country_mat.index:
        return totals.values
    return country_mat.loc[family].reindex(all_iso, fill_value=0).values


def _label(fam: str) -> str:
    return family_label(fam, fe.get(fam, ""))


labels_to_z: dict[str, list[int]] = {"All families": totals.astype(int).tolist()}
for fam in sorted(country_mat.index):
    labels_to_z[_label(fam)] = _z_for(fam).astype(int).tolist()

_hover_cd = np.column_stack([country_names, totals_raw.astype(int).values])

# YlOrRd as used by Plotly; first stop replaced so only z==0 (norm 0) reads light grey.
_GEO_YL_OR_RD = [
    [0.0, "rgb(255,255,204)"],
    [0.125, "rgb(255,237,160)"],
    [0.25, "rgb(254,217,118)"],
    [0.375, "rgb(254,178,76)"],
    [0.5, "rgb(253,141,60)"],
    [0.625, "rgb(252,78,42)"],
    [0.75, "rgb(227,26,28)"],
    [0.875, "rgb(189,0,38)"],
    [1.0, "rgb(128,0,38)"],
]
_geo_cs_eps = 1e-6
_GEO_COLORSCALE = (
    [[0.0, "rgb(230,230,230)"], [_geo_cs_eps, _GEO_YL_OR_RD[0][1]]] + _GEO_YL_OR_RD[1:]
)

fig = go.Figure(
    go.Choropleth(
        locations=all_iso,
        z=totals.values,
        locationmode="ISO-3",
        customdata=_hover_cd,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Number of species: %{z:.0f}<extra></extra>"
        ),
        colorscale=_GEO_COLORSCALE,
        colorbar_title="species",
        marker_line_color="white",
        marker_line_width=0.3,
    )
)

fig.update_layout(
    title="Species per country — all families (eBird regional list × AviList)",
    height=600,
    margin=dict(l=10, r=10, t=60, b=10),
    geo=dict(projection_type="natural earth", showframe=False, showcoastlines=True),
    # No layout tween when the family picker restyles z (snappier map updates).
    transition=dict(duration=0),
)

DIV_ID = "geo-choropleth"
fig_html = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, div_id=DIV_ID)

payload_json = json.dumps(labels_to_z)


display(
    HTML(
        f"""
<div class="geo-family-picker" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  margin-bottom: 10px; position: relative; max-width: min(520px, 96vw);">
  <label for="{DIV_ID}-search" style="display:block; font-size: 0.82rem; font-weight: 600; color: #24292f; margin-bottom: 4px;">
    Family <span style="font-weight:400;color:#57606a;">(type to filter, ↑↓ Enter)</span>
  </label>
  <input id="{DIV_ID}-search" type="text"
         placeholder="e.g. Parrot, Thraupidae, Accipitridae…"
         autocomplete="off" spellcheck="false"
         role="combobox" aria-autocomplete="list" aria-controls="{DIV_ID}-suggest" aria-expanded="false"
         style="width: 100%; box-sizing: border-box; padding: 8px 10px;
         border: 1px solid #d0d7de; border-radius: 6px; font-size: 14px; outline: none;" />
  <div id="{DIV_ID}-suggest" role="listbox" aria-label="Family suggestions"
       style="display: none; position: absolute; left: 0; right: 0; z-index: 100;
       margin-top: 4px; max-height: min(320px, 42vh); overflow-y: auto;
       background: #fff; border: 1px solid #d0d7de; border-radius: 6px;
       box-shadow: 0 12px 28px rgba(31,35,40,0.18);"></div>
</div>
{fig_html}
<script>
(function() {{
  const payload = {payload_json};
  const ALL_KEY = "All families";
  const input = document.getElementById("{DIV_ID}-search");
  const panel = document.getElementById("{DIV_ID}-suggest");
  const LABELS = Object.keys(payload);
  let visible = [];
  let activeIdx = -1;

  function escapeHtml(s) {{
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }}

  function highlight(label, qt) {{
    if (!qt) return escapeHtml(label);
    const ll = label.toLowerCase();
    const ql = qt.toLowerCase();
    const i = ll.indexOf(ql);
    if (i < 0) return escapeHtml(label);
    return escapeHtml(label.slice(0, i))
      + '<mark style="background:#fff8c5;padding:0 1px;border-radius:2px;">'
      + escapeHtml(label.slice(i, i + qt.length)) + "</mark>"
      + escapeHtml(label.slice(i + qt.length));
  }}

  function buildVisible(q) {{
    const qt = q.trim().toLowerCase();
    if (!qt) {{
      const rest = LABELS.filter(function (l) {{ return l !== ALL_KEY; }})
        .sort(function (a, b) {{ return a.localeCompare(b); }});
      return {{ rows: [ALL_KEY].concat(rest.slice(0, 22)), more: Math.max(0, rest.length - 22) }};
    }}
    const hit = LABELS.filter(function (l) {{ return l.toLowerCase().indexOf(qt) >= 0; }});
    hit.sort(function (a, b) {{
      const ca = a.toLowerCase().indexOf(qt);
      const cb = b.toLowerCase().indexOf(qt);
      if (ca !== cb) return ca - cb;
      return a.localeCompare(b);
    }});
    return {{ rows: hit.slice(0, 80), more: Math.max(0, hit.length - 80) }};
  }}

  function apply(label) {{
    if (!(label in payload)) return;
    Plotly.restyle("{DIV_ID}", {{ z: [payload[label]] }}, [0]);
    Plotly.relayout("{DIV_ID}", {{
      "title.text": "Species per country — " + label + " (eBird × AviList)",
    }});
  }}

  function selectAndApply(lbl) {{
    input.value = lbl;
    apply(lbl);
    panel.style.display = "none";
    input.setAttribute("aria-expanded", "false");
  }}

  function renderList() {{
    const q = input.value;
    const qt = q.trim();
    const built = buildVisible(q);
    visible = built.rows;
    activeIdx = -1;
    let html = "";
    for (let idx = 0; idx < visible.length; idx++) {{
      const lbl = visible[idx];
      html +=
        '<div role="option" class="geo-suggest-row" data-idx="' +
        idx +
        '" style="padding:8px 12px;cursor:pointer;font-size:13px;line-height:1.4;' +
        'border-bottom:1px solid #f0f3f6;">' +
        highlight(lbl, qt) +
        "</div>";
    }}
    if (built.more > 0) {{
      html +=
        '<div style="padding:7px 12px;font-size:12px;color:#57606a;background:#f6f8fa;' +
        'border-top:1px solid #eaeef2;">' +
        (!qt
          ? "…and " + built.more + " more families — keep typing to search"
          : "…" + built.more + " more matches — refine your search") +
        "</div>";
    }}
    if (!html) {{
      html =
        '<div style="padding:10px 12px;color:#57606a;font-size:13px;">No matching families</div>';
    }}
    panel.innerHTML = html;
    Array.prototype.forEach.call(panel.querySelectorAll(".geo-suggest-row"), function (el) {{
      el.addEventListener("mousedown", function (e) {{ e.preventDefault(); }});
      el.addEventListener("click", function () {{
        const i = parseInt(el.getAttribute("data-idx"), 10);
        const lbl = visible[i];
        if (lbl) selectAndApply(lbl);
      }});
    }});
  }}

  function showPanel() {{
    panel.style.display = "block";
    input.setAttribute("aria-expanded", "true");
    renderList();
  }}

  function hidePanel() {{
    panel.style.display = "none";
    input.setAttribute("aria-expanded", "false");
    activeIdx = -1;
  }}

  function updateHighlight() {{
    const rows = panel.querySelectorAll(".geo-suggest-row");
    for (let i = 0; i < rows.length; i++) {{
      rows[i].style.background = i === activeIdx ? "#ddf4ff" : "";
    }}
    if (activeIdx >= 0 && rows[activeIdx]) {{
      rows[activeIdx].scrollIntoView({{ block: "nearest" }});
    }}
  }}

  input.addEventListener("focus", function () {{ showPanel(); }});
  input.addEventListener("input", function () {{
    showPanel();
    const v = input.value.trim();
    if (v in payload) apply(v);
  }});
  input.addEventListener("change", function () {{
    const v = input.value.trim();
    if (v in payload) apply(v);
  }});
  input.addEventListener("keydown", function (e) {{
    const n = visible.length;
    if (panel.style.display === "none") {{
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {{
        e.preventDefault();
        showPanel();
        if (e.key === "ArrowDown") activeIdx = visible.length ? 0 : -1;
        else activeIdx = visible.length ? visible.length - 1 : -1;
        updateHighlight();
      }}
      return;
    }}
    if (e.key === "ArrowDown") {{
      e.preventDefault();
      if (activeIdx < 0) activeIdx = 0;
      else activeIdx = Math.min(activeIdx + 1, n - 1);
      updateHighlight();
    }} else if (e.key === "ArrowUp") {{
      e.preventDefault();
      if (activeIdx < 0) activeIdx = n - 1;
      else activeIdx = Math.max(activeIdx - 1, 0);
      updateHighlight();
    }} else if (e.key === "Enter") {{
      if (activeIdx >= 0 && visible[activeIdx]) {{
        e.preventDefault();
        selectAndApply(visible[activeIdx]);
      }}
    }} else if (e.key === "Escape") {{
      hidePanel();
    }}
  }});
  document.addEventListener("click", function (e) {{
    const wrap = input.closest(".geo-family-picker");
    if (wrap && !wrap.contains(e.target)) hidePanel();
  }});
}})();
</script>
"""
    )
)

```

    [eBird choropleth] ISO3 without ISO-2 map: 0 | API/network failures: 0
      eBird codes not in taxonomy table: 2,078 | on list but not in AviList (binomial): 380
      eBird list × country dropped (not in AviList Range_countries when parsed): 29,162









</details>

<iframe src="/assets/data-science/avilist/figures/geo-choropleth.html" style="width:min(900px,100%);height:700px;border:none;border-radius:8px;display:block;margin:1em auto;" loading="lazy"></iframe>


Visualizing the geographic distribution of bird families can reveal some amazing insights into how birds evolved and disperesed across the globe since the K-Pg extinction event when diversification really "took off" (my wife Sara insisted I include this joke in my writeup). At this time the Earth's continents were in the process of breaking apart from the supercontinents of Laurasia (north) and Gondwana (south) into the landmasses we recognize today. As tectonic plates shifted, the Atlantic Ocean widened and created an insurmountable barrier, isolating bird lineages into the Old World (Europe, Asia, Africa, and Australasia) and New World (North and South America). Geographically isolated by the Atlantic, the ancestors of modern bird species underwent "adaptive radiation" evolving to fill the specific ecological niches available to them. While this did create specialization, the Old World and the New World often contained very similar ecological niches (e.g., tropical rainforests, arid deserts, temperate woodlands) leading to a phenomonen known as **convergent evolution** in which evolutionarily distant and completely unrelated species evolved the exact same evolutionary adaptations to take advantage of similarities in their ecological niches (such as seed-eating or nectar-sipping).

![hummingbird sunbird](/images/data-science/avilist/hummingbird_sunbird.png)
<br>
_Comparison shots I took back from 2025 of a Green-and-white Hummingbird (Elliotomyia viridicauda) I saw in Peru with a Sahul Sunbird (Cinnyris frenatus) I saw in Indonesia_

A classic example of convergent evolution in ornithology is given by the distantly related hummingbird and sunbird. At first glance hummingbirds and sunbirds seem like they'd be very closely related: with their small size, irridescent plumage, and nectar-driven diets, these bird lineages look and behave extremely similar. However, Hummingbirds (family _Trochilidae_) and Sunbirds (family _Nectariniidae_) are actually only very distantly related with hummingbirds being more closely related to swifts and sunbirds being more closely related to passerines such as crows (go back to the evolutionary tree and seach for each family to see for yourself!). When we take a look at their geographic distribution (try typing in "hummingbird" and then "sunbird" in the above search bar), we see that Hummingbirds are exclusively found in the New World while Sunbirds are exclusively found in the Old World - their last common ancestor dates back to before the continents broke apart! Their similar appearance, morphology, and behavior evolved completely indepedently under geographic isolation as common adaptations to similar ecological niches continents apart.

### Under- / over-representation of birds by continent

Given that some families show pretty extreme geographic isolation (e.g. hummingbirds in the Americas and nowhere else), I was curious to visualize this for the top 40 species-rich bird families. Relying only on AviList metadata, I calculated a *Family × Continent* species count, then computed a **z-score per family** across continents where a positive z-score (red) means over-represented on that continent relative to its global distribution and a negative z-score (blue) means under-represented.


```python
fc = (
    df_species[["Family", "Range_continents"]].explode("Range_continents")
    .dropna(subset=["Family", "Range_continents"]).rename(columns={"Range_continents": "Continent"})
)
fc_mat = fc.groupby(["Family", "Continent"]).size().unstack(fill_value=0)
fc_top = fc_mat.reindex(richest_families["Family"].head(40)).fillna(0)
_continent_plot_order = [
    "North America", "South America", "Europe", "Africa", "Asia", "Oceania", "Antarctic",
]
_cols = [c for c in _continent_plot_order if c in fc_top.columns]
_cols.extend([c for c in fc_top.columns if c not in _cols])
fc_top = fc_top[_cols]
fe = df_family.set_index("Scientific_name")["Family_English_name"].to_dict()
ytick = [family_label(f, fe.get(f, "")) for f in fc_top.index]
fc_z = fc_top.sub(fc_top.mean(1), 0).div(fc_top.std(1).replace(0, np.nan), 0).fillna(0)
xtick = [CONTINENT_DISPLAY.get(c, c) for c in fc_top.columns]
fig, ax = plt.subplots(figsize=(10, 14))
sns.heatmap(
    fc_z, cmap="RdBu_r", center=0, annot=fc_top.astype(int), fmt="d", 
    cbar_kws={"label": "z-score"}, lw=0.3, ax=ax, 
    xticklabels=xtick, yticklabels=ytick
)
ax.set_xlabel("")
ax.set_ylabel("")
plt.tight_layout()
plt.show()

```

    /var/folders/99/lcs5c5z50pv845b2s0_pvzw40000gn/T/ipykernel_2227/2168864800.py:15: Pandas4Warning: Starting with pandas version 4.0 all arguments of mean will be keyword-only.
      fc_z = fc_top.sub(fc_top.mean(1), 0).div(fc_top.std(1).replace(0, np.nan), 0).fillna(0)
    /var/folders/99/lcs5c5z50pv845b2s0_pvzw40000gn/T/ipykernel_2227/2168864800.py:15: Pandas4Warning: Starting with pandas version 4.0 all arguments of std will be keyword-only.
      fc_z = fc_top.sub(fc_top.mean(1), 0).div(fc_top.std(1).replace(0, np.nan), 0).fillna(0)



    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_49_1.png)
    


The first thing I noticed in the above plot is that the three most species-rich families (_Tyrannidae_, _Thraupidae_, and _Trochilidae_) are almost entirely over-represented in the New World, specifically in the Neotropics (Central + South America). Why is this? After some digging in the scientific literature, I found that the reason is largely due to geographic isolation; for tens of millions of years during the Cenozoic Era, South America was a massive island continent (similar to Australia today) allowing its ancestral bird species to evolve without competition from Old World birds with similar evolutionary adaptations. About 25 million years ago, geological upheaval formed the massive Andes mountain range fragmenting ecological niches into micro-climates and aggressively driving speciation of the ancestral Neotropic lineages. Add in the fact that just on the otherside of this massive mountain range was the Amazon rainforest, one of the most biodiverse areas on the entire planet, and South America became a hotspot for speciation. 

Traveling along Peru's Manu Road, a legendary spot for birding, up through the Andes, down through cloud forest, and ultimately to the Amazon river basin remains arguably the richest area on the planet for birding (certainly the most new species I've ever seen in such a small amount of time!). Around 3 million years ago, the Isthus of Panama rose from the sea, connecting South America and North America allowing these New World Lineages to spread up North (which is why we see a milder over-representation in North America compared to South America but an enrichment of both compared to other continents).

## 5) Conservation

I was curious about what the AviList's metadata could tell me about the conservation status of different bird lineages. To do this, I extracted threat and extinction codes across  global avifauna, using [IUCN Red List](https://www.iucnredlist.org/) status attached to each AviList species.

### Which orders are the most threatened?

Below I generated stacked bar plots representing every bird order (ranked by species count) and then colored percent of species by IUCN status.


```python
from matplotlib.patches import Rectangle

iucn_plot_order = ["LC", "NT", "VU", "EN", "CR", "EW", "EX", "DD", "NE"]
iucn_colors = {"LC": "#60c060", "NT": "#cfd862", "VU": "#f2c64e", "EN": "#ef8a3b", "CR": "#d83333", "EW": "#6f21a0", "EX": "#2a2a2a", "DD": "#a0a0a0", "NE": "#dedede"}
iucn_by_order = df_species.groupby(["Order", "IUCN"], observed=True).size().unstack(fill_value=0).reindex(columns=iucn_plot_order, fill_value=0)
iucn_by_order["total"] = iucn_by_order.sum(1)
iucn_by_order = iucn_by_order.sort_values("total", ascending=True)
frac = iucn_by_order.drop(columns=["total"]).div(iucn_by_order["total"], 0)
yl = [order_label(o) for o in frac.index]
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_facecolor("white")
bottom = np.zeros(len(frac))
for cat in iucn_plot_order:
    ax.barh(yl, frac[cat], left=bottom, color=iucn_colors[cat], label=cat, ec="white", lw=0.3)
    bottom += frac[cat].values
ax.set_xlim(0, 1)
ax.margins(x=0)
y0, y1 = ax.get_ylim()
y_lo, y_hi = min(y0, y1), max(y0, y1)
hatch_bg = Rectangle((0, y_lo), 1, y_hi - y_lo, facecolor="#d8d8d8", edgecolor="none", hatch="xx", zorder=0)
ax.add_patch(hatch_bg)
for p in ax.patches:
    if p is not hatch_bg:
        p.set_zorder(2)
for y_pos, n_sp in zip(range(len(yl)), iucn_by_order["total"]):
    ax.text(1.02, y_pos, f"n={int(n_sp)}", va="center", ha="left", fontsize=9, clip_on=False, zorder=3)
ax.set_xlabel("fraction of species")
ax.set_title("IUCN by order")
ax.legend(bbox_to_anchor=(1.14, 1), loc="upper left")
plt.tight_layout(rect=(0.02, 0.03, 0.88, 0.98))
plt.show()

```

    /var/folders/99/lcs5c5z50pv845b2s0_pvzw40000gn/T/ipykernel_2227/13489930.py:6: Pandas4Warning: Starting with pandas version 4.0 all arguments of sum will be keyword-only.
      iucn_by_order["total"] = iucn_by_order.sum(1)



    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_55_1.png)
    


**IUCN Red List legend**

| Code | Category | In plain English |
|------|----------|------------------|
| **LC** | Least concern | Not considered threatened at a global scale. |
| **NT** | Near threatened | Close to qualifying as threatened, or likely to become threatened. |
| **VU** | Vulnerable | High risk of extinction in the wild. |
| **EN** | Endangered | Very high risk of extinction in the wild. |
| **CR** | Critically endangered | Extremely high risk of extinction in the wild. |
| **EW** | Extinct in the wild | Only survives in captivity or outside its natural range. |
| **EX** | Extinct | No reasonable doubt the last wild individual is gone. |
| **DD** | Data deficient | Too little information to assess extinction risk. |
| **NE** | Not evaluated | Not yet assessed against Red List criteria (or missing / nonstandard values mapped here in this notebook). |

Each colored segment is the **fraction of species** in that order falling in that category; the value of `n=` on the right indicates the number of species in that order.

What's the takeaway from the above bar plot? Depressingly, it seems like virtually no bird order is immune from conservation risk. However, the most threatened orders (depending on how we calculate it) seem to be:
- **Gruiformes (cranes, rails, coots)**
- **Procellariiformes (albatrosses, petrels, shearwaters)**
- **Pelecaniformes (pelicans, herons, ibises)**
- **Podicipediformes (grebes)**

Interestingly, they all seem to be seabirds/shorebirds... When I dug into this a little further, a number of leading causes emerged from the literature:
- **climate change and habitat loss** (specifically wetland degradation)
- **high levels of bycatch** (longline fishing and gillnets)
- **"K-selection" as the evolutionary breeding strategy** (slow to reach sexual maturity with few young that require heavy investments)

Because I chose to plot the above visualization as percentage of total species within an order, some orders like Passeriformes look like they're doing relatively well in terms of conservation. However, in terms of total number of species under threat, the most threatened order actually is **Passeriformes**! At approximately 600 species under threat, 9% of Passeriformes have a Red List status ranging from Vulnerable to Extinct. To put this in perspective, ~600 species is more species than entirety of the next largest bird order (swifts and hummingbirds with n=472).

### Which orders have the most extinctions?

This becomes clear when we instead plot extinctions by order and see that the number of extinct passerines overwhelms the next most extinction-prone orders.


```python
extinct = df_species[df_species["is_extinct"]].copy()
print(f"{len(extinct)} extinct / possibly extinct")
ext_by_order = extinct["Order"].value_counts().sort_values(ascending=True)
yl = [order_label(o) for o in ext_by_order.index]
fig, ax = plt.subplots(figsize=(9, max(4, len(ext_by_order) * 0.35)))
ax.barh(yl, ext_by_order.values, color="#6f21a0")
ax.set_xlabel("extinct / possibly extinct")
ax.set_title("Extinct by order")
plt.tight_layout()
plt.show()

```

    168 extinct / possibly extinct



    
![png](/images/data-science/avilist/2026-05-12-ebird-avilist_61_1.png)
    


So what can you and I do to help promote bird conservation and protect brids threatened by extinction?

- Support conservation oragnizations like the the [Cornell Lab of Ornithology](https://www.birds.cornell.edu/home/), [Birds Canada](https://www.birdscanada.org/), and the [Audubon Society](https://www.audubon.org/) by donating your money or time
- Practice ethical birding, and educate yourself and others
- Become a community scientist by logging your sightings on platforms like [eBird](https://ebird.org/home)
- Make windows safer by installing screens or applying decals (up to 1 billion birds die annually in North America alone from window collisions)
- Keep cats indoors (free-roaming domestic and feral cats kill billions of birds annually)
- Turn off your lights (especially during spring and fall migration seasons)

As with most of these data science posts, my main goals was to develop a deeper intuition for the subject matter and build some tools to help myself (and others) explore this rich dataset.

Hopefully you learned something and maybe even got excited about birding along the way.

{% endraw %}
