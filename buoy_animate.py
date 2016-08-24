import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation


isfile = os.path.isfile
join = os.path.join

directory = '/media/byrne/4CBC-C118/ms3/trunk/projects/cable_dynamics/Data/'
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

#plt.setp(ax.get_xticklabels(), visible=False)

fig = mpl.pyplot.gcf()
fig.set_size_inches(12, 7.5, forward=True)

cable, = ax.plot([], [], 'k-' , lw='7')
buoys, = ax.plot([], [], 'ro' , markersize=30)
track, = ax.plot([], [], 'g--', lw='3')
timetext = ax.text(0.45,1.02,"",transform=ax.transAxes,fontsize=27) 

# initialization function: plot the background of each frame
def init():
    timetext.set_text("initial")
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
    label = "t=%.2f (s)" % (d[0,0])
    timetext.set_text(label)
     

    d = np.loadtxt(filename, skiprows=1)

    buoy_dataX.append(d[-1,0])
    buoy_dataY.append(d[-1,1])
    
    if i > 8 :
        del buoy_dataX[0]
        del buoy_dataY[0]

    # Plot buoy track (green)
    track.set_data(buoy_dataX,buoy_dataY)
    
    # Plot water line (blue)
    plt.axhline(y=0.1,linewidth=5, color='b',alpha=0.5)
    
    # Plot buoys (red)
    xb=[d[0,0],d[-1,0]]
    yb=[d[0,1],d[-1,1]]
    buoys.set_data(xb,yb)
    
    # Plot cable (black)
    cable.set_data(d[:,0],d[:,1])

    zmin=min(d[:,1])-1
    xcmin=min(d[:,0])
    xmax=max(d[:,0])+3
    xbmin=min(buoy_dataX)
    values=[xcmin,xbmin]
    index_min = min(xrange(len(values)), key=values.__getitem__)
    if index_min == 0:
        xmin=values[0]-1
    else:
        xmin=values[1]
    
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([-24,2])
    
    fig.canvas.draw()
    return cable, buoys, track,


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=18, interval=20, blit=True)
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

