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

*Adapted from my PhD oral defense (September 15, 2020, Stanford University). Slide wording below follows the defense deck; narrative passages are adapted from my speaker notes.*

**Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age** (title slide; schematic credit: Lancaster University).

Today I am excited to share an overview of my thesis work in Dr. Anne Brunet’s lab on how chromatin dynamics and cell migration change with age in neural stem cells. Before graduate school at Stanford, I had already spent about four years working on molecular aging research in Boston—context that shaped why these questions still feel urgent.

---

## Changing demographics: an aging population (Ortman *et al.*, 2014)

One of my primary motivations for continuing in aging biology is that we are living through a rapid shift in population demographics. More and more of the global population is becoming geriatric; in the next few decades, the geriatric population in the United States is projected to roughly double. The slides framed this with Ortman *et al.* (2014) and U.S. population aged 65+ (in millions), alongside general-interest aging-in-place framing from the original deck.

![U.S. population aged 65+ (millions), after Ortman *et al.*, 2014](/images/data-science/thesis/us-population-65plus.jpg)

![Aging and demographic context (slides adapted from public sources in the original deck)](/images/data-science/thesis/aging-psychology-chart.png)

![Additional demographic / aging-in-place framing from the defense slides](/images/data-science/thesis/aging-psychology-chart-2.png)

## Aging is the single greatest risk factor for cognitive decline and neurodegenerative disease

Why does that demographic shift matter for biomedicine? In the defense I framed it broadly first: **aging is the single greatest risk factor for a host of devastating pathologies**, including **cardiovascular disease**, **cancer**, and **neurodegenerative disease**. The next slide narrowed the emphasis to the brain: **aging is the single greatest risk factor for cognitive decline and neurodegenerative disease**—including Alzheimer’s disease, Parkinson’s disease, stroke, and vascular dementia—with prevalence increasing as a population ages. There is a growing need to understand the basic biology of brain aging and to engineer regenerative therapies. One exciting avenue is harnessing adult neural stem cells, which can generate newborn glial cells and neurons and potentially mitigate disease-related pathology.

## Neural stem cells (NSCs) reside in a complex niche: the sub-ventricular zone (SVZ) (Navarro Negredo\* and Yeo\*, 2020)

It was accepted only relatively recently that new neurons are generated during adulthood. We now know that rare adult neural stem cells live in specialized **neurogenic niches**. In the Brunet lab, a central model is the **sub-ventricular zone (SVZ)**, which lines the lateral ventricles. As a niche, the SVZ contains many cell types, but critically it harbors rare **quiescent** and **activated** NSCs. **Quiescent NSCs** sit near ependymal cells at the ventricular surface, where they integrate cues from the microenvironment and decide when to activate. With the right growth factors or environmental changes, quiescent NSCs can **activate**, re-enter proliferation, and progress through the lineage.

Upon activation, **aNSCs** differentiate toward neural progenitor cells and neuroblasts, which migrate along the **rostral migratory stream** to the **olfactory bulb** as terminally differentiated interneurons. Functionally, that ongoing neurogenesis lets an organism adapt to a changing environment by integrating new neurons into olfactory circuitry. Because NSCs can make newborn neurons, they also carry **regenerative potential**: after acute injuries such as stroke or traumatic brain injury, NSCs can initiate neurogenesis and migrate toward injury sites to differentiate into glia and neurons and support repair—as the defense diagram summarized (stroke / TBI arrows toward the SVZ).

![SVZ niche, lineages, and injury context (slide artwork; third-party credits on original deck)](/images/data-science/thesis/svz-niche-schematic.png)

![Alternative SVZ / RMS schematic after Gonzales-Roybal *et al.*, 2013, as in the defense slides](/images/data-science/thesis/svz-niche-gonzales-a.png)
![Rostral migratory stream and olfactory bulb context (same source)](/images/data-science/thesis/svz-niche-gonzales-b.png)

## Neurogenesis and neural stem cell activation decline with age (Bondolfi *et al.*, 2004)

While neurogenesis and lineage progression are robust in young animals, **aging reduces both quiescent NSC activation and the ability of proliferative NSCs to differentiate successfully into functional neurons**—the point of the Bondolfi *et al.* (2004) framing in the deck (“number of newly generated cells” across ages).

![Neurogenesis and NSC activation decline with age (Bondolfi *et al.*, 2004)](/images/data-science/thesis/neurogenesis-decline-age.png)

## Potential mechanisms of age-related neurogenic decline

Mechanisms remain only partly defined, but two hypotheses recur. First, **cell-intrinsic changes in quiescent NSCs** may make it harder to release cell-cycle hold and activate appropriately. Second, cells that do become proliferative may show **lineage skewing**—for example favoring glial/astrocytic outcomes at the expense of de novo neurons—consistent with the simple schematic on the slide (qNSCs, aNSCs, glia, neurons).

## Mechanisms of neural stem cell aging — mostly studied at the transcriptional level

So what cell-intrinsic changes contribute to declining neurogenic potential? **Next-generation sequencing** lets us profile young and old NSCs genomically. **So far, this has mostly been carried out at the transcriptional level**—within the Brunet lab (Leeman, 2018; Dulken\*, Buckley\*, Navarro Negredo\*, *et al.*, 2019) and in many other studies (Artegiani, 2017; Basak, 2018; Hochgerner, 2018; Kalamakis, 2019; Llorens-Bobadilla, 2015; Luo, 2015; Mizrak, 2019; Shi, 2018; Shin, 2015; Zywitza, 2018).

**Transcriptional studies** have highlighted pathways including **proteostasis**, **autophagy**, and **inflammation**. Yet transcriptional profiling emphasizes **gene expression from coding loci** and can miss regulatory information in **non-coding** DNA. When I joined the lab, I was drawn to that gap: **how chromatin state in NSCs changes with age**.

![Transcriptional profiling of NSC aging: themes and representative studies from the defense slides](/images/data-science/thesis/nsc-aging-transcriptome-studies.png)

## The chromatin landscape defines cell state and could reveal aspects of NSC aging

**What is the chromatin landscape, and what could it reveal about stem-cell aging in the brain?** Chromatin—the complex of DNA and regulatory proteins—**physically determines the accessibility and activity of genetic loci**. How tightly chromatin is packed helps specify cell identity and state by shaping which programs can be regulated. When identity shifts (including during aging), regions can **gain accessibility (“open”)** or **lose accessibility (“closed”)**, so we can profile those dynamic regions to reveal new features of stem-cell aging and their regulation.

The deck also emphasized that **aging is accompanied by epigenetic changes** that alter chromatin and **can disrupt transcriptional regulation**—especially consequential for stem cells that must maintain tightly controlled programs. **Chromatin profiling** complements RNA by highlighting **poised accessible loci**, **cis-regulatory regions such as enhancers**, and **transcription-factor binding**—angles that are easy to miss if we only measure transcripts from coding genes.

![Chromatin profiling complements transcription: cell state, enhancers, and TF binding (concept slide)](/images/data-science/thesis/chromatin-landscape-young-old-nsc.png)

A motivation that runs through the latter parts of the talk is that **comparing chromatin landscapes across age and activation state** can move beyond description and point toward **specific regulators**—and, in this thesis, a testable intervention in old activated NSCs.

## Outline (defense slide)

- **Part 1:** Chromatin landscapes of cell populations from the SVZ  
- **Part 2:** Dynamic chromatin changes during NSC aging affect adhesion/migration  
- **Part 3:** Functional validation of age-related changes to adhesion/migration  
- **Part 4:** Rejuvenation of old aNSC motility by targeting a regulator of adhesion  

---

## Part 1 — What does chromatin profiling reveal about NSC populations throughout aging?

We sorted **biologically defined populations** from the young and old SVZ; the defense introduced this as **sorting cell populations from the young and old SVZ** before genome-wide accessibility profiling.

![Sorting strategy for young vs. old SVZ populations](/images/data-science/thesis/svz-sorting-strategy-a.png)
![FACS / sorting readouts (continued)](/images/data-science/thesis/svz-sorting-strategy-b.png)

### ATAC-seq: a tool to assess chromatin accessibility (Buenrostro *et al.*, 2013)

**ATAC-seq is ideally suited to profile the chromatin landscape of rare cell populations *in vivo*.** That made it the right tool for native-tissue NSC populations at limited abundance.

![ATAC-seq for chromatin accessibility in rare populations *in vivo* (Buenrostro *et al.*, 2013)](/images/data-science/thesis/atac-seq-overview.png)

### The pro-neural *Ascl1* locus displays differential chromatin accessibility upon NSC activation

Before summarizing genome-wide patterns, the defense walked through a locus example. ***Ascl1* is required for neuronal differentiation.** The tracks compare young and old across five sorted populations; the y-axis reflects accessibility. There is a **5′ peak** shared across NSC-lineage cells that likely reflects a **poised regulatory element**, whereas the **transcription start site** gains accessibility most clearly **upon NSC activation**—matching transcriptomic data where *Ascl1* rises with activation and neuronal differentiation. In other words, the ATAC-seq libraries showed **expected biology at a neurogenic locus**: regulatory regions of *Ascl1* are accessible in astrocyte/qNSC and aNSC/NPC compartments but not in endothelial cells, consistent with *Ascl1*’s lineage-restricted role.

![*Ascl1* locus: differential accessibility with activation and age](/images/data-science/thesis/ascl1-locus-accessibility-a.png)
![*Ascl1* locus (continued)](/images/data-science/thesis/ascl1-locus-accessibility-b.png)

### Principal component analysis separates endothelial cells, quiescent NSCs, and activated NSCs

**Principal component analysis (PCA)**—here on **chromatin accessibility (ATAC-seq peaks)**—reduces complexity to a few axes. Globally, **accessibility separates endothelial cells from neural-lineage cells**, and further **separates quiescent astrocyte/qNSC-related profiles from activated aNSC/NPC-related profiles** (slide labels: Endothelial; Astrocyte/qNSC; aNSC/NPC).

![PCA separates endothelial, quiescent, and activated NSC chromatin states](/images/data-science/thesis/pca-nsc-chromatin-by-cell-state.png)

### Principal component analysis of NSC chromatin landscapes separates with age

Focusing on NSC chromatin, **PCA also separates young and old**—the next layer beyond cell-class separation.

![PCA separates NSC chromatin libraries by age](/images/data-science/thesis/pca-nsc-chromatin-by-age.png)

### Opposing changes in quiescent versus activated NSCs with age

**The chromatin landscape of quiescent and activated NSCs undergoes opposing changes with age: with age, the quiescent landscape becomes more restricted while the activated landscape becomes more permissive.**

![Opposing chromatin changes in quiescent vs. activated NSCs with age](/images/data-science/thesis/opposing-chromatin-qnsC-ansC-age.png)

### The same genomic elements — distal and intronic regions (putative enhancers)

**Opposing chromatin changes are mediated by the same genomic elements: distal and intronic regions (containing putative enhancers).** Promoter accessibility and gene expression remain **globally positively correlated** across the cell types and ages surveyed, but **distal and intronic peaks disproportionately encode state- and age-specificity**—the pattern summarized across the peak-distribution and correlation figures below.

![Distal and intronic regions (putative enhancers) mediate opposing age-related changes](/images/data-science/thesis/distal-intronic-enhancer-regions.png)

![Promoter accessibility vs. gene expression across cell types and ages](/images/data-science/thesis/atac-rna-promoter-correlation.png)

![Genomic distribution of ATAC-seq peaks in NSCs](/images/data-science/thesis/atac-peak-genomic-distribution-a.png)
![Peak annotation (promoters, introns, distal)](/images/data-science/thesis/atac-peak-genomic-distribution-b.png)

![Distal and intronic accessibility specifies state and age](/images/data-science/thesis/distal-intronic-specify-state-age.png)

### Part 1: Conclusion (slide wording)

- Chromatin landscapes **separate NSCs by quiescent and activated states as well as age**.  
- With age, **quiescent chromatin becomes more restricted** while **activated chromatin becomes more permissive**.  
- **The majority of age-related changes occur within introns and distal regions**, suggesting that **cis-regulatory elements (e.g., enhancers)** may underlie age-related changes in neurogenic potential.

---

## Part 2 — What cellular pathways underlie the opposing age-related changes to the NSC chromatin landscape?

Pathway analyses in the deck condensed to a clear pattern: **with age, qNSCs downregulate pathways involved in cellular adhesion whereas aNSCs upregulate them**—with rich GO-term panels on the original slide (cell-cell adhesion, cadherin-mediated adhesion, adherens junction organization, and related categories).

![Pathways enriched in opposing directions: adhesion and motility in qNSCs vs. aNSCs](/images/data-science/thesis/pathways-adhesion-qnsC-down-ansC-up.png)

### Adhesion loci and concordant RNA

**With age, qNSCs downregulate accessibility in cellular adhesion chromatin loci whereas aNSCs upregulate them**—illustrated at families such as **cadherins, integrins, and MMPs**. **With age, qNSCs downregulate gene expression of cellular adhesion pathways whereas aNSCs upregulate them** (Dulken\*, Buckley\*, Navarro Negredo\*, *et al.*, 2019; qNSC/astrocytic versus aNSC/NPC comparisons).

![Open chromatin at adhesion loci (cadherins, integrins, MMPs)](/images/data-science/thesis/adhesion-gene-loci-accessibility.png)

![Open chromatin enriched in adhesion/migration pathways (summary panel)](/images/data-science/thesis/open-chromatin-adhesion-pathways.png)

![RNA-seq concordance: adhesion programs in qNSC/ast vs. aNSC/NPC](/images/data-science/thesis/rna-seq-adhesion-expression.png)

![scRNA-seq of the young SVZ: cell adhesion gene expression across lineages](/images/data-science/thesis/scrna-adhesion-by-lineage-a.png)
![Adhesion expression by cluster (continued)](/images/data-science/thesis/scrna-adhesion-by-lineage-b.png)
![Adhesion expression by cluster (continued)](/images/data-science/thesis/scrna-adhesion-by-lineage-c.png)

### NF1 motif enrichment (with Mahfuza Sharmin)

**Motif for NF1, a regulator of cellular adhesion, is enriched in young qNSCs and old aNSCs.** The NF1 family **regulates cell adhesion and cell motion**—linking the chromatin signatures to a concrete transcription-factor hypothesis (motif analysis with **Mahfuza Sharmin** in the **Kundaje** group).

![NF1 / NFI motif enrichment (young qNSCs and old aNSCs)](/images/data-science/thesis/nf1-motif-enrichment.png)

![NF1 motif analysis (extended panel, Kundaje lab collaboration)](/images/data-science/thesis/nf1-motif-qnsC-young-old-ansC.jpg)

![Shared adhesion signature: young qNSCs and old aNSCs](/images/data-science/thesis/young-qnsC-old-ansC-adhesion-signature.png)

### Part 2: Conclusion (slide wording)

- **Aging causes an opposite adhesion response from qNSCs and aNSCs:**  
  - With age, **qNSCs lose accessibility at adhesion pathways**.  
  - With age, **aNSCs gain accessibility at adhesion pathways**.  
- **These analyses of dynamic ATAC-seq chromatin accessibility data predict that aging impairs the ability of aNSCs to migrate.**

---

## Part 3 — Can we experimentally validate the prediction that aging affects NSC adhesion and migration?

**Based on age-related chromatin changes, I predicted:**

- **Old qNSCs move faster than young qNSCs.**  
- **Old aNSCs move slower than young aNSCs.**

The defense then framed **quantifying NSC migratory capability *in vitro*** with **Imaris** tracking.

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

### Migration results (slide bullets)

- **Age decreases aNSC migration speed.**  
- **Young qNSCs rarely migrate, while old qNSCs show a small degree of motility.**  
- **aNSCs readily migrate while qNSCs are largely immobile.**  
- **With age, qNSCs functionally become more migratory whereas aNSCs become less migratory.**

![Migration speed and behavior: qNSCs vs. aNSCs, young vs. old](/images/data-science/thesis/migration-speed-qnsC-ansC-age.png)

### Why activated NSC migration matters for regeneration

**Migratory activated NSCs have regenerative potential that is impaired in old age.** Upon activation, NSCs show **morphological signs of motility**; they **mobilize and differentiate** to support lifelong neurogenesis and **repair after acute injury**. **Age-related impairment in aNSC motility** therefore suggests **reduced neurogenic/regenerative potential** in older animals—motivating mechanistic work on migration.

![Regenerative context: activated NSCs, migration, and repair](/images/data-science/thesis/activated-nsc-regenerative-context-a.jpg)
![Mobilization and differentiation (continued)](/images/data-science/thesis/activated-nsc-regenerative-context-b.jpg)

![Time-lapse morphology: quiescent vs. activated NSC migration](/images/data-science/thesis/migration-morphology-timecourse-a.png)
![Migration morphology (continued)](/images/data-science/thesis/migration-morphology-timecourse-b.png)

![Cytoskeletal staining: quiescent vs. activated NSCs](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-a.png)
![Cytoskeletal staining (continued)](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-b.png)

### Orthogonal ECM assay

**An orthogonal assay measures aNSC migration through extracellular matrix.** **Aging decreases the migratory ability of aNSCs** over **0–48 hours** in the deck’s timeline layout (young versus old).

![ECM migration assay design](/images/data-science/thesis/ecm-migration-assay-overview.png)

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/ecm-migration-assay-overview.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/migration-assay-video.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/migration-assay-video.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>Embedded slide video: ECM migration assay (from the defense PowerPoint).</em></figcaption>
</figure>
{:/nomarkdown}

![ECM migration: young vs. old aNSCs (0–48 h)](/images/data-science/thesis/ecm-migration-young-old-24-48h-a.png)
![ECM migration (continued)](/images/data-science/thesis/ecm-migration-young-old-24-48h-b.png)

### FRET, stress fibers, and focal adhesions

The slide title read: **“FRET analysis reveals that focal adhesions and actin stress fibers co-localize and could be an important mechanism that gets dysregulated with age.”** In the spoken narrative I emphasized that **focal adhesions and actin stress fibers co-localize at the leading and lagging ends of aNSCs**—a cell-biological picture that connects adhesion biochemistry to the migration phenotypes above. **RGD tension sensors** (with **Brian Zhong**, **Dunn lab**) map force patterns alongside **actin stress fibers**.

![FRET / RGD sensor and actin stress fibers](/images/data-science/thesis/fret-actin-stress-fibers-a.png)
![Focal adhesion / force patterns (continued)](/images/data-science/thesis/fret-actin-stress-fibers-b.png)

![Vinculin and focal adhesions (concept)](/images/data-science/thesis/vinculin-focal-adhesion-explainer.png)

### Vinculin accumulates in old aNSCs (*in vitro* and *in vivo*)

**With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein**—and **in vivo in the SVZ** with **Olivia Zhou** (panel labels: DAPI, Ki67, vinculin, GFAP; aNSCs).

![Vinculin staining in old aNSCs (*in vitro*)](/images/data-science/thesis/vinculin-staining-old-ansC-in-vitro.png)

![Vinculin in the SVZ *in vivo* (Ki67, GFAP, DAPI)](/images/data-science/thesis/vinculin-in-vivo-svz.jpg)

Together, the migration assays, ECM behavior, and adhesion cytoskeleton readouts support a linked story: **chromatin predicts adhesion pathway imbalance; adhesion and cytoskeletal organization track with slower migration in old activated NSCs.**

### Part 3: Conclusion (slide wording)

- **Activated NSCs are migratory while quiescent NSCs remain immobile, and aging functionally causes opposing changes in migratory potential.**  
- **Activated NSCs primarily display F-actin stress fibers and adhesive force patterns at the leading and lagging ends of the cell.**  
- **Old activated NSCs exhibit impaired migration and increased staining for vinculin, a component of focal adhesions.**

---

## Part 4 — Can chromatin changes in old aNSCs reveal a molecular target for rejuvenation?

**Chromatin peaks that open up in old aNSCs are enriched for upstream regulators of ROCK** (pathway panel on the original slide).

![Pathway enrichment linking old aNSC open chromatin to ROCK-related programs](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-a.png)
![Upstream regulator summary (continued)](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-b.png)

### ROCK inhibition with Y-27632

**ROCK is a master regulator of cytoskeletal dynamics.** The deck reviewed **context-dependent effects of ROCK inhibition** with **Y-27632** across cell types—sometimes **boosting** migration (examples included myoblasts, glioma cells, microglia, fibroblasts) and sometimes **impairing** migration (dendritic cells, keratinocytes, medulloblastoma cells). For NSCs, the answer had to be empirical.

![ROCK / Y-27632 context across cell types (from defense slides)](/images/data-science/thesis/rock-inhibition-literature-context.png)

### **Inhibition of ROCK (via Y-27632 administration) improves old aNSC migration**

**Y-27632 is a small-molecule inhibitor of ROCK.** The key result, repeated on consecutive result slides, is that **ROCK inhibition improves migration in old aNSCs**.

![Y-27632 improves old aNSC migration](/images/data-science/thesis/y27632-rescue-migration-a.png)
![Y-27632 rescue (continued)](/images/data-science/thesis/y27632-rescue-migration-b.png)

![Migration time course with Y-27632 (converted from slide figure)](/images/data-science/thesis/y27632-migration-timeline.png)

### Stress-fiber mechanism

**Elimination of actin stress fibers could be a cellular mechanism by which ROCK inhibition improves migration in old aNSCs.** Consistent with that idea, **inhibition of ROCK (via Y-27632 administration) eliminates actin stress fibers** associated with focal adhesions.

![ROCK inhibition reduces actin stress fibers](/images/data-science/thesis/rock-inhibition-stress-fibers.png)

### Part 4: Conclusion (slide wording)

- **ROCK emerged as the top target associated with old aNSC chromatin changes.**  
- **Inhibition of ROCK:**  
  - **improves migration in old aNSCs**  
  - **eliminates actin stress fibers associated with focal adhesions**

---

## Summary (slide wording)

- **Aging elicits a differential chromatin response in qNSCs and aNSCs involving accessibility changes in adhesion and migration pathways.**  
- **Functionally, old aNSCs migrate slower than young aNSCs and exhibit marks of increased cell adhesion.**  
- **ROCK inhibition is capable of rescuing the age-related impairment in old aNSCs.**

![Working model: aging, chromatin, adhesion, migration, and neurogenesis](/images/data-science/thesis/working-model-chromatin-adhesion.png)

## Implications and future directions (slide wording)

- **Explore how enhancers mediate age-related neurogenic decline.**  
- **Recapitulate age-related decline in aNSC migration *in vivo*.**  
- **Explore the effects of impaired old aNSC migration and ROCK in stroke and TBI models.**

Stated in more biological terms, the longer arc is to connect **cis-regulatory remodeling** to **niche exit and repair migration**, and to ask when chromatin-level changes are **causal** versus **permissive** for regenerative failure—using the stroke/TBI framing where the talk began.

## Closing title slide

**Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age**—bringing the narrative back to the opening question about how **regulatory DNA organization** relates to **activated NSC migration** and **neurogenic potential**.

**Acknowledgments (from the defense slide).** **Anne Brunet**; NSC team members **Matthew Buckley**, **Jackie Butterfield**, **Ben Dulken**, **Katja Hebestreit**, **Chloe Kashiwagi**, **Subheksha Kc**, **Dena Leeman**, **Paloma Navarro**, **Tyson Ruetz**, **Lucy Xu**, **Xiaoai Zhao**, **Olivia Zhou**; collaborators **Aaron Daugherty**, **Anshul Kundaje**, **Mahfuza Sharmin**, **Alex Dunn**, **Steven Tan**, **Brian Zhong**, **Jonathan Long**, and the Brunet lab; thesis committee **Michael Bassik**, **Anshul Kundaje**, **Julien Sage**, and **Tony Wyss-Coray**; funding **Stanford Graduate Fellowship (SGF)**, **Genentech Graduate Fellowship**, and **Stanford Genome Training Program (SGTP)**.
