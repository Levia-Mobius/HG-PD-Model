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
1. You can refer to `Data_description.txt` for more information about `.csv` `.xlsx` `.pt` and `.npy` files in our codes.
2. Code files
   Include 2 types:
   - Python scripts `.py` for collecting Sina Weibo's data (`Sina_crawl`) and some model-training related functions
   - Jupyter files `.ipyn` for (a) data processing; (b) all experiments in paper; and (c) visualization for HG-PD (i.e., exp3)
   - All Jupyter files are in 2 language versions, i.e., Chinese and English, for better understanding :D
3. Python scripts (`.py`)
   - `Sina_crawl`: Used for crawling the data we need from Sina weibo (You can use it for crawling other Sina Weibo posts )
   - `userInter`: HomoG-based model framework for exp2
   - `mcr_HGPD`: HG-PD model framework for exp3
   - `mcrLoss`: MCR2 loss function
   - `augment`: Data augmentation
   - `other_func`: Used for constructing membership matrix \Pi
   - `savePara`: Used for saving loss `.csv` and model states `.pt`
5. Jupyter files (`.ipynb`)
   - `Data_processing`: Include all data processing steps for 3 experiments
   - `K-Prototype`: Inmplementation of exp1 in our paper; Results are saved in `Train_record/KPrototype`
   - `Ablation`: Implementation of exp2 with related visualizations in our paper; Training results are saved in `Train_record/Ablation` and visualizations in `Visualization`
   - `Model`: Implementation of exp3 in our paper; Results are saved in `Train_record/Model`
   - `Analysis_visualize`: Visualizations of exp3 in our paper; Figures are saved in `Visualization`

## Contact
If you have any question on the code, feel free to contact [zili7472.uni.sydney.edu.au](mailto:zili7472.uni.sydney.edu.au) or ()
