from four_pc_archetype_fit import fitStats
from five_pc_leg_fit import fitLegArmor
from five_pc_exotic_fit import fitExoArmor
from interpreter import convert, convertExo
import tkinter as tk
from tkinter import scrolledtext

exostats = []
request = []
output = []

root = tk.Tk()
root.withdraw()  # Hide the main root window

def determine_mode(): 
    window = tk.Toplevel(root)
    window.title("Choose intended setup: ")
    window.geometry("300x150")

    btn_normal = tk.Button(window, text="Exotic Normal", command=open_normal_exotic_window)
    btn_class = tk.Button(window, text="Exotic Class", command=open_exotic_class_window)
    btn_none = tk.Button(window, text="No Exotic", command=open_leg_window)

    # Place buttons on the window
    btn_normal.pack(pady=5)
    btn_class.pack(pady=5)
    btn_none.pack(pady=5)


labels = [
    "Health",
    "Melee",
    "Grenade",
    "Super",
    "Class",
    "Weapons"
]

def open_exotic_class_window():
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

        # show results with scroll
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


def open_normal_exotic_window():
    root3 = tk.Toplevel(root)
    root3.title("Requested Stats: ")

    entries = []

    for i, text in enumerate(labels):
        tk.Label(root3, text=text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        entry = tk.Entry(root3, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def submitrequest():
        global request, output
        request.clear()
        output.clear()
        request.extend([entry.get() for entry in entries])
        root3.destroy()

        print("STOPPPING")
        print("Request:", request)

        pieces, padding = fitExoArmor(request)
        for i in range(len(pieces)):
            output.append(convertExo(pieces[i]))
            output.append(list(map(str, padding[i])))

        lines = [" ".join(row) for row in output]
        text = "\n".join(lines)

        # show results with scroll
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

    submit_btn = tk.Button(root3, text="Submit", command=submitrequest)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10)

def open_leg_window():
    root4 = tk.Toplevel(root)
    root4.title("Requested Stats: ")

    entries = []

    for i, text in enumerate(labels):
        tk.Label(root4, text=text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        entry = tk.Entry(root4, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def submitrequest():
        global request, output
        request.clear()
        output.clear()
        request.extend([entry.get() for entry in entries])
        root4.destroy()

        print("STOPPPING")
        print("Request:", request)

        pieces, padding = fitLegArmor(request)
        for i in range(len(pieces)):
            output.append(convert(pieces[i]))
            output.append(list(map(str, padding[i])))

        lines = [" ".join(row) for row in output]
        text = "\n".join(lines)

        # show results with scroll
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

    submit_btn = tk.Button(root4, text="Submit", command=submitrequest)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10)

# start w/ mode window
determine_mode()

root.mainloop()