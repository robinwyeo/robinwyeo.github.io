---
title: "(Data) Science"
permalink: /data-science/
author_profile: true
---

# Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age

*Adapted from my PhD oral defense (September 15, 2020, Stanford University). Niche and brain illustrations on the original slides included third-party credits (e.g., Lancaster University).*

As populations age, understanding how adult stem cells change—and whether those changes can be modified—becomes central to neuroscience and regenerative medicine. My graduate work asked a chromatin-focused question about **neural stem cells (NSCs)** in the adult mouse brain: **how does the accessible genome remodel with age, and does that remodeling help explain why activated NSCs lose the ability to migrate?** Below is a narrative version of the defense, followed (after a break) by a separate **PCA workshop** from a later seminar.

## On this page

- [The challenge of an aging brain](#challenge-aging-brain)
- [Neural stem cells and the subventricular zone niche](#svz-niche)
- [Why neurogenesis research turned to the genome—and beyond RNA](#genome-beyond-rna)
- [Part 1 — Chromatin landscapes of SVZ populations](#part1-chromatin)
- [Part 2 — Pathways underlying opposing chromatin shifts](#part2-pathways)
- [Part 3 — Functional tests of adhesion and migration](#part3-migration)
- [Part 4 — ROCK inhibition as a rejuvenation lever](#part4-rock)
- [Synthesis, implications, and next steps](#synthesis-next)
- [Workshop: Principal Component Analysis (PCA)](#workshop-pca)

---

## The challenge of an aging brain {: #challenge-aging-brain}

Demographic projections highlight steady growth in the fraction of adults aged 65 and older—so conditions that accumulate with age are not only biomedical problems but societal ones (for example, Ortman *et al.*, 2014, on U.S. population trends). **Aging is the strongest risk factor for cognitive decline and for several neurodegenerative and cerebrovascular diseases**, including Alzheimer’s disease, Parkinson’s disease, stroke, and vascular dementia. The scientific motivation is therefore twofold: we need mechanistic clarity, and we need interventions that preserve or restore the brain’s capacity for maintenance and repair.

## Neural stem cells and the subventricular zone niche {: #svz-niche}

In the adult mammalian brain, **neural stem cells reside in a structured niche**, notably the **subventricular zone (SVZ)** lining the lateral ventricles. From this niche, lineages of quiescent and activated stem cells, progenitors, and neuroblasts feed **migration toward the olfactory bulb** and can be mobilized after insults such as **stroke or traumatic brain injury**. The niche is cellularly complex: ependymal cells, endothelial cells, microglia, the choroid plexus, and diverse NSC states interact so that **stem cell behavior is not cell-autonomous in a vacuum**—it is co-produced by local signals and physical context (see also Navarro Negredo and Yeo, 2020, equal-contribution authors, for niche framing).

A consistent observation in rodents is that **adult neurogenesis and NSC activation decline with age**—fewer newly generated cells and damped activation dynamics across classic time points (for example, Bondolfi *et al.*, 2004). Yet the field still debated *which* molecular programs best explain **age-related neurogenic decline** and how those programs might differ between **quiescent NSCs (qNSCs)** and **activated NSCs (aNSCs)**.

## Why neurogenesis research turned to the genome—and beyond RNA {: #genome-beyond-rna}

Next-generation sequencing made it possible to compare **young and old NSCs** at scale. Much of the early mechanistic synthesis emphasized **transcriptional** change. Within the Brunet lab and across the field, single-cell and bulk RNA-centered studies implicated shifts in **proteostasis**, **autophagy**, and **inflammation** pathways, among others (including Leeman, 2018; Dulken, Buckley, Navarro Negredo, *et al.*, 2019; Artegiani, 2017; Basak, 2018; Hochgerner, 2018; Kalamakis, 2019; Llorens-Bobadilla, 2015; Luo, 2015; Mizrak, 2019; Shi, 2018; Shin, 2015; Zywitza, 2018).

RNA measurements, however, predominantly capture **expressed coding loci** and can **miss or under-weight regulatory architecture** in non-coding regions. A major gap was therefore **how the chromatin landscape of NSCs evolves with age**—especially in rare populations profiled *in vivo*.

**Chromatin accessibility** is attractive because it can report on **cell state** in ways that complement abundance-based RNA readouts: **poised or primed regulatory sites**, **candidate enhancers** in distal and intronic DNA, and **motifs consistent with transcription factor occupancy**. Aging is associated with broad epigenetic drift; the open question for NSCs was whether accessibility reorganization might **reveal new regulatory logic** for declining activation, migration, or repair.

---

## Part 1 — Chromatin landscapes of SVZ populations across age and activation state {: #part1-chromatin}

**Question:** What does genome-wide chromatin profiling reveal about NSC populations—and how do young and old cells differ?

We sorted **biologically defined populations** from the young and old SVZ and profiled **chromatin accessibility with ATAC-seq** (Assay for Transposase-Accessible Chromatin using sequencing; Buenrostro *et al.*, 2013). ATAC-seq is particularly well suited when populations are **rare** and must be measured **in native tissue context**: it yields high-resolution maps of **open chromatin** with practical inputs.

At individual loci, the defense highlighted **dynamic accessibility at neurogenic regulators**—for example, the **pro-neural *Ascl1*** locus showed **age- and state-dependent** patterns of open chromatin along the gene body and surrounding regulatory geography (young versus old; quiescent versus activated comparisons).

At the genome-wide level, **principal component analysis (PCA)** of accessibility libraries **separated major cell classes**—for instance **endothelial cells**, **astrocyte/qNSC-related** profiles, and **aNSC/neural progenitor-related** profiles—showing that chromatin structure carries **strong cell-identity signal**. Crucially, PCA also **separated young and old NSC chromatin**, indicating that aging imprints a **quantifiable shift** in regulatory DNA organization.

The headline statistical pattern was **opposing trajectories** between states: **with age, qNSC chromatin became more restricted (less permissive), while aNSC chromatin became more permissive**. That opposition is biologically striking because it argues against a single “everything loosens” or “everything compacts” story; instead, **quiescence and activation remodel accessibility in opposite directions**.

Mechanistically, the **same classes of genomic elements** mediated much of the divergence: **distal regions and introns**—the neighborhoods that often harbor **enhancers and other *cis*-regulatory elements**—rather than wholesale rewriting of promoter accessibility alone. Promoter accessibility and gene expression remained **globally positively correlated** across cell types and ages (ATAC-seq and RNA-seq concordance at promoters), but **distal and intronic peaks disproportionately encoded state and age specificity**. In other words, **promoters often look similar** while **enhancer-like regions carry the aging signature**.

**Part 1 conclusion (in plain language):** Chromatin separates NSCs by **activation state** and by **age**; **qNSCs and aNSCs undergo opposing accessibility changes**; and **most age-specific remodeling sits in intronic and distal DNA**, pointing to **enhancer-level mechanisms** as candidates for altered neurogenic potential.

---

## Part 2 — Pathways underlying opposing chromatin shifts with age {: #part2-pathways}

**Question:** Which cellular programs are statistically associated with those accessibility changes—and what do they predict about behavior?

Pathway-level integration showed a coherent theme: **with age, qNSCs tended to lose accessibility (and gene expression) in programs linked to adhesion and motility**, whereas **aNSCs gained accessibility (and expression) in those same broad classes**. Gene Ontology–style summaries in the deck grouped terms around **cell–cell adhesion**, **cadherin-related junctions**, **integrin-linked adhesion**, **cytoskeletal organization**, and related signaling (including Wnt- and cAMP-associated annotations as presented).

The chromatin predictions were **not abstract**: locus-level views highlighted **cadherins**, **integrins**, and **matrix metalloproteinases (MMPs)** as families where **young versus old** and **qNSC versus aNSC** trajectories moved in **opposite directions** for accessibility—and **RNA-seq from Dulken, Buckley, Navarro Negredo, *et al.*, 2019** supported **concordant expression changes** (qNSC/astrocytic signatures versus aNSC/NPC signatures).

Motif analysis added a **transcription-factor hypothesis**: the **NF1 family** emerged as enriched in **young qNSCs** and **old aNSCs**, linking the chromatin states to regulators with documented roles in **adhesion and cell motion** (motif analysis with **Mahfuza Sharmin** in the **Kundaje** group). Related slides noted **NFI** biology in brain development and **qNSC-associated enhancers**, framing NF1-family enrichment as more than a statistical artifact.

**Part 2 conclusion:** Aging produces **mirror-image adhesion programs** in qNSCs versus aNSCs at the level of **open chromatin and gene expression**. The simplest behavioral prediction is that **migration—an adhesion- and cytoskeleton-heavy process—should change specifically in activated NSCs**, where repair and neuroblast supply depend on motility.

---

## Part 3 — Functional tests of adhesion and migration {: #part3-migration}

**Question:** Can we experimentally validate the prediction that **aging alters NSC migration**—and connect phenotypes to **adhesive structures**?

The defense stated two directional hypotheses: **old qNSCs might move faster than young qNSCs**, while **old aNSCs might move slower than young aNSCs**. **Live-cell tracking** (including analysis with **Imaris**) quantified **migration speed** and **path complexity** *in vitro*.

The results matched the chromatin mirror: **aNSC migration speed decreased with age**, while **qNSCs were largely immobile in youth** but could exhibit **modest motility in old age**. In narrative terms, **aging makes activated NSCs less migratory and nudges quiescent NSCs toward a slightly more migratory regime**—a functional symmetry that parallels **opposing chromatin remodeling**.

Why care about **activated** migration? **Activated NSCs** display morphologies consistent with motility (**lamellipodia**, **filopodia**) and, in physiological and injury contexts, **mobilization and differentiation** support **ongoing neurogenesis** and **responses to acute damage**. If **old aNSCs migrate poorly**, one interpretation is **impaired regenerative or homeostatic capacity**, motivating a search for **druggable cytoskeletal nodes**.

Orthogonal **extracellular-matrix** assays reinforced the trend: **aging reduced how far aNSCs migrated** over **24–48 hours** in the presented experiments.

To connect migration to **force-bearing adhesions**, **FRET-based RGD tension sensors** (work with **Brian Zhong** in the **Dunn** lab) illustrated how **focal adhesions** and **actin stress fibers** can **co-localize**—and thus how **adhesion strength** might enter a mechanistic chain linking **chromatin states** to **movement**.

Finally, **vinculin**, a **focal-adhesion adaptor** coupling integrins to actin, showed **higher staining in old aNSCs** *in vitro* and **in the SVZ in vivo** (work with **Olivia Zhou**), aligning with the idea that **old activated NSCs are more “anchored”** even as they move less effectively.

**Part 3 conclusion:** **Opposing age-related changes in migration** mirror **opposing chromatin and expression shifts**; **adhesion-associated cytoskeletal structures** and **vinculin-rich focal adhesions** provide a plausible cellular intermediate phenotype for **old aNSCs**.

---

## Part 4 — ROCK inhibition as a rejuvenation lever for old activated NSCs {: #part4-rock}

**Question:** If old aNSC chromatin implicates **adhesion–cytoskeleton** programs, can we identify a **specific regulator** to test—and does modulating it **rescue migration**?

Pathway integration highlighted **ROCK** among upstream nodes associated with regions that **gain accessibility in old aNSCs**. **Rho-associated kinase (ROCK)** is often described as a **master regulator of actin-myosin contractility** and stress-fiber biology. Pharmacology with **Y-27632** is a standard probe of ROCK dependence.

The literature context is worth stating carefully: **ROCK inhibition can increase or decrease migration depending on cell type and context** (examples in the slides included **myoblasts**, **glioma cells**, **microglia**, **fibroblasts**, **dendritic cells**, **keratinocytes**, and **medulloblastoma cells**). The empirical question for NSCs is therefore not rhetorical—it is **empirical**.

The experimental answer shown in the defense was that **Y-27632 improved migration of old aNSCs**—a **partial rejuvenation** of a functional readout. Mechanistically, the deck argued that **stress-fiber elimination** is a plausible cellular route: **ROCK inhibition reduced actin stress fibers** in line with restored motility.

**Part 4 conclusion:** **ROCK** surfaced as a **top testable target** from **old aNSC chromatin changes**; **ROCK inhibition** improved **old aNSC migration** and **reversed a stress-fiber-heavy adhesive phenotype**.

---

## Synthesis, implications, and next steps {: #synthesis-next}

**Synthesis.** Aging triggers **divergent chromatin remodeling** in **quiescent versus activated NSCs**, enriched in **distal and intronic regulatory DNA** and coherent with **adhesion–migration pathways**. **Functionally, old activated NSCs migrate more slowly** and show **signs of stronger focal adhesion**, and **ROCK inhibition** can **restore migration**—linking **epigenomic state** to a **pharmacologically accessible cytoskeletal control point**.

**Future directions** sketched in the defense included: **mechanistic dissection of enhancers** that mediate age-related neurogenic decline; **in vivo** tests that recapitulate **migration phenotypes** observed *in vitro*; and **injury models** (stroke, TBI) asking how **old aNSC migration** and **ROCK** intersect with repair.

**Acknowledgments (abbreviated).** I am grateful to **Anne Brunet** and the **NSC team** and collaborators named on the original slides—including **Matthew Buckley**, **Jackie Butterfield**, **Ben Dulken**, **Katja Hebestreit**, **Chloe Kashiwagi**, **Subheksha Kc**, **Dena Leeman**, **Paloma Navarro Negredo**, **Tyson Ruetz**, **Lucy Xu**, **Xiaoai Zhao**, **Olivia Zhou**, and many others across Stanford—as well as committee members **Michael Bassik**, **Anshul Kundaje**, **Julien Sage**, and **Tony Wyss-Coray**, with support from a **Stanford Graduate Fellowship**, **Genentech Graduate Fellowship**, and **Stanford Genome Training Program**.

---

# Workshop: Principal Component Analysis (PCA) {: #workshop-pca}

*Originally presented at BDS Learning Seminar, December 8, 2022*

---

## Supervised vs. Unsupervised Learning

**Supervised learning** attempts to model relationships between *p* features X<sub>1</sub>, X<sub>2</sub>, ..., X<sub>p</sub> with a response variable *Y* based on *n* observations. Examples include regression and classification models.

**Unsupervised learning** instead explores relationships between the *p* features in the absence of any response variable (no prediction). This is an important part of **exploratory data analysis (EDA)**.

Two common techniques in unsupervised learning are:
- **Principal Component Analysis (PCA)**
- **Clustering techniques** (hierarchical clustering, k-means clustering, etc.)

![Supervised vs. Unsupervised Learning](/images/data-science/pca/supervised_unsupervised.png)

---

## What is PCA?

**Principal Component Analysis (PCA)** is a widely used unsupervised learning technique for the analysis of high-dimensional data.

High-dimensional data are data with many more features (*p*) than observations (*n*). High-throughput sequencing libraries (e.g. RNA-seq) are a classic example of high-dimensional data (*p* = 20,000 genes; *n* = 10 libraries).

PCA is a technique that allows us to summarize data with a large set of features with a **smaller number of representative features** that explain most of the variability present in the original data by computing **principal components**.

**Principal components** are the directions in feature space along which the original data are highly variable.

The most common applications of PCA are:
- Visualization of high-dimensional data
- Feature generation through dimensionality reduction

![PCA Concept](/images/data-science/pca/pca_concept.png)

---

## Why PCA? Visualizing High-Dimensional Data

We can easily visualize 150 datapoints with 2 features using a 2D scatterplot. Increasing dimensionality to 3 features, we can still use a 3D scatterplot. But what about 4 features? Or *n* >> 4 features? It becomes impossible to spatially visualize high-dimensional data.

![2D and 3D visualization](/images/data-science/pca/scatter_2d.png)

With such high-dimensional data, a natural question is: **are all features/dimensions equally informative?**

There often exist redundant features that are highly correlative with other features -- they don't actually add much new information. The **manifold hypothesis** states that high-dimensional datasets that occur in the real world lie along low-dimensional latent manifolds.

One natural way of visualizing high-dimensional data is to find a low-dimensional representation of the data that captures most of the information present.

---

## Workshop: Exploring the Iris Dataset in R

The built-in R **iris** dataset is a classic tutorial for data exploration. It contains 150 observations of 3 flower species (*setosa*, *versicolor*, *virginica*) with 4 features: Sepal Length, Sepal Width, Petal Length, and Petal Width.

![Iris flower species](/images/data-science/pca/iris_flower.png)

Since there are 4 features, we can't directly visualize the global properties of these 150 observations in a single plot. How can we answer questions like **which flower species are the most similar**?

### Exploring pairwise relationships

We can explore pairs of variables and plot them in 2D. For example, maybe we hypothesize there exists a relationship between width and length of sepals and petals:

```r
library(ggplot2)

ggplot(iris, aes(x = Sepal.Length, y = Sepal.Width)) +
  geom_point(size = 2, alpha = 0.7) +
  labs(x = "Sepal Length", y = "Sepal Width", title = "Sepal Length vs Width") +
  theme_minimal()

ggplot(iris, aes(x = Petal.Length, y = Petal.Width)) +
  geom_point(size = 2, alpha = 0.7) +
  labs(x = "Petal Length", y = "Petal Width", title = "Petal Length vs Width") +
  theme_minimal()
```

![Sepal scatter](/images/data-science/pca/iris_sepal_scatter.png)

![Petal scatter](/images/data-science/pca/iris_petal_scatter.png)

We can see a relationship between petal length and width but not much structure in the sepal measurements. However, we haven't learned anything about which species are globally most similar. Let's color by species:

```r
ggplot(iris, aes(x = Petal.Length, y = Petal.Width, color = Species)) +
  geom_point(size = 2, alpha = 0.7) +
  labs(x = "Petal Length", y = "Petal Width", title = "Petal Length vs Width") +
  theme_minimal()
```

![Petal scatter colored by species](/images/data-science/pca/iris_petal_scatter_color.png)

By coloring the points by species, we can start to see that *versicolor* and *virginica* might be more closely related. But this is only plotting 2 of the 6 possible feature relationships, so it doesn't capture all information in our data.

### Plotting all pairwise relationships

There are nice statistical functions that automate this process for us (e.g. `ggpairs` from the `GGally` package) and plot relationships between all features:

```r
library(GGally)

ggpairs(iris, columns = 1:4, aes(color = Species, alpha = 0.5)) +
  theme_minimal()
```

![Iris ggpairs](/images/data-science/pca/iris_ggpairs.png)

This works great for 4 features -- we get a nice summary of how the different features relate to one another, requiring \(\binom{4}{2} = 6\) scatterplots. However, the number of plots needed grows combinatorially with features (e.g. 10 features requires 45 plots, 100 features requires 4,950 plots).

### PCA to the rescue

What we need is a statistical tool that captures as much global information as possible about the relationship between these 4 features and allows us to visualize them in **2D**. **This is exactly what PCA does.**

```r
iris_pca <- prcomp(iris[, 1:4], center = TRUE, scale. = TRUE)

pca_df <- data.frame(
  PC1 = iris_pca$x[, 1],
  PC2 = iris_pca$x[, 2],
  Species = iris$Species
)

ggplot(pca_df, aes(x = PC1, y = PC2, color = Species)) +
  geom_point(size = 2, alpha = 0.7) +
  labs(
    x = sprintf("PC1 (%.1f%% variance)", summary(iris_pca)$importance[2, 1] * 100),
    y = sprintf("PC2 (%.1f%% variance)", summary(iris_pca)$importance[2, 2] * 100),
    title = "PCA of Iris Dataset"
  ) +
  theme_minimal()
```

![Iris PCA biplot](/images/data-science/pca/iris_pca_biplot.png)

We now have a **2-dimensional projection** of a 4-dimensional feature space. The PCA clearly shows that *setosa* is well-separated from the other two species, and that *versicolor* and *virginica* overlap considerably -- confirming that they are the most similar pair.

---

## How Does PCA Work?

PCA attempts to find a low-dimensional representation of the data that captures as much information about the features as possible.

The idea is that *n* observations live in *p*-dimensional space, but not all of these dimensions are equally informative. PCA distills these *p* dimensions down to *L* dimensions where the new dimensions are **linear combinations of the originals** constructed to capture as much possible variation in the *n* observations as possible.

### Finding the principal components

For a dataset of *n* observations with *p* features, the **first principal component** Z<sub>1</sub> is the normalized linear combination of features:

Z<sub>1</sub> = &phi;<sub>11</sub>X<sub>1</sub> + &phi;<sub>21</sub>X<sub>2</sub> + ... + &phi;<sub>p1</sub>X<sub>p</sub>

that has the **largest variance**. The coefficients &phi;<sub>11</sub>, &phi;<sub>21</sub>, ..., &phi;<sub>p1</sub> are called the **loadings** of the first principal component.

![PC1 and PC2 on population vs. ad spending data](/images/data-science/pca/pc_population_adspend.png)

In the example above, we are looking at population size and ad spending for 100 cities (*n* = 100, *p* = 2). The first principal component Z<sub>1</sub> = 0.839X<sub>1</sub> + 0.544X<sub>2</sub> is along the solid green line (the direction of largest variance). The **second principal component** Z<sub>2</sub> is the linear combination that has maximal variance out of all linear combinations that are **uncorrelated** with Z<sub>1</sub>: Z<sub>2</sub> = 0.544X<sub>1</sub> - 0.839X<sub>2</sub> (the dotted blue line, perpendicular to PC1).

### Proportion of variance explained

Each principal component is constructed to maximize variability explained, but each successive principal component explains less and less of the total variance. This can be visualized as a **scree plot**:

```r
var_explained <- summary(iris_pca)$importance[2, ] * 100
scree_df <- data.frame(PC = paste0("PC", 1:4), Variance = var_explained)
scree_df$PC <- factor(scree_df$PC, levels = scree_df$PC)

ggplot(scree_df, aes(x = PC, y = Variance)) +
  geom_col(fill = "steelblue") +
  geom_line(aes(group = 1), linewidth = 1) +
  geom_point(size = 3) +
  labs(x = "Principal Component", y = "% Variance Explained",
       title = "Scree Plot - Iris PCA") +
  theme_minimal()
```

![Iris scree plot](/images/data-science/pca/iris_scree_plot.png)

For the iris dataset, PC1 explains 73.0% and PC2 explains 22.9% of the total variance -- together they capture **95.9%** of the total variance, providing a very accurate 2D representation of the 4D data.

![USA Arrests: biplot and scree plot](/images/data-science/pca/usarrests_biplot.png)

![USA Arrests: scree plot](/images/data-science/pca/usarrests_scree.png)

In the USA Arrests dataset, PC1 (constructed primarily from Rape, Assault, and Murder numbers) explains 62% of the data while PC2 (driven mostly by urban proportion) explains 25% -- projecting these 4D data onto PC1 and PC2 captures 87% of the total variance.

### Geometric interpretation

Statistically, principal component loading vectors are directions in feature space along which data varies the most. **Geometrically**, principal components provide low-dimensional surfaces that are **closest** to the datapoints.

![Geometric interpretation: 3D data with projection plane](/images/data-science/pca/geometric_3d.png)

![Projected onto 2D](/images/data-science/pca/geometric_projection.png)

Computing the first two principal components defines the plane closest to our data (minimizing the Euclidean squared distance). When the original data are projected onto this plane, we retain the global features that distinguish the groups and are able to visualize them in a lower dimension.

---

## Mathematical Walkthrough: Student Grades Example

*Adapted from [The Mathematics Behind Principal Component Analysis](https://towardsdatascience.com/the-mathematics-behind-principal-component-analysis-fff2d7f4b643)*

**Goal:** Transform a given dataset **X** of dimension *p* to an alternative dataset **Y** of smaller dimension *k*.

The steps are:

1. Organize data into matrix **X** of dimensions *n* &times; *p*
2. Compute the mean for each dimension *p*
3. Calculate the covariance matrix of the whole dataset
4. Compute the eigenvalues and corresponding eigenvectors of the covariance matrix
5. Sort eigenvectors by decreasing eigenvalues and select *k* eigenvectors to form a *p* &times; *k* matrix **W**
6. Use the eigenvector matrix **W** to transform original data and project onto the new basis

### Step 1: Organize the data

Let's calculate PCA for a simple dataset about the grades of 5 students in 3 classes: Math, English, and Art.

![Student grades table](/images/data-science/pca/grades_table.png)

### Step 2: Compute the mean for each dimension

We remove the labels from our dataframe and get a numerical matrix **A** with 3 dimensions, then compute the mean of each:

![Grades matrix](/images/data-science/pca/grades_matrix.png)

![Grades mean](/images/data-science/pca/grades_mean.png)

### Step 3: Calculate the covariance matrix

We compute the covariance of two variables using the standard formula:

![Covariance formula](/images/data-science/pca/cov_formula.png)

![Covariance computation](/images/data-science/pca/cov_matrix.png)

![Covariance result](/images/data-science/pca/cov_result.png)

Key observations about the covariance matrix:
- The **diagonal entries** (blue) show the variance of each test
- Covariance between math and other subjects is **positive** -- higher math scores are correlated with higher scores in other subjects
- Covariance between english and art is **zero** -- there is no correlation between english and art scores

### Step 4: Compute eigenvalues and eigenvectors

Intuitively, an **eigenvector** is a vector whose direction remains unchanged when a linear transformation is applied to it.

**Definition:** Let **A** be a square matrix, **v** a vector, and &lambda; a scalar that satisfies **Av** = &lambda;**v**, then &lambda; is an **eigenvalue** associated with eigenvector **v** of **A**.

In practice, we compute the eigenvalues of **A** by solving for roots of the characteristic equation det(**A** - &lambda;**I**) = 0.

![Eigenvalue equation](/images/data-science/pca/eigen_equation.png)

![Determinant expansion](/images/data-science/pca/eigen_det.png)

![Characteristic equation](/images/data-science/pca/eigen_characteristic.png)

Solving the characteristic equation gives three eigenvalues:

![Eigenvalues](/images/data-science/pca/eigen_values.png)

Having calculated the eigenvalues, we plug each into the equation (**A** - &lambda;**I**)**v** = 0 to calculate their respective eigenvectors:

![Eigenvectors](/images/data-science/pca/eigen_vectors.png)

### Step 5: Sort eigenvectors and form matrix W

We now have 3 distinct eigenvalues, each with their associated eigenvector. The greater the eigenvalue, the more variance explained by that principal component.

![Eigenvector matrix W](/images/data-science/pca/eigsort_matrix_w.png)

To reduce our 3-dimensional data to 2-dimensional PC space, we construct the matrix **W** from the two eigenvectors with the largest eigenvalues.

### Step 6: Project onto the new basis

We use the eigenvector matrix **W** (3&times;2) to transform our original data **A** (5&times;3) onto PC space:

![Projection result](/images/data-science/pca/projection_result.png)

Let's verify this in R:

```r
grades <- matrix(c(90, 60, 90,
                    90, 90, 30,
                    60, 60, 60,
                    60, 60, 90,
                    30, 30, 30), nrow = 5, byrow = TRUE)
colnames(grades) <- c("Math", "English", "Art")
students <- c("Student 1", "Student 2", "Student 3", "Student 4", "Student 5")

grades_pca <- prcomp(grades, center = TRUE, scale. = FALSE)
proj_df <- data.frame(
  PC1 = grades_pca$x[, 1],
  PC2 = grades_pca$x[, 2],
  Student = students
)

ggplot(proj_df, aes(x = PC1, y = PC2, label = Student)) +
  geom_point(size = 3, color = "steelblue") +
  geom_text(vjust = -1, size = 3.5) +
  labs(
    x = sprintf("PC1 (%.1f%% variance)", summary(grades_pca)$importance[2, 1] * 100),
    y = sprintf("PC2 (%.1f%% variance)", summary(grades_pca)$importance[2, 2] * 100),
    title = "PCA Projection of Student Grades"
  ) +
  theme_minimal()
```

![Student grades PCA projection](/images/data-science/pca/grades_pca_plot.png)

PC1 captures 57.5% and PC2 captures 39.7% of the variance, together accounting for **97.2%** of the information in the original 3D data.

---

## PCA in Scientific Applications

PCA is extremely widely used for visualizing high-dimensional biological data. Here are two examples from the genomics literature.

### ATAC-seq data (~100K features)

ATAC-seq (Assay for Transposase-Accessible Chromatin using sequencing) measures chromatin accessibility across the genome. PCA is routinely used to visualize relationships between libraries with ~100,000 accessibility peaks as features.

![ATAC-seq PCA examples](/images/data-science/pca/atacseq_1.png)

![ATAC-seq PCA examples](/images/data-science/pca/atacseq_2.png)

![ATAC-seq PCA examples](/images/data-science/pca/atacseq_3.png)

### Genome-wide SNP data (~500K features)

PCA of genome-wide single nucleotide polymorphisms (SNPs) can reveal population structure and ancestry. With ~500,000 SNP features per individual, PCA compresses this information into interpretable 2D projections.

![Genome-wide SNP PCA examples](/images/data-science/pca/snp_1.png)

![Genome-wide SNP PCA examples](/images/data-science/pca/snp_2.png)

![Genome-wide SNP PCA examples](/images/data-science/pca/snp_3.png)

---

## PCA vs. t-SNE and UMAP

Two popular dimensionality reduction and visualization techniques that are very commonly used in single-cell RNA-seq are:
- **t-SNE** (t-distributed Stochastic Neighbor Embedding)
- **UMAP** (Uniform Manifold Approximation and Projection for Dimension Reduction)

In single-cell RNA-seq data, we typically have 10,000+ observations, each with ~5,000 dimensions. Due to the "curse of dimensionality," this leads to an incredibly sparse and disconnected network.

PCA is one natural approach for dimensionality reduction and visualization, but it is not particularly well-suited for the highly non-linear and sparse nature of scRNA-seq data.

Both t-SNE and UMAP are **neighbor graph algorithms** that attempt to preserve local relationships between data -- making them great at defining cell clusters and identifying heterogeneity in single-cell data.

![Comparison of PCA, t-SNE, and UMAP on single-cell data](/images/data-science/pca/pca_tsne_umap_comparison.png)

Key differences:
- **PCA**: Linear; distances in PCA plots have quantitative meaning; great for bulk data
- **t-SNE**: Non-linear; preserves local structure; distances between clusters are not meaningful
- **UMAP**: Non-linear; preserves both local and some global structure; faster than t-SNE

---

## Dimensionality Reduction: Amino Acid Descriptors

Beyond visualization, PCA is also powerful for **feature engineering** through dimensionality reduction.

**VHSE** (Vectors of Hydrophobic, Steric, and Electronic properties by principal components) is a great example. The authors gathered 50 physicochemical features for the 20 naturally occurring amino acids:
- 18 hydrophobic properties
- 17 steric properties
- 15 electronic properties

While this is descriptive, it's not very concise, and many of these features are likely redundant (do we really need 18 different values to describe the hydrophobicity of an amino acid?).

The authors performed 3 separate principal component analyses, reducing dimensionality from **50 to 8**:
- Hydrophobic properties: 18 &rarr; 2 (capturing 74.33% variance)
- Steric properties: 17 &rarr; 2 (capturing 78.68% variance)
- Electronic properties: 15 &rarr; 4 (capturing 77.97% variance)

![VHSE table](/images/data-science/pca/vhse_table.png)

![VHSE PCA](/images/data-science/pca/vhse_pca.png)

By using PCA, they dramatically reduced the number of dimensions needed to describe amino acid properties from 50 to 8 while retaining the majority of the information.

---

## Benefits and Limitations of PCA

### Benefits

- Reduces dimensionality of high-dimensional data through linear combinations
- Easy to compute
- Quantitative explanation of proportion of variance explained by PCs
- Distance in PCA plots has quantitative meaning (unlike t-SNE, UMAP, etc.)

### Limitations

- Low interpretability of PCs (especially with a high number of features)
- By definition, dimensionality reduction using PCs is accompanied by information loss
- Requires linearly correlative features
- Sensitive to scale of features
- PCA is not robust to outliers
