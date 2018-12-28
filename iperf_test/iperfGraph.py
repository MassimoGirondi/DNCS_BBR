import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter

SHOW=False

def show_or_save(plt, name):
    if SHOW:
        plt.show()
    else:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(10, 7)
        plt.savefig(name, dpi=100, transparent=True)



data = pd.read_table("iperf.dat", sep="\t", names=['loss','protocol','bw'])
data['bw'] = pd.to_numeric(data['bw'])/1024.0


#Simple plot
for p in data['protocol'].unique():
    d=data[data['protocol']==p].sort_values('loss', ascending = True)
    m = d.groupby('loss')['bw'].mean()
    k= d['loss'].unique()
    plt.plot(k,m,  label=p)
    
plt.legend()
#plt.title("Iperf: 20 seconds test")
plt.xlabel("Loss (%)")
plt.ylabel("Speed (Mbps)")
show_or_save(plt,"plot.pdf")

plt.yscale("log")
show_or_save(plt,"plot_log.pdf")

plt.clf()

#Simple plot with markers for std deviation
for p in data['protocol'].unique():
    d=data[data['protocol']==p].sort_values('loss', ascending = True)
    m = d.groupby('loss')['bw'].mean()
    std=d.groupby('loss')['bw'].std()
    k= d['loss'].unique()
    plt.errorbar(k,m,yerr=std,  label=p)
    
plt.legend()
#plt.title("Iperf: 20 seconds test")
plt.xlabel("Loss (%)")
plt.ylabel("Speed (Mbps)")
#plt.yscale("log")
show_or_save(plt,"plot_std_markers.pdf")
plt.clf()


# Violin plots, side by side
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(4, 4), sharey='all')

def violin(pos,d,protocol):
    d_p=d[d['protocol'] == protocol]
    ls=d_p['loss'].unique()
    v=[ d_p[d_p['loss'] == l]['bw'].tolist() for l in ls]
    pos.violinplot(v,ls,showmeans=True)
    pos.set_title(protocol)
    pos.set_xlabel("Loss (%)")
    pos.set_ylabel("Speed (Mbps)")



violin(axes[0],data,'bbr')
violin(axes[1],data,'reno')
violin(axes[2],data,'cubic')
show_or_save(plt,"violinplot.pdf")

for i in range(3):
    #axes[i].plot([0,50],[1,1], linestyle='--', dashes=(1,5))
    axes[i].set_yscale("log")
    axes[i].yaxis.set_major_formatter(FormatStrFormatter("%.1f"))

show_or_save(plt,"violinplot_log.pdf")
