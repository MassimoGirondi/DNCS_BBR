import os
import matplotlib.pyplot as plt

files=os.listdir("page")
sizes=[os.stat("page/"+f).st_size/1024 for f in files]

#plt.plot(sizes)
plt.hist(sizes)
plt.xlabel("Element size (KB)")
plt.ylabel("Amount")
#plt.title("Elements' size distribution in the test")
#plt.savefig("page_stat.pdf")
figure = plt.gcf() # get current figure
figure.set_size_inches(10, 7)
plt.savefig("page_stat.pdf", dpi=100, transparent=True)


plt.show()
