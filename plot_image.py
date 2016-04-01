#!/usr/bin/python
import sys
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import math

# parse input file
def parse(filename,column):
    
    data = []
    for line in open(filename).readlines():
        d = line.split()
        data.append( float(d[column]) )
    
    return data

#Argument parsing
if len(sys.argv)==1:
    name = sys.argv[0].split("/")[-1]
    print "Usage:"
    print "{0} <column> <filename> ".format(name)
    print "\nExample:"
    print "{0} 2 myfile.dat".format(name)
    exit(0)

filename = sys.argv[2]
columnread= sys.argv[1]
imagedata=parse(filename,2)
imagedata=np.array(imagedata)

N=math.sqrt(len(imagedata))
imagedata=np.reshape(imagedata,(N,N))
imagedata=np.log10(imagedata)

fig = plt.figure(2)
cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['blue','black','red'],
                                           256)
img2 = plt.imshow(imagedata,interpolation='nearest',
                    cmap = cmap2,
                    origin='lower')

#v = np.linspace(0, N-1, 6,endpoint=True)
#plt.xticks(v)
#plt.yticks(v)
plt.xlabel('$N_x$',{'fontsize':35})
plt.ylabel('$N_y$',{'fontsize':35})
plt.tick_params(axis='both', which='major', labelsize=25)

v = np.linspace(0, max(imagedata.flatten()), 6,endpoint=True)
cbaxes = fig.add_axes([0.82, 0.1, 0.03, 0.8]) #[left,bottom,width,height] 
cb=plt.colorbar(img2,cmap=cmap2,cax=cbaxes,ticks=v)
cb.ax.tick_params(labelsize=25) 
cb.set_label(label='$\mathrm{log_{10}( T )}$',size=35,weight='bold')

fig.savefig("image.png",
            bbox_inches='tight', 
            transparent=True,
            pad_inches=0)
