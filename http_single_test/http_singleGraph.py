import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter

SHOW=False
title="Single HTTP file download test - 120 seconds timeout"
def show_or_save(plt, name):
    if SHOW:
        plt.show()
    else:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(10, 7)
        plt.savefig(name, dpi=100, transparent=True)

def convert_speed(x):
    print("%s  --->  " % x, end='')
    factor=1
    if "KB/s" in x:
        factor=1024
    elif "MB/s" in x:
        factor=1024**2
    elif "GB/s" in x:
        factor=1024**3

    x= float(x.split(" ")[0])*factor

    print(x)
    return x

def convert_time(x):
    print("%s  --->  " % x, end='')
    if "m" in x and "s" in x: #Seconds and minutes
        x= float(x.split("m")[0]) *60 + float(x.split("m ")[1][:-1])
    elif "m" in x: #Only minutes
        x=float(x.split("m")[0])*60
    elif "s" in x: #Only seconds
        x=float(x[:-1])
    else: # No unit
        x=0
    print(x)
    return x



'''
sizes=[]
with open("field_list") as f:
    sizes=f.read().split('\n')[:-1]
'''
sizes=['500K','1M','2M','5M','10M','100M']
print(sizes)

columns=['loss','protocol']+sizes
#print(columns)

data = pd.read_table("http.dat", sep="\t", names=columns, index_col=False)
for s in sizes:
    print(s)
    data[s]=pd.to_numeric(data[s].apply(convert_speed))
    data[s]/=1024 #Convert to Kbps

protocols=['reno','cubic', 'bbr']

# Simple plots, side by side
fig, axes = plt.subplots(ncols=int(len(sizes)/2), nrows=2, figsize=(1, 1), sharey='all')

def plot(pos,d,size):
    d_s=d[['loss','protocol', size]]
    ls=d_s['loss'].unique()
    
    for p in data['protocol'].unique():
        d=data[data['protocol']==p].sort_values('loss', ascending = True)
        m = d.groupby('loss')[size].mean()
        k= d['loss'].unique()
        pos.plot(k,m,  label=p)
        
    pos.set_title(size)
    #pos.set_xlabel("Loss (%)")
    pos.set_ylabel("Speed (Kbps)")

for i in range(len(sizes)):
    size=sizes[i]
    print(size)
    plot(axes[i%2][i//2],data,size)

legend = plt.legend(loc=1)
#fig.legend( lines, labels, loc = (0.5, 0), ncol=5 )
show_or_save(plt,"sizes_plot.pdf")

for i in range(len(sizes)):
    #axes[i].plot([0,50],[1,1], linestyle='--', dashes=(1,5))
    axes[i%2][i//2].set_yscale("log")
    axes[i%2][i//2].yaxis.set_major_formatter(FormatStrFormatter("%.1f"))

show_or_save(plt,"sizes_plot_log.pdf")
plt.clf()


# BBR performances across the size
data_bbr=data[data['protocol']=='bbr']

for size in sizes:
    d=data_bbr[['loss', size]].sort_values('loss', ascending = True)
    ls=d['loss'].unique()
    m=[ d[d['loss'] == l][size].mean() for l in ls]
    print(ls)
    print(m)
    plt.plot(ls, m, label=size)
    
plt.legend()
#plt.title(title)
plt.xlabel("Loss (%)")
plt.ylabel("Speed (Kbps)")
show_or_save(plt,"size_bbr_plot.pdf")

plt.yscale("log")
show_or_save(plt,"size_bbr_plot_log.pdf")

plt.clf()
