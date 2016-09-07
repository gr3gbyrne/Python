import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import matplotlib.patches as patches
import sys

   
# initialization function: plot the background of each frame
def init():
    #timetext.set_text("initial")
    cable.set_data([], [])
    buoys.set_data([], [])
    return cable, buoys, 
 
def animate(i):

    global Nfiles
    global buoy_dataX
    global buoy_dataY

    filename_suffix="dat"
    basefilename = "steadyCableSol_%05d" % (i)
    filename=os.path.join(directory, basefilename + "." + filename_suffix)
    
    print filename
    
    
    d = np.loadtxt(filename, skiprows=0)
    # downsample array.  Notation is equivalent to print(d[0:d.size:5])
    d = d[::5]
    

    #label = "t=%.2f (s)" % (d[1,0])
    #timetext.set_text(label)
    #d = np.loadtxt(filename, skiprows=2)

    # buoy locations
    xb=[d[0,0],d[-1,0]]
    yb=[d[0,1],d[-1,1]]

    #arrow.xy= (xb[1],yb[1])
    #annotation.xy = (xb[1],yb[1])
    #arrow.set_data("",xy=(0.5,0.5),xytext=(0,0))
    #arrow.set_data(xb[1],yb[1],0.2,0.2)
    #plt.arrow(xb[1],yb[1],0.2,0.2)
    #ax.arrow(0, 0, 0.5, 0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')

    #buoy_dataX.append(xb[1])
    #buoy_dataY.append(yb[1])
    
    #if i > 8 :
    #    del buoy_dataX[0]
    #    del buoy_dataY[0]

    # Plot buoy track (green)
    #track.set_data(buoy_dataX,buoy_dataY)
    
    # Plot buoys (red)
    buoys.set_data(xb,yb)
    
    # Plot cable (black)
    cable.set_data(d[:,0],d[:,1])

    if len(sys.argv)==3:
        filename_suffix="dat"
        basefilename = "current_data_%04d" % (i+1)
        filename=os.path.join(currentdirectory, basefilename + "." + filename_suffix)
        d = np.loadtxt(filename, skiprows=0)
        # Rescale current [0,2] to X range
        d[:,1]= [(m*x) + xmin for x in d[:,1]]
        pts=np.column_stack((d[:,1],-d[:,0]))
        #a = np.array([ [xmin, 0], [d[1,1], 0], [xmin,zmin], [d[-1,1],zmin] ])
        a = np.array([ [xmin, 0], [d[1,1], 0] ])
        pts=np.concatenate((a,pts), axis=0)
        a = np.array([ [d[-1,1],zmin], [xmin,zmin] ])
        pts=np.concatenate((pts,a), axis=0)
        #print pts
        #stop
        #d1=np.array([d[:,1],-d[:,0]]);
        #current.set_data(d[:,1],-d[:,0])
        #pts[:,0]+=i
        
        go.set_xy(pts)
        patch=ax.add_patch(go)

    #print d[:,1]
    #stop

    #zmin=min(d[:,1])-1
    
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
    print "\t{0} <directory containing data files>".format(name)
    print "\n\tExample:"
    print "\t{0} /home/byrne/CableData/\n\n".format(name)
    exit(0)

directory = sys.argv[1]

if len(sys.argv)==3:
    currentdirectory=sys.argv[2]    

isfile = os.path.isfile
join = os.path.join
filename_suffix="dat"

#directory = '/media/byrne/4CBC-C118/ms3/trunk/projects/cable_dynamics/Data/'
number_of_files = sum(1 for item in os.listdir(directory) if isfile(join(directory, item)))

Nfiles = number_of_files
#Nfiles=200
buoy_dataX = []
buoy_dataY = []

# set up figure
fig = plt.figure(facecolor="white")
ax  = plt.axes()
axes = plt.gca()
plt.tick_params(labelsize=20)
axes.set_xlabel('X (m)',fontsize=30)
axes.set_ylabel('Depth (m)',fontsize=30)
zmin=-2800; 
zmax=150;
xmin=-400; 
xmax=50;
axes.set_xlim([xmin,xmax])
axes.set_ylim([zmin,zmax])

ax2 = ax.twiny()
ax2.set_xlabel("Current |V| (m/s)",fontsize=20)
ax2.xaxis.set_label_coords(0.35, 1.08)
plt.tick_params(labelsize=20)
ax2.set_xlim([xmin,xmax])
m=abs(xmin)/2.0
xr=range(-400,-50,50)
xl=[(x/m)+2 for x in xr]
xl=["%.2f" % x for x in xl]
ax2.set_xticks(xr)
ax2.set_xticklabels(xl)


#plt.tick_params(axis='x',top='off',bottom='off',labelbottom='off')

fig = mpl.pyplot.gcf()
fig.set_size_inches(12, 7.5, forward=True)

# Plot water line (blue)
plt.axhline(y=0.1,linewidth=5, color='b',alpha=0.5)
    
# Plot objects
cable, = ax.plot([], [], 'k-' , lw='7')
buoys, = ax.plot([], [], 'ro' , markersize=30)

# Plot current profile
if len(sys.argv)==3:
    #current.set_data(d[:,1],-d[:,0])
    #current, = ax.plot([], [], 'g-' , lw='9', alpha=0.5)
    
    basefilename = "current_data_%04d" % (1)
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
    

#timetext = ax.text(0.45,1.02,"",transform=ax.transAxes,fontsize=27) 

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=Nfiles, interval=20, blit=True)
anim.save('cable_animation.wmv', fps=3,codec="libx264")
# extra_args=['-vcodec', 'libx264'])
#anim.save('cable_animation.mp4', fps=5, codec="libx264")

