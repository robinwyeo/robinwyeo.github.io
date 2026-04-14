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

*Adapted from my PhD thesis defense slides (September 15, 2020, Stanford University). Section headings match the defense slide titles; speaker notes from the deck follow the figures where available (advisor-only notes omitted). Where there were no speaker notes, the text is taken from the slide.*

## Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age

![Title slide art: three profiles of heads formed from tree foliage, evoking aging from lush green through autumn color to sparse branches](/images/data-science/thesis/thesis-defense-title-trees-heads.png)


Today I’m excited to share with you an overview of my thesis work in Dr. Anne Brunet’s lab on how chromatin dynamics and cell migration change with age in neural stem cells.

Prior to starting graduate school at Stanford and joining the Brunet Lab, I actually had been working in the field of molecular aging research for the past 4 years back in Boston.

---

## Changing demographics: an aging population (Ortman *et al.*, 2014)

![U.S. population aged 65+ (millions), after Ortman *et al.*, 2014](/images/data-science/thesis/us-population-65plus.jpg)


Changing demographics: an aging population Ortman et al., 2014 US population aged 65+ (in millions) https:// positivepsychology.com /positive-aging/


One of my primary motivations in continuing to investigate the field of aging biology stems from the fact that we are currently experiencing an unprecedented global shift in population demographics.

More and more of the global population is becoming increasingly geriatric, and in the next 30 years, the geriatric population within the US will double.

![Aging and demographic context (slides adapted from public sources in the original deck)](/images/data-science/thesis/aging-psychology-chart.png)


Changing demographics: an aging population Ortman et al., 2014 US population aged 65+ (in millions) https:// www.psychologytoday.com /

_Aging demographics: Predicted number of individuals in the U.S. aged over 65 (in millions)_

## Aging is the single greatest risk factor for cognitive decline and neurodegenerative disease

![Prevalence (%) of Alzheimer’s disease, stroke, vascular dementia, and Parkinson’s disease versus age (years); lines rise with age, especially after ~80 (thesis defense slide)](/images/data-science/thesis/neurodegenerative-prevalence-by-age.png)


Aging is the single greatest risk factor for cognitive decline and neurodegenerative disease Alzheimer’s Disease Parkinson’s Disease Stroke Vascular Dementia 55 60 65 70 75 80 85 90 95 100 0 5 10 15 20 25 30 45 50 Age (years) Prevalence (%)


Why is this so important?

Aging is the single greatest risk factor for a host of devastating pathologies including cardiovascular disease, cancer, and neurodegenerative disease.

As you can see here, as a population ages so too does the prevalence of AD, stroke, dementia, PD.

As such, there is a greater need than ever to develop a better understanding of the basic biology behind brain aging and engineer novel regenerative therapies.

I think one particularly exciting prospective avenue of research in this area involves harnessing the power of adult neural stem cells which have the potential to differentiate into newborn glial cells and newborn neurons and mitigate disease pathology.

## Neural stem cells (NSCs) reside in a complex niche: the sub-ventricular zone (SVZ) (Navarro Negredo\* and Yeo\*, 2020)

![SVZ niche, lineages, and injury context (slide artwork; third-party credits on original deck)](/images/data-science/thesis/svz-niche-schematic.png)

![Alternative SVZ / RMS schematic after Gonzales-Roybal *et al.*, 2013, as in the defense slides](/images/data-science/thesis/svz-niche-gonzales-a.png)
![Rostral migratory stream and olfactory bulb context (same source)](/images/data-science/thesis/svz-niche-gonzales-b.png)

Navarro Negredo* and Yeo*, 2020 Neural stem cells (NSCs) reside in a complex niche: the sub-ventricular zone (SVZ) Olfactory Bulb Stroke / Traumatic Brain Injury SVZ Quiescent NSC Activated NSC NPC Neuroblast Endothelial cells Microglia Choroid Plexus Ependymal cells Take advantage of silence. Break between important points Cell compose the niche Migration (break into 2 slides) If you keep 1 slides: break with silence, but you connect with Graph (for location)


Incredibly it was not until relatively recently that it was accepted that neurons can develop during adulthood.

However we now know that there exist specialized brain regions that contain populations of rare adult neural stem cells known as neurogenic niches.

One such neurogenic niche that we investigate in the Brunet Lab is known as the sub-ventricular zone (SVZ) and lines the lateral ventricles of both hemispheres.

As a neurogenic niche, the sub-ventricular zone is composed of a multitude of different cell types, but, critically, it contains rare populations of NSCs.

The cells at the head of this lineage are called quiescent neural stem cells, and they maintain an active state of dormancy in the cell cycle.

Quiescent NSCs maintain tight localization next to the ependymal cells lining the ventricular wall so they can integrate extracellular cues from their microenvironment and determine the appropriate time to activate.

Upon the introduction of the correct growth factors or changes to environmental conditions, these quiescent NSCs can become activated, releasing their hold on the cell cycle and beginning to proliferate.

[CUE DIAGRAM]

Upon activation, aNSCs begin to differentiate into neural progenitor cells and then neuroblasts which physically migrate out of the niche along the rostral migratory stream, finally arriving in the olfactory bulb as terminally differentiated interneurons.

This has the functional consequence of allowing an organism to better adapt to a changing environment by generating newborn neurons throughout its lifespan which can integrate into the pre-existing olfactory bulb neural circuitry.

Due to their ability to generate newborn neurons, neural stem cells also contain regenerative potential.

Upon acute injury (such as stroke or TBI), NSCs initiate neurogenesis and physically migrate towards the site of injury in order to differentiate into glial cells and neurons to enhance repair.

## Neurogenesis and neural stem cell activation decline with age (Bondolfi *et al.*, 2004)

![Neurogenesis and NSC activation decline with age (Bondolfi *et al.*, 2004)](/images/data-science/thesis/neurogenesis-decline-age.png)


Neurogenesis NSC Activation Age ( months ) 2 12 18 2 12 18 24 Bondolfi et al., 2004 Neurogenesis and neural stem cell activation decline with age Number of newly generated cells


However, while this process occurs quite robustly in the brain of a young animal; throughout aging, both the ability of quiescent NSCs to activate, as well as the capacity of proliferative NSCs to successfully differentiate into functional neurons drastically diminish.

## Potential mechanisms of age-related neurogenic decline


Potential mechanisms of age-related neurogenic decline ? ? ? Quiescent NSCs ( qNSCs ) Activated NSCs ( aNSCs ) Glia Neurons Need-to-know? 1) Eliminate all together (not scholar) OR 2) Close the loop (loop closing may Come too late for people’s taste)


While the specific mechanisms underlying this age-related decline in neurogenesis still remain only partially elucidated, over the years two primary hypotheses have emerged.

One is that throughout aging some cell-intrinsic changes occur within the population of quiescent NSCs that cause them to become unable to release their hold on the cell cycle and properly activate.

And the other is that those cells that do become proliferative tend to display a preferential lineage skewing, differentiating primarily into glial cells, in particular astrocytes, at the expense of generating de novo neurons.

## Mechanisms of neural stem cell aging

![Transcriptional profiling of NSC aging: themes and representative studies from the defense slides](/images/data-science/thesis/nsc-aging-transcriptome-studies.png)


Mechanisms of neural stem cell aging Next-generation sequencing technologies allow us to profile young and old NSCs So far, this has mostly been carried out at the transcriptional level -within the Brunet Lab ( Leeman 2018 ; Dulken *, Buckley*, Navarro Negredo * 2019 ) -as well as by others ( Artegiani 2017; Basak 2018; Hochgerner 2018; Kalamakis 2019; Llorens - Bobadilla 2015; Luo 2015; Mizrak 2019; Shi 2018; Shin 2015; Zywitza 2018 ) Transcriptional studies have so far revealed mechanisms of NSC aging including changes to proteostasis , autophagy, and inflammation pathways However, transcriptional studies only profile gene expression from coding loci and miss information about regulatory features in non-coding portions of the genome -significant gap in knowledge about how the chromatin landscape of NSCs changes with age


So, what exactly are the cell intrinsic changes that occur to NSCs that contribute to this decline in neurogenic potential?

One way to answer this question is to use next-generation sequencing technologies to profile cellular characteristics of young and old NSCs using genomic sequencing.

So far, this has mostly been carried out at the transcriptional level within the Brunet lab as well as others.

Transcriptional studies have so far revealed mechanisms of NSC aging including changes to proteostasis, autophagy, and inflammation pathways.

However transcriptional profiling really only focuses on gene expression from coding loci and misses a lot of information about regulatory features in non-coding portions of the genome.

So when I joined the lab as a graduate student, I was really intrigued by this significant gap in knowledge about how the chromatin state of NSCs is affected by aging.

## The chromatin landscape defines cell state and could reveal aspects of NSC aging and provide insight into their regulation

![Chromatin profiling complements transcription: cell state, enhancers, and TF binding (concept slide)](/images/data-science/thesis/chromatin-landscape-young-old-nsc.png)


The chromatin landscape defines cell state and could reveal aspects of NSC aging and provide insight into their regulation Chromatin profiling can reveal changes to cell states Aging is accompanied by a host of epigenetic changes that affect a cell’s chromatin landscape and can result in loss of transcriptional regulation with age Chromatin profiling has increased sensitivity and yields insights beyond transcription: -presence of poised accessible loci -novel cis-regulatory regions (e.g. enhancers) -binding of regulatory transcription factors Young NSC Old NSC


What exactly is chromatin landscape and what can changes to chromatin states reveal about stem cell aging in the brain?

Very briefly, chromatin is the complex of DNA and regulatory proteins (that you can see in this diagram) that physically determine the accessibility and activity of specific genetic loci.

This is important because how tightly packed chromatin is in certain regions specifies, to a large degree, cell identity and cell state by physically determining genetic regulation.

CUE DIAGRAM

When changes to cell identity occur, for example during aging, these physical features of the genome change, and regions can dynamically gain accessibility (or become "open") or lose accessibility (or become "closed").

So we can profile this dynamically changing chromatin regions throughout aging to reveal new characteristics of stem cell aging and provide insight into their regulation.

In a diverse number of systems, aging is accompanied by a host of epigenetic changes that affect the chromatin landscape and can result in loss of transcriptional regulation with age.

This is especially important for stem cells which must ensure tight transcriptional regulation in order to maintain a pluripotent cell identity throughout natural aging.

## Outline

Part 1: Chromatin landscapes of cell populations from the SVZ Part 2: Dynamic chromatin changes during NSC aging affect adhesion/migration Part 3: Functional validation of age-related changes to adhesion/migration Part 4: Rejuvenation of old aNSC motility by targeting a regulator of adhesion


It would be nice to announce in the intro that analyzing the chromatin changes globally by comparing them with other changes in chromatin (true?)

Could reveal new rejuvenation strategies.

(TAKEN FROM A ROCK SLIDE BUT I MOVED UP HERE)

---

## Part 1: What does chromatin profiling reveal about NSC populations throughout aging?

![Sorting strategy for young vs. old SVZ populations](/images/data-science/thesis/svz-sorting-strategy-a.png)
![FACS / sorting readouts (continued)](/images/data-science/thesis/svz-sorting-strategy-b.png)

### Sorting cell populations from the young and old SVZ

Sorting cell populations from the young and old SVZ

### ATAC-seq: a tool to assess chromatin accessibility (Buenrostro *et al.*, 2013)

![ATAC-seq for chromatin accessibility in rare populations *in vivo* (Buenrostro *et al.*, 2013)](/images/data-science/thesis/atac-seq-overview.png)


Buenrostro et al., 2013 ATAC- seq : a tool to assess chromatin accessibility ATAC- seq is ideally suited to profile the chromatin landscape of rare cell populations in vivo .

### The pro-neural *Ascl1* locus displays differential chromatin accessibility upon NSC activation

![*Ascl1* locus: differential accessibility with activation and age](/images/data-science/thesis/ascl1-locus-accessibility-a.png)
![*Ascl1* locus (continued)](/images/data-science/thesis/ascl1-locus-accessibility-b.png)


The pro-neural Ascl1 locus displays differential chromatin accessibility upon NSC activation Young Old Young Old Young Old Young Old Young Old 3’ 5’ Ascl1


Before diving into the analysis, I wanted to show you what the raw chromatin accessibility signaling track looks like at the neurogenic locus Ascl1, which is required for neuronal differentiation.

Presented here are the 5 different cell types from both young and old animals, and the y-axis of each track represents the degree of accessibility present at this locus.

We can observe here that a 5’ peak, likely representing a poised transcription factor binding site is shared among cells of the NSC lineage but that the transcription start site really only gains accessibility upon activation of the NSCs.

This in fact matches what is observed in our corresponding transcriptomic data in which Ascl1 becomes expressed upon activation and subsequent neuronal differentiation.

### Principal component analysis separates endothelial cells, quiescent NSCs, and activated NSCs

![PCA separates endothelial, quiescent, and activated NSC chromatin states](/images/data-science/thesis/pca-nsc-chromatin-by-cell-state.png)


Principal component analysis separates endothelial cells, quiescent NSCs, and activated NSCs Endothelial Astrocyte / qNSC aNSC / NPC

### Principal component analysis of NSC chromatin landscapes separates with age

![PCA separates NSC chromatin libraries by age](/images/data-science/thesis/pca-nsc-chromatin-by-age.png)


Principal component analysis of NSC chromatin landscapes separates with age

### The chromatin landscape of quiescent and activated NSCs undergo opposing changes with age

![Opposing chromatin changes in quiescent vs. activated NSCs with age](/images/data-science/thesis/opposing-chromatin-qnsC-ansC-age.png)

The chromatin landscape of quiescent and activated NSCs undergo opposing changes with age With age, the quiescent landscape becomes more restricted while the activated landscape becomes more permissive

![Distal and intronic regions (putative enhancers) mediate opposing age-related changes](/images/data-science/thesis/distal-intronic-enhancer-regions.png)

### Opposing chromatin changes are mediated by the same genomic elements: distal and intronic regions (containing putative enhancers)

Opposing chromatin changes are mediated by the same genomic elements: distal and intronic regions (containing putative enhancers)

![Promoter accessibility vs. gene expression across cell types and ages](/images/data-science/thesis/atac-rna-promoter-correlation.png)

![Genomic distribution of ATAC-seq peaks in NSCs](/images/data-science/thesis/atac-peak-genomic-distribution-a.png)
![Peak annotation (promoters, introns, distal)](/images/data-science/thesis/atac-peak-genomic-distribution-b.png)

![Distal and intronic accessibility specifies state and age](/images/data-science/thesis/distal-intronic-specify-state-age.png)

### Part 1: Conclusion


Part 1: Conclusion -Chromatin landscapes separate NSCs by quiescent and activated states as well as age -With age, quiescent chromatin becomes more restricted while activated chromatin becomes more permissive -The majority of age-related changes occur within introns and distal regions suggesting that cis -regulatory elements (e.g. enhancers) may be responsible for age-related changes in neurogenic potential

---

## Part 2: What cellular pathways underlie the opposing age-related changes to the NSC chromatin landscape?

![Pathways enriched in opposing directions: adhesion and motility in qNSCs vs. aNSCs](/images/data-science/thesis/pathways-adhesion-qnsC-down-ansC-up.png)

### With age, qNSCs downregulate pathways involved in cellular adhesion whereas aNSCs upregulate them

With age, qNSCs downregulate pathways involved in cellular adhesion whereas aNSCs upregulate them Negative regulation of cell motility cAMP-mediated signaling Neuron projection development Response to forskolin Protein localization to early endosome Canonical Wnt signaling Cell-cell adhesion (plasma membrane) Endocardial cushion morphogenesis Regulation of toll-like receptor signaling Mesoderm formation Regulation of heart contraction Regulation of cell communication Adherens junction organization Regulation of cell communication Homophilic cell adhesion (plasma membrane) Cell-cell adhesion (mediated by cadherins)

![Open chromatin at adhesion loci (cadherins, integrins, MMPs)](/images/data-science/thesis/adhesion-gene-loci-accessibility.png)

### With age, qNSCs downregulate accessibility in cellular adhesion chromatin loci whereas aNSCs upregulate them

With age, qNSCs downregulate accessibility in cellular adhesion chromatin loci whereas aNSCs upregulate them Cadherins Integrins MMPs Cadherins Integrins MMPs

![Open chromatin enriched in adhesion/migration pathways (summary panel)](/images/data-science/thesis/open-chromatin-adhesion-pathways.png)

![RNA-seq concordance: adhesion programs in qNSC/ast vs. aNSC/NPC](/images/data-science/thesis/rna-seq-adhesion-expression.png)

### With age, qNSCs downregulate gene expression of cellular adhesion pathways whereas aNSCs upregulate them

With age, qNSCs downregulate gene expression of cellular adhesion pathways whereas aNSCs upregulate them ( Dulken *, Buckley*, Navarro Negredo*, et al. 2019) Young Old Young Old qNSC / Ast aNSC /NPC

![scRNA-seq of the young SVZ: cell adhesion gene expression across lineages](/images/data-science/thesis/scrna-adhesion-by-lineage-a.png)
![Adhesion expression by cluster (continued)](/images/data-science/thesis/scrna-adhesion-by-lineage-b.png)
![Adhesion expression by cluster (continued)](/images/data-science/thesis/scrna-adhesion-by-lineage-c.png)

![NF1 / NFI motif enrichment (young qNSCs and old aNSCs)](/images/data-science/thesis/nf1-motif-enrichment.png)

### Motif for NF1, a regulator of cellular adhesion, is enriched in young qNSCs and old aNSCs

Motif for NF1, a regulator of cellular adhesion, is enriched in young qNSCs and old aNSCs With Mahfuza Sharmin TF Motif TF Name TF Motif TF Name NF1 family of transcription factors regulates cell adhesion and cell motion

![NF1 motif analysis (extended panel, Kundaje lab collaboration)](/images/data-science/thesis/nf1-motif-qnsC-young-old-ansC.jpg)

![Shared adhesion signature: young qNSCs and old aNSCs](/images/data-science/thesis/young-qnsC-old-ansC-adhesion-signature.png)

### Part 2: Conclusion


Part 2: Conclusion -Aging causes an opposite adhesion response from qNSCs and aNSCs : -With age, qNSCs lose accessibility at adhesion pathways -With age, aNSCs gain accessibility at adhesion pathways -These analyses of dynamic ATAC-seq chromatin accessibility data predict that aging impairs the ability of aNSCs to migrate

---

## Part 3: Can we experimentally validate the prediction that aging affects NSC adhesion and migration?

![Hypotheses for qNSC vs. aNSC migration with age](/images/data-science/thesis/migration-hypotheses-in-vitro.png)

### Based on age-related chromatin changes, I predict:

Based on age-related chromatin changes, I predict: -old qNSCs to move faster than young qNSCs -old aNSCs to move slower than young qNSCs Quantifying NSC migratory capability in vitro

![Live-cell migration tracking (Imaris)](/images/data-science/thesis/live-cell-tracking-imaris.png)

### Tracking migration using Imaris

Tracking migration using Imaris

{::nomarkdown}
<figure class="thesis-video">
  <video controls playsinline preload="metadata" poster="/images/data-science/thesis/live-cell-tracking-imaris.png" style="max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px;">
    <source src="/images/data-science/thesis/migration-tracking-imaris.mp4" type="video/mp4">
    Your browser does not support embedded video; use the still image above or open the <a href="/images/data-science/thesis/migration-tracking-imaris.mp4">MP4 file</a> directly.
  </video>
  <figcaption><em>Embedded slide video: migration tracking (Imaris), exported from the defense PowerPoint.</em></figcaption>
</figure>
{:/nomarkdown}


-Age causes migration speed of aNSCs to decrease -Young qNSCs rarely migrate at all, while old qNSCs show a small degree of motility - aNSCs readily migrate while qNSCs are largely immobile With age, qNSCs functionally become more migratory whereas aNSCs become less migratory

![Migration speed and behavior: qNSCs vs. aNSCs, young vs. old](/images/data-science/thesis/migration-speed-qnsC-ansC-age.png)

![Regenerative context: activated NSCs, migration, and repair](/images/data-science/thesis/activated-nsc-regenerative-context-a.jpg)
![Mobilization and differentiation (continued)](/images/data-science/thesis/activated-nsc-regenerative-context-b.jpg)

### Migratory activated NSCs have regenerative potential which is impaired in old age

Migratory activated NSCs have regenerative potential which is impaired in old age Upon activation, NSCs display morphological signs of motility Activated NSCs mobilize and differentiate to generate newborn neurons throughout life and to repair acute injury The age-related impairment in aNSC motility suggests that old aNSCs have impaired neurogenic/regenerative potential Mechanisms underlying impaired migration in old aNSCs could reveal novel regenerative targets to improve old brain health Quiescent Activated

![Time-lapse morphology: quiescent vs. activated NSC migration](/images/data-science/thesis/migration-morphology-timecourse-a.png)
![Migration morphology (continued)](/images/data-science/thesis/migration-morphology-timecourse-b.png)

![Cytoskeletal staining: quiescent vs. activated NSCs](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-a.png)
![Cytoskeletal staining (continued)](/images/data-science/thesis/cytoskeleton-qnsC-vs-ansC-b.png)

![ECM migration assay design](/images/data-science/thesis/ecm-migration-assay-overview.png)

### An orthogonal assay measures aNSC migration through extracellular matrix

An orthogonal assay measures aNSC migration through extracellular matrix

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

### Aging decreases the migratory ability of aNSCs

Aging decreases the migratory ability of aNSCs Young Old 0 hrs 24 hrs 48 hrs

![FRET / RGD sensor and actin stress fibers](/images/data-science/thesis/fret-actin-stress-fibers-a.png)
![Focal adhesion / force patterns (continued)](/images/data-science/thesis/fret-actin-stress-fibers-b.png)

### FRET analysis reveals that focal adhesions and actin stress fibers co-localize and could be an important mechanism that gets dysregulated with age

FRET analysis reveals that focal adhesions and actin stress fibers co-localize and could be an important mechanism that gets dysregulated with age Actin Stress Fibers RGD Force Sensor Pattern With Brian Zhong


FRET analysis reveals that focal adhesions and actin stress fibers co-localize at leading and lagging ends of aNSCs; this could be an important mechanism that gets dysregulated with age.

![Vinculin and focal adhesions (concept)](/images/data-science/thesis/vinculin-focal-adhesion-explainer.png)

![Vinculin staining in old aNSCs (*in vitro*)](/images/data-science/thesis/vinculin-staining-old-ansC-in-vitro.png)

### With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein

With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein

![Vinculin in the SVZ *in vivo* (Ki67, GFAP, DAPI)](/images/data-science/thesis/vinculin-in-vivo-svz.jpg)

### With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein, *in vivo*

With age, aNSCs exhibit increased staining for vinculin, a focal adhesion protein, in vivo With Olivia Zhou In vivo SVZ DAPI Ki67 Vinculin GFAP aNSCs

### Part 3: Conclusion


Part 3: Conclusion -Activated NSCs are migratory while quiescent NSCs remain immobile, and aging functionally causes opposing changes in migratory potential -Activated NSCs primarily display F-actin stress fibers and adhesive force patterns at the leading and lagging ends of the cell -Old activated NSCs exhibit impaired migration and increased staining for vinculin, a component of focal adhesions

---

## Part 4: Can chromatin changes in old aNSCs reveal a molecular target for rejuvenation?

![Pathway enrichment linking old aNSC open chromatin to ROCK-related programs](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-a.png)
![Upstream regulator summary (continued)](/images/data-science/thesis/rock-pathway-enrichment-old-ansC-b.png)

### Chromatin peaks that open up in old aNSCs are enriched for upstream regulators of ROCK

Chromatin peaks that open up in old aNSCs are enriched for upstream regulators of ROCK Axonal guidance signaling Synaptogenesis signaling Gα 12/13 signaling Role of NFAT in cardiac hypertrophy Heparan sulfate biosynthesis Gαi signaling GABA receptor signaling Heparan sulfate biosynthesis (late stages) Opioid signaling Gap junction signaling

![ROCK / Y-27632 context across cell types (from defense slides)](/images/data-science/thesis/rock-inhibition-literature-context.png)

### Testing the effects of ROCK inhibition on aNSC migration

Testing the effects of ROCK inhibition on aNSC migration ROCK is a master regulator of cytoskeletal dynamics ROCK inhibition with the small molecule Y-27632: -boosts migration ( myoblasts ( Goetsch 2014), gliomas ( Salhia 2005, Chen 2014), microglia (Fu 2018), and fibroblasts ( Kiltti 2015) ) -impairs migration ( dendritic cells (Rudolph 2016), keratinocytes (Srinivasan 2019), and medulloblastoma cells ( Dyberg 2020) ) How does ROCK inhibition affect aNSC migration?

![Y-27632 improves old aNSC migration](/images/data-science/thesis/y27632-rescue-migration-a.png)
![Y-27632 rescue (continued)](/images/data-science/thesis/y27632-rescue-migration-b.png)

### Inhibition of ROCK (via Y-27632 administration) improves old aNSC migration

Inhibition of ROCK (via Y-27632 administration) improves old aNSC migration No Treatment + Y-27632 Old aNSC Old aNSC

![Migration time course with Y-27632 (converted from slide figure)](/images/data-science/thesis/y27632-migration-timeline.png)

### Old aNSC + Y-27632

Old aNSC + Y-27632 Inhibition of ROCK (via Y-27632 administration) improves old aNSC migration

![ROCK inhibition reduces actin stress fibers](/images/data-science/thesis/rock-inhibition-stress-fibers.png)

### Elimination of actin stress fibers could be a cellular mechanism by which ROCK inhibition improves migration in old aNSCs

Elimination of actin stress fibers could be a cellular mechanism by which ROCK inhibition improves migration in old aNSCs Inhibition of ROCK (via Y-27632 administration) eliminates actin stress fibers

### Part 4: Conclusion


Part 4: Conclusion -ROCK emerged as the top target associated with old aNSC chromatin changes -Inhibition of ROCK: -improves migration in old aNSCs -eliminates actin stress fibers associated with focal adhesions

---

## Summary

-Aging elicits a differential chromatin response in qNSCs and aNSCs involving accessibility changes in adhesion and migration pathways -Functionally, old aNSCs migrate slower than young aNSCs and exhibit marks of increased cell adhesion -ROCK inhibition is capable of rescuing the age-related impairment in old aNSCs

![Working model: aging, chromatin, adhesion, migration, and neurogenesis](/images/data-science/thesis/working-model-chromatin-adhesion.png)

## Implications & Future Directions

-Explore how enhancers mediate age-related neurogenic decline -Recapitulate age-related decline in aNSC migration in vivo -Explore the effects of impaired old aNSC migration and ROCK in stroke and TBI models Olfactory Bulb Stroke / Traumatic Brain Injury SVZ

## Chromatin accessibility dynamics underlie a decline in neural stem cell migratory ability with age

Quiescent NSCs Activated NSCs Glia Neurons

## Acknowledgments

Anne Brunet NSC Team: Matthew Buckley Jackie Butterfield Ben Dulken Katja Hebestreit Chloe Kashiwagi Subheksha Kc Dena Leeman Paloma Navarro Tyson Ruetz Lucy Xu Xiaoai Zhao Olivia Zhou Funding: Stanford Graduate Fellowship (SGF) Genentech Graduate Fellowship Stanford Genome Training Program (SGTP) Aaron Daugherty Anshul Kundaje Mahfuza Sharmin Alex Dunn Steven Tan Brian Zhong Jonathan Long Entire Brunet Lab (A-TEAM) Thesis Committee: Michael Bassik Anshul Kundaje Julien Sage Tony Wyss-Coray
