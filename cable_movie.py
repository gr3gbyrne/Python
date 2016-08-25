import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import sys

   
# initialization function: plot the background of each frame
def init():
    timetext.set_text("initial")
    Utext.set_text("initial")
    Vtext.set_text("initial")
    cable.set_data([], [])
    buoys.set_data([], [])
    track.set_data([], [])
    return cable, buoys, track,
 
def animate(i):

    global Nfiles
    global buoy_dataX
    global buoy_dataY

    filename_suffix="dat"
    basefilename = "cable_data_%05d" % (i)
    filename=os.path.join(directory, basefilename + "." + filename_suffix)
    
    print filename
    
    d = np.loadtxt(filename, skiprows=0)
    U = d[0,0]
    V = d[0,1]
    #mag = np.sqrt(U**2 + V**2)
    label = "t=%.2f (s)" % (d[1,0])
    timetext.set_text(label)
    label = "U=%.2f (m/s)" % (U)
    Utext.set_text(label)
    label = "V=%.2f (m/s)" % (V)
    Vtext.set_text(label)
     
    d = np.loadtxt(filename, skiprows=2)

    # buoy locations
    xb=[d[0,0],d[-1,0]]
    yb=[d[0,1],d[-1,1]]

    buoy_dataX.append(xb[1])
    buoy_dataY.append(yb[1])
    
    if i > 8 :
        del buoy_dataX[0]
        del buoy_dataY[0]

    # Plot buoy track (green)
    track.set_data(buoy_dataX,buoy_dataY)
    
    # Plot buoys (red)
    buoys.set_data(xb,yb)
    
    # Plot cable (black)
    cable.set_data(d[:,0],d[:,1])

    zmin=min(d[:,1])-1
    
    xmin=min(d[:,0])-3
    xmax=max(d[:,0])+3
          

    axes.set_xlim([xmin,xmax])
    axes.set_ylim([-24,2])
    
    fig.canvas.draw()
    return cable, buoys, track,


################# MAIN #####################


if len(sys.argv)==1:
    name = sys.argv[0].split("/")[-1]
    print "\n\n\t-------------------------------------------"
    print "\tThis script creates a movie using a set of" 
    print "\tASCII files containing cable position and"
    print "\tvelocity data"
    print "\n\tGreg Byrne, Metron Inc. 2016"
    print "\t-------------------------------------------"
    print "\n\tUsage:"
    print "\t{0} <directory containing data files>".format(name)
    print "\n\tExample:"
    print "\t{0} /home/byrne/CableData/\n\n".format(name)
    exit(0)

directory = sys.argv[1]
    
isfile = os.path.isfile
join = os.path.join

#directory = '/media/byrne/4CBC-C118/ms3/trunk/projects/cable_dynamics/Data/'
number_of_files = sum(1 for item in os.listdir(directory) if isfile(join(directory, item)))

Nfiles = number_of_files
buoy_dataX = []
buoy_dataY = []

# set up figure
fig = plt.figure(facecolor="white")
ax  = plt.axes()
#ax.xaxis.set_visible(False)
plt.tick_params(labelsize=20)
axes = plt.gca()
plt.tick_params(axis='x',top='off',bottom='off',labelbottom='off')
axes.set_ylabel('Y',fontsize=30)
axes.set_xlabel('X',fontsize=30)

fig = mpl.pyplot.gcf()
fig.set_size_inches(12, 7.5, forward=True)

# Plot water line (blue)
plt.axhline(y=0.1,linewidth=5, color='b',alpha=0.5)
    
cable, = ax.plot([], [], 'k-' , lw='7')
buoys, = ax.plot([], [], 'ro' , markersize=30)
track, = ax.plot([], [], 'g--', lw='3')

timetext = ax.text(0.45,1.02,"",transform=ax.transAxes,fontsize=27) 
Utext    = ax.text(0.8,0.85,"",transform=ax.transAxes,fontsize=17) 
Vtext    = ax.text(0.8,0.81,"",transform=ax.transAxes,fontsize=17) 

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=Nfiles, interval=20, blit=True)
anim.save('cable_animation.wmv', fps=5)
#anim.save('cable_animation.mp4', fps=5, extra_args=['-vcodec', 'libx264'])

