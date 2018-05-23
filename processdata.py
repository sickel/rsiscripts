import sys
import csv
import ntpath

if len(sys.argv)<4:
    print("Oppgi fil som skal prosseseres - første og siste kanal")
    sys.exit(1)
    
readfile=sys.argv[1]
firstch=int(sys.argv[2])
lastch=int(sys.argv[3])
print(firstch,lastch)
basename=ntpath.basename(readfile)
writefile="proc_"+str(firstch)+"_"+str(lastch)+"_"+basename
print(basename)
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
            print(ch00,latix,lonix,altix)
            wf=open(writefile,"w")
            wf.write("lat,lon,alt,Ch_"+str(firstch)+"_"+str(lastch)+"\n")
        if lnr>3:
            data=list(map(int,line[ch00+firstch:ch00+lastch+1]))
            wf.write(",".join([line[latix],line[lonix],line[altix],str(sum(data))]))
            wf.write("\n")
wf.close()
#print(file)