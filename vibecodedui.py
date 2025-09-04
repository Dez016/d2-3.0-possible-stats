import tkinter as tk
from tkinter import ttk, scrolledtext

from four_pc_archetype_fit import fitStats
from five_pc_leg_fit import fitLegArmor
from five_pc_exotic_fit import fitExoArmor
from interpreter import convert, convertExo

class EditableValue(ttk.Frame):
    def __init__(self, parent, slider, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.slider = slider
        
        self.value_var = tk.StringVar(value=str(int(self.slider.get())))
        
        self.label = ttk.Label(self, textvariable=self.value_var, width=4, anchor="center", cursor="hand2")
        self.label.pack()
        
        self.entry = ttk.Entry(self, width=5, justify="center")
        
        self.label.bind("<Button-1>", self.start_edit)
        self.entry.bind("<Return>", self.finish_edit)
        self.entry.bind("<FocusOut>", self.finish_edit)
        
        self.slider.configure(command=self.update_label)
        self.slider.bind("<Button-1>", self.on_click)
        
        self.dragging = False

    def update_label(self, val):
        if not self.entry.winfo_ismapped():
            self.value_var.set(str(int(float(val))))

    def start_edit(self, event):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.value_var.get())
        self.label.pack_forget()
        self.entry.pack()
        self.entry.focus()
        self.entry.selection_range(0, tk.END)

    def finish_edit(self, event):
        try:
            val = int(self.entry.get())
        except ValueError:
            val = int(self.slider.get())

        val = max(0, min(200, val))

        self.slider.set(val)
        self.value_var.set(str(val))

        self.entry.pack_forget()
        self.label.pack()

    def on_click(self, event):
        slider_length = self.slider.winfo_width()
        click_x = event.x

        if click_x < 0:
            click_x = 0
        elif click_x > slider_length:
            click_x = slider_length

        from_, to_ = float(self.slider.cget("from")), float(self.slider.cget("to"))
        proportion = click_x / slider_length
        value = from_ + proportion * (to_ - from_)

        self.slider.set(value)
        self.update_label(value)

        # Start dragging from this point:
        self.dragging = True
        self.slider.bind("<B1-Motion>", self.on_drag)
        self.slider.bind("<ButtonRelease-1>", self.on_release)

        return "break"  # Stop native drag to control it manually

    def on_drag(self, event):
        if not self.dragging:
            return

        slider_length = self.slider.winfo_width()
        drag_x = event.x

        if drag_x < 0:
            drag_x = 0
        elif drag_x > slider_length:
            drag_x = slider_length

        from_, to_ = float(self.slider.cget("from")), float(self.slider.cget("to"))
        proportion = drag_x / slider_length
        value = from_ + proportion * (to_ - from_)

        self.slider.set(value)
        self.update_label(value)

        return "break"

    def on_release(self, event):
        self.dragging = False
        self.slider.unbind("<B1-Motion>")
        self.slider.unbind("<ButtonRelease-1>")
        return "break"


class SliderUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Slider UI")
        self.geometry("800x580")
        
        left_panel = ttk.Frame(self, padding=10)
        left_panel.pack(side="left", fill="y")
        
        labels = ["Health", "Melee", "Grenade", "Super", "Class", "Weapons"]
        self.sliders = {}
        
        for label in labels:
            ttk.Label(left_panel, text=label).pack(anchor="w", pady=(10,0))
            
            slider_frame = ttk.Frame(left_panel)
            slider_frame.pack(fill="x")
            
            slider = ttk.Scale(slider_frame, from_=0, to=200, orient="horizontal", length=220)
            slider.pack(side="left", fill="x", expand=True)
            slider.set(0)
            
            editable_value = EditableValue(slider_frame, slider)
            editable_value.pack(side="left", padx=(5,0))
            
            self.sliders[label.lower()] = slider
        
        button_frame = ttk.Frame(left_panel, padding=(0, 20, 0, 0))
        button_frame.pack(fill="x")
        
        self.buttons = []
        texts = ["Exotic Class", "Exotic Armor", "No Exotic"]
        for text in texts:
            btn = tk.Button(button_frame, text=text, relief="raised", bd=2,
                            command=lambda b=text: self.on_button_click(b))
            btn.pack(side="left", expand=True, fill="x", padx=5)
            self.buttons.append(btn)
        
        self.selected_button = None
        
        # Frame for dropdowns, initially empty and hidden
        self.dropdown_frame = ttk.Frame(left_panel)
        self.dropdown_frame.pack(fill="x", pady=(10,0))
        
        self.dropdown_widgets = []
        self.dropdown_vars = {}
        
        # Calculate button
        self.calculate_btn = ttk.Button(left_panel, text="Calculate", command=self.calculate)
        self.calculate_btn.pack(fill="x", pady=(20, 0))
        
        # Right-side results box
        right_panel = ttk.Frame(self, padding=10)
        right_panel.pack(side="right", fill="both", expand=True)

        ttk.Label(right_panel, text="Results", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))

        self.results_text = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, state="disabled")
        self.results_text.pack(expand=True, fill="both")

    def on_button_click(self, btn_text):
        for btn in self.buttons:
            if btn.cget("text") == btn_text:
                btn.config(bg="#6699FF", fg="white", relief="sunken")
                self.selected_button = btn_text
            else:
                btn.config(bg=self.cget("bg"), fg="black", relief="raised")
        
        if btn_text == "Exotic Class":
            self.show_dropdowns()
        else:
            self.hide_dropdowns()
    
    def show_dropdowns(self):
        for widget in self.dropdown_widgets:
            widget.destroy()
        self.dropdown_widgets.clear()
        self.dropdown_vars.clear()

        ttk.Label(self.dropdown_frame, text="Exotic Stats:").grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 5))

        self.dropdown_vars["exostats"] = []

        for i in range(6):
            var = tk.StringVar(value="0")
            entry = ttk.Entry(self.dropdown_frame, width=4, justify="center", textvariable=var)
            entry.grid(row=1, column=i, padx=3)
            self.dropdown_vars["exostats"].append(var)
            self.dropdown_widgets.append(entry)

    def hide_dropdowns(self):
        for widget in self.dropdown_widgets:
            widget.destroy()
        self.dropdown_widgets.clear()
        self.dropdown_vars.clear()
    
    def display_results(self, results_2d):
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)

        for row in results_2d:
            line = " ".join(str(item) for item in row)
            self.results_text.insert(tk.END, line + "\n")

        self.results_text.config(state="disabled")

    def calculate(self):
        stats = [int(self.sliders[label].get()) for label in ["health", "melee", "grenade", "super", "class", "weapons"]]
        
        if self.selected_button == "Exotic Class":
            exo_vars = self.dropdown_vars.get("exostats", [])
            exostats = []
            for var in exo_vars:
                try:
                    val = int(var.get())
                except ValueError:
                    val = 0
                exostats.append(max(5, val)) # at least 5

            result = self.func_exotic_class(stats, exostats)
        elif self.selected_button == "Exotic Armor":
            result = self.func_exotic_armor(stats)
        elif self.selected_button == "No Exotic":
            result = self.func_no_exotic(stats)
        else:
            result = "No button selected!"
        
        if not result: 
            result.append("No Combinations Found :(")
            
        self.display_results(result)

    def func_exotic_class(self, stats, exostats):
        output = []
        #make a switch between every exotic thing later; ts is pmoing

        possibilties, padding = fitStats(stats, exostats)
        for i in range(len(possibilties)):
            output.append(convert(possibilties[i]))
            output.append(padding[i].tolist()
)
        return output
    
    def func_exotic_armor(self, stats):
        output = []
        possibilties, padding = fitExoArmor(stats)
        for i in range(len(possibilties)):
            output.append(convertExo(possibilties[i]))
            output.append(padding[i].tolist())
        return output
    
    def func_no_exotic(self, stats):
        output = []
        possibilties, padding = fitLegArmor(stats)
        for i in range(len(possibilties)):
            output.append(convert(possibilties[i]))
            output.append(padding[i].tolist()
)
        return output

if __name__ == "__main__":
    app = SliderUI()
    app.mainloop()

import tkinter as tk
from tkinter import scrolledtext


