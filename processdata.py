import sys
import csv
import ntpath
import collections
import datetime

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
args=sys.argv[2:]
for arg in sys.argv[2:]:
    print(arg)
    if ":" in arg:
        chs=arg.split(":")
        try:
            roiname = int(chs[0])
            roiname="_".join(["ROI",chs[0],chs[1]])
        except ValueError:
            roiname=chs.pop(0)
        print(roiname)
        rois[roiname]=[int(chs[0]),int(chs[1])]
        
#else:
if False:
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

    
for roi in rois:
    print(roi,rois[roi])
basename=ntpath.basename(readfile)
timestamp=datetime.datetime.now().strftime("%y%m%d_%H%M%S")
writefile="proc_"+timestamp+"_"+basename
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
            roivalues=[]
        #TODO: Use rois[] to get firstch and lastch
            for roiname in rois:
                roi=rois[roiname]
                roivalue=sum(list(map(int,line[ch00+roi[0]:ch00+roi[1]+1])))
                roivalues.append(str(roivalue))
            wf.write(",".join([line[latix],line[lonix],line[altix],",".join(roivalues)]))
            wf.write("\n")
wf.close()
#print(file)