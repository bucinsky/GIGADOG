# GIGADOG

The GIGADOG project is a showcase of hit candidates picking among ZINC15 compounds in 3D mol2 format
to non-covalently bind in the Mpro active site of SARS-CoV-2.

## DATA STRUCTURE

- python\_codes
- bash\_scripts
- mol2\_data\_files
- mol2\_gz\_files
- csv\_result\_files

## HOW TO RUN

git clone https://github.com/bucinsky/GIGADOG
<br>

Check the Environment variables section at the bottom.

### Run the prediction

Please note the current version is just a prediction simulation, we have selected a sample of 100 files in each letter bin to show
the _mol2.gz_ to _xyz_ conversion (including the presence of broken files).
The prediction step is not really done, we rather copy the results.  
Please cite the ZINC15 database, if using the files present in the mol2\_gz\_files directory:   
Sterling and Irwin, J. Chem. Inf. Model, 2015 https://pubs.acs.org/doi/abs/10.1021/acs.jcim.5b00559    
Irwin, Sterling, Mysinger, Bolstad and Coleman, J. Chem. Inf. Model, 2012 DOI: 10.1021/ci3001277   
Irwin and Shoichet, J. Chem. Inf. Model. 2005;45(1):177-82.  10.1021/ci049714+   
https://zinc15.docking.org/
<br>

To run the prediction choose a new directory
  `mkdir run_prediction`  
  `cd run_prediction`  
For all letters L (from A-K), it is mandatory to continue the following:
  `mkdir xyz_L_predict` \# This must be like this for all letter bins A-K  
  `cd xyz_L_predict`  
Run the prediction (see REQUIREMENTS):  
  `bash $GDR/bash_scripts/do_run_predict_score.sh` \# This is Kevin! 
<br>

Check for broken _mol2.gz_ to _xyz_ conversions (e.g. xyz\_B\_predict)   
if present, then run:  
1. conversion of _mol2.gz_ to _xyz_    
  `nohup bash $GDR/bash_scripts/run_predict_score_BROKEN_1.sh &`    
2. gather the prediction csv file   
  `nohup bash $GDR/bash_scripts/run_predict_score_BROKEN_2.sh &`
<br>

For results analysis and molecular docking calculatios, only description 
and sample files are provided, see below.

### Prepare the prediction histogram data 

Now move back to the run\_prediction directory. Launch the bash script to prepare the histogram input file
get\_all\_pds\_avg\_to\_one\_dat\_file.dat:  
   `bash $GDR/bash_scripts/get_all_pds_avg_to_one_dat_file.sh`    
Run the python code the prepare png and eps figures. Please edit the py code to pick A-F or G-K part (default is A-F):    
   `python3 $GDR/python_codes/make_pds_avg_graph_histogram_csv_bar.py`
<br>

### Analysis of hit candidates 

To get the hit candidates according to PDS<sub>avg</sub> you have to run in each xyz\_L\_predict dirctory the python code:   
   `python3 $GDR/python_codes/best_predict_3_avg.py`  
Note that you may want to set the threshold to your convenience: 'ds\_lim'.  
To obtain the list of hit candidates for further mol2 file extraction (and
subsequent docking) run:   
   ` python3 $GDR/python_codes/make_pds_VinaAD_results_2_pds10_5000.py`
to prepare the file X\_comparison\_pds10\_scores\_5000.csv with file tag
(mol2.gz \_ ZINC15 label \_ compound order).   
This file is later processed in mol2\_L\_avg3PDS10\_dock directory to obtain the mol2 files of hit candidates
for a further validation via molecular docking:   
  `mkdir mol2_L_avg3PDS10_dock`    
  `cd mol2_L_avg3PDS10_dock`    
  `ln -s ../X_comparison_pds10_scores_5000.csv`    
   `python3 $GDR/python_codes/make_best_mol2_for_dock10_2.py X_comparison_pds10_scores_5000.csv L > X_comparison_pds10_scores_5000.out &`   
with `L` being the letter A-K of the current directory. Now you have gathered the mol2 files so you
can now do the molecular docking calculation. Herein,...
<br>

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

### Environment variables 

Set your `GIGADOG_ROOT = GDR` variable!  
For instance, create a file, named GDR.s, with:  
  `GIGADOG_ROOT=/path/to/the/directory/GIGADOG`  
  `GDR=$GIGADOG_ROOT`  
  `export GDR`  
Activate the GDR variable via command:  
  `source GDR.s`   
You are done with the environment!

### The SchNet models of J. Matúška [1,2,3]

Please install the code and edit the bash\_scripts/run\_predict\_score\_prototype.sh 
according to your needs,   
see: <a> https://github.com/j-matuska/schnet_hyperparameters_optimization </a>

### python3 / bash / slurm

[comment]: # (pip3 install -r requirements.txt)
Essetially you need RDkit, but you better grep "import" in the python files!   
In addition, take care of the python3 environment. In the our case we do "activate" our python environment
in the bash scripts.
<br>

Bash scripts are using standard commands so nothing special should be needed!  
<br>

We rely on the sbatch of slurm, if you are using a different batch scheduler you need to adapt the code!
