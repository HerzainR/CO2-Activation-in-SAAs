# CO2-Activation-in-SAAs
This repository contains supporting information related to the work titled "Rules Describing CO2 Activation on Single-Atom Alloys from DFT-meta-GGA Calculations and Artificial Intelligence"

The provided information is divided in three folders:

1. screening_candidates/

This folder contain .csv files with the full lists of candidate and selected SA and DA alloy surface sites. In particular, the lists refer to the results displayed in Table 3.

SAAs
Total candidate sites: 60
Sites selected by the rules: 23

DAAs
Total candidate sites:1,488
Sites selected by the rules: 383

2. SAAs_paper_results/

The results of the SGD analysis described in the paper are provided in the folder output/

Additionally, we provide a jupyter notebook mented extract the information of the output/ folder and reproduce the SGD results discussed in the paper:

CO2_activation_rules_by_SGD.ipynb


3. run_SGD

The folder has the python script script_sgd_realK.py, which allows to run SGD with realKD. The realKD version used to perfomed the studies in our work is also provided (reakKD folder).  

