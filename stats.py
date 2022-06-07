from datetime import date, time
from glob import glob
import os
import re

curdir = os.path.split(__file__)[0]
lst = os.listdir("./")
lst.remove("stats.py")
lst = sorted(lst, key=lambda path: path.split('-')[0] + str(int(path.split('-')[1])/350))

stats = dict()

for entry in lst:
    if entry == "stats.py":
        continue
    name = entry
    path = os.path.join(curdir, name)
    logfiles = glob(os.path.join(path, "*[!profile].log"))
    
    if len(logfiles) == 0:
        continue
    
    sorted(logfiles, key=os.path.getmtime)

    runfile = logfiles[0]

    stats[name] = {}
    bgcs = 0
    with open(runfile) as logfile:
        timeregex = re.compile("(\\d{4}-\\d{2}-\\d{2}[ _]\\d{2}[:-]\\d{2}[:-]\\d{2})")
        for line in logfile:
            if " BGCs)" in line:
                bgcs += int(line.split("(")[1].split(" ")[0])
            matches = timeregex.match(line.rstrip())
            if not matches:
                continue
            timestamp_parts = matches.group(1).replace("_", " ").split(" ")
            date = timestamp_parts[0]
            time = timestamp_parts[1].replace("-", ":")
            timestamp = " ".join([date, time])
            if "Including files with" in line:
                stats[name]["start"] = timestamp
            if "Finished generating domtable files" in line or "Finished predicting domains" in line:
                stats[name]["hmmscan"] = timestamp
            if "Trying to read domain alignments" in line:
                stats[name]["hmmalign"] = timestamp
            if not "hmmalign" in stats[name] and "Finished creating figures" in line:
                stats[name]["hmmalign"] = timestamp
            if "Main function took" in line:
                stats[name]["end"] = timestamp
        stats[name]["bgcs"] = bgcs

print("branch,gbks,bgcs,start   ,hmmscan  ,hmmalign,end")
for entry, entrystats in stats.items():
    entrystats: dict()
    parts = entry.split("-")
    branch = parts[0]
    gbks = parts[1]
    bgcs = entrystats["bgcs"]
    if "start" in entrystats:
        start = entrystats["start"]
    if "hmmscan" in entrystats:
        hmmscan = entrystats["hmmscan"]
    if "hmmalign" in entrystats:
        hmmalign = entrystats["hmmalign"]
    if "end" in entrystats:
        end = entrystats["end"]

    if "hmmscan" in entrystats and "hmmalign" in entrystats and "start" in entrystats and "end" in entrystats:
        print(f"{branch},{gbks},{bgcs},{start},{hmmscan},{hmmalign},{end}")
    else:
        print(f"{branch},{gbks},{bgcs},,,,")
