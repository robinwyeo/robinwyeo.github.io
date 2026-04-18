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

_Adapted from my oral PhD defense presented to my thesis committee at Stanford University, Department of Genetics on September 15, 2020. Published in Nature Aging as [Yeo & Zhou et al. 2023](https://www.nature.com/articles/s43587-023-00449-3)._

---
# Introduction

![U.S. population aged 65+ (millions), after Ortman *et al.*, 2014](/images/data-science/thesis/us-population-65plus.jpg)
_Source: Psychology Today_

## Changing demographics: an aging population

One of my primary motivations in continuing to investigate the field of aging biology after my undergraduate work in the field stemmed from the fact that we are globally experiencing an unprecedented demographic shift in population age.

More and more of the global population is becoming increasingly geriatric, and in the next 30 years, the geriatric population within the US will double.

![Aging and demographic context (slides adapted from public sources in the original deck)](/images/data-science/thesis/ortman.png)
_Source: Ortman et al. (2014)_


## Aging is the single greatest risk factor for cognitive decline and neurodegenerative disease

![Prevalence (%) of Alzheimer’s disease, stroke, vascular dementia, and Parkinson’s disease versus age (years); lines rise with age, especially after ~80 (thesis defense slide)](/images/data-science/thesis/neurodegenerative-prevalence-by-age.png)

Aging is the single greatest risk factor for a host of devastating pathologies including cardiovascular disease, cancer, and neurodegenerative disease.

As you can see in the above plot, as a population ages so too does the prevalence of Alzheimer's Disease, stroke, dementia, and Parkinson's Disease (to name only a few age-related brain diseases).

As such, there is a greater need than ever to develop a better understanding of the basic biology behind brain aging and engineer novel regenerative therapies.

One particularly exciting prospective avenue of research in this area involves harnessing the power of adult neural stem cells which have the potential to differentiate into newborn glial cells and newborn neurons and mitigate disease pathology.


## Neural stem cells (NSCs) reside in a complex niche: the sub-ventricular zone (SVZ)

![Neural stem cells (NSCs) reside in a complex niche: the sub-ventricular zone (SVZ)](/images/data-science/thesis/nsc-svz-niche-navarro-yeo-2020.png)
_Source: Navarro Negredo\* and Yeo\* (2020)_

Incredibly, it was not until relatively recently that it was accepted that neurons can develop during adulthood. However we now know that there exist specialized brain regions that contain populations of rare adult neural stem cells known as neurogenic niches. One such neurogenic niche that we investigate in the Brunet Lab is known as the sub-ventricular zone (SVZ) and lines the lateral ventricles of both hemispheres.

As a neurogenic niche, the sub-ventricular zone is composed of a multitude of different cell types, but, critically, it contains rare populations of NSCs. The cells at the head of this lineage are called quiescent neural stem cells (qNSCs), and they maintain a controlled state of dormancy in the cell cycle. Quiescent NSCs maintain tight localization next to the ependymal cells lining the ventricular wall so they can integrate extracellular cues from their microenvironment and determine the appropriate time to activate.

Upon the introduction of the correct growth factors or changes to environmental conditions, these quiescent NSCs can become activated, releasing their hold on the cell cycle and beginning to proliferate. Upon activation, aNSCs begin to differentiate into neural progenitor cells and then neuroblasts which physically migrate out of the niche along the rostral migratory stream, finally arriving in the olfactory bulb as terminally differentiated interneurons.

This has the functional consequence of allowing an organism to better adapt to a changing environment by generating newborn neurons throughout its lifespan which can integrate into the pre-existing olfactory bulb neural circuitry.


## Neurogenesis and neural stem cell activation decline with age

Due to their ability to generate newborn neurons, neural stem cells also possess regenerative potential. In fact, upon acute injury (such as stroke or TBI), NSCs initiate neurogenesis and physically migrate towards the site of injury in order to differentiate into glial cells and neurons to enhance repair.

![Neurogenesis and NSC activation decline with age (Bondolfi *et al.*, 2004)](/images/data-science/thesis/neurogenesis-nsc-activation-decline-screenshot.png)
_Source: Bondolfi et al. (2004)_

However, while this process occurs quite robustly in the brain of a young animal; throughout aging, both the ability of quiescent NSCs to activate, as well as the capacity of proliferative NSCs to successfully differentiate into functional neurons drastically diminish.


## Potential mechanisms of age-related neurogenic decline

![Model of age-related blockades in neurogenesis](/images/data-science/thesis/nsc-aging-blockades-lineage.png)

While the specific mechanisms underlying this age-related decline in neurogenesis still remain only partially elucidated, over the years two primary hypotheses have emerged:
- one is that throughout aging some cell-intrinsic changes occur within the population of quiescent NSCs that cause them to become unable to release their hold on the cell cycle and properly activate
- the other is that those cells that do become proliferative tend to display a preferential lineage skewing, differentiating primarily into glial cells, in particular astrocytes, at the expense of generating de novo neurons


## Mechanisms of neural stem cell aging

![Transcriptional profiling of NSC aging: themes and representative studies from the defense slides](/images/data-science/thesis/dna-ribbon.png)

**So, what exactly are the cell intrinsic changes that occur to NSCs that contribute to this decline in neurogenic potential?**

One way to answer this question is to use next-generation sequencing technologies to profile cellular characteristics of young and old NSCs using genomic sequencing.

So far, this has mostly been carried out at the transcriptional level
- within the Brunet Lab (_Leeman et al, 2018 ; Dulken, Buckley, & Navarro Negredo et al, 2019_)
- as well as by others (_Artegiani et al, 2017; Basak et al, 2018; Hochgerner et al, 2018; Kalamakis et al, 2019; Llorens-Bobadilla et al, 2015; Luo et al, 2015; Mizrak et al, 2019; Shi et al, 2018; Shin et al, 2015; Zywitza et al, 2018_)

Transcriptional studies have thus far revealed a number of mechanisms of NSC aging including changes to proteostasis, autophagy, and inflammation pathways.

However transcriptional profiling really only focuses on gene expression from coding loci and misses critical information about regulatory features in non-coding portions of the genome.


## The chromatin landscape defines cell state and could reveal aspects of NSC aging and provide insight into their regulation

What exactly is chromatin landscape and what can changes to chromatin states reveal about stem cell aging in the brain?

Very briefly, chromatin is the complex of DNA and regulatory proteins (see diagram below) that physically determine the accessibility and activity of specific genetic loci.

This is important because how tightly packed chromatin is in certain regions specifies, to a large degree, cell identity and cell state by physically determining genetic regulation.

![Chromatin profiling complements transcription: cell state, enhancers, and TF binding (concept slide)](/images/data-science/thesis/chromatin-landscape-young-old-nsc.png)
_Source: Klemm, S. L., Shipony, Z., & Greenleaf, W. J. (2019)_

When changes to cell identity occur, for example during aging, these physical features of the genome change, and regions can dynamically gain accessibility (become "open") or lose accessibility (become "closed").

So we can profile these dynamically changing chromatin regions throughout aging to reveal new characteristics of stem cell aging and provide insight into their regulation. Compared to transcriptomic readouts, chromatin profiling has increased sensitivity and yields regulatory insights beyond transcription such as:
- presence of poised accessible loci
- novel cis-regulatory regions (e.g. enhancers)
- binding of regulatory transcription factors

In a diverse number of systems, aging is accompanied by a host of epigenetic changes that affect the chromatin landscape and can result in loss of transcriptional regulation with age. This is especially important for stem cells which must ensure tight transcriptional regulation in order to maintain a pluripotent cell identity throughout natural aging.

---


# Part 1: What does chromatin profiling reveal about NSC populations throughout aging?

## Sorting cell populations from the young and old SVZ

![Sorting strategy for young vs. old SVZ populations](/images/data-science/thesis/svz-sorting-strategy-a.png)

To begin with, we need a way to actually isolate and subsequently characterize young and old NSCs. To do this, we used a GFAP-GFP transgenic mouse line, and aged a colony of animals until they were 20-24mo old.

We then sacrificed young and old cohorts, microdissected out the SVZ, and used fluorescence-activated cell sorting (FACS) against CD31, GFAP, PROM1, and EGFR to isolate 5 different resident celltypes from the young and old neurogenic niche:

- *Endothelial Cells (Endo)*
- *Astrocytes (Ast)*
- *Quiescent NSCs (qNSC)*
- *Activated NSCs (aNSC)*
- *Neural Progenitor Cells (NPC)*

![FACS / sorting readouts (continued)](/images/data-science/thesis/svz-sorting-strategy-b.png)

In the above figure, you can see an example of the FACS gating protocol used to sort out 4/5 of the resident cell populations of interest.


## ATAC-seq: a tool to assess chromatin accessibility

Near the beginning of my time in graduate school, Jason Buenrostro developed a novel assay to profile chromatin accessibility that had high sensitivity with a very low input cell number (_Buenrostro et al., 2013_), making it ideally suited for profiling rare populations of _ex vivo_ NSCs.

![ATAC-seq for chromatin accessibility in rare populations *in vivo* (Buenrostro *et al.*, 2013)](/images/data-science/thesis/atac-seq-overview.png)
_Source: Buenrostro et al. (2013)_

Briefly, after cell sorting and genomic DNA isolation, a Tn5 transposase is added to the DNA which simultaneously transposes open chromatin regions and inserts amplification barcodes. Subsequent DNA amplification by PCR dollowed by DNA sequencing then allows us to charcaterize open regions of the genome.


## The pro-neural *Ascl1* locus displays differential chromatin accessibility upon NSC activation

Before diving into the analysis, I wanted to show you what the raw chromatin accessibility signaling track looks like at the neurogenic locus _Ascl1_, a gene required for neuronal differentiation.

![ATAC-seq accessibility at the Ascl1 locus by cell type and age, including Endothelial, Astrocyte, qNSC, aNSC, NPC, and annotations](/images/data-science/thesis/ascl1-locus-accessibility-screenshot.png)

Presented above are the 5 different cell types from both young and old animals, and the y-axis of each track represents the degree of accessibility present at this locus. We can observe here that a 5’ peak, likely representing a poised transcription factor binding site is shared among cells of the NSC lineage but that the transcription start site really only gains accessibility upon activation of the NSCs.This in fact matches what is observed in our corresponding transcriptomic data in which _Ascl1_ becomes expressed upon activation and subsequent neuronal differentiation.


## Principal component analysis reveals both celltype and aging clusters

![PCA separates endothelial, quiescent, and activated NSC chromatin states](/images/data-science/thesis/pca-nsc-chromatin-by-cell-state.png)

Principal component analysis (PCA) is a powerful visualization tool that uses unsupervised learning to reduce the dimensionality of high-dimensional datasets into something we can visualize. Applying PCA to all 25 sorted SVZ libraries cleanly separates the celltypes into three clusters: 
- endothelial cells
- a quiescent subpopulation (Ast + qNSCs)
- an activated subpopulation(aNSCs + NPCs)

![PCA separates NSC chromatin libraries by age](/images/data-science/thesis/pca-nsc-chromatin-by-age.png)

By subsetting our libraries down to only the young and old qNSC and aNSC celltypes we see that PC1 separates quiescence from activation while PC3 separates young from old NSCs; this separation along PC3 implies that there are a significant number of discernable age-related changes occuring at the chromatin level in SVZ stem cell populations.


## The chromatin landscape of quiescent and activated NSCs undergo opposing changes with age

![Opposing chromatin changes in quiescent vs. activated NSCs with age](/images/data-science/thesis/opposing-chromatin-qnsC-ansC-age.png)

Surprisingly, the chromatin landscape of quiescent and activated NSCs undergo opposing changes during the aging process. With age, the quiescent landscape becomes more restricted (chromatin sites close) while the activated landscape becomes more permissive (chromatin sites open).

## Opposing chromatin changes are mediated by the same genomic elements: distal and intronic regions (containing putative enhancers)

![Peak annotation (promoters, introns, distal)](/images/data-science/thesis/atac-peak-genomic-distribution-b.png)

The majority of chromatin peaks in both young and old NSCs share similar genomic annotations: accessible chromatin peaks are largely found in regions of the genome annotated as promoters (the regulatory subunits 5' proximal to the gene body), distal (non-coding regions of the genome) or introns (non-coding regions of the genome within a genetic coding locus).

![Genomic distribution of ATAC-seq peaks in NSCs](/images/data-science/thesis/atac-peak-genomic-distribution-a.png)

Based on the above, we can then subset chromatin peaks for young and old NSCs into these three categories to see whether their chromatin profiles all do an equally good job of discriminating between celltypes and age.

![Distal and intronic accessibility specifies state and age](/images/data-science/thesis/distal-intronic-specify-state-age.png)

Interestingly, distal and intronic peaks easily serparate queiscence from activation, and young cells from old cells while the chromatin status of promoters is much more similar across the different libraries. This suggests that celltype-specific and age-related changes are likely to be driven by changes in non-coding regulatory units such as enhancers and insulators typically found in distal and intronic regions of the genome.

## Part 1: Conclusion

- Chromatin landscapes separate NSCs by quiescent and activated states as well as age
- With age, quiescent chromatin becomes more restricted while activated chromatin becomes more permissive
- The majority of age-related changes occur within introns and distal regions suggesting that cis-regulatory elements (e.g. enhancers) may be responsible for age-related changes in neurogenic potential

---

# Part 2: What cellular pathways underlie the opposing age-related changes to the NSC chromatin landscape?

## With age, qNSCs downregulate pathways involved in cellular adhesion whereas aNSCs upregulate them

I used DESEQ2 and EdgeR to call dynamic chromatin peaks that are differentially accessible throughout aging in the qNSC and aSNC populations. Using Gene Ontology (GO), we can perform statistical enrichment of known annotated molecular and cellular processes to get a sense of which pathways and phenotypes are being dysregulated with age.

![Pathways enriched in opposing directions: adhesion and motility in qNSCs vs. aNSCs](/images/data-science/thesis/pathways-adhesion-qnsC-down-ansC-up.png)

Surprisingly, as we age qNSCs downregulate pathways involved in cellular adhesion whereas aNSCs upregulate them.

Another way of visualizing this is to look at the normalized chromatin accessibility values at each of these dynamic ATAC-seq peaks as a heatmap.

![Open chromatin at adhesion loci (cadherins, integrins, MMPs)](/images/data-science/thesis/adhesion-gene-loci-accessibility.png)

This visualization reveals not only the opposing directionality of age-related changes between quiescent and activated NSCs but also the strong enrichment of adhesion and migration pathways that are dynamically changing throughout aging in both.

I then re-analyzed a publically available single cell RNA-seq (scRNA-seq) dataset published from our lab (_Dulken, Buckley, & Navarro-Negredo et al, 2019_) to verify if similar changes were observed within these cell populations during aging at the level of gene expression.

![RNA-seq concordance: adhesion programs in qNSC/ast vs. aNSC/NPC](/images/data-science/thesis/rna-seq-adhesion-expression.png)

Encouragingly, transcription of cellular adhesion pathways changes throughout aging in the same manner predicted by our observed chromatin changes! Throughout age, quiescent subpopulations in the SVZ transcriptionally downregulate cellular adhesion pathways whereas activated subpopulations upregulate them.


## Motif for NF1, a regulator of cellular adhesion, is enriched in the chromatin of young qNSCs and old aNSCs

Transcription factors (TFs) are an important subclass of proteins that bind directly to DNA sequences to regulate gene expression. This is accomplished in part by only binding to specific DNA motifs that are unique to a TF or class of TFs.

To identify predicted TF binding within the chromatin peaks that open/close during NSC aging, I extracted the DNA sequences of these dynamically accessible chromatin regions and performed statistical enrichment for DNA motifs using publicly available databases. We subsequently orthogonally verified these findings in collaboration with the Kundaje lab using their deep learning foundation models.

![NF1 motif](/images/data-science/thesis/nf1-motif.png)

We found that the motif for NF1, a master regulator of cellular adhesion, is enriched in both young qNSCs and old aNSCs suggesting that changes in accessibility might be driving upstream changes in TF binding by the NF1 family and leading to regulatory changes that impact cellular adhesion during NSC aging.


## Part 2: Conclusion

- Aging causes an opposite adhesion response from qNSCs and aNSCs:
   - With age, qNSCs lose accessibility at adhesion pathways
   - With age, aNSCs gain accessibility at adhesion pathways 
- These analyses of dynamic ATAC-seq chromatin accessibility data predict that aging impairs the ability of aNSCs to migrate

---


# Part 3: Can we experimentally validate the prediction that aging affects NSC adhesion and migration?

In order to experimentally validate the prior genomic predictions, I designed an experiment to sort out live NSCs to study their adhesive and migratory properties.

![Hypotheses for qNSC vs. aNSC migration with age](/images/data-science/thesis/migration-hypotheses-in-vitro.png)

Briefly, I microdissected the SVZ out of young and old brains, dissociated them, and cultured them in the appropriate growth factors to induce quiescence or activation. I then used flow cytometry to sort 1000 cells per well on PDL-coated ImageLock plates which were then imaged continuously over the course of 24-28 hours in a tissue culture incubator.

Based on age-related chromatin changes, I predict:
- old qNSCs to move faster than young qNSCs
- old aNSCs to move slower than young qNSCs 

## Quantifying NSC migratory capability in vitro with real-time imaging

I used the tracking software Imaris to analyze and quantify video of qNSCs and aNSCs migrating on PDL-coated plates.

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/migration-tracking-imaris.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/migration-tracking-imaris.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/migration-tracking-imaris.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>Migration tracking of activated NSCs using real-time imaging.</em></figcaption>
</figure>
{:/nomarkdown}

## With age, qNSCs functionally become more migratory whereas aNSCs become less migratory 

![Imaris q vs a](/images/data-science/thesis/imaris-extra.png)

By extracting and calculating velocities for each NSC continuously imaged, we can quantify the migratory properties of NSC subpopulations from the SVZ and determine how aging affects their migratory potential and speed.

![Migration speed and behavior: qNSCs vs. aNSCs, young vs. old](/images/data-science/thesis/migration-speed-qnsC-ansC-age.png)

After analyzing hundreds of hours of NSC migration video, we found that:
- aNSCs readily migrate while qNSCs are largely immobile
- Young qNSCs rarely migrate at all, while old qNSCs show a small degree of motility
- Age causes migration speed of aNSCs to decrease


## Migratory activated NSCs have regenerative potential which is impaired in old age

![Regenerative context: activated NSCs, migration, and repair](/images/data-science/thesis/activated-nsc-regenerative-context-a.png)

As one can see from the above confocal microscopy images of quiescent and activated NSCs cultured _in vitro_, qNSCs and aNSCs have markedly different morphologies. Upon activation, NSCs display morphological signs of motility such as lamellipodia & filopodia. These morphological differences are inherent to their different functions in the niche as aNSCs are required to mobilize out of the niche as they differentiate to generate newborn neurons throughout life and to repair acute injury.

The age-related impairment in aNSC motility suggests that old aNSCs have impaired neurogenic/regenerative potential as they may be unable to properly mobilize out of the neurogenic niche and properly differentiate into neurons or glial cells. Thus the mechanisms underlying impaired migration in old aNSCs represent potentially therapeutically important novel regenerative targets to improve old brain health.


## An orthogonal assay measures aNSC migration through extracellular matrix

Due to the highly _in vitro_ nature of the prior migration assay, I designed an orthogonal experiment to analyze the migratory capability of young vs old aNSCs in which a cluster of aNSCs are imaged as they radially migrate outwards through 3-dimensional extracellular matrix (ECM) to better simulate physiological migration conditions.

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/ecm-migration-assay-video.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/ecm-migration-assay-video.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/ecm-migration-assay-video.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>ECM migration assay.</em></figcaption>
</figure>
{:/nomarkdown}

We can then quantify the area and distance migrated by these aNSC clusters to determine how aging impacts migratory potential.

![ECM migration: young vs. old aNSCs (0–48 h)](/images/data-science/thesis/ecm-migration-young-old-24-48h-a.png)
![ECM migration (continued)](/images/data-science/thesis/ecm-migration-young-old-24-48h-b.png)

As before, I observed a statistically significant decrease in the migratory ability of old aNSCs compared to young aNSCs through ECM supporting our prior findings that aging impairs migration in the activated NSC subpopulation.


## Using Förster resonance energy transfer (FRET) sensors to study NSC biophysics

I next wanted to better understand and visualize the biomechanical underpinnings of this decreased migratory potential observed in old aNSCs so I initiated a collaboration with Alex Dunn's group in Stanford's Chemical Engineering Department.

![FRET sensor diagram](/images/data-science/thesis/fret-overview.png)

The Dunn Lab had developed molecular force sensors that ingeniously leveraged Förster resonance energy transfer (FRET) upon binding with extracellular integrin heterodimers (which mediate focal adhesions) to directly quantify binding force with the substrate through fluorescence.

![FRET / RGD sensor and actin stress fibers](/images/data-science/thesis/fret-actin-stress-fibers-a.png)

By sparsely seeding aNSCs onto these molecular force sensors, we were then able to use confocal microscopy to visualize and quantify how aNSCs adhere to their substrate. FRET analysis revealed that focal adhesions and actin stress fibers co-localize at leading and lagging ends of aNSCs and become dysregulated with age.


## With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein, *in vivo*

Since the above experiments were all performed with _in vitro_ aNSCs, I wanted to confirm that there was evidence of age-related changes in cellular adhesion _in vivo_.

![Vinculin staining in old aNSCs (*in vitro*)](/images/data-science/thesis/vinculin-staining-old-ansC-in-vivo.png)

To do this, we cryosectioned whole young and old brains and then performed immunohistochemical staining of sections containing the SVZ neurogenic niche for vinculin, a key focal adhesion protein. We then quantified the strength of vinculin staining specifically in aNSCs and confirmed that there was a slight but statistically significant increase in the focal adhesion strength of old aNSCs to their niche, consistent with their decreased migratory ability.


## Part 3: Conclusion

- Activated NSCs are migratory while quiescent NSCs remain immobile, and aging functionally causes opposing changes in migratory potential
- Activated NSCs primarily display F-actin stress fibers and adhesive force patterns at the leading and lagging ends of the cell
- Old activated NSCs exhibit impaired migration and increased staining for vinculin, a component of focal adhesions

---


# Part 4: Can chromatin changes in old aNSCs reveal a molecular target for rejuvenation?

Now that we've experimentally confirmed that old aNSCs exhibit decreased migratory ability as predicted by chromatin and transcriptomic profiling, I wanted to return to the differential chromatin landscape of old aNSCs to mine it for targets to reverse these age-related changes that may be mediating their declining neurogenic potential.

## Chromatin peaks that open up in old aNSCs are enriched for upstream regulators of ROCK

![Pathway enrichment linking old aNSC open chromatin to ROCK-related programs](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-a.png)

I re-analyzed the chromatin peaks that become accessible in old aNSCs and found that many of them were related to G⍺12/13 signaling, a primary intracellular pathway used by G protein-coupled receptors (GPCRs) to regulate the cytoskeleton, cell shape, and motility. A key downstream effector of this pathway is Rho-associated protein kinase (ROCK), a serine/threonine kinase acting downstream of the RhoA GTPase that regulates actomyosin cytoskeleton contractility.

![ROCK / Y-27632 context across cell types (from defense slides)](/images/data-science/thesis/rock-inhibition-literature-context.png)

Since ROCK is a master regulator of cytoskeletal dynamics, I dug into the literature to determine if we could target it directly in aNSCs.

Conflicting studies of ROCK inhibition with the small molecule Y-27632 across various celltypes have been shown to:
- boost migration (**myoblasts** (_Goetsch et al., 2014_), **gliomas** (_Salhia et al., 2005, Chen et al., 2014_), **microglia** (_Fu et al., 2018_), and **fibroblasts** (_Kiltti et al., 2015_))
- impair migration (**dendritic cells** (_Rudolph et al., 2016_), **keratinocytes** (_Srinivasan et al., 2019_), and **medulloblastoma cells** (_Dyberg et al., 2020_)) 

The question remains: how does ROCK inhibition affect **aNSC migration**?


## Inhibition of ROCK (via Y-27632 administration) improves old aNSC migration

Given our genomic prediction from chromatin profiling, I decided to target ROCK with the small molecule inhibitor Y-27632. I treated both young and old aNSCs _in vitro_ with this compound and continuously imaged them over the course of 2 days to quantify their migratory velocity.

![Y-27632 improves old aNSC migration](/images/data-science/thesis/y27632-rescue-migration-a.png)

Inhibition of ROCK by Y-27632 drastically improved migratory speed in both young and old aNSCs in this experiment.

![Migration time course with Y-27632 (converted from slide figure)](/images/data-science/thesis/y27632-migration-timeline.png)

We then repeated our second functional migration assay, testing how ROCK inhibition affects migration through ECM. Interestingly, in this assay, Y-27632 administration had no impact on young aNSCs but did rescue the age-related decline in migration exhibited by old aNSCs, returning distance migrated back to a youthful status.


## Inhibition of ROCK (via Y-27632 administration) eliminates actin stress fibers

![ROCK inhibition reduces actin stress fibers](/images/data-science/thesis/rock-inhibition-stress-fibers.png)

To gain a better insight into what intracellular changes may be mediating the Y-27632-dependent change in migration, we performed immunohistochemistry on old aNSCs +/- treatment and quantified their F-actin stress fibers finding a near total elimination of stress fibers in old aNSCs when ROCK is inhibited. This suggests that elimination of actin stress fibers could be a cellular mechanism by which ROCK inhibition improves migration in old aNSCs.


## Part 4: Conclusion

- ROCK emerged as a top target associated with old aNSC chromatin changes
- Inhibition of ROCK:
   - improves migration in old aNSCs
   - eliminates actin stress fibers associated with focal adhesions

---

# Overall Summary

- Aging elicits a differential chromatin response in qNSCs and aNSCs involving accessibility changes in adhesion and migration pathways
- Functionally, old aNSCs migrate slower than young aNSCs and exhibit marks of increased cell adhesion
- ROCK inhibition is capable of rescuing the age-related impairment in old aNSCs

## Implications & Future Directions

![conclusion diagram](/images/data-science/thesis/conclusion-diagram.png)

- Explore how enhancers mediate age-related neurogenic decline
- Recapitulate age-related decline in aNSC migration in vivo
- Explore the effects of impaired old aNSC migration and ROCK in stroke and TBI models 

