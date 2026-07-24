
# import modules
import glob
import pandas as pd


def get_pds_Vina_dirs():
    dirs=sorted(glob.glob('xyz_*_predict'))
    return dirs

def get_fdat(fdat):

    df = pd.read_csv(fdat,sep=";",comment="#")
    data = df.values.transpose()
    avgs=[]
    for d1,d2,d3,d4,d5 in zip(data[2],data[3],data[4],data[5],data[6]):
        a=d1+d2+d3+d4+d5
        a=a/5.0
        avgs.append(a)

    names=[]
    for i,d0 in enumerate(data[0]):
        name=data[0][i]+"_"+data[1][i]+"_"+str(data[7][i])
        names.append(name)
    
    return names,avgs

def make_csv_file_5000(fcsv,names,avgs,ds_value=5000):
    data = {
       'name':names,
       'avg_pds':avgs,
       'DS_5000':ds_value}
    
    df = pd.DataFrame(data)
    df.to_csv(fcsv,index=False,sep=";")

    return 0

# MAIN
if __name__ == "__main__":
    
    # input file
    ndat="best_pds_3_avg_10.dat"

    # output file
    ncsv="X_comparison_pds10_scores_5000.csv"
    
    # get folder names with VinAD docking results
    pds_VinaAD_dirs=get_pds_Vina_dirs() 
    print(pds_VinaAD_dirs)
    print()
    
    all_names=[]
    all_avgs=[]

    for ndir in pds_VinaAD_dirs:
        L=ndir.split("_")[1]
        print(ndir,":",L)

        #read best_pds_3_avg_10.dat
        #zinc15_file;name;01;02;03;04;05;#order
        #BCADRP.xaa;ZINC000906518870;-9.08425;-9.63204;-8.944895;-8.928605;-8.479963;24211
        fdat=ndir+"/"+ndat
        xdat_names,xavgs=get_fdat(fdat)

        all_names.extend(xdat_names)
        all_avgs.extend(xavgs)
    
    # make csv with all compounds
    make_csv_file_5000(ncsv,all_names,all_avgs,ds_value=5000)

    exit ()
