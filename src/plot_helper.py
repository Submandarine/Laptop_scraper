import matplotlib.pyplot as plt
import csv
import numpy as np
from typing import Literal


def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))


def dat_filter(data, column_i: int, comparison: Literal["==", "!=", ">", "<", ">=", "<="], value: str):
    if comparison == "==":
        filtered_data = data[data[:, column_i] == value]
    elif comparison == "!=":
        filtered_data = data[data[:, column_i] != value]
    elif comparison == ">":
        filtered_data = data[data[:, column_i].astype(float) > float(value)]
    elif comparison == "<":
        filtered_data = data[data[:, column_i].astype(float) < float(value)]
    elif comparison == ">=":
        filtered_data = data[data[:, column_i].astype(float) >= float(value)]
    elif comparison == "<=":
        filtered_data = data[data[:, column_i].astype(float) <= float(value)]
    return filtered_data


def dat_filter2(data, column_i1, comparison: Literal["==", "!=", ">", "<"], column_i2):
    if comparison == "==":
        filtered_data = data[data[:, column_i1] == data[:, column_i2]]
    elif comparison == "!=":
        filtered_data = data[data[:, column_i1] != data[:, column_i2]]
    elif comparison == ">":
        filtered_data = data[data[:, column_i1].astype(float) > data[data[:, column_i1].astype(float)]]
    elif comparison == "<":
        filtered_data = data[data[:, column_i1].astype(float) < data[data[:, column_i1].astype(float)]]
    return filtered_data


# filter out columns which don't conform to the function, args have to be integer columns
def dat_filter3(data, function, *args):
    filtered_data = []
    for line in data:
        elements = [line[i].astype(int) for i in args]
        if function(*elements):
            filtered_data.append(line)
        # else:
        #     print(f"eliminated {line}")

    return np.array(filtered_data)


# filter out columns which don't conform to the function, args dont to be integer columns
def dat_filter3b(data, function, *args):
    filtered_data = []
    for line in data:
        func_args = [line[i] for i in args]
        if function(*func_args):
            filtered_data.append(line)
        # else:
        #     print(f"eliminated {line}")

    return np.array(filtered_data)


# # example
# def average_duplicates(data):
#     relevant_fields = [c.gpus, c.io_procs, c.mpi_procs, c.nproma, c.nproma_sub]
#     performance_fields = [c.job_runtime, c.perf]
#     result = []
#     processed = np.full_like(data[:, 0], False, dtype=bool)
#     for i in range(len(data)):
#         if not processed[i]:
#             rel = data[:, relevant_fields]
#             duplicate_mask = np.all(rel == rel[i], axis=1)
#             if np.sum(duplicate_mask) > 1:
#                 dup_lines = data[duplicate_mask]
#                 newline = np.copy(dup_lines[0])
#                 newline[c.log] = "averaged"
#                 for field in performance_fields:
#                     # print(dup_lines[:, field])
#                     values = dat_filter(dup_lines, field, "!=", "None")[:, field].astype(float)
#                     # print(f'val: {values}')
#                     if len(values) == 0:
#                         newline[field] = "None"
#                     else:
#                         newline[field] = np.average(values)

#                 processed = processed | duplicate_mask
#                 # print(dup_lines)
#                 # print(newline)
#                 # print('\n')
#                 result.append(newline)
#             else:
#                 result.append(data[i])
#                 processed[i] = True
#     return np.array(result)


def assign_col(array):
    colors = [
        "r",
        "g",
        "b",
        "k",
        "y",
        "orange",
        "aqua",
        "skyblue",
        "brown",
        "brown",
        "brown",
        "brown",
        "brown",
        "brown",
        "brown",
        "brown",
    ]
    val_set = list(set(array))
    val_set.sort()
    try:
        val_set = sorted(val_set, key=float)
    except:
        # not numeric, do nothing
        pass
    # print(val_set)
    col_list = np.full_like(array, "")
    for i in range(len(col_list)):
        col_list[i] = colors[val_set.index(array[i])]

    # for i in range(len(val_set)):
    #     col_list += np.where(array == val_set[i], colors[i], "")
    return (col_list, zip(val_set, colors))


def assign_mark(array):
    markers = [
        "o",
        "^",
        "p",
        "s",
        "D",
    ]
    val_set = np.sort(list(set(array)))
    mark_list = np.full_like(array, "")
    for i in range(len(val_set)):
        mark_list += np.where(array == val_set[i], markers[i], "")
    return mark_list


# # example
# def plot_nproma(data):
#     fig, ax = plt.subplots(figsize=(10, 5))
#     # filter data based on needs, 3 levels of filter functions

#     # data = dat_filter(data, c.perf, '<', '360')
#     # exclusive runs are needed if more than one gpus is used, filter out faulty data
#     data = dat_filter3(data, lambda excl, gpus: excl == 1 or gpus == 1 or gpus == 8, c.excl, c.gpus)
#     # data = dat_filter(data, c.nproma, ">", "7000")
#     data = dat_filter2(data, c.nproma, "==", c.nproma_sub)
#     data = dat_filter(data, c.gpu, "==", "A40")
#     data = dat_filter(data, c.compiler, "==", "22.7")
#     data = dat_filter3(
#         data, lambda gpus, mpi, io: mpi == gpus + io, c.gpus, c.mpi_procs, c.io_procs
#     )  # remove bad proc configs

#     for _x, _y, _c, _m, _l in zip(
#         data[:, c.nproma].astype(int),  # nproma on x-axis
#         data[:, c.perf].astype(float),  # performance on y-axis
#         assign_col(data[:, c.gpus]),  # assign colors based on gpus
#         assign_mark(data[:, c.io_procs]),  # assign markers based on io_procs
#         # np.full_like(data[:, 0], "o"),  # assign same marker for all
#         data[:, c.gpus] + " GPUs, " + data[:, c.io_procs] + " io procs",  # assign labels based on gpus
#     ):
#         ax.scatter(_x, _y, c=_c, marker=_m, label=_l)

#     plt.xlabel("nproma")
#     plt.ylim(bottom=0)
#     plt.ylabel("time(s) (lower is better)")
#     plt.title("Performance impact nproma on A40 (Alex)")
#     plt.tight_layout()
#     legend_without_duplicate_labels(ax)
#     plt.savefig("perf.png")
