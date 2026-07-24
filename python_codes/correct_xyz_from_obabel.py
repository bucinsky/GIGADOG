# import modules
import sys

# MAIN
if __name__ == "__main__":
    
    file_xyz0=sys.argv[1]
    with open(file_xyz0,'r') as f0:
        content0=f0.readlines()
    f0.close()
    
    LCH=file_xyz0.split(".")[0][-1]
    charge=ord(LCH)-ord("N") 
    content=[]
    for line in content0:
        if 'ZINC' in line:
          name=line.strip()
          comment_line='Properties=species:S:1:pos:R:3 pbc="F F F" name='
          comment_line+=name+' energy=5000.0 charge='+str(charge)
          content.append(comment_line+"\n")
        else:
          content.append(line)

    file_xyz=file_xyz0[:-4]+'xyz'
    w = open(file_xyz,"w")
    for line in content:
        w.write(line)
    w.close()


