import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter

SHOW=False
title="Comple Web page download test - 120 seconds timeout"

def show_or_save(plt, name):
    if SHOW:
        plt.show()
    else:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(8, 6)
        plt.savefig(name, dpi=100)

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





data = pd.read_table("http.dat", sep="\t", names=['loss','protocol','speed', 'time'])
data['speed']=pd.to_numeric(data['speed'].apply(convert_speed))
data['time']=pd.to_numeric(data['time'].apply(convert_time))



data['speed']/=1024 #Convert to Kbps




#Simple plot
for p in data['protocol'].unique():
    d=data[data['protocol']==p].sort_values('loss', ascending = True)
    m = d.groupby('loss')['speed'].mean()
    k= d['loss'].unique()
    plt.plot(k,m,  label=p)
    
plt.legend()
plt.title(title)
plt.xlabel("Loss (%)")
plt.ylabel("Speed (Kbps)")
show_or_save(plt,"plot.pdf")

plt.yscale("log")
show_or_save(plt,"plot_log.pdf")

plt.clf()

#Simple plot with markers for std deviation
for p in data['protocol'].unique():
    d=data[data['protocol']==p].sort_values('loss', ascending = True)
    m = d.groupby('loss')['speed'].mean()
    std=d.groupby('loss')['speed'].std()
    k= d['loss'].unique()
    plt.errorbar(k,m,yerr=std,  label=p)
    
plt.legend()
plt.title(title)
plt.xlabel("Loss (%)")
plt.ylabel("Speed (Kbps)")
#plt.yscale("log")
show_or_save(plt,"plot_std_markers.pdf")
plt.clf()


# Violin plots, side by side
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(4, 4), sharey='all')

def violin(pos,d,protocol):
    d_p=d[d['protocol'] == protocol]
    ls=d_p['loss'].unique()
    v=[ d_p[d_p['loss'] == l]['speed'].tolist() for l in ls]
    pos.violinplot(v,ls,showmeans=True)
    pos.set_title(protocol)
    pos.set_xlabel("Loss (%)")
    pos.set_ylabel("Speed (Kbps)")



violin(axes[0],data,'bbr')
violin(axes[1],data,'reno')
violin(axes[2],data,'cubic')
show_or_save(plt,"violinplot.pdf")

for i in range(3):
    #axes[i].plot([0,50],[1,1], linestyle='--', dashes=(1,5))
    axes[i].set_yscale("log")
    axes[i].yaxis.set_major_formatter(FormatStrFormatter("%.1f"))

show_or_save(plt,"violinplot_log.pdf")
