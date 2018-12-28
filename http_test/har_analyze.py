import json
import os
import shutil

# Analyze a HAR file, created via a browser and generate a 
# fake webpage with the same sizes of components
# Run `cd page && python -m SimpleHTTPServer`
# Then, `wget -r SERVERIP:8000`


har=json.load(open("page.har"))
sizes=[ h['response']['content']['size'] for h in har['log']['entries']]
print("Total size %ib (%.3f MB) for %i requests" % (sum(sizes), sum(sizes)/1024.0**2,len(sizes)))

if os.path.exists("page"):
    shutil.rmtree("page")
os.makedirs("page")

html="<html>\n<body>\n"

for i,s in enumerate(sizes):
    with open('page/file_'+str(i),"wb") as f:
        f.write(os.urandom(int(s)-1))        
        f.write(b"\0")
        html+="<img src='file_%i'/>\n" %i

html+="</body></html>"
with open("page/index.html", "w+") as f:
    f.write(html)
    


