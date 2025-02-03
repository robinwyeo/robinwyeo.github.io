---
permalink: /
title: "Travel notes through Southeast Asia"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---  

============================================


About
======

My name’s Robin W. Yeo and I’m a biological data scientist specializing primarily in bioinformatics, epigenomics, and computational protein engineering. I received my B.Sc. in Biological Engineering from MIT and my Ph.D. in Genetics in the Brunet Lab at Stanford University. After 10 years living in the Bay Area (California, USA), my wife and I quit our jobs to go travel and work on some personal projects/goals. Over the course of 2024/2025, we’ll be backpacking through North America, Southeast Asia, and South America.

![Robin_Sara_About](https://drive.google.com/thumbnail?id=1GZopkcv8_BpmCG-JNJPGcEdD-Osi4DWj&sz=w1000)
<br/>
<br/>
<br/>

Research Background
======

**PhD in genetics with extensive genomics and bioinformatics experience including next-generation sequencing analysis and machine learning/deep learning expertise. 15+ years of research experience including molecular biology and genetic manipulation in numerous _in vitro_ and _in vivo_ systems. Expert in CRISPR-Cas systems and their therapeutic applications. Strong independent and collaborative publication record in both primary research and scientific literature reviews. Passionate about genome editing, aging biology, epigenetics, neuroscience, and computational protein engineering.**


## Engineering CRISPR-Cas Systems for Epigenetic Regulation

![NBT](/images/Research_Summary/NeurIPS.jpeg)
<br/>

&emsp;&emsp;Over the past decade, CRISPR has revolutionized our ability to easily and precisely edit the genome, dramatically accelerating functional genomic and gene therapy research. More recently, this technology has been developed into next-generation tools such as CRISPRi and CRISPRa capable of modulating gene expression without causing double-stranded breaks by fusing functional peptides capable of epigenetic changes to nuclear-inactive Cas molecules. 
<br/>
&emsp;&emsp;At [EpiCRISPR Biotechnologies](https://epicrispr.com/), one of my first projects involved bioinformatically analyzing high-throughout screening data of putative functional peptides sourced from human, viral, and archaeal genomes for their ability to modulate gene expression. Working with Dr. Giovanni A. Carosso and the Technology Development team, we discovered a host of novel hypercompact transcriptional modulators, including high-potency activators capable of mitotically stable gene activation; we further improved these therapeutic peptides through iterative rounds of rational protein engineering by leveraging machine learning models I trained to predict their biochemical and biophysical characteristics [(Biorxiv, 2023)](https://www.biorxiv.org/content/10.1101/2023.06.02.543492v4).
<br/>
&emsp;&emsp;I then leveraged these high-throughput screening data to train an ensemble model composed of a gradient-boosted decision tree (XGBoost) and a convolutional neural network (CNN) to predict which peptides were capable of gene activation from sequence alone (augmented by transfer learning using the large protein language model ESM-2). We used this ensemble model to perform ML-guided protein engineering of novel, highly diverse gene activators, boosting our discovery rate ~50x compared to our original high-throughput screen by leveraging a novel evolutionary sampling algorithm designed by my colleague Dr. M. Zaki Jawaid [(NeurIPS Workshop on Generative AI and Biology, 2023)](https://openreview.net/pdf?id=b54p3jCgBw).
<br/>
&emsp;&emsp;However, for CRISPRi and CRISPRa to therapeutically modulate gene expression, they require a guide RNA (gRNA) to direct the complex to a target gene of interest.  In an effort to make CRISPR more accessible to the general scientific community, I wrote a guide design algorithm for CasMINI specifically devised to exhaustively assess putative off-target binding sites and thus prioritize safe, therapeutic guides for gene therapy applications [(Biorxiv, 2024)](https://www.biorxiv.org/content/10.1101/2023.09.17.558168v2). We then ran the guide design tool comprehensively against every gene in the human genome and created a website tool to host the database as a free resource for the scientific community: [www.casmini-tool.com](www.casmini-tool.com).


## Neural Stem Cell (NSC) Aging

![NSC_aging](/images/Research_Summary/NSC_Aging.jpeg)
<br/>

&emsp;&emsp;The mammalian brain contains rare populations of neural stem cells (NSCs) that are capable of activating into progenitor cells and terminally differentiating into glial cells (i.e. astrocytes, oligodendrocytes, …) and neurons. However, during aging, NSC populations markedly decline and their neurogenic ability suffers dramatically. During my PhD in Dr. Anne Brunet’s lab (Stanford University - Department of Genetics), I co-authored a review on this subject with Dr. Paloma Navarro Negredo discussing the mechanisms that regulate NSC biology during aging, focusing on metabolism, genetic regulation, and the surrounding niche, as well as emerging rejuvenation strategies [(Cell Stem Cell, 2020)](https://pubmed.ncbi.nlm.nih.gov/32726579/).
<br/>
&emsp;&emsp;For my thesis work in the Brunet Lab, I investigated the mechanisms underlying this decline by profiling the genome-wide chromatin landscape of NSCs _in vivo_ and _in vitro_ during aging. By comparing the chromatin landscapes of young and old NSCs, I identified changes in accessibility at genes and enhancers regulating cellular adhesion and migration as a key hallmark of NSC aging. Along with my co-author Dr. Olivia Zhou, we demonstrated that old activated NSCs exhibit decreased migration _in vitro_ and diminished mobilization out of the niche for neurogenesis _in vivo_. By inhibiting the cytoskeletal-regulating kinase ROCK (a target we identified from genome-wide chromatin accessibility data), we were able to restore migration in old activated NSCs _in vitro_, and boost neurogenesis _in vivo_ [(Nature Aging, 2023)](https://pubmed.ncbi.nlm.nih.gov/37443352/).
<br/>
&emsp;&emsp;Over the course of my time in the Brunet Lab, I also had the opportunity to contribute to various other research projects investigating NSC aging - specifically Dr. Deena Leeman’s work on lysosome and proteostatic decline in aging NSCs [(Science, 2018)](https://pubmed.ncbi.nlm.nih.gov/29590078/), and Dr. Tyson Ruetz’s work identifying regulators of NSC aging with high-throughput CRISPR-Cas screening [(Nature, 2024)](https://pubmed.ncbi.nlm.nih.gov/39358505/).


## _C. elegans_ Metabolism, Epigenetics, and Reproduction

![C_elegans_Daugherty_Yeo](/images/Research_Summary/C_elegans_Daugherty_Yeo.png)
<br/>

&emsp;&emsp;For over 10 years, I got to study _C. elegans_, one of my favorite model organisms, across various experimental and computational projects in the Guarente Lab (MIT), Mair Lab (Harvard School of Public Health), and Brunet Lab (Stanford University). My first _C. elegans_ project involved investigating the mechanisms of action underlying the Sirtuin family’s critical role in organismal aging in the Guarente Lab. This led to a project in Will Mair’s lab on elucidating AMPK and CRTC-1’s role in cellular energy homeostasis in the context of _C. elegans_ aging [(Cell, 2015)](https://pubmed.ncbi.nlm.nih.gov/25723162/). Shifting from metabolism to epigenetics in the Brunet Lab, I then co-authored a paper with Dr. Aaron Daugherty in which we profiled the chromatin accessibility landscape of the _C. elegans_ genome throughout development in order to identify novel cis-regulatory elements (i.e. distal enhancers) that regulated gene activity in a tissue-specific manner [(Genome Research, 2017)](https://pubmed.ncbi.nlm.nih.gov/29141961/). As I moved from wetlab to drylab research, I had the opportunity to collaborate with my baymate Dr. Lauren Booth on her postdoctoral work elucidating the underlying genetic mechanisms of male-induced demise during _C. elegans_ reproduction [(elife, 2019)](https://pubmed.ncbi.nlm.nih.gov/31282863/)[(Nature Aging, 2022)](https://pubmed.ncbi.nlm.nih.gov/37118502/).


