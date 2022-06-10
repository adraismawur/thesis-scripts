from datetime import date, time
from glob import glob
import os
import sys
from dateutil import parser

curdir = os.path.split(__file__)[0]

name = sys.argv[1]
path = os.path.join(curdir, name)
logfiles = glob(os.path.join(path, "*profile.log"))

sorted(logfiles, key=os.path.getmtime)

runfile = logfiles[0]

with open(runfile) as logfile:
    # skip first line
    logfile.readline()
    print("second,cpu,mem_mb,mem_percent")

    first_timestamp = None
    for line in logfile:
        lineparts = line.split(",")

        timestamp = lineparts[0].split(".")[0]

        if first_timestamp == None:
            first_timestamp = parser.parse(timestamp)

        seconds = (parser.parse(timestamp) - first_timestamp).seconds

        cpu_percent = lineparts[1]

        memory_mb = lineparts[3]

        memory_percent = lineparts[4].rstrip()

        print(f"{seconds},{cpu_percent},{memory_mb},{memory_percent}")
