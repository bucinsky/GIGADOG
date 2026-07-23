# GIGADOG

The project to predict the affinity of ZINC15 compounds in 3D mol2 format
to non-covalently bind in the Mpro active site of SARS-CoV-2.

## DATA STRUCTURE

- python\_codes
- bash\_scripts
- mol2\_data\_files
- mol2\_gz\_files
- csv\_result\_files

## HOW TO RUN

git clone https://github.com/bucinsky/GIGADOG

### Environment variables 

Set your GIGADOG\_ROOT = GDR variable!  
For instance, create a file, named GDR.s, with:  
  `GIGADOG_ROOT=/path/to/the/directory/GIGADOG`
  `GDR=$GIGADOG_ROOT`  
  `export GDR`  
Activate the GDR variable via command:  
  `source GDR.s`   
You are done!

### Run the prediction

  `mkdir run_prediction`  
  `cd run_prediction`  
  `mkdir xyz_A_predict` \# This must be like this for all letter bins A-K  
  `cd xyz_A_predict`  
Run the prediction:  
  `bash $GDR/bash_scripts/do_run_predict.sh` \# This is Kevin! 

### The SchNet models of J. Matúška [1,2,3]

Please install the code and edit the bash\_scripts/run\_predict\_score\_prototype.sh 
according to your needs,   
see: https://github.com/j-matuska/schnet\_hyperparameters\_optimization

## HOW TO CITE

[comment]: # (This may be the most platform independent comment)
Adriána Dunárová, Marián Gall, Ján Matúška, Michal Pitoňák, Marek Štekláč, Lukas Bucinsky.
Machine Learning Prediction of Docking Scores for 616 Million ZINC15 Compounds: Accuracy and Speed vs. Model and Infrastructure.
(2026) _to be submitted_.

The models used are from:  
[1] L. Bucinsky, M. Gall, J. Matúška, M. Pitoňák, M. Štekláč.
Advances and critical assessment of machine learning techniques for prediction of docking scores. 
Int. J. Quantum Chem. 123 (2023) e27110. DOI: 10.1002/qua.27110
[2] J. Matúška, L. Bucinsky, M. Gall, M. Pitoňák, M. Štekláč. 
SchNetPack Hyperparameter Optimization for a More Reliable Top Docking Scores Prediction. 
J. Phys. Chem. B128 (2024) 4943-4951. DOI: 10.1021/acs.jpcb.4c00296 
[3] J. Matúška, L. Bucinsky, M. Gall, M. Pitoňák, M. Štekláč. 
https://github.com/j-matuska/schnet\_hyperparameters\_optimization 

## REQUIREMENTS

[comment]: # (pip3 install -r requirements.txt)
Essetially you need RDkit, but you better grep "import" in the python files!   
Bash scripts are using standard commands so nothing special should be needed!  
We rely on the sbatch of slurm, if you are using a different batch scheduler you need to adapt the code!
