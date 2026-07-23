# Authors: Adriana Dunarova and Lukas Bucinsky
# python codes for ZINC15 docking score prediction and evaluation
# Diploma thesis of Adriana Dunarova 
# 2023, Bratislava, STU

# import modules with functions and all the staff
import os
import sys
import gzip
import shutil
import pathlib

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors 

# our functions:

# https://www.mail-archive.com/rdkit-discuss@lists.sourceforge.net/msg01510.html
# Uwe Hoffmann Fri, 18 Feb 2011 15:12:41 -0800 
# Re: [Rdkit-discuss] Read MULTIPLE molecules from a mol2 file
def RetrieveMol2Block(fileLikeObject, delimiter="@<TRIPOS>MOLECULE"):
    """generator which retrieves one mol2 block at a time
    """
    mol2 = []
    for line in fileLikeObject:
        if line.startswith(delimiter) and mol2:
            yield "".join(mol2)
            mol2 = []
        mol2.append(line)
    if mol2:
        yield "".join(mol2)

# https://www.mail-archive.com/rdkit-discuss@lists.sourceforge.net/msg01510.html
# Uwe Hoffmann Fri, 18 Feb 2011 15:12:41 -0800 
# Re: [Rdkit-discuss] Read MULTIPLE molecules from a mol2 file
def rdkit_process_mol2_gz_file(mol2_gz_file):

    # not needed:
    #import sys
    #import rdkit.Chem.Descriptors as descr
    #from rdkit.Chem import Descriptors
    
    #
    src=mol2_gz_file
    dst=mol2_gz_file.split("/")[-1]
    mol2_file=dst[:-3]  
    #print(src,dst,mol2_file)

    shutil.copy2(src, dst)
    #with gzip.open(dst, 'rb') as file_in:
    #    with open(mol2_file, 'wb') as file_out:
    with gzip.open(dst, 'rb') as file_in:
        with open(mol2_file, 'wb') as file_out:
            try:  
               shutil.copyfileobj(file_in, file_out)
            except:
               return 0 # we will find broken mol2 files 
            #print('example.json file created')
        file_out.close()
    file_in.close()    
    
    names=[]
    #with gzip.open(dst,'rb') as fi0:
    with open(mol2_file,'r') as fi:
        for mol2 in RetrieveMol2Block(fi):
            #mol = rdkit.Chem.MolFromMol2Block(mol2)
            #mol = Chem.MolFromMol2Block(mol2)
            #try:
            #   mol = Chem.MolFromMol2Block(mol2)
            #except:
            #   mol = Chem.MolFromMol2Block(mol2,sanitize=False)

            #check whether things works
            #name=mol.GetProp("_Name")
            #names.append(name)
            names.append(0)
            #NA=mol.GetNumAtoms()
            #MW=Descriptors.MolWt(mol)
            #print(name,NA,MW)
    
    n_mol2=len(names)
    os.remove(dst)
    os.remove(mol2_file)

    return n_mol2

# we loop through a list of mol2 files to read them
def process_mol2_files_to_single_xyz(names_mol2,DS):

    xyz_file="best_DS.xyz"
  
    ms=[]
    # we need to loop through the names_mol2
    for name in names_mol2:
        mol2_file=name+".mol2"
        with open(mol2_file,'r') as fi:
            for mol2 in RetrieveMol2Block(fi):
                mol = Chem.MolFromMol2Block(mol2,removeHs=False) #we need write removeHs because in xyz file we don't have hydrogens)
                ms.append(mol)       

    write_xyz_from_ms2(ms,names_mol2,DS,xyz_file)
    
    return 0

# we loop through a list of mol2 files to read them
# but we also check subdirs to find the very specific file
def process_mol2_files_to_single_xyz_v2(names_mol2,DS):

    xyz_file="best_DS.xyz"
    ms=[]
    
    p=pathlib.Path(".")
    print()
    
    # we need to loop through the names_mol2
    #for name in names_mol2:
    #    mol2_file_name=name+".mol2"
    #    for f in p.rglob(mol2_file_name):
    #        mol2_file=f
    #    print(f)
    
    mol2_index={}
    for f in p.rglob("*.mol2"):
        mol2_index[f.name] = f
    # Process only required mol2 files using fast lookup
    for name in names_mol2:
        mol2_file = mol2_index[name + ".mol2"]

        with open(mol2_file,'r') as fi:
            for mol2 in RetrieveMol2Block(fi):
                mol = Chem.MolFromMol2Block(mol2,removeHs=False) #we need write removeHs because in xyz file we don't have hydrogens)
                ms.append(mol)
        #break        

    write_xyz_from_ms2(ms,names_mol2,DS,xyz_file)
    
    return 0

# https://www.mail-archive.com/rdkit-discuss@lists.sourceforge.net/msg01510.html
# Uwe Hoffmann Fri, 18 Feb 2011 15:12:41 -0800 
# Re: [Rdkit-discuss] Read MULTIPLE molecules from a mol2 file
def rdkit_process_mol2_gz_file_to_xyz(mol2_gz_file):

    # not needed:
    #import sys
    #import rdkit.Chem.Descriptors as descr
    #from rdkit.Chem import Descriptors
    
    #
    src=mol2_gz_file
    dst=mol2_gz_file.split("/")[-1]
    mol2_file=dst[:-3]  
    xyz_file=mol2_file[:-4]+"xyz"  
    #print(src,dst,mol2_file,xyz_file)

    shutil.copy2(src, dst)
    try:
       with gzip.open(dst, 'rb') as file_in:
          with open(mol2_file, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
            #print('example.json file created')
          file_out.close()
       file_in.close()    
    except(OSError, ValueError):
       print("ERROR XXX mol2.gz FAIL:", file_in) 
    
    ms=[]
    names=[]
    #with gzip.open(dst,'rb') as fi0:
    with open(mol2_file,'r') as fi:
        for mol2 in RetrieveMol2Block(fi):
            #mol = rdkit.Chem.MolFromMol2Block(mol2)
            #mol = Chem.MolFromMol2Block(mol2)
            mol = Chem.MolFromMol2Block(mol2,removeHs=False)
            ms.append(mol)        

            #check whether things works
            name=mol.GetProp("_Name")
            names.append(name)
            #NA=mol.GetNumAtoms()
            #MW=Descriptors.MolWt(mol)
            #print(name,NA,MW)
    
    write_xyz_from_ms(ms,xyz_file)
    n_mol2=len(names)
    os.remove(dst)
    os.remove(mol2_file)

    return n_mol2

def write_xyz_from_ms2(ms,names_mol2,DS,xyz_file):

    # content of the xyz file
    xyz_content=[]
    
    for imol,mol in enumerate(ms):

       # get charge ? according to the gz file name !!!
       LCH0=names_mol2[imol].split("_")[0]
       LCH=LCH0.split(".")[0][-1]
       charge=ord(LCH)-ord("N") 
       #charge=0

       # get name
       name=names_mol2[imol]
       
       # get number of atoms
       NA=mol.GetNumAtoms()
       xyz_content.append(str(NA)+"\n")

       # get docking score
       score=DS[imol]

       # make the comment line
       
       # the second xyz file line contains the following info:
       # Properties=species:S:1:pos:R:3 pbc="F F F" name=ZINC000245189325_0 energy=5000.0 charge=-1
       comment_line='Properties=species:S:1:pos:R:3 pbc="F F F" name='
       comment_line+=name+' energy='+str(score)+' charge='+str(charge)
       xyz_content.append(comment_line+"\n")

       # here we writ the element symbol an coordinates
       for i, atom in enumerate(mol.GetAtoms()):
           #positions = mol.GetConformer().GetAtomPosition(i)
           #print(atom.GetSymbol(), positions.x, positions.y, positions.z)
           pos = mol.GetConformer().GetAtomPosition(i)
           #print(atom.GetSymbol(), pos.x, pos.y, pos.z)
           atom_line=str(atom.GetSymbol())+" "+str(pos.x)+" "+str(pos.y)+" "+str(pos.z)
           xyz_content.append(atom_line+"\n")

    f = xyz_file
    w = open(f,"w")
    #w = Chem.SDWriter(f)
    for line in xyz_content:
        w.write(line)
    w.close()
    #print()
    xyz_content.clear()

    return 0

# on input: molecule objects of rdkit (ms), on output an sdf file 
def write_xyz_from_ms(ms,xyz_name):
    
    xyz_content=[]
    
    # get charge as the last character of the xyz_name, where N is a neutral charge
    # ABACMN.xaa.xyz we need ABACMN and the last character N actually
    LCH=xyz_name.split(".")[0][-1]
    #print(LCH,ord(LCH),ord(LCH)-ord("N"))
    #just a formal charge according to the file name
    charge=ord(LCH)-ord("N") 

    for mol in ms:

       #print(mol.GetProp("_Name"))
       name=mol.GetProp("_Name")
       #print(Chem.MolToSmiles(mol))
       #print(mol.GetNumAtoms())
       #charge = Chem.GetFormalCharge(mol)
       #print(charge)
    #no extra charges in sdf since open babel complex
    #pyMP = AllChem.MMFFGetMoleculeProperties(mol)
    #Gasteiger charegs ???
    #for i in range(mol.GetNumAtoms()):
    #   mol.GetAtomWithIdx(i).SetProp('molFileAlias', '{0:.4f}'.format(pyMP.GetMMFFPartialCharge(i)))
    #   print(mol.GetAtomWithIdx(i).GetSymbol(),pyMP.GetMMFFPartialCharge(i))
    #w = Chem.SDWriter(sys.stdout)
        
       #for i in range(mol.GetNumAtoms()):
       #    at = mol.GetAtomWithIdx(i).GetSymbol()
       #    pos = mol.GetConformer().GetAtomPosition(i)
       #    print(at,pos.x,pos.y.pos.z)
       
       # the first xyz file line contains the number of atoms
       NA=mol.GetNumAtoms()
       xyz_content.append(str(NA)+"\n")
       
       # the second xyz file line contains the following info:
       # Properties=species:S:1:pos:R:3 pbc="F F F" name=ZINC000245189325_0 energy=5000.0 charge=-1
       comment_line='Properties=species:S:1:pos:R:3 pbc="F F F" name='
       comment_line+=name+' energy=5000.0 charge='+str(charge)
       xyz_content.append(comment_line+"\n")

       # here we writ the element symbol an coordinates
       for i, atom in enumerate(mol.GetAtoms()):
           #positions = mol.GetConformer().GetAtomPosition(i)
           #print(atom.GetSymbol(), positions.x, positions.y, positions.z)
           pos = mol.GetConformer().GetAtomPosition(i)
           #print(atom.GetSymbol(), pos.x, pos.y, pos.z)
           atom_line=str(atom.GetSymbol())+" "+str(pos.x)+" "+str(pos.y)+" "+str(pos.z)
           xyz_content.append(atom_line+"\n")

    f = xyz_name
    w = open(f,"w")
    #w = Chem.SDWriter(f)
    for line in xyz_content:
        w.write(line)
    w.close()
    #print()
    xyz_content.clear()

    return 0

# on input: molecule object of rdkit (ms), on output an sdf file 
def write_data_from_ms(ms):
    for mol in ms:

       print(mol.GetProp("_Name"))
       name=mol.GetProp("_Name")
       print(Chem.MolToSmiles(mol))
       print(mol.GetNumAtoms())
       charge = Chem.GetFormalCharge(mol)
       print(charge)
    #no extra charges in sdf since open babel complex
    #pyMP = AllChem.MMFFGetMoleculeProperties(mol)
    #Gasteiger charegs ???
    #for i in range(mol.GetNumAtoms()):
    #   mol.GetAtomWithIdx(i).SetProp('molFileAlias', '{0:.4f}'.format(pyMP.GetMMFFPartialCharge(i)))
    #   print(mol.GetAtomWithIdx(i).GetSymbol(),pyMP.GetMMFFPartialCharge(i))
    #w = Chem.SDWriter(sys.stdout)
       
       #for i in range(mol.GetNumAtoms()):
       #    at = mol.GetAtomWithIdx(i).GetSymbol()
       #    pos = mol.GetConformer().GetAtomPosition(i)
       #    print(at,pos.x,pos.y.pos.z)
       #for i, atom in enumerate(mol.GetAtoms()):
       #    #positions = mol.GetConformer().GetAtomPosition(i)
       #    #print(atom.GetSymbol(), positions.x, positions.y, positions.z)
       #    pos = mol.GetConformer().GetAtomPosition(i)
       #    print(atom.GetSymbol(), pos.x, pos.y, pos.z)
           
       #f=name+".sdf"
       #w = Chem.SDWriter(f)
       #w.write(mol)
       #w.close()
       #print()
    return 0

if __name__ == '__main__':
    print("This is rdkit_mol2_gz.py")
