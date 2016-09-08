import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import matplotlib.patches as patches
import sys

   
# initialization function: plot the background of each frame
def init():
    cable.set_data([], [])
    buoys.set_data([], [])
    return cable, buoys, 
 
def animate(i):

    #global Nfiles
    #global buoy_dataX
    #global buoy_dataY

    filename_suffix="dat"
    basefilename = "steadyCableSol_%05d" % (i)
    filename=os.path.join(cabledirectory, basefilename + "." + filename_suffix)
    
    print filename

    # set the date
    label = "%d-%d-%d  %02d:%02d:%02d" % (datetime[i,1],datetime[i,2],datetime[i,0],datetime[i,3],datetime[i,4],datetime[i,5])
    datetext.set_text(label)


    d = np.loadtxt(filename, skiprows=0)
    # downsample array.  Notation is equivalent to print(d[0:d.size:5])
    d = d[::5]
    
    # buoy locations
    xb=[d[0,0],d[-1,0]]
    yb=[d[0,1],d[-1,1]]

    # Plot buoys (red)
    buoys.set_data(xb,yb)
    
    # Plot cable (black)
    cable.set_data(d[:,0],d[:,1])

    # Plot current profile (blue)
    filename_suffix="dat"
    basefilename = "current_data_%04d" % (i+1)
    filename=os.path.join(currentdirectory, basefilename + "." + filename_suffix)
    d = np.loadtxt(filename, skiprows=0)
    # Rescale current [0,2] to X range
    d[:,1]= [(m*x) + xmin for x in d[:,1]]
    pts=np.column_stack((d[:,1],-d[:,0]))
    a = np.array([ [xmin, 0], [d[1,1], 0] ])
    pts=np.concatenate((a,pts), axis=0)
    a = np.array([ [d[-1,1],zmin], [xmin,zmin] ])
    pts=np.concatenate((pts,a), axis=0)
    go.set_xy(pts)
    patch=ax.add_patch(go)

    fig.canvas.draw()
    return cable, buoys, patch,


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
    print "\t{0} <directory containing cable profiles>,<directory containing current profiles>,<file containing timestamp information>".format(name)
    print "\n\tExample:"
    print "\t{0} /home/byrne/CableData/ /home/byrne/Currents/ /home/byrne/timedata/timestamps.dat\n\n".format(name)
    exit(0)

cabledirectory    = sys.argv[1]
currentdirectory  = sys.argv[2]  
timestampfile     = sys.argv[3] 

#if len(sys.argv)==3:
#sys.exit()

isfile = os.path.isfile
join = os.path.join
filename_suffix="dat"

Nfiles = sum(1 for item in os.listdir(cabledirectory) if isfile(join(cabledirectory, item)))
#Nfiles=30
buoy_dataX = []
buoy_dataY = []

# set up the figure
fig = plt.figure(facecolor="white")
ax  = plt.axes()
axes = plt.gca()
plt.tick_params(labelsize=20)
axes.set_xlabel('X (m)',fontsize=30)
axes.set_ylabel('Depth (m)',fontsize=30)
zmin=-2800; 
zmax=150;
xmin=-500; 
xmax=50;
axes.set_xlim([xmin,xmax])
axes.set_ylim([zmin,zmax])

# Set up velocity axis at the top
ax2 = ax.twiny()
ax2.set_xlabel("Current |V| (m/s)",fontsize=20)
ax2.xaxis.set_label_coords(0.35, 1.08)
plt.tick_params(labelsize=20)
ax2.set_xlim([xmin,xmax])
m=abs(xmin)/2.0
xr=range(xmin,-50,50)
xl=[(x/m)+2 for x in xr]
xl=["%.2f" % x for x in xl]
ax2.set_xticks(xr)
ax2.set_xticklabels(xl)

fig = mpl.pyplot.gcf()
fig.set_size_inches(12, 8, forward=True)

# Plot water line (blue)
plt.axhline(y=0.1,linewidth=5, color='b',alpha=0.5)
    
# Plot objects
cable, = ax.plot([], [], 'k-' , lw='7')
buoys, = ax.plot([], [], 'ro' , markersize=30)

# Plot current profile
basefilename = "current_data_%04d" % (0)
filename=os.path.join(currentdirectory, basefilename + "." + filename_suffix)
d = np.loadtxt(filename, skiprows=0)
# Rescale current [0,2] to X range
d[:,1]= [(m*x) + xmin for x in d[:,1]]
pts=np.column_stack((d[:,1],-d[:,0]))
#a = np.array([[xmin,-d[-1,0]], [xmin, -d[0,0]]])
a = np.array([ [xmin, 0], [d[1,1], 0], [xmin,zmin], [d[-1,1],zmin] ])
pts=np.concatenate((pts, a), axis=0)
go= patches.Polygon(pts,closed=True, fc='b', ec='k',alpha=0.5)
patch=ax.add_patch(go)
    

# datetext
#timestampfile="/home/byrne/CableDynamics/ExpData/deployment1_mooring1/datetime/datetime.dat"

datetime = np.loadtxt(timestampfile, skiprows=0)
datetext = ax.text(0.85,1.08,"",transform=ax.transAxes,fontsize=17) 

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=Nfiles, interval=20, blit=True)
anim.save('cable_animation.wmv', fps=3,codec="libx264")

