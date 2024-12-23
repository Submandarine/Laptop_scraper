import csv
from matplotlib import pyplot as plt
import numpy as np
import plot_helper as ph
import tkinter as tk
from tkinter import ttk
import webbrowser
from database import c
from structure import *


data = []
with open(p_database, "r", encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile, delimiter=",")
    for row in rows:
        data.append(np.array(row))
data = np.array(data[1:])  # remove header

ram_min = "8"
ram_max = "64"
ssd_min = "0"
ssd_max = "2000"
price_min = "0"
price_max = "450"
current_data = data.copy()
current_selection = 0


def plot_price_per_score(offline_offers):
    global current_data
    ax.clear()

    current_data = ph.dat_filter(data, c.cpu_mark, "!=", "None")
    if not offline_offers.get():
        current_data = ph.dat_filter(current_data, c.online, "==", "1")
    current_data = ph.dat_filter3b(current_data, lambda name: "Defekt" not in name, c.name)

    current_data = ph.dat_filter(current_data, c.disk, ">=", ssd_min)
    current_data = ph.dat_filter(current_data, c.disk, "<=", ssd_max)
    current_data = ph.dat_filter(current_data, c.ram, ">=", ram_min)
    current_data = ph.dat_filter(current_data, c.ram, "<=", ram_max)
    current_data = ph.dat_filter(current_data, c.price, ">=", price_min)
    current_data = ph.dat_filter(current_data, c.price, "<=", price_max)
    sorted = np.array(current_data[:, c.cpu_mark], dtype=int)
    sorted.sort()

    sc = ax.scatter(
        current_data[:, c.price].astype(float),  # x-axis
        current_data[:, c.cpu_mark].astype(int),  # y-axis
        c=ph.assign_col(current_data[:, c.ram])[0],  # colors based on RAM
        # label="All points",  # optional: you can add a general label here
        picker=True,  # enable picking on all points
    )
    # custom label fix
    col_zip = ph.assign_col(current_data[:, c.ram])[1]
    for z in col_zip:
        ax.scatter([], [], label=z[0] + "GB RAM", color=z[1])

    plt.xlabel("Price")
    plt.ylabel("CPU Mark score")
    plt.ylim(bottom=0)
    plt.title(f"CPU Score at price, {ram_min}-{ram_max}GB RAM {ssd_min}-{ssd_max}GB SSD")
    plt.legend()
    plt.tight_layout()
    # ph.legend_without_duplicate_labels(ax)
    fig.canvas.draw_idle()


# Event: Display details of clicked entry
def on_pick(event):
    global current_selection
    ind = event.ind[0]  # Single index
    current_selection = ind
    # browser_app.open_link(data[ind, c.url])
    details_text.delete("1.0", tk.END)  # Clear existing text
    details = (
        f"Name: {current_data[ind, c.name]}\n"
        f"Price: {current_data[ind, c.price]}\n"
        f"CPU Mark: {current_data[ind, c.cpu_mark]}\n"
        f"RAM: {current_data[ind, c.ram]} GB\n"
        f"SSD: {current_data[ind, c.disk]} GB\n"
        f"Link: {current_data[ind, c.url]}"
    )
    details_text.insert(tk.END, details)


# GUI and Plot setup
root = tk.Tk()
root.title("Laptop_Scraper")

# GUI Components
frame = ttk.Frame(root, padding=10, borderwidth=2, relief="solid")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

filter_frame = ttk.Frame(frame, padding=10, borderwidth=2, relief="solid")
filter_frame.grid(row=1, column=2, padx=5, pady=5)

# Display clicked entry details
details_label = ttk.Label(frame, text="Details of Clicked Entry:")
details_label.grid(row=0, column=0, sticky=tk.W)
details_text = tk.Text(frame, height=8, width=50)
details_text.grid(row=1, column=0, columnspan=2, sticky=tk.W)

ram_label_min = ttk.Label(filter_frame, text="RAM (GB):    Min")
ram_label_min.grid(row=0, column=0, sticky=tk.N, padx=5, pady=5)
ram_entry_min = ttk.Entry(filter_frame)
ram_entry_min.grid(row=0, column=1, sticky=tk.N, padx=5, pady=5)
ram_entry_min.insert(0, ram_min)
ram_label_max = ttk.Label(filter_frame, text="   Max")
ram_label_max.grid(row=0, column=2, sticky=tk.N, padx=5, pady=5)
ram_entry_max = ttk.Entry(filter_frame)
ram_entry_max.grid(row=0, column=3, sticky=tk.N, padx=5, pady=5)
ram_entry_max.insert(0, ram_max)

ssd_label_min = ttk.Label(filter_frame, text="SSD (GB):    Min")
ssd_label_min.grid(row=1, column=0, sticky=tk.N, padx=5, pady=5)
ssd_entry_min = ttk.Entry(filter_frame)
ssd_entry_min.grid(row=1, column=1, sticky=tk.N, padx=5, pady=5)
ssd_entry_min.insert(0, ssd_min)
ssd_label_max = ttk.Label(filter_frame, text="   Max")
ssd_label_max.grid(row=1, column=2, sticky=tk.N, padx=5, pady=5)
ssd_entry_max = ttk.Entry(filter_frame)
ssd_entry_max.grid(row=1, column=3, sticky=tk.N, padx=5, pady=5)
ssd_entry_max.insert(0, ssd_max)

price_label_min = ttk.Label(filter_frame, text="Price (€):    Min")
price_label_min.grid(row=2, column=0, sticky=tk.N, padx=5, pady=5)
price_entry_min = ttk.Entry(filter_frame)
price_entry_min.grid(row=2, column=1, sticky=tk.N, padx=5, pady=5)
price_entry_min.insert(0, price_min)
price_label_max = ttk.Label(filter_frame, text="   Max")
price_label_max.grid(row=2, column=2, sticky=tk.N, padx=5, pady=5)
price_entry_max = ttk.Entry(filter_frame)
price_entry_max.grid(row=2, column=3, sticky=tk.N, padx=5, pady=5)
price_entry_max.insert(0, price_max)

link_button = ttk.Button(frame, text="Open on Ebay")
link_button.grid(row=3, column=0, sticky=tk.W)
filter_button = ttk.Button(frame, text="Apply Filter")
filter_button.grid(row=3, column=2, sticky=tk.W)
offline_offers = tk.IntVar()
checkbox = tk.Checkbutton(frame, text="Include Historic offers", variable=offline_offers)
checkbox.grid(row=3, column=2, sticky=tk.E)


def entry_val_or_default(val, default):
    v = val.get()
    try:
        v = int(v)
    except Exception:
        v = default
    return v


def open_link():
    url = current_data[current_selection, c.url]
    webbrowser.open(url, new=0, autoraise=True)


def apply_filter():
    global ram_min
    global ram_max
    global ssd_min
    global ssd_max
    global price_min
    global price_max
    global offline_offers

    ram_min = entry_val_or_default(ram_entry_min, ram_min)
    ram_max = entry_val_or_default(ram_entry_max, ram_max)
    ssd_min = entry_val_or_default(ssd_entry_min, ssd_min)
    ssd_max = entry_val_or_default(ssd_entry_max, ssd_max)
    price_min = entry_val_or_default(price_entry_min, price_min)
    price_max = entry_val_or_default(price_entry_max, price_max)

    plot_price_per_score(offline_offers)


fig, ax = plt.subplots(figsize=(19, 8))

fig.canvas.callbacks.connect("pick_event", on_pick)
filter_button.config(command=apply_filter)
link_button.config(command=open_link)
# Embed plot in GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, sticky=tk.E)


def on_close():
    print("Closing the application...")
    root.destroy()  # Destroy the Tkinter window
    exit()  # Exit the program explicitly


root.protocol("WM_DELETE_WINDOW", on_close)

apply_filter()
root.mainloop()
