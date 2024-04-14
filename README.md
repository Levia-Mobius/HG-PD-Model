# HG-PD-Model
This repository is the official implementation of the group polarization detection model proposed in our paper "Heterogeneous Graph-based Polarization Detection (HG-PD): 
a Model Balancing Crude Processing with Rich Semantics"

## What is HG-PD and Why?
Previous studies examining the detection and analysis of online group polarization have primarily concentrated on the single data type, such as self-reported measures, texts and graph structure. Typically these approaches depict group polarization as two factions with opposing viewpoints. However, such methodologies encounter limitations when applied to entertainment topics.  To fill this research gap, this paper proposes a novel self-supervised model, termed HG-PD, for polarization detection on online social media. 

Leveraging a heterogeneous graph, the model integrates multiple data types. Subsequently, Graph Neural Networks are then utilized to learn the user nodes' representations, guided by [MCR2](https://github.com/ryanchankh/mcr2) loss function, for the downstream clustering task. Utilizing a real-world dataset, our model adeptly discerns nuanced differences among users with similar stances, transcending the traditional dichotomy. Furthermore, ablation experiments demonstrate that incorporating multifaceted information enriches the semantic depth of the graph, thereby furnishing meaningful interpretations that facilitate group polarization detection.

## Requirments
- Python version: `3.10.13`
- All packages versions are listed in `package_version.txt`

## Usage Instruction
1. Code files
   Include 2 types:
   - Python scripts `.py` for collecting Sina Weibo's data (`Sina_crawl`) and some model-training related functions
   - Jupyter file `.ipyn` for data processing and 

3. 
