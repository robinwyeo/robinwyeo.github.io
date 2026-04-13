---
title: "Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age"
date: 2020-09-15
tags:
  - thesis
  - neural stem cells
  - ATAC-seq
  - chromatin
permalink: /data-science/nsc-chromatin-migration-thesis/
---

*Adapted from my PhD oral defense (September 15, 2020, Stanford University). Figures below are exported from the original PowerPoint deck; niche and brain illustrations retain third-party credits where noted on the slides (e.g., Lancaster University, Gonzales-Roybal *et al.*, 2013).*

As populations age, understanding how adult stem cells change—and whether those changes can be modified—becomes central to neuroscience and regenerative medicine. My graduate work asked a chromatin-focused question about **neural stem cells (NSCs)** in the adult mouse brain: **how does the accessible genome remodel with age, and does that remodeling help explain why activated NSCs lose the ability to migrate?** Below is a narrative version of the defense, with the original slide figures integrated for context.

---

## The challenge of an aging brain

Demographic projections highlight steady growth in the fraction of adults aged 65 and older—so conditions that accumulate with age are not only biomedical problems but societal ones (for example, Ortman *et al.*, 2014, on U.S. population trends). **Aging is the strongest risk factor for cognitive decline and for several neurodegenerative and cerebrovascular diseases**, including Alzheimer’s disease, Parkinson’s disease, stroke, and vascular dementia. The scientific motivation is therefore twofold: we need mechanistic clarity, and we need interventions that preserve or restore the brain’s capacity for maintenance and repair.

![U.S. population aged 65+ (millions), after Ortman *et al.*, 2014](/images/data-science/thesis/us-population-65plus.jpg)

![Aging and demographic context (slides adapted from public sources in the original deck)](/images/data-science/thesis/aging-psychology-chart.png)

![Additional demographic / aging-in-place framing from the defense slides](/images/data-science/thesis/aging-psychology-chart-2.png)

## Neural stem cells and the subventricular zone niche

In the adult mammalian brain, **neural stem cells reside in a structured niche**, notably the **subventricular zone (SVZ)** lining the lateral ventricles. From this niche, lineages of quiescent and activated stem cells, progenitors, and neuroblasts feed **migration toward the olfactory bulb** and can be mobilized after insults such as **stroke or traumatic brain injury**. The niche is cellularly complex: ependymal cells, endothelial cells, microglia, the choroid plexus, and diverse NSC states interact so that **stem cell behavior is not cell-autonomous in a vacuum**—it is co-produced by local signals and physical context (see also Navarro Negredo and Yeo, 2020, equal-contribution authors, for niche framing).

![SVZ niche, lineages, and injury context (slide artwork; third-party credits on original deck)](/images/data-science/thesis/svz-niche-schematic.png)

![Alternative SVZ / RMS schematic after Gonzales-Roybal *et al.*, 2013, as in the defense slides](/images/data-science/thesis/svz-niche-gonzales-a.png)
![Rostral migratory stream and olfactory bulb context (same source)](/images/data-science/thesis/svz-niche-gonzales-b.png)

A consistent observation in rodents is that **adult neurogenesis and NSC activation decline with age**—fewer newly generated cells and damped activation dynamics across classic time points (for example, Bondolfi *et al.*, 2004). Yet the field still debated *which* molecular programs best explain **age-related neurogenic decline** and how those programs might differ between **quiescent NSCs (qNSCs)** and **activated NSCs (aNSCs)**.

![Neurogenesis and NSC activation decline with age (Bondolfi *et al.*, 2004)](/images/data-science/thesis/neurogenesis-decline-age.png)

## Why neurogenesis research turned to the genome—and beyond RNA

Next-generation sequencing made it possible to compare **young and old NSCs** at scale. Much of the early mechanistic synthesis emphasized **transcriptional** change. Within the Brunet lab and across the field, single-cell and bulk RNA-centered studies implicated shifts in **proteostasis**, **autophagy**, and **inflammation** pathways, among others (including Leeman, 2018; Dulken, Buckley, Navarro Negredo, *et al.*, 2019; Artegiani, 2017; Basak, 2018; Hochgerner, 2018; Kalamakis, 2019; Llorens-Bobadilla, 2015; Luo, 2015; Mizrak, 2019; Shi, 2018; Shin, 2015; Zywitza, 2018).

![Transcriptional profiling of NSC aging: themes and representative studies from the defense slides](/images/data-science/thesis/nsc-aging-transcriptome-studies.png)

RNA measurements, however, predominantly capture **expressed coding loci** and can **miss or under-weight regulatory architecture** in non-coding regions. A major gap was therefore **how the chromatin landscape of NSCs evolves with age**—especially in rare populations profiled *in vivo*.

**Chromatin accessibility** is attractive because it can report on **cell state** in ways that complement abundance-based RNA readouts: **poised or primed regulatory sites**, **candidate enhancers** in distal and intronic DNA, and **motifs consistent with transcription factor occupancy**. Aging is associated with broad epigenetic drift; the open question for NSCs was whether accessibility reorganization might **reveal new regulatory logic** for declining activation, migration, or repair.

![Chromatin profiling complements transcription: cell state, enhancers, and TF binding (concept slide)](/images/data-science/thesis/chromatin-landscape-young-old-nsc.png)

---

## Part 1 — Chromatin landscapes of SVZ populations across age and activation state

**Question:** What does genome-wide chromatin profiling reveal about NSC populations—and how do young and old cells differ?

We sorted **biologically defined populations** from the young and old SVZ and profiled **chromatin accessibility with ATAC-seq** (Assay for Transposase-Accessible Chromatin using sequencing; Buenrostro *et al.*, 2013). ATAC-seq is particularly well suited when populations are **rare** and must be measured **in native tissue context**: it yields high-resolution maps of **open chromatin** with practical inputs.

![Sorting strategy for young vs. old SVZ populations](/images/data-science/thesis/svz-sorting-strategy-a.png)
![FACS / sorting readouts (continued)](/images/data-science/thesis/svz-sorting-strategy-b.png)

![ATAC-seq for chromatin accessibility in rare populations *in vivo* (Buenrostro *et al.*, 2013)](/images/data-science/thesis/atac-seq-overview.png)

At individual loci, the defense highlighted **dynamic accessibility at neurogenic regulators**—for example, the **pro-neural *Ascl1*** locus showed **age- and state-dependent** patterns of open chromatin along the gene body and surrounding regulatory geography (young versus old; quiescent versus activated comparisons).

![*Ascl1* locus: differential accessibility with activation and age](/images/data-science/thesis/ascl1-locus-accessibility-a.png)
![*Ascl1* locus (continued)](/images/data-science/thesis/ascl1-locus-accessibility-b.png)

At the genome-wide level, **principal component analysis (PCA)** of accessibility libraries **separated major cell classes**—for instance **endothelial cells**, **astrocyte/qNSC-related** profiles, and **aNSC/neural progenitor-related** profiles—showing that chromatin structure carries **strong cell-identity signal**. Crucially, PCA also **separated young and old NSC chromatin**, indicating that aging imprints a **quantifiable shift** in regulatory DNA organization.

![PCA separates endothelial, quiescent, and activated NSC chromatin states](/images/data-science/thesis/pca-nsc-chromatin-by-cell-state.png)

![PCA separates NSC chromatin libraries by age](/images/data-science/thesis/pca-nsc-chromatin-by-age.png)

The headline statistical pattern was **opposing trajectories** between states: **with age, qNSC chromatin became more restricted (less permissive), while aNSC chromatin became more permissive**. That opposition is biologically striking because it argues against a single “everything loosens” or “everything compacts” story; instead, **quiescence and activation remodel accessibility in opposite directions**.

![Opposing chromatin changes in quiescent vs. activated NSCs with age](/images/data-science/thesis/opposing-chromatin-qnsC-ansC-age.png)

Mechanistically, the **same classes of genomic elements** mediated much of the divergence: **distal regions and introns**—the neighborhoods that often harbor **enhancers and other *cis*-regulatory elements**—rather than wholesale rewriting of promoter accessibility alone. Promoter accessibility and gene expression remained **globally positively correlated** across cell types and ages (ATAC-seq and RNA-seq concordance at promoters), but **distal and intronic peaks disproportionately encoded state and age specificity**. In other words, **promoters often look similar** while **enhancer-like regions carry the aging signature**.

![Distal and intronic regions (putative enhancers) mediate opposing age-related changes](/images/data-science/thesis/distal-intronic-enhancer-regions.png)

![Promoter accessibility vs. gene expression across cell types and ages](/images/data-science/thesis/atac-rna-promoter-correlation.png)

![Genomic distribution of ATAC-seq peaks in NSCs](/images/data-science/thesis/atac-peak-genomic-distribution-a.png)
![Peak annotation (promoters, introns, distal)](/images/data-science/thesis/atac-peak-genomic-distribution-b.png)

![Distal and intronic accessibility specifies state and age](/images/data-science/thesis/distal-intronic-specify-state-age.png)

**Part 1 conclusion (in plain language):** Chromatin separates NSCs by **activation state** and by **age**; **qNSCs and aNSCs undergo opposing accessibility changes**; and **most age-specific remodeling sits in intronic and distal DNA**, pointing to **enhancer-level mechanisms** as candidates for altered neurogenic potential.

---

## Part 2 — Pathways underlying opposing chromatin shifts with age

**Question:** Which cellular programs are statistically associated with those accessibility changes—and what do they predict about behavior?

Pathway-level integration showed a coherent theme: **with age, qNSCs tended to lose accessibility (and gene expression) in programs linked to adhesion and motility**, whereas **aNSCs gained accessibility (and expression) in those same broad classes**. Gene Ontology–style summaries in the deck grouped terms around **cell–cell adhesion**, **cadherin-related junctions**, **integrin-linked adhesion**, **cytoskeletal organization**, and related signaling (including Wnt- and cAMP-associated annotations as presented).

![Pathways enriched in opposing directions: adhesion and motility in qNSCs vs. aNSCs](/images/data-science/thesis/pathways-adhesion-qnsC-down-ansC-up.png)

![Open chromatin at adhesion loci (cadherins, integrins, MMPs)](/images/data-science/thesis/adhesion-gene-loci-accessibility.png)

![Open chromatin enriched in adhesion/migration pathways (summary panel)](/images/data-science/thesis/open-chromatin-adhesion-pathways.png)

The chromatin predictions were **not abstract**: locus-level views highlighted **cadherins**, **integrins**, and **matrix metalloproteinases (MMPs)** as families where **young versus old** and **qNSC versus aNSC** trajectories moved in **opposite directions** for accessibility—and **RNA-seq from Dulken, Buckley, Navarro Negredo, *et al.*, 2019** supported **concordant expression changes** (qNSC/astrocytic signatures versus aNSC/NPC signatures).

![RNA-seq concordance: adhesion programs in qNSC/ast vs. aNSC/NPC](/images/data-science/thesis/rna-seq-adhesion-expression.png)

![scRNA-seq of the young SVZ: cell adhesion gene expression across lineages](/images/data-science/thesis/scrna-adhesion-by-lineage-a.png)
![Adhesion expression by cluster (continued)](/images/data-science/thesis/scrna-adhesion-by-lineage-b.png)
![Adhesion expression by cluster (continued)](/images/data-science/thesis/scrna-adhesion-by-lineage-c.png)

Motif analysis added a **transcription-factor hypothesis**: the **NF1 family** emerged as enriched in **young qNSCs** and **old aNSCs**, linking the chromatin states to regulators with documented roles in **adhesion and cell motion** (motif analysis with **Mahfuza Sharmin** in the **Kundaje** group). Related slides noted **NFI** biology in brain development and **qNSC-associated enhancers**, framing NF1-family enrichment as more than a statistical artifact.

![NF1 / NFI motif enrichment (young qNSCs and old aNSCs)](/images/data-science/thesis/nf1-motif-enrichment.png)

![NF1 motif analysis (extended panel, Kundaje lab collaboration)](/images/data-science/thesis/nf1-motif-qnsC-young-old-ansC.jpg)

![Shared adhesion signature: young qNSCs and old aNSCs](/images/data-science/thesis/young-qnsC-old-ansC-adhesion-signature.png)

**Part 2 conclusion:** Aging produces **mirror-image adhesion programs** in qNSCs versus aNSCs at the level of **open chromatin and gene expression**. The simplest behavioral prediction is that **migration—an adhesion- and cytoskeleton-heavy process—should change specifically in activated NSCs**, where repair and neuroblast supply depend on motility.

---

## Part 3 — Functional tests of adhesion and migration

**Question:** Can we experimentally validate the prediction that **aging alters NSC migration**—and connect phenotypes to **adhesive structures**?

The defense stated two directional hypotheses: **old qNSCs might move faster than young qNSCs**, while **old aNSCs might move slower than young aNSCs**. **Live-cell tracking** (including analysis with **Imaris**) quantified **migration speed** and **path complexity** *in vitro*.

![Hypotheses for qNSC vs. aNSC migration with age](/images/data-science/thesis/migration-hypotheses-in-vitro.png)

![Live-cell migration tracking (Imaris)](/images/data-science/thesis/live-cell-tracking-imaris.png)

The results matched the chromatin mirror: **aNSC migration speed decreased with age**, while **qNSCs were largely immobile in youth** but could exhibit **modest motility in old age**. In narrative terms, **aging makes activated NSCs less migratory and nudges quiescent NSCs toward a slightly more migratory regime**—a functional symmetry that parallels **opposing chromatin remodeling**.

![Migration speed and behavior: qNSCs vs. aNSCs, young vs. old](/images/data-science/thesis/migration-speed-qnsC-ansC-age.png)

Why care about **activated** migration? **Activated NSCs** display morphologies consistent with motility (**lamellipodia**, **filopodia**) and, in physiological and injury contexts, **mobilization and differentiation** support **ongoing neurogenesis** and **responses to acute damage**. If **old aNSCs migrate poorly**, one interpretation is **impaired regenerative or homeostatic capacity**, motivating a search for **druggable cytoskeletal nodes**.

![Regenerative context: activated NSCs, migration, and repair](/images/data-science/thesis/activated-nsc-regenerative-context-a.jpg)
![Mobilization and differentiation (continued)](/images/data-science/thesis/activated-nsc-regenerative-context-b.jpg)

![Time-lapse morphology: quiescent vs. activated NSC migration](/images/data-science/thesis/migration-morphology-timecourse-a.png)
![Migration morphology (continued)](/images/data-science/thesis/migration-morphology-timecourse-b.png)

![Cytoskeletal staining: quiescent vs. activated NSCs](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-a.png)
![Cytoskeletal staining (continued)](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-b.png)

Orthogonal **extracellular-matrix** assays reinforced the trend: **aging reduced how far aNSCs migrated** over **24–48 hours** in the presented experiments.

![ECM migration assay design](/images/data-science/thesis/ecm-migration-assay-overview.png)

![ECM migration: young vs. old aNSCs (0–48 h)](/images/data-science/thesis/ecm-migration-young-old-24-48h-a.png)
![ECM migration (continued)](/images/data-science/thesis/ecm-migration-young-old-24-48h-b.png)

To connect migration to **force-bearing adhesions**, **FRET-based RGD tension sensors** (work with **Brian Zhong** in the **Dunn** lab) illustrated how **focal adhesions** and **actin stress fibers** can **co-localize**—and thus how **adhesion strength** might enter a mechanistic chain linking **chromatin states** to **movement**.

![FRET / RGD sensor and actin stress fibers](/images/data-science/thesis/fret-actin-stress-fibers-a.png)
![Focal adhesion / force patterns (continued)](/images/data-science/thesis/fret-actin-stress-fibers-b.png)

![Vinculin and focal adhesions (concept)](/images/data-science/thesis/vinculin-focal-adhesion-explainer.png)

Finally, **vinculin**, a **focal-adhesion adaptor** coupling integrins to actin, showed **higher staining in old aNSCs** *in vitro* and **in the SVZ in vivo** (work with **Olivia Zhou**), aligning with the idea that **old activated NSCs are more “anchored”** even as they move less effectively.

![Vinculin staining in old aNSCs (*in vitro*)](/images/data-science/thesis/vinculin-staining-old-ansC-in-vitro.png)

![Vinculin in the SVZ *in vivo* (Ki67, GFAP, DAPI)](/images/data-science/thesis/vinculin-in-vivo-svz.jpg)

**Part 3 conclusion:** **Opposing age-related changes in migration** mirror **opposing chromatin and expression shifts**; **adhesion-associated cytoskeletal structures** and **vinculin-rich focal adhesions** provide a plausible cellular intermediate phenotype for **old aNSCs**.

---

## Part 4 — ROCK inhibition as a rejuvenation lever for old activated NSCs

**Question:** If old aNSC chromatin implicates **adhesion–cytoskeleton** programs, can we identify a **specific regulator** to test—and does modulating it **rescue migration**?

Pathway integration highlighted **ROCK** among upstream nodes associated with regions that **gain accessibility in old aNSCs**. **Rho-associated kinase (ROCK)** is often described as a **master regulator of actin-myosin contractility** and stress-fiber biology. Pharmacology with **Y-27632** is a standard probe of ROCK dependence.

![Pathway enrichment linking old aNSC open chromatin to ROCK-related programs](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-a.png)
![Upstream regulator summary (continued)](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-b.png)

The literature context is worth stating carefully: **ROCK inhibition can increase or decrease migration depending on cell type and context** (examples in the slides included **myoblasts**, **glioma cells**, **microglia**, **fibroblasts**, **dendritic cells**, **keratinocytes**, and **medulloblastoma cells**). The empirical question for NSCs is therefore not rhetorical—it is **empirical**.

![ROCK / Y-27632 context across cell types (from defense slides)](/images/data-science/thesis/rock-inhibition-literature-context.png)

The experimental answer shown in the defense was that **Y-27632 improved migration of old aNSCs**—a **partial rejuvenation** of a functional readout. Mechanistically, the deck argued that **stress-fiber elimination** is a plausible cellular route: **ROCK inhibition reduced actin stress fibers** in line with restored motility.

![Y-27632 improves old aNSC migration](/images/data-science/thesis/y27632-rescue-migration-a.png)
![Y-27632 rescue (continued)](/images/data-science/thesis/y27632-rescue-migration-b.png)

![Migration time course with Y-27632 (converted from slide figure)](/images/data-science/thesis/y27632-migration-timeline.png)

![ROCK inhibition reduces actin stress fibers](/images/data-science/thesis/rock-inhibition-stress-fibers.png)

**Part 4 conclusion:** **ROCK** surfaced as a **top testable target** from **old aNSC chromatin changes**; **ROCK inhibition** improved **old aNSC migration** and **reversed a stress-fiber-heavy adhesive phenotype**.

---

## Synthesis, implications, and next steps

**Synthesis.** Aging triggers **divergent chromatin remodeling** in **quiescent versus activated NSCs**, enriched in **distal and intronic regulatory DNA** and coherent with **adhesion–migration pathways**. **Functionally, old activated NSCs migrate more slowly** and show **signs of stronger focal adhesion**, and **ROCK inhibition** can **restore migration**—linking **epigenomic state** to a **pharmacologically accessible cytoskeletal control point**.

![Working model: aging, chromatin, adhesion, migration, and neurogenesis](/images/data-science/thesis/working-model-chromatin-adhesion.png)

**Future directions** sketched in the defense included: **mechanistic dissection of enhancers** that mediate age-related neurogenic decline; **in vivo** tests that recapitulate **migration phenotypes** observed *in vitro*; and **injury models** (stroke, TBI) asking how **old aNSC migration** and **ROCK** intersect with repair.

**Acknowledgments (abbreviated).** I am grateful to **Anne Brunet** and the **NSC team** and collaborators named on the original slides—including **Matthew Buckley**, **Jackie Butterfield**, **Ben Dulken**, **Katja Hebestreit**, **Chloe Kashiwagi**, **Subheksha Kc**, **Dena Leeman**, **Paloma Navarro Negredo**, **Tyson Ruetz**, **Lucy Xu**, **Xiaoai Zhao**, **Olivia Zhou**, and many others across Stanford—as well as committee members **Michael Bassik**, **Anshul Kundaje**, **Julien Sage**, and **Tony Wyss-Coray**, with support from a **Stanford Graduate Fellowship**, **Genentech Graduate Fellowship**, and **Stanford Genome Training Program**.
