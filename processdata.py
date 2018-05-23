import sys
import csv
import ntpath
import collections


# TODO: Add several sets of ROIs
# Eg: processdata <file> 20,30,40 80,90,100,110
# Makes a two window set with ch 20-30 and ch 30-40 and a three window set with ch 80-90, ch 90-100 and ch 100-110
# These should be named ROI_01_1, ROI_01_2, ROI_02_1 etc.
# Possible to name ROIS on command line: 
# Eg: processdata <file> 20,30,40,R1 80,90,100,110,R2
# These should be named R1_1, R1_2, R2_1 etc.

def tree():
    return collections.defaultdict(tree)
    # Makes handling of multidimentional dicts easier

rois=tree()

if len(sys.argv)==1:
    print("Oppgi fil som skal prosseseres - første og siste kanal")
    sys.exit(1)
    
readfile=sys.argv[1]
if len(sys.argv)>2:
    firstch=int(sys.argv[2])
else:
    firstch=0
if len(sys.argv)>3:
    lastch=int(sys.argv[3])
else:
    lastch=1023

roiname="_".join(["ROI",str(firstch),str(lastch)])
rois[roiname]=[firstch,lastch]

    

print(firstch,lastch)
basename=ntpath.basename(readfile)
writefile="proc_"+str(firstch)+"_"+str(lastch)+"_"+basename
print("Reading: "+basename)
print("Writing: "+writefile)
lnr=0
ch00=-1
wf=None
with open(readfile) as rf:
    reader = csv.reader(rf, delimiter=",")
    for i, line in enumerate(reader):
        lnr=lnr+1
        if lnr==3:
            ch00=line.index("Ch_00")
            lonix=line.index("Long")
            latix=line.index("Lat")
            altix=line.index("Alt[m]")
            wf=open(writefile,"w")
            header="lat,lon,alt"
            roilist=",".join(rois.keys())
            wf.write(header+","+roilist+"\n")
        if lnr>3:
        #TODO: Use rois[] to get firstch and lastch
            data=list(map(int,line[ch00+firstch:ch00+lastch+1]))
            wf.write(",".join([line[latix],line[lonix],line[altix],str(sum(data))]))
            wf.write("\n")
wf.close()
#print(file)