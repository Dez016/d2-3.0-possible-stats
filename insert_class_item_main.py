from four_pc_archetype_fit import fitStats
from interpreter import convert
import tkinter as tk
from tkinter import scrolledtext

exostats = []
request = []
output = []

root = tk.Tk()
root.withdraw()  # Hide the main root window

labels = [
    "Health",
    "Melee",
    "Grenade",
    "Super",
    "Class",
    "Weapons"
]

def open_exotic_window():
    exotic_win = tk.Toplevel(root)
    exotic_win.title("Exotic Stats: ")

    exo = []

    for i, text in enumerate(labels):
        tk.Label(exotic_win, text=text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        exostat = tk.Entry(exotic_win, width=30)
        exostat.grid(row=i, column=1, padx=10, pady=5)
        exo.append(exostat)

    def submitexo():
        global exostats
        exostats.clear()
        exostats.extend([entry.get() for entry in exo])
        exotic_win.destroy()
        open_request_window()

    submit_btn = tk.Button(exotic_win, text="Submit", command=submitexo)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10)

def open_request_window():
    root2 = tk.Toplevel(root)
    root2.title("Requested Stats: ")

    entries = []

    for i, text in enumerate(labels):
        tk.Label(root2, text=text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        entry = tk.Entry(root2, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def submitrequest():
        global request, output
        request.clear()
        output.clear()
        request.extend([entry.get() for entry in entries])
        root2.destroy()

        print("STOPPPING")
        print("Request:", request)
        print("Exostats:", exostats)

        pieces, padding = fitStats(request, exostats)
        for i in range(len(pieces)):
            output.append(convert(pieces[i]))
            output.append(list(map(str, padding[i])))

        lines = [" ".join(row) for row in output]
        text = "\n".join(lines)

        # Display results in a scrollable text widget
        result_win = tk.Toplevel(root)
        result_win.title("Armor Combos")

        text_widget = scrolledtext.ScrolledText(result_win, width=100, height=20, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=10)

        text_widget.insert(tk.END, text)
        text_widget.config(state='normal')

        def on_close():
            print("Window is closing!")
            result_win.destroy()
            root.destroy()

        result_win.protocol("WM_DELETE_WINDOW", on_close)

    submit_btn = tk.Button(root2, text="Submit", command=submitrequest)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10)

# Start the process by opening the exotic stats window
open_exotic_window()

root.mainloop()