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
GIGADOG\_ROOT=/path/to/the/directory/GIGADOG  
GDR=$GIGADOG\_ROOT  
export GDR
Activate the GDR variable via command:  
source GDR.s   
You are done!

## HOT TO CITE

[comment]: # (This may be the most platform independent comment)
Adriána Dunárová, Marián Gall, Ján Matúška, Michal Pitoňák, Marek Štekláč, Lukas Bucinsky.
Machine Learning Prediction of Docking Scores for 616 Million ZINC15 Compounds: Accuracy and Speed vs. Model and Infrastructure.
(2026) _to be submitted_.


## REQUIREMENTS

[comment]: # (pip3 install -r requirements.txt)
Essetially you need RDkit, but you better grep "import" in the python files!  
Bash scripts are using standard commands so nothing special should be needed!

