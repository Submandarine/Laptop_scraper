import csv

import numpy as np
import plot_helper as ph
from structure import *


def get_cpu_type(name):
    iname = next(
        (
            x
            for x in [
                "Celeron",
                "i3",
                "i5",
                "i7",
                "i9",
                "Ryzen 3 PRO",
                "Ryzen 5 PRO",
                "Ryzen 7 PRO",
                "Ryzen 3",
                "Ryzen 5",
                "Ryzen 7",
            ]
            if x in name
        ),
        "None",
    )
    cpu_name_full = "None"
    if iname != "None":
        try:
            index = name.index(iname)
            index += len(iname) + 3  # type string normally starts here
            start = end = index
            while start > 0 and name[start - 1] not in [" ", "-", ","]:
                start -= 1
            while end < len(name) and name[end] not in [" ", "-", ","]:
                end += 1
            cpu_name = name[start:end]
            if "i" in iname:
                cpu_name_full = iname + "-" + cpu_name
            else:
                cpu_name_full = iname + " " + cpu_name
        except Exception:
            # no name found, just keep None
            pass

    # get cpu mark score
    cpu_perf_database = []
    with open(p_cpu_perf, "r") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            cpu_perf_database.append(np.array(row))
    cpu_perf_database = np.array(cpu_perf_database[1:])  # remove header

    # find column in performance database
    filtered = ph.dat_filter3b(cpu_perf_database, lambda name: cpu_name_full in name, 0)
    perf = "None"
    if len(filtered) > 0:
        perf = filtered[0][2]

    return (cpu_name_full, perf)
