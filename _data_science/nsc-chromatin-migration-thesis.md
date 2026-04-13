---
title: "Thesis Defense: Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age"
date: 2020-09-15
tags:
  - thesis
  - neural stem cells
  - ATAC-seq
  - chromatin
permalink: /data-science/nsc-chromatin-migration-thesis/
---

*Adapted from my PhD oral defense (September 15, 2020, Stanford University): "Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age."*

As populations age, understanding adult stem-cell aging and repair becomes central to neuroscience and regenerative medicine. This defense asked: **how does chromatin accessibility change with age in adult mouse neural stem cells (NSCs), and can those dynamics explain declining activated-NSC migration?** The post below follows the oral-defense flow and slide language, with original figures integrated for context.

---

## Changing demographics: an aging population

Demographic projections show a steadily growing older population (for example, Ortman *et al.*, 2014). **Aging is the single greatest risk factor for cognitive decline and neurodegenerative disease**, including Alzheimer’s disease, Parkinson’s disease, stroke, and vascular dementia. This motivates a mechanistic question: what age-related NSC changes limit maintenance and repair in the brain?

![U.S. population aged 65+ (millions), after Ortman *et al.*, 2014](/images/data-science/thesis/us-population-65plus.jpg)

![Aging and demographic context (slides adapted from public sources in the original deck)](/images/data-science/thesis/aging-psychology-chart.png)

![Additional demographic / aging-in-place framing from the defense slides](/images/data-science/thesis/aging-psychology-chart-2.png)

## Neural stem cells reside in a complex niche: the SVZ

In the adult mammalian brain, **NSCs reside in the subventricular zone (SVZ)**, a complex niche that includes quiescent NSCs, activated NSCs, progenitors, and neuroblasts, together with endothelial cells, microglia, ependymal cells, and choroid plexus inputs. These populations support migration toward the olfactory bulb and are mobilized after injuries such as stroke and traumatic brain injury (see also Navarro Negredo and Yeo, 2020).

![SVZ niche, lineages, and injury context (slide artwork; third-party credits on original deck)](/images/data-science/thesis/svz-niche-schematic.png)

![Alternative SVZ / RMS schematic after Gonzales-Roybal *et al.*, 2013, as in the defense slides](/images/data-science/thesis/svz-niche-gonzales-a.png)
![Rostral migratory stream and olfactory bulb context (same source)](/images/data-science/thesis/svz-niche-gonzales-b.png)

A consistent observation in rodents is that **adult neurogenesis and NSC activation decline with age**—fewer newly generated cells and damped activation dynamics across classic time points (for example, Bondolfi *et al.*, 2004). Yet the field still debated *which* molecular programs best explain **age-related neurogenic decline** and how those programs might differ between **quiescent NSCs (qNSCs)** and **activated NSCs (aNSCs)**.

![Neurogenesis and NSC activation decline with age (Bondolfi *et al.*, 2004)](/images/data-science/thesis/neurogenesis-decline-age.png)

## Why neurogenesis research turned to the genome—and beyond RNA

Next-generation sequencing enabled profiling of **young and old NSCs**, and most prior work focused on the **transcriptional level**. In the Brunet lab and in other studies, RNA analyses highlighted pathways including **proteostasis**, **autophagy**, and **inflammation** (Leeman, 2018; Dulken, Buckley, Navarro Negredo, *et al.*, 2019; Artegiani, 2017; Basak, 2018; Hochgerner, 2018; Kalamakis, 2019; Llorens-Bobadilla, 2015; Luo, 2015; Mizrak, 2019; Shi, 2018; Shin, 2015; Zywitza, 2018).

![Transcriptional profiling of NSC aging: themes and representative studies from the defense slides](/images/data-science/thesis/nsc-aging-transcriptome-studies.png)

However, transcriptional profiling mainly measures expression from **coding loci** and misses key regulatory information in non-coding DNA. A major gap was therefore **how the chromatin landscape of NSCs changes with age**, especially in rare populations profiled *in vivo*.

**Chromatin accessibility profiling** can define cell state and add insight beyond RNA, including **poised accessible loci**, **cis-regulatory regions such as enhancers**, and **transcription-factor binding signatures**. Because aging is accompanied by widespread epigenetic change, the key question was whether chromatin accessibility could reveal new mechanisms of NSC aging.

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

**Part 1 conclusion (slide wording):**
- Chromatin landscapes separate NSCs by quiescent and activated states, as well as by age.
- With age, quiescent chromatin becomes more restricted while activated chromatin becomes more permissive.
- The majority of age-related changes occur within introns and distal regions, suggesting that **cis-regulatory elements** (for example, enhancers) may underlie age-related changes in neurogenic potential.

---

## Part 2 — Pathways underlying opposing chromatin shifts with age

**Question:** Which cellular programs are statistically associated with those accessibility changes—and what do they predict about behavior?

Pathway analyses showed a consistent pattern: **with age, qNSCs downregulated accessibility and expression in cellular-adhesion pathways, whereas aNSCs upregulated them**. Enriched terms in the slides clustered around **cell-cell adhesion**, **cadherin-mediated adhesion**, **adherens junction organization**, and related signaling categories.

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

**Part 2 conclusion (slide wording):**
- Aging causes opposite adhesion responses in qNSCs and aNSCs.
- With age, qNSCs lose accessibility at adhesion pathways, while aNSCs gain accessibility at adhesion pathways.
- Dynamic ATAC-seq accessibility analyses predict that aging impairs the migratory ability of aNSCs.

---

## Part 3 — Functional tests of adhesion and migration

**Question:** Can we experimentally validate the prediction that **aging alters NSC migration**—and connect phenotypes to **adhesive structures**?

The defense tested two directional hypotheses: **old qNSCs move faster than young qNSCs**, while **old aNSCs move slower than young aNSCs**. **Live-cell imaging and Imaris tracking** quantified migration behavior *in vitro*.

![Hypotheses for qNSC vs. aNSC migration with age](/images/data-science/thesis/migration-hypotheses-in-vitro.png)

![Live-cell migration tracking (Imaris)](/images/data-science/thesis/live-cell-tracking-imaris.png)

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/live-cell-tracking-imaris.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/migration-tracking-imaris.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/migration-tracking-imaris.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>Embedded slide video: migration tracking (Imaris), exported from the defense PowerPoint.</em></figcaption>
</figure>
{:/nomarkdown}

The results followed the chromatin prediction: **aNSC migration speed decreased with age**, while **young qNSCs were largely immobile and old qNSCs showed a small degree of motility**. In short, aging causes qNSCs to become relatively more migratory and aNSCs to become less migratory.

![Migration speed and behavior: qNSCs vs. aNSCs, young vs. old](/images/data-science/thesis/migration-speed-qnsC-ansC-age.png)

Why focus on **activated** migration? Activated NSCs show clear migratory morphology (**lamellipodia** and **filopodia**) and mobilize/differentiate to support neurogenesis and acute-injury responses. Impaired migration in old aNSCs therefore suggests reduced regenerative potential.

![Regenerative context: activated NSCs, migration, and repair](/images/data-science/thesis/activated-nsc-regenerative-context-a.jpg)
![Mobilization and differentiation (continued)](/images/data-science/thesis/activated-nsc-regenerative-context-b.jpg)

![Time-lapse morphology: quiescent vs. activated NSC migration](/images/data-science/thesis/migration-morphology-timecourse-a.png)
![Migration morphology (continued)](/images/data-science/thesis/migration-morphology-timecourse-b.png)

![Cytoskeletal staining: quiescent vs. activated NSCs](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-a.png)
![Cytoskeletal staining (continued)](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-b.png)

An orthogonal extracellular-matrix assay reinforced this result: **aging decreases the migratory ability of aNSCs** over **24-48 hours**.

![ECM migration assay design](/images/data-science/thesis/ecm-migration-assay-overview.png)

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/ecm-migration-assay-overview.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/ecm-migration-assay-video.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/ecm-migration-assay-video.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>Embedded slide video: ECM migration assay (from the defense PowerPoint).</em></figcaption>
</figure>
{:/nomarkdown}

![ECM migration: young vs. old aNSCs (0–48 h)](/images/data-science/thesis/ecm-migration-young-old-24-48h-a.png)
![ECM migration (continued)](/images/data-science/thesis/ecm-migration-young-old-24-48h-b.png)

To link migration with adhesion mechanics, **FRET-based RGD tension sensors** (with **Brian Zhong**, **Dunn lab**) showed co-localization of **focal-adhesion force patterns** and **actin stress fibers**, supporting a dysregulated-adhesion mechanism in aging cells.

![FRET / RGD sensor and actin stress fibers](/images/data-science/thesis/fret-actin-stress-fibers-a.png)
![Focal adhesion / force patterns (continued)](/images/data-science/thesis/fret-actin-stress-fibers-b.png)

![Vinculin and focal adhesions (concept)](/images/data-science/thesis/vinculin-focal-adhesion-explainer.png)

Finally, **vinculin**, a focal-adhesion protein linking integrins to the actin cytoskeleton, showed **increased staining in old aNSCs** *in vitro* and **in vivo** in the SVZ (with **Olivia Zhou**), consistent with stronger adhesion in old activated cells.

![Vinculin staining in old aNSCs (*in vitro*)](/images/data-science/thesis/vinculin-staining-old-ansC-in-vitro.png)

![Vinculin in the SVZ *in vivo* (Ki67, GFAP, DAPI)](/images/data-science/thesis/vinculin-in-vivo-svz.jpg)

**Part 3 conclusion (slide wording):**
- Activated NSCs are migratory while quiescent NSCs remain largely immobile, and aging causes opposing changes in migratory potential.
- Activated NSCs primarily show F-actin stress fibers and adhesive force patterns at the leading and lagging cell edges.
- Old activated NSCs exhibit impaired migration and increased staining for vinculin, a focal-adhesion component.

---

## Part 4 — ROCK inhibition as a rejuvenation lever for old activated NSCs

**Question:** If old aNSC chromatin implicates **adhesion–cytoskeleton** programs, can we identify a **specific regulator** to test—and does modulating it **rescue migration**?

Pathway integration showed that peaks opening in old aNSCs were enriched for upstream regulators including **ROCK**. Because **ROCK** is a major regulator of cytoskeletal dynamics, the defense tested ROCK inhibition with **Y-27632**.

![Pathway enrichment linking old aNSC open chromatin to ROCK-related programs](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-a.png)
![Upstream regulator summary (continued)](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-b.png)

Prior literature shows **context-dependent effects**: ROCK inhibition can either increase or impair migration depending on cell type (examples in the slides included myoblasts, glioma cells, microglia, fibroblasts, dendritic cells, keratinocytes, and medulloblastoma cells). The NSC question was therefore explicitly empirical.

![ROCK / Y-27632 context across cell types (from defense slides)](/images/data-science/thesis/rock-inhibition-literature-context.png)

The experimental answer was that **Y-27632 improves migration in old aNSCs**. A proposed cellular mechanism was **elimination of actin stress fibers** following ROCK inhibition, consistent with improved motility.

![Y-27632 improves old aNSC migration](/images/data-science/thesis/y27632-rescue-migration-a.png)
![Y-27632 rescue (continued)](/images/data-science/thesis/y27632-rescue-migration-b.png)

![Migration time course with Y-27632 (converted from slide figure)](/images/data-science/thesis/y27632-migration-timeline.png)

![ROCK inhibition reduces actin stress fibers](/images/data-science/thesis/rock-inhibition-stress-fibers.png)

**Part 4 conclusion (slide wording):**
- **ROCK** emerged as the top target associated with old aNSC chromatin changes.
- Inhibition of ROCK improves migration in old aNSCs.
- Inhibition of ROCK eliminates actin stress fibers associated with focal adhesions.

---

## Summary, implications, and future directions

**Summary (slide wording):**
- Aging elicits a differential chromatin response in qNSCs and aNSCs involving accessibility changes in adhesion and migration pathways.
- Functionally, old aNSCs migrate slower than young aNSCs and exhibit marks of increased cell adhesion.
- ROCK inhibition can rescue age-related migratory impairment in old aNSCs.

![Working model: aging, chromatin, adhesion, migration, and neurogenesis](/images/data-science/thesis/working-model-chromatin-adhesion.png)

**Implications and future directions (slide wording):**
- Explore how enhancers mediate age-related neurogenic decline.
- Recapitulate age-related decline in aNSC migration **in vivo**.
- Explore how impaired old-aNSC migration and ROCK signaling shape repair in stroke and TBI models.

**Acknowledgments (abbreviated).** I am grateful to **Anne Brunet** and the **NSC team** and collaborators named on the original slides—including **Matthew Buckley**, **Jackie Butterfield**, **Ben Dulken**, **Katja Hebestreit**, **Chloe Kashiwagi**, **Subheksha Kc**, **Dena Leeman**, **Paloma Navarro Negredo**, **Tyson Ruetz**, **Lucy Xu**, **Xiaoai Zhao**, **Olivia Zhou**, and many others across Stanford—as well as committee members **Michael Bassik**, **Anshul Kundaje**, **Julien Sage**, and **Tony Wyss-Coray**, with support from a **Stanford Graduate Fellowship**, **Genentech Graduate Fellowship**, and **Stanford Genome Training Program**.
