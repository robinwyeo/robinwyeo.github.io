---
title: "Enhancer prediction through multi-omics integration"
date: 2022-02-10
tags:
  - enhancers
  - EPIC
  - ENCODE
  - ChromHMM
  - multi-omics
permalink: /data-science/epic-enhancer-prediction-multi-omics/
---

*Originally presented at Epic Bio BDS Learning Seminar (February 10, 2022)*

**[Download the original slides (PowerPoint)](/files/data-science/epic-enhancer-presentation-2022-02-10.pptx)**

This talk walks from **what enhancers are** and **why they matter**, through **how we measure them** (genomic and functional assays), to a **practical ENCODE-based pipeline** for prioritizing candidate enhancers—and finally to a **richer multi-omics feature set** and **HepG2** examples. It ends with an honest summary of why enhancer prediction remains hard.

---

## What are enhancers?

**Transcriptional enhancers** are *cis*-regulatory DNA elements that help control **when and where genes are expressed**. Nucleated cells share the same genome but adopt distinct lineages during development through **differential epigenetic regulation**. Each cell type expresses a characteristic gene program even though the core transcriptional machinery (e.g., RNA polymerase II) is broadly shared and recruited to promoters near transcription start sites (TSSs).

That machinery is often **not sufficient** on its own: distal **cis-regulatory elements**, including **enhancers**, provide additional regulatory logic. Enhancers harbor **short DNA motifs** that bind **sequence-specific transcription factors (TFs)**. TF occupancy helps recruit **co-activators and co-repressors**, tuning gene expression in a **cell-type-specific** way.

![Concept slide: identical genomes, differential regulation, and cis-regulatory elements](/images/data-science/epic-enhancer-2022/cis-regulatory-enhancer-overview.png)

### Common characteristics

Enhancers tend to share several features (none of which is perfectly diagnostic on its own):

- **Non-coding** sequence enriched for **TF binding motifs**
- Can lie at **any distance**—sometimes **megabases**—from the TSS they regulate, which complicates mapping enhancer–target relationships
- **Open chromatin** with **nucleosome depletion** at the active core
- Flanking nucleosomes often carry characteristic histone modifications such as **H3K4me1** and **H3K27ac**
- Activity is often **orientation-independent**
- Often show **elevated evolutionary conservation** relative to neutrally evolving background

---

## Why do we care about enhancers?

Enhancers are bound and regulated in a **cell-type-specific** and **spatiotemporally restricted** manner, making them central to **lineage specification** and **development**. Many enhancers remain **poorly annotated**, yet they matter for **development**, **evolution**, and **disease**.

A large fraction of **GWAS** and disease-associated variants fall in **distal non-coding** sequence—often in putative enhancers—so these regions are plausible **therapeutic** or **allele-specific engineering** targets. Because enhancers can coordinate **regulatory hubs** or **gene families**, modulating a single element can in principle reshape expression programs in a **cell-type-biased** way.

![Examples from the slides linking enhancers, SNPs, and globin expression contexts](/images/data-science/epic-enhancer-2022/disease-snps-globin-expression-panel-a.png)
![Continued: regulatory and expression context](/images/data-science/epic-enhancer-2022/disease-snps-globin-expression-panel-b.png)
![Continued](/images/data-science/epic-enhancer-2022/disease-snps-globin-expression-panel-c.png)
![Continued](/images/data-science/epic-enhancer-2022/disease-snps-globin-expression-panel-d.png)
![Continued](/images/data-science/epic-enhancer-2022/disease-snps-globin-expression-panel-e.png)

---

## How are enhancers identified experimentally?

Approaches split broadly into **genomic (correlative)** methods and **functional (causal)** assays.

### Genomic methods

Because enhancer activity depends on **TF binding**, **ChIP-seq** against a TF of interest is a standard way to nominate occupied regions. **Open chromatin** assays—**DNase-seq** or **ATAC-seq**—highlight nucleosome-depleted, TF-accessible DNA. **ChIP-seq for histone marks** such as **H3K4me1** and **H3K27ac** is widely used to annotate putative active or poised enhancers; as Shlyueva, Stampfel, and Stark note, histone-based prediction is now **routine** in genome annotation and **agrees reasonably well** with activity assays—while still being imperfect.

![Genomic modalities: TF ChIP, accessibility, and histone marks](/images/data-science/epic-enhancer-2022/genomic-methods-chip-atac-histone.png)

**The target-gene problem:** accessibility and histone peaks alone rarely say **which promoter** an enhancer contacts. **3D genome** methods help. **ChIA-PET** and **HiChIP** combine **chromatin conformation capture** with **ChIP** so that one simultaneously learns **protein binding** and **spatial proximity**. Common pull-downs include **Pol II**, **cohesin (e.g., Rad21)**, **Mediator (e.g., Med1)**, and **H3K27ac**.

![Enhancer–promoter proximity via ChIA-PET / HiChIP (concept)](/images/data-science/epic-enhancer-2022/chia-pet-hichip-enhancer-promoter.png)

![Example: overlapping accessible peaks with Pol II ChIA-PET contacts](/images/data-science/epic-enhancer-2022/pol2-chiapet-atac-looping-example.png)

In practice, **ChIA-PET/HiChIP coverage is still limited** for many cell types, so enhancer–gene maps from 3D alone can be **sparse**.

**ChromHMM** integrates multiple histone marks across tissues to assign **chromatin states** genome-wide—including states enriched for regulatory elements.

![ChromHMM state definitions (slide overview)](/images/data-science/epic-enhancer-2022/chromhmm-states-overview.png)
![ChromHMM / browser-style context](/images/data-science/epic-enhancer-2022/chromhmm-genome-browser-example.png)

### Functional methods

The **gold standard** test of enhancer activity is to place a candidate sequence **upstream of a minimal promoter** driving a reporter (e.g., **GFP**) and ask whether expression increases—often in **transgenic** models in developmental biology. That definition is powerful but **low throughput** for genome-wide surveys.

**Massively parallel reporter assays (MPRAs)** and **STARR-seq** scale enhancer testing by linking **candidate fragments** to **barcoded reporters**, transducing a cell type of interest, and using **sequencing** as a readout of activity. Limitations include **non-native chromatin context**, use of a **generic minimal promoter** rather than the endogenous target promoter, and dependence on **efficient delivery** in chosen cell types.

![Reporter-based enhancer identification (concept)](/images/data-science/epic-enhancer-2022/reporter-gfp-enhancer-assay.png)

![MPRA / STARR-seq style genome-wide screening (slide figure)](/images/data-science/epic-enhancer-2022/mpra-starr-genome-wide-screening.jpg)

**CRISPR-based** tools can recruit activators, repressors, or machinery to **endogenous loci**, or insert reporters into defined chromatin states, to probe **native** regulatory function.

![CRISPR-based interrogation of endogenous enhancers (slide figure)](/images/data-science/epic-enhancer-2022/crispr-endogenous-enhancer-reporter.png)

---

## A simple ENCODE-based enhancer prioritization pipeline

The deck outlines a **practical filter chain** using public **ENCODE** data:

**Data types**

- **RNA-seq** (expression context)
- **ATAC-seq** or **DNase-seq** (accessibility)
- **H3K27ac ChIP-seq** (active enhancer-associated mark)
- **p300 ChIP-seq** (co-activator associated with enhancer function)
- **18-state ChromHMM** annotations

**Steps (conceptual)**

1. Define candidate regions as **ATAC/DNase peaks** that are **intronic** or **distal/intergenic** (excluding purely promoter-proximal noise if desired).
2. Require overlap with ChromHMM states annotated as **enhancer-like** within the 18-state model.
3. Require overlap with **H3K27ac** peaks.
4. To improve odds of linking to a gene, optionally restrict to candidates within a **≤10 kb** window of a TSS (a pragmatic heuristic—not a biological universal).

---

## Case study: *SERPINA1*—where are the enhancers?

The slides walk a **locus-specific** example with stacked tracks (accessibility, histones, TF/co-activator data, ChromHMM). One note emphasized in the deck: **H3K27ac** signal often **dips at the summit** of an accessibility peak, consistent with **nucleosome depletion** at the TF-accessible core.

![*SERPINA1* locus: multi-track view (slide 1)](/images/data-science/epic-enhancer-2022/serpina1-enhancer-tracks-1.png)
![*SERPINA1* locus: H3K27ac depletion at peak summits (slide callout)](/images/data-science/epic-enhancer-2022/serpina1-enhancer-tracks-h3k27ac-note.png)

---

## Shared vs. cell-type-specific enhancers (K562 and Jurkat)

Comparing **K562** and **Jurkat** illustrates **shared** regulatory elements versus **lineage-restricted** ones—useful when thinking about which predictions transfer across cell types.

![Shared enhancers between K562 and Jurkat](/images/data-science/epic-enhancer-2022/shared-enhancers-k562-jurkat.png)
![Cell-type-specific enhancer patterns](/images/data-science/epic-enhancer-2022/cell-type-specific-enhancers-k562-jurkat.png)

---

## Why prediction is still messy

Shlyueva, Stampfel, and Stark summarize the tension well (quoted on the slides):

> “Enhancers and their activity states cannot be reliably predicted from their DNA sequences or from chromatin features, nor can the important parts of the sequence of an enhancer be easily identified.”

> “Given the widespread use of histone modifications to predict enhancers, it is interesting that there is **no consensus** about which marks should be used. […] Generally, the rules used to predict enhancers seem to be driven by the availability of data sets.”

> “None of the known histone modifications correlates perfectly with enhancer activity, and even combinations of marks are not perfect predictors.”

The honest takeaway: **integrate multiple lines of evidence**, know the **limits of each assay**, and treat predictions as **hypotheses** to test functionally when it matters.

---

## Expanding the feature set for *in silico* prediction

A richer panel of public data can include, in addition to the simple pipeline above:

- **H3K4me1** ChIP-seq  
- **Med1** (Mediator) and **Rad21** (cohesin) ChIP-seq  
- **POL2RA ChIA-PET** (Pol II–linked loops)  
- **hg38 20-way PhastCons** conservation  
- **H3K27me3** as a **negative** context mark (active enhancers typically should not sit in dense Polycomb domains)

![Integrated feature panel (slide schematic)](/images/data-science/epic-enhancer-2022/multi-omics-enhancer-prediction-features.png)

---

## HepG2 enhancer identification (examples)

The deck closes with **HepG2** examples applying the integrated view—browser-style panels tying accessibility, marks, and state calls together.

![HepG2 example (panel 1)](/images/data-science/epic-enhancer-2022/hepg2-enhancer-prediction-1.png)
![HepG2 example (panel 2)](/images/data-science/epic-enhancer-2022/hepg2-enhancer-prediction-2.png)
![HepG2 example (panel 3)](/images/data-science/epic-enhancer-2022/hepg2-enhancer-prediction-3.png)

---

## Closing

Enhancer biology sits at the intersection of **genetics**, **epigenomics**, **3D genome structure**, and **functional genomics**. Public consortia such as **ENCODE** make it possible to build **transparent, reproducible filters**—but **no shortcut** replaces careful interpretation and, when stakes are high, **direct functional tests**.

