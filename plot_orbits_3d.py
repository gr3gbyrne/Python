#!/usr/bin/python
 
import numpy as np
from scipy import integrate
import sys
 
import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
 
def parse(fdata,columns):
 
    data = []
    for line in open(fdata).readlines():
        d = line.split()
        data.append( [float(d[c]) for c in columns] )
 
    return data
 
#Argument parsing
if len(sys.argv)==1:
    name = sys.argv[0].split("/")[-1]
    print "Usage:"
    print "{0} <#x,#y,#z> <trajectory file 1> ... <trajectory file N>".format(name)
    print "\nExample:"
    print "{0} 1,2,3 popath.dat".format(name)
    exit(0)
 
cols = map(int,sys.argv[1].split(","))
if len(cols)!=3:
    print "Expected 3 columns for x,y,z coordinates."
    exit(0)
 
dataFiles = sys.argv[2:]#["popath.dat","shadow.dat"]
 
 #Data parsing
dat=parse(dataFiles[0],[0])
dat=np.array(dat)
Torbit=dat[-1]-dat[0]

x_t = [parse(dataFile,cols) for dataFile in dataFiles]
x_t = np.array(x_t)
 
N_trajectories = x_t.shape[0]
 
# Set up figure & 3D axis for animation
fig = plt.figure(facecolor="white")
ax = fig.add_axes([0.05, 0.05, 0.9, 0.9], projection='3d')
timetext = ax.text2D(0.07,0.82,"",transform=ax.transAxes) 

# choose a different color for each trajectory
#colors = ["red","blue"]
#From http://paletton.com/
#colors = ["#413075","#A8AA39"]
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))
 
# set up lines and points
lines = sum([ax.plot([], [], [], '-',alpha=0.35, c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])
 
# prepare the axes limits
ax.set_xlim(x_t[:,:,0].min()*0.9,x_t[:,:,0].max()*1.1)
ax.set_ylim(x_t[:,:,1].min()*0.9,x_t[:,:,1].max()*1.1)
ax.set_zlim(x_t[:,:,2].min()*0.9,x_t[:,:,2].max()*1.1)
 
mpl.rcParams.update({'font.size': 22})
 
ax.text2D(0.85,0.1,r'x(t)',transform=ax.transAxes)
ax.text2D(0.2,0.0,r'x(t+$\tau$)',transform=ax.transAxes)
ax.text2D(-0.02,0.5,r'x(t+2$\tau$)',rotation=90,transform=ax.transAxes)
 
# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 30)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])
 
        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts
 
# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    i = (3 * i) % x_t.shape[1]
    global Torbit

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)
 
        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])
 
        label = "P%.1f periodic orbit\nt=%.2f (s)" % (Torbit,i*(1./30.))
        timetext.set_text(label)
                
        #clear previous text box
        fig.texts
        for txt in fig.texts:
            txt.set_visible(False)

    fig.canvas.draw()
    return lines + pts
 
# it's time for the animator
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=x_t.shape[1]/3, interval=30, blit=True)
 
# Save as movie. This requires mplayer or ffmpeg to be installed
anim.save('movie.avi',writer="mencoder", fps=15,bitrate=-1)
#plt.show()

label = "P%.1f periodic orbit\n" % (Torbit)
timetext.set_text(label)

plt.savefig('porbit.png', bbox_inches='tight')


