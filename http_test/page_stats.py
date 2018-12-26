import os
import matplotlib.pyplot as plt

files=os.listdir("page")
sizes=[os.stat("page/"+f).st_size/1024 for f in files]

#plt.plot(sizes)
plt.hist(sizes)
plt.xlabel("Element size (KB)")
plt.ylabel("Amount")
plt.savefig("page_stat.pdf")
plt.show()
