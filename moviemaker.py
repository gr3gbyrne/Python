#!/usr/bin/python
import sys 
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import math
import os

from scipy import integrate
from matplotlib import animation
 
# parse input file
def readData(filename,column):
    
    data = []
    for line in open(filename).readlines():
        d = line.split()
        data.append( float(d[column]) )
    
    return data

def gendatafiles(filename,Nfiles):
    string=filename.split(".")
    index=int(string[1])
    filenames = [ ];
    for i in xrange(index,index+Nfiles):
        tmp = "%s.%05d.dat" % (string[0],i)
        filenames.append( tmp )

    return filenames


#################################################
#Argument parsing
if len(sys.argv)==1:
    name = sys.argv[0].split("/")[-1]
    print "Usage:"
    print "{0} <column> <Nfiles> <filename> ".format(name)
    print "\nExample:"
    print "{0} 2 100 myfile.dat".format(name)
    exit(0)
 


###os.system("cd ")

columnread = sys.argv[1];
Nfiles     = int(sys.argv[2]);
filename   = sys.argv[3];

fileNames=gendatafiles(filename,Nfiles)

ims=[]
fig = plt.figure()
filedir="../../data/movie"

for filename in fileNames:
    
    # convert .bin files to ascii.dat
    string=filename.split(".")
    ftmp="%s.%s.bin" % (string[0],string[1])
    cmd = "./%s/convertbin2ascii -i %s/%s" % (filedir,filedir,ftmp)
    os.system(cmd)
    
    imagedata=readData("asciifile.dat",2)
    imagedata=np.array(imagedata)
    N=math.sqrt(len(imagedata))
    imagedata=np.reshape(imagedata,(N,N))
    im = plt.imshow(imagedata,
                    interpolation='nearest',
                    cmap = 'jet',
                    origin='lower', 
                    animated=True)
    plt.axis("off")
    im.axes.get_xaxis().set_visible(False)
    im.axes.get_yaxis().set_visible(False)
    
    ims.append([im])
    
    ftmp="%s.%s.png" % (string[0],string[1])
    fig.savefig(ftmp,
                bbox_inches='tight',
                pad_inches=0)
    cmd="convert %s %s.%s.gif" % (ftmp,string[0],string[1])
    os.system(cmd)

    


# Create animated gif
os.system("convert -delay 30 -resize 50% -loop 1 *.png animation.gif")

# Create mp4
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)
ani.save('animation.mp4',writer='mencoder',fps=15)

# Clean up
os.system("rm karma*")
os.system("rm *.dat")

#plt.show()

