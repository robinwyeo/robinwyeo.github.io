---
title: "Stanford University Thesis Defense: Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age"
date: 2020-09-15
tags:
  - thesis
  - neural stem cells
  - ATAC-seq
  - chromatin
permalink: /data-science/nsc-chromatin-migration-thesis/
---

_Adapted from my PhD oral defense presented to the Department of Genetics, Stanford University on September 15, 2020. Published in Nature Aging as [Yeo & Zhou et al. 2013](https://www.nature.com/articles/s43587-023-00449-3)._

---
# Introduction

![U.S. population aged 65+ (millions), after Ortman *et al.*, 2014](/images/data-science/thesis/us-population-65plus.jpg)

## Changing demographics: an aging population

One of my primary motivations in continuing to investigate the field of aging biology after my undergraduate work in the field stems from the fact that we are currently experiencing an unprecedented global shift in population demographics.

More and more of the global population is becoming increasingly geriatric, and in the next 30 years, the geriatric population within the US will double (Ortman et al., 2014).

![Aging and demographic context (slides adapted from public sources in the original deck)](/images/data-science/thesis/aging-psychology-chart.png)
_Aging demographics: Predicted number of individuals in the U.S. aged over 65 (in millions)_


## Aging is the single greatest risk factor for cognitive decline and neurodegenerative disease

![Prevalence (%) of Alzheimer’s disease, stroke, vascular dementia, and Parkinson’s disease versus age (years); lines rise with age, especially after ~80 (thesis defense slide)](/images/data-science/thesis/neurodegenerative-prevalence-by-age.png)
_Aging is the single greatest risk factor for cognitive decline and neurodegenerative disease including Alzheimer’s Disease, Parkinson’s Disease, Stroke, and Vascular Dementia._


Why is this so important?

Aging is the single greatest risk factor for a host of devastating pathologies including cardiovascular disease, cancer, and neurodegenerative disease.

As you can see in the above plot, as a population ages so too does the prevalence of AD, stroke, dementia, PD.

As such, there is a greater need than ever to develop a better understanding of the basic biology behind brain aging and engineer novel regenerative therapies.

One particularly exciting prospective avenue of research in this area involves harnessing the power of adult neural stem cells which have the potential to differentiate into newborn glial cells and newborn neurons and mitigate disease pathology.


## Neural stem cells (NSCs) reside in a complex niche: the sub-ventricular zone (SVZ) (_Navarro Negredo\* and Yeo\*, 2020_)

![Neural stem cells (NSCs) reside in a complex niche: the sub-ventricular zone (SVZ)](/images/data-science/thesis/nsc-svz-niche-navarro-yeo-2020.png)

Incredibly it was not until relatively recently that it was accepted that neurons can develop during adulthood.

However we now know that there exist specialized brain regions that contain populations of rare adult neural stem cells known as neurogenic niches.

One such neurogenic niche that we investigate in the Brunet Lab is known as the sub-ventricular zone (SVZ) and lines the lateral ventricles of both hemispheres.

As a neurogenic niche, the sub-ventricular zone is composed of a multitude of different cell types, but, critically, it contains rare populations of NSCs.

The cells at the head of this lineage are called quiescent neural stem cells, and they maintain an active state of dormancy in the cell cycle.

Quiescent NSCs maintain tight localization next to the ependymal cells lining the ventricular wall so they can integrate extracellular cues from their microenvironment and determine the appropriate time to activate.

Upon the introduction of the correct growth factors or changes to environmental conditions, these quiescent NSCs can become activated, releasing their hold on the cell cycle and beginning to proliferate.
Upon activation, aNSCs begin to differentiate into neural progenitor cells and then neuroblasts which physically migrate out of the niche along the rostral migratory stream, finally arriving in the olfactory bulb as terminally differentiated interneurons.

This has the functional consequence of allowing an organism to better adapt to a changing environment by generating newborn neurons throughout its lifespan which can integrate into the pre-existing olfactory bulb neural circuitry.

Due to their ability to generate newborn neurons, neural stem cells also contain regenerative potential.

Upon acute injury (such as stroke or TBI), NSCs initiate neurogenesis and physically migrate towards the site of injury in order to differentiate into glial cells and neurons to enhance repair.


## Neurogenesis and neural stem cell activation decline with age (Bondolfi *et al.*, 2004)

![Neurogenesis and NSC activation decline with age (Bondolfi *et al.*, 2004)](/images/data-science/thesis/neurogenesis-nsc-activation-decline-screenshot.png)
_Neurogenesis and neural stem cell activation decline with age. Number of newly generated cells measured in the adult mouse brain shows a dramatic decline with increasing age in both neurogenesis (red) and NSC activation (blue), based on Bondolfi *et al.*, 2004._

However, while this process occurs quite robustly in the brain of a young animal; throughout aging, both the ability of quiescent NSCs to activate, as well as the capacity of proliferative NSCs to successfully differentiate into functional neurons drastically diminish.


## Potential mechanisms of age-related neurogenic decline

![Model of age-related blockades in neurogenesis](/images/data-science/thesis/nsc-aging-blockades-lineage.png)

While the specific mechanisms underlying this age-related decline in neurogenesis still remain only partially elucidated, over the years two primary hypotheses have emerged.

One is that throughout aging some cell-intrinsic changes occur within the population of quiescent NSCs that cause them to become unable to release their hold on the cell cycle and properly activate.

And the other is that those cells that do become proliferative tend to display a preferential lineage skewing, differentiating primarily into glial cells, in particular astrocytes, at the expense of generating de novo neurons.


## Mechanisms of neural stem cell aging

![Transcriptional profiling of NSC aging: themes and representative studies from the defense slides](/images/data-science/thesis/dna-ribbon.png)

So, what exactly are the cell intrinsic changes that occur to NSCs that contribute to this decline in neurogenic potential?

One way to answer this question is to use next-generation sequencing technologies to profile cellular characteristics of young and old NSCs using genomic sequencing.

So far, this has mostly been carried out at the transcriptional level
- within the Brunet Lab (_Leeman et al, 2018 ; Dulken, Buckley, & Navarro Negredo et al, 2019_)
- as well as by others (_Artegiani et al, 2017; Basak et al, 2018; Hochgerner et al, 2018; Kalamakis et al, 2019; Llorens-Bobadilla et al, 2015; Luo et al, 2015; Mizrak et al, 2019; Shi et al, 2018; Shin et al, 2015; Zywitza et al, 2018_)

Transcriptional studies have so far revealed mechanisms of NSC aging including changes to proteostasis, autophagy, and inflammation pathways.

However transcriptional profiling really only focuses on gene expression from coding loci and misses a lot of information about regulatory features in non-coding portions of the genome.

![Transcriptional profiling of NSC aging: themes and representative studies from the defense slides](/images/data-science/thesis/dna-ribbon.png)

## The chromatin landscape defines cell state and could reveal aspects of NSC aging and provide insight into their regulation

What exactly is chromatin landscape and what can changes to chromatin states reveal about stem cell aging in the brain?

Very briefly, chromatin is the complex of DNA and regulatory proteins (that you can see in this diagram) that physically determine the accessibility and activity of specific genetic loci.

This is important because how tightly packed chromatin is in certain regions specifies, to a large degree, cell identity and cell state by physically determining genetic regulation.

![Chromatin profiling complements transcription: cell state, enhancers, and TF binding (concept slide)](/images/data-science/thesis/chromatin-landscape-young-old-nsc.png)

When changes to cell identity occur, for example during aging, these physical features of the genome change, and regions can dynamically gain accessibility (or become "open") or lose accessibility (or become "closed").

So we can profile this dynamically changing chromatin regions throughout aging to reveal new characteristics of stem cell aging and provide insight into their regulation. Compared to transcriptionalo readouts, chromatin profiling has increased sensitivity and yields regulatory insights beyond transcription: 
- presence of poised accessible loci
- novel cis-regulatory regions (e.g. enhancers)
- binding of regulatory transcription factors Young NSC Old NSC

In a diverse number of systems, aging is accompanied by a host of epigenetic changes that affect the chromatin landscape and can result in loss of transcriptional regulation with age. This is especially important for stem cells which must ensure tight transcriptional regulation in order to maintain a pluripotent cell identity throughout natural aging.

---

# Part 1: What does chromatin profiling reveal about NSC populations throughout aging?

## Sorting cell populations from the young and old SVZ

![Sorting strategy for young vs. old SVZ populations](/images/data-science/thesis/svz-sorting-strategy-a.png)

To begin with, we need a way to actually isolate and subsequently characterize young and old NSCs. To do this, we used a GFAP-GFP transgenic mouse line and aged a colony of animals until they were 20-24mo old.

We then sacrificed them, microdissected out the SVZ, and used a FACS gating protocol involving CD31, GFAP, PROM1, and EGFR to isolate 5 different resident celltypes from the young and old neurogenic niche:

- *Endothelial Cells (Endo)*
- *Astrocytes (Ast)*
- *Quiescent NSCs (qNSC)*
- *Activated NSCs (aNSC)*
- *Neural Progenitor Cells (NPC)*

![FACS / sorting readouts (continued)](/images/data-science/thesis/svz-sorting-strategy-b.png)

## ATAC-seq: a tool to assess chromatin accessibility

![ATAC-seq for chromatin accessibility in rare populations *in vivo* (Buenrostro *et al.*, 2013)](/images/data-science/thesis/atac-seq-overview.png)

Near the beginning of my time in graduate school, Jason Buenrostro developed a novel assay to profile chromatin accessibility that had high sensitivity with a very low input cell number (_Buenrostro et al., 2013_), making it ideally suited for profiling rare populations of _ex vivo_ NSCs.

Briefly, after cell sorting and genomic DNA isolation, a Tn5 transposase is added to the DNA which simultaneously transposes open chromatin regions and inserts amplification barcodes. Subsequent DNA amplification by PCR and DNA sequencing then allows us to charcaterize open regions of the genome.


## The pro-neural *Ascl1* locus displays differential chromatin accessibility upon NSC activation

![ATAC-seq accessibility at the Ascl1 locus by cell type and age, including Endothelial, Astrocyte, qNSC, aNSC, NPC, and annotations](/images/data-science/thesis/ascl1-locus-accessibility-screenshot.png)

Before diving into the analysis, I wanted to show you what the raw chromatin accessibility signaling track looks like at the neurogenic locus _Ascl1_, a gene required for neuronal differentiation.

Presented above are the 5 different cell types from both young and old animals, and the y-axis of each track represents the degree of accessibility present at this locus. We can observe here that a 5’ peak, likely representing a poised transcription factor binding site is shared among cells of the NSC lineage but that the transcription start site really only gains accessibility upon activation of the NSCs.This in fact matches what is observed in our corresponding transcriptomic data in which Ascl1 becomes expressed upon activation and subsequent neuronal differentiation.


## Principal component analysis reveals both celltype and aging clusters

![PCA separates endothelial, quiescent, and activated NSC chromatin states](/images/data-science/thesis/pca-nsc-chromatin-by-cell-state.png)

Principal component analysis (PCA) is a powerful visualization tool that uses unsupervised learning to reduce the dimensionality of high-dimensional datasets into something we can visualize. Applyying PCA to all 25 sorted SVZ libraries cleanly separates the celltypes into three clusters: 
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

The majority of chromatin peaks in both young and old NSCs share simialr genomic annotations: accessible chromatin is typically called in regions of the genome annotated as promoters (the regulatory subunits 5' proximal to the gene body), distal (non-coding regions of the genome) or introns (non-coding regions of the genome within a gene body).

![Genomic distribution of ATAC-seq peaks in NSCs](/images/data-science/thesis/atac-peak-genomic-distribution-a.png)

We can then subset chromatin peaks for young and old NSCs into these three categories to see whether their chromatin profiles all do an equally good job of discriminating between celltypes and age.

![Distal and intronic accessibility specifies state and age](/images/data-science/thesis/distal-intronic-specify-state-age.png)

Interestingly, distal and intronic peaks easily serparate queiscence from activation, and young cells from old cells while the chromatin status of promoters is much more similar across the different libraries. This suggests that celltype-specific and age-related changes are likely to be driven by changes in non-coding regulatory units such as enhancers and insulators typically found in distal and intronic regions of the genome.

## Part 1: Conclusion

- Chromatin landscapes separate NSCs by quiescent and activated states as well as age\
- With age, quiescent chromatin becomes more restricted while activated chromatin becomes more permissive
- The majority of age-related changes occur within introns and distal regions suggesting that cis
- regulatory elements (e.g. enhancers) may be responsible for age-related changes in neurogenic potential

---

# Part 2: What cellular pathways underlie the opposing age-related changes to the NSC chromatin landscape?

## With age, qNSCs downregulate pathways involved in cellular adhesion whereas aNSCs upregulate them

I used DESEQ2 and EdgeR to call dynamic chromatin peaks that are differentially accessible throughout aging in the qNSC and aSNC populations. Using Gene Ontology (GO), we can perform statistical enrichment within known annotated molecular and cellular processes to get a sense of which pathawys and phenotypes are being affected throughout aging.

![Pathways enriched in opposing directions: adhesion and motility in qNSCs vs. aNSCs](/images/data-science/thesis/pathways-adhesion-qnsC-down-ansC-up.png)

Surprisingly, with age, qNSCs downregulate pathways involved in cellular adhesion whereas aNSCs upregulate them.

Another way of visualizing this is to look at the normalized chromatin accessibility values at each of these dynamic ATAC-seq peaks as a heatmap.

![Open chromatin at adhesion loci (cadherins, integrins, MMPs)](/images/data-science/thesis/adhesion-gene-loci-accessibility.png)

This visualization reveals not only the opposing directionality of age-related changes between quiescent and activated NSCs but also the strong enrichment of adhesion and migration pathways that are dynamically changing throughout aging in both.

I then re-analyzed a publically available single cell RNA-seq (scRNA-seq) dataset published from our lab (_Dulken, Buckley, & Navarro-Negredo et al, 2019_) to verify if similar changes were observed wiwthin these cell populations during aging at the level of gene expression.

![RNA-seq concordance: adhesion programs in qNSC/ast vs. aNSC/NPC](/images/data-science/thesis/rna-seq-adhesion-expression.png)

Encouragingly, transcription of cellular adhesion pathways changes throughout aging in the same manner predicted by our observed chromatin changes! Throughout age, quiescent subpopulations in the SVZ transcriptionally dowwnregulate cellular adhesion pathways whereas activated subpopulations upregulate them.


## Motif for NF1, a regulator of cellular adhesion, is enriched in young qNSCs and old aNSCs

Transcription factors (TFs) are an important subclass of proteins that bind directly to DNA sequences - typically to regulate gene expression. This is accomplished in part by only binding to specific DNA motifs that are unique to a TF or class of TFs.

![NF1 motif](/images/data-science/thesis/nf1-motif.png)

To identify predicted TF binding within the chromatin peaks that open/close with NSC aging, I extracted the DNA sequences of these synamically accessible chromatin regions and performed statistical enrichment for DNA motifs using publically available databases. We subsequently orthogonally verified these findings in collaboration with the Kundaje lab using their deep learning foundation models.

We found that the motif for NF1, a master regulator of cellular adhesion, is enriched in young qNSCs and old aNSCs suggesting that changes in accessibility might be driving upstream changes in TF binding by the NF1 family and leading to to regulatory changes in cellular adhesion during NSC aging.


## Part 2: Conclusion

- Aging causes an opposite adhesion response from qNSCs and aNSCs:
   - With age, qNSCs lose accessibility at adhesion pathways
   - With age, aNSCs gain accessibility at adhesion pathways 
- These analyses of dynamic ATAC-seq chromatin accessibility data predict that aging impairs the ability of aNSCs to migrate

---

# Part 3: Can we experimentally validate the prediction that aging affects NSC adhesion and migration?

![Hypotheses for qNSC vs. aNSC migration with age](/images/data-science/thesis/migration-hypotheses-in-vitro.png)

Based on age-related chromatin changes, I predict:
- old qNSCs to move faster than young qNSCs
- old aNSCs to move slower than young qNSCs 

![Live-cell migration tracking (Imaris)](/images/data-science/thesis/live-cell-tracking-imaris.png)

## Quantifying NSC migratory capability in vitro using Imaris

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/live-cell-tracking-imaris.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/migration-tracking-imaris.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/migration-tracking-imaris.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>Embedded slide video: migration tracking (Imaris), exported from the defense PowerPoint.</em></figcaption>
</figure>
{:/nomarkdown}

## With age, qNSCs functionally become more migratory whereas aNSCs become less migratory 

![Migration speed and behavior: qNSCs vs. aNSCs, young vs. old](/images/data-science/thesis/migration-speed-qnsC-ansC-age.png)

- aNSCs readily migrate while qNSCs are largely immobile
- Young qNSCs rarely migrate at all, while old qNSCs show a small degree of motility
- Age causes migration speed of aNSCs to decrease


## Migratory activated NSCs have regenerative potential which is impaired in old age

![Regenerative context: activated NSCs, migration, and repair](/images/data-science/thesis/activated-nsc-regenerative-context-a.png)

- Upon activation, NSCs display morphological signs of motility
- Activated NSCs mobilize and differentiate to generate newborn neurons throughout life and to repair acute injury
- The age-related impairment in aNSC motility suggests that old aNSCs have impaired neurogenic/regenerative potential
- Mechanisms underlying impaired migration in old aNSCs could reveal novel regenerative targets to improve old brain health Quiescent Activated


## An orthogonal assay measures aNSC migration through extracellular matrix

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/ecm-migration-assay-overview.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/migration-assay-video.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/migration-assay-video.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>Embedded slide video: ECM migration assay (from the defense PowerPoint).</em></figcaption>
</figure>
{:/nomarkdown}


## Aging decreases the migratory ability of aNSCs

![ECM migration: young vs. old aNSCs (0–48 h)](/images/data-science/thesis/ecm-migration-young-old-24-48h-a.png)
![ECM migration (continued)](/images/data-science/thesis/ecm-migration-young-old-24-48h-b.png)


## Using Förster resonance energy transfer (FRET) sensors to study NSC biophysics

![FRET sensor diagram](/images/data-science/thesis/fret-overview.png)

![FRET / RGD sensor and actin stress fibers](/images/data-science/thesis/fret-actin-stress-fibers-a.png)


FRET analysis reveals that focal adhesions and actin stress fibers co-localize at leading and lagging ends of aNSCs; this could be an important mechanism that gets dysregulated with age.

## With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein

![Vinculin staining in old aNSCs (*in vitro*)](/images/data-science/thesis/vinculin-staining-old-ansC-in-vitro.png)

## With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein, *in vivo*

![Vinculin in the SVZ *in vivo* (Ki67, GFAP, DAPI)](/images/data-science/thesis/vinculin-in-vivo-svz.jpg)

## Part 3: Conclusion

- Activated NSCs are migratory while quiescent NSCs remain immobile, and aging functionally causes opposing changes in migratory potential
- Activated NSCs primarily display F-actin stress fibers and adhesive force patterns at the leading and lagging ends of the cell
- Old activated NSCs exhibit impaired migration and increased staining for vinculin, a component of focal adhesions

---

# Part 4: Can chromatin changes in old aNSCs reveal a molecular target for rejuvenation?

## Chromatin peaks that open up in old aNSCs are enriched for upstream regulators of ROCK

![Pathway enrichment linking old aNSC open chromatin to ROCK-related programs](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-a.png)
![Upstream regulator summary (continued)](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-b.png)


## Testing the effects of ROCK inhibition on aNSC migration

![ROCK / Y-27632 context across cell types (from defense slides)](/images/data-science/thesis/rock-inhibition-literature-context.png)

ROCK is a master regulator of cytoskeletal dynamics. Conflicting studies of ROCK inhibition with the small molecule Y-27632 have been shown to:
- boost migration (myoblasts (_Goetsch et al., 2014_), gliomas (_Salhia et al., 2005, Chen et al., 2014_), microglia (_Fu et al., 2018_), and fibroblasts (_Kiltti et al., 2015_))
- impair migration (dendritic cells (_Rudolph et al., 2016_), keratinocytes (_Srinivasan et al., 2019_), and medulloblastoma cells (_Dyberg et al., 2020_)) 

The question remains: how does ROCK inhibition affect aNSC migration?


## Inhibition of ROCK (via Y-27632 administration) improves old aNSC migration

![Y-27632 improves old aNSC migration](/images/data-science/thesis/y27632-rescue-migration-a.png)


![Migration time course with Y-27632 (converted from slide figure)](/images/data-science/thesis/y27632-migration-timeline.png)

Old aNSC + Y-27632 Inhibition of ROCK (via Y-27632 administration) improves old aNSC migration


## Inhibition of ROCK (via Y-27632 administration) eliminates actin stress fibers

![ROCK inhibition reduces actin stress fibers](/images/data-science/thesis/rock-inhibition-stress-fibers.png)

Elimination of actin stress fibers could be a cellular mechanism by which ROCK inhibition improves migration in old aNSCs Inhibition of ROCK (via Y-27632 administration) eliminates actin stress fibers


## Part 4: Conclusion

- ROCK emerged as the top target associated with old aNSC chromatin changes
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

## Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age

Quiescent NSCs Activated NSCs Glia Neurons

## Acknowledgments

Anne Brunet NSC Team: Matthew Buckley Jackie Butterfield Ben Dulken Katja Hebestreit Chloe Kashiwagi Subheksha Kc Dena Leeman Paloma Navarro Tyson Ruetz Lucy Xu Xiaoai Zhao Olivia Zhou Funding: Stanford Graduate Fellowship (SGF) Genentech Graduate Fellowship Stanford Genome Training Program (SGTP) Aaron Daugherty Anshul Kundaje Mahfuza Sharmin Alex Dunn Steven Tan Brian Zhong Jonathan Long Entire Brunet Lab (A-TEAM) Thesis Committee: Michael Bassik Anshul Kundaje Julien Sage Tony Wyss-Coray
