---
title: "Transcriptional enhancer prediction through multi-omics integration"
date: 2022-02-10
tags:
  - enhancers
  - EPIC
  - ENCODE
  - ChromHMM
  - multi-omics
permalink: /data-science/epic-enhancer-prediction-multi-omics/
---

![Title](/images/data-science/epic-enhancer-2022/Enhancer_Title_Image.png)

*Adapted from my oral presentation at Epic Bio BDS Learning Seminar (February 10, 2022)*

---

## Basic biology of transcriptional enhancers

Nucleated cells contain identical genomes yet differentiate into multiple cellular lineages during development through differential epigenetic regulation. These different cell types have differential gene expression profiles despite all possessing (and expressing) identical transcriptional machinery (e.g. RNA Polymerase II, etc) which is recruited to core promoters around the TSS. The downstream differences in cellular transcriptional profiles are possible because transcriptional machinery alone is often insufficient to drive gene expression in the absence of more distal functional DNA regions known as cis-regulatory elements.

![Panel from slides](/images/data-science/epic-enhancer-2022/disease-snps-globin-expression-panel-b.png)
<br>
_Source: Corces et al., 2016_

As one can see from the above heatmaps (_Corces et al., 2016_) depicting the chromatin accessibility profiles of haematopoeitic lineage cells at either promoters or distal DNA sites, it is the chromatin profiles at distal non-coding regulatory sites that largely specifies lineage instead of the chromatin profiles at promoter sequences. 

These distal regulatory sites contain cis-regulatory elements, such as enhancers, which have short DNA motifs that act as binding sites for sequence-specific transcription factors (TFs). TF binding to enhancers serve to recruit co-activators/co-repressors that drive differential gene expression in a cell-type specific manner.


## Characteristics of transcriptional enhancers

![Figure from slides: characteristics of transcriptional enhancers](/images/data-science/epic-enhancer-2022/cis-regulatory-enhancer-overview.png)
_Source: Shlyueva, Stampfel, and Stark, 2014_

Enhancers share a set of common characteristics:
- DNA sequence is non-coding and contains TF binding motifs.
- Located at any distance (up to megabases away) from their TSS making identification challenging.
- DNA is accessible and devoid of nucleosomes.
- Nucleosomes around enhancer contain specific post-translational modifications (H3K4me1 and H3K27ac).
- Enhancer activity is independent of sequence orientation.
- Exhibit higher evolutionary conservation than background sequences.


## Why do we care about enhancers?

Enhancers are bound/regulated by TFs in a highly celltype-specific and spatiotemporally-specific manner allowing them to drive cellular lineage specification and development. The vast majority of enhancers remain unknown/uncharacterized but contribute key roles in development, evolution, and disease.

From a therapuetics perspective, enhancers can regulate entire gene families or regulatory hubs making them attractive targets if there is a therapeutic desire to modulate entire gene families in a celltype-specific manner. Additionally many disease-associated SNPs occur in distal non-coding enhancers making them potential therapeutic targets.


## Genomic methods for enhancer identification

![Figure from slides: genomic methods](/images/data-science/epic-enhancer-2022/genomic-methods-chip-atac-histone.png)
_Source: Dixon et al., 2016_

Since enhancer function is dependent upon TF binding, **ChIP-seq against a known TF** is a common way to identify enhancers via identification of TF binding sites.

Since active enhancers are depleted of nucleosomes and contain accessible chromatin to be permissive to TF binding, **DNAse-seq or ATAC-seq** can be used to identify accessible DNA regions.

Nucleosomes flanking enhancers carry specific, characteristic post-translational modifications which can be identified using **ChIP-seq against histone marks (H3K4me1 and H3K27ac)**.

“The predictions of enhancers using histone marks is now widely used, for example, in the annotation of genome-wide functional elements by individual groups and international consortia, and it agrees well with enhancer activity assays.” (_Shlyueva, Stampfel, & Stark_)

**Problem: The above methods give no indication of which gene is being regulated by an enhancer!**

Enhancers are physically brought into close spatial proximity with their target promoters to regulate gene expression. This can be exploited to identify enhancers and enhancer-gene relationships.

**ChIA-PET and HiChIP** essentially couple chromatin conformation capture technology (e.g. 3C,4C,5C,Hi-C) and ChIP-seq to identify enhancer-promoter interactions.

![Figure from slides: ChIA-PET and HiChIP](/images/data-science/epic-enhancer-2022/chia-pet-hichip-enhancer-promoter.png)
_Source: Dekker et al., 2013_

These technologies simultaneously identify binding sites for proteins involved in the transcriptional machinery (via ChIP) and spatial proximity contacts (via Hi-C).

Common targets include:
- Pol II
- Cohesin
- Mediator
- H3K27ac


## Example: Enhancer-promoter looping with RNA Polymerase II

![Figure from slides: ATAC-seq and POL2RA ChIA-PET](/images/data-science/epic-enhancer-2022/pol2-chiapet-atac-looping-example.png)

Co-localization of accessible chromatin peaks (ATAC-seq) with POL2RA ChIA-PET can predict enhancer-promoter loops.

HOWEVER, ChIA-PET/HiChIP datasets are pretty scarce making this an unreliable strategy.


## ChromHMM: Integrating multiple histone marks across diverse tissues into to annotate chromatin states genome-wide

One attractive strategy to identify enhancers _in silico_ is to use the publicly available ChromHMM profiles on ENCODE.

![Figure from slides: ChromHMM states](/images/data-science/epic-enhancer-2022/chromhmm-states-overview.png)
_Source: Ernst & Kellis, 2012_

ChromHMM is a technique developed in Manolis Kellis' lab at MIT ([Ernst & Kellis, 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3577932/)) that integrates multiple histone marks via ChIP-seq and applies a multivariate Hidden Markov Model to produce a chromatin state annotation to binned bps across the entire genome.

![Figure from slides: ChromHMM in genome context](/images/data-science/epic-enhancer-2022/chromhmm-genome-browser-example.png)
_Source: Ernst & Kellis, 2012_

## Functional methods for enhancer identification

Genomics-based methods indirectly predict enhancer regions based on specific known properties of cis-regulatory elements but these DNA sequences can also be directly tested for enhancer activity.


**Image-based enhancer identification**

![Figure from slides: reporter-based enhancer identification](/images/data-science/epic-enhancer-2022/reporter-gfp-enhancer-assay.png)
_Source: Daugherty<sup>*</sup> & Yeo<sup>*</sup>, 2013_

DNA regions can be tested for for their ability to activate or enhance transcription by cloning the DNA region upstream from a minimal core promoter driving GFP.

This activity, independent of the enhancer’s native sequence context, is the defining property of enhancers and is used as the **gold standard** in enhancer prediction.

Image-based enhancer identification is frequently used in developmental biology to identify enhancers that drive lineage-specific cellular differentiation.

Since these image-based enhancer identification experiments require generation of transgenic animals, they are not suitable for genome-wide enhancer screens.


**Genome-wide functional enhancer screening**

Genome-wide enhancer testing can be accomplished with modern methods such as **MPRAs (massively parallel reporter assays)** or **STARR-seq (self-transcribing active regulatory region sequencing)**.

![Figure from slides: MPRA / STARR-seq](/images/data-science/epic-enhancer-2022/mpra-starr-genome-wide-screening.jpg)
_Source: Claussnitzer et al., 2020_

Plasmid libraries containing putative enhancer regions upstream of a minimal promoter driving unique barcodes can be introduced to a celltype of interest and deep sequencing of barcodes can be used as readout of enhancer activity.

However, these techniques have several limitations:
- lack of native chromatin context
- use of general promoter (instead of enhancer-specific promoter)
-0 only applicable to certain celltypes that can be efficiently transduced


## How can we predict functional enhancers in silico?

I'll now walk through how to computationally develop a simple pipeline for enhancer identification using publicly available ENCODE data.

**Datasets:**

Downloaded publicly available datasets from ENCODE:
- RNA-seq (gene expression)
- ATAC-seq/DNAse-seq (chromatin accessibility)
- H3K27ac ChIP-seq (enhancer activation histone mark)
- p300 ChIP-seq (TF involved in enhancer-mediated transcription)
- 18 state ChromHMM annotation

**Pipeline:**

- First, I identified a large set of potential enhancers by looking at accessible chromatin peaks that are either intronic or distal/intergenic
- I then subset this list to only include peaks that overlap one of the 5 ”enhancer” annotations in the 18-state ChromHMM profile
- I further subset this list to only include peaks that overlap H3K27ac ChIP-seq peaks
- To maximize odds of correct enhancer-gene annotations, I then exclude any putative enhancer further than 10 kB from a TSS

---

**A warning before proceeding: predicting enhancers is not straightforward!**

_“Enhancers and their activity states cannot be reliably predicted from their DNA sequences or from chromatin features, nor can the important parts of the sequence of an enhancer be easily identified.” (Shlyueva, Stampfel, & Stark)_

_“Given the widespread use of histone modifications to predict enhancers, it is interesting that there is no consensus about which marks should be used. […] Generally, the rules used to predict enhancers seem to be driven by the availability of data sets.” (Shlyueva, Stampfel, & Stark)_

_“None of the known histone modifications correlates perfectly with enhancer activity, and even combinations of marks are not perfect predictors.” (Shlyueva, Stampfel, & Stark)_


---

We can go a bit further and try to exhaustively include all possible relevant datasets for _in silico_ enhancer identification.

**Exhaustive Datasets:**

Downloaded publicly available datasets from ENCODE:

- 18 state ChromHMM annotation
- ATAC-seq (chromatin accessibility)
- H3K27ac ChIP-seq (enhancer histone mark)
- H3K4me1 ChIP-seq (enhancer histone mark)
- p300 ChIP-seq (histone acetyltransferase mark)
- Med1 ChIP-seq (Mediator – enhancer-promoter contact mark)
- Rad21 ChIP-seq (Cohesin – enhancer-promoter contact mark)
- POL2RA ChiA-PET (RNA Polymerase II – enhancer-promoter looping)
- hg38 20-way PhastCon scores (evolutionary conservation)
- H3K27me3 (enhancers should not carry this mark)

![Figure from slides: integrated data sources for enhancer prediction](/images/data-science/epic-enhancer-2022/multi-omics-enhancer-prediction-features.png)

As I like to say, _in silico_ enhancer identification is as much art as science and every potential cis-regulatory locus should be approached in a case-by-case basis. When the ENCODE datasets are available for your celltype of interest, aggregating more source of information is always helpful but be way of batch effect caused by different patient samples, experimental protocols, and analysis pipeline differences when integrating data across disparate public sources.
