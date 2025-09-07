import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy

from four_pc_archetype_fit import fitStats
from five_pc_leg_fit import fitLegArmor
from five_pc_exotic_fit import fitExoArmor
from interpreter import convert, convertExo
from classtostat import classitemtostats

def sorter(tuple):
        possibilties, padding = tuple

        if not possibilties:
            return []

        sorted = [[] for _ in range(76)]
        output = []
        
        paddings = numpy.array(padding)
        sums = numpy.sum(paddings.astype(int), axis = 1)

        for i in range(len(sums)):
            sorted[sums[i]].append((possibilties[i], paddings[i]))

        for row in sorted:
            for pair in row:
                output.append(pair)
        
        return output

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

        ttk.Label(self.dropdown_frame, text="Select Options:").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))

        # Define options for the first dropdown
        options_3 = ["Warlock", "Titan", "Hunter"]
        
        # Define dependent options for the second and third dropdowns based on first dropdown selection
        dependent_options = {
            "Warlock": {
                "second": ["Spirit of the Assassin", "Spirit of Inmost Light", "Spirit of the Ophidian", "Spirit of the Stag", "Spirit of the Filament", "Spirit of the Necrotic", "Spirit of Osmiomancy", "Spirit of Apotheosis"],
                "third": ["Spirit of the Star-Eater", "Spirit of Synthoceps", "Spirit of Verity", "Spirit of Vesper", "Spirit of Harmony", "Spirit of Starfire", "Spirit of the Swarm", "Spirit of the Claw"],
            },
            "Titan": {
                "second": ["Spirit of the Assassin", "Spirit of Inmost Light", "Spirit of the Ophidian", "Spirit of Severance", "Spirit of Hoarfrost", "Spirit of the Eternal Warrior", "Spirit of the Abeyant", "Spirit of the Bear"],
                "third": ["Spirit of the Star-Eater", "Spirit of Synthoceps", "Spirit of Verity", "Spirit of Contact", "Spirit of Scars", "Spirit of the Horn", "Spirit of Alpha Lupi", "Spirit of the Armamentarium"],
            },
            "Hunter": {
                "second": ["Spirit of the Assassin", "Spirit of Inmost Light", "Spirit of the Ophidian", "Spirit of the Dragon", "Spirit of Galanor", "Spirit of the Foetracer", "Spirit of Caliban", "Spirit of Renewal"],
                "third": ["Spirit of the Star-Eater", "Spirit of Synthoceps", "Spirit of Verity", "Spirit of the Cyrtarachne", "Spirit of the Gyrfalcon", "Spirit of the Liar", "Spirit of the Wormhusk", "Spirit of the Coyote"],
            }
        }

        # First dropdown
        var1 = tk.StringVar(value=options_3[0])
        dropdown1 = ttk.Combobox(self.dropdown_frame, values=options_3, textvariable=var1, state="readonly", width=12)
        dropdown1.grid(row=1, column=0, padx=5)
        self.dropdown_vars["first"] = var1
        self.dropdown_widgets.append(dropdown1)

        # Second dropdown (initial values set based on first dropdown's default)
        var2 = tk.StringVar(value=dependent_options[options_3[0]]["second"][0])
        dropdown2 = ttk.Combobox(self.dropdown_frame, values=dependent_options[options_3[0]]["second"], textvariable=var2, state="readonly", width=12)
        dropdown2.grid(row=1, column=1, padx=5)
        self.dropdown_vars["second"] = var2
        self.dropdown_widgets.append(dropdown2)

        # Third dropdown (initial values set based on first dropdown's default)
        var3 = tk.StringVar(value=dependent_options[options_3[0]]["third"][0])
        dropdown3 = ttk.Combobox(self.dropdown_frame, values=dependent_options[options_3[0]]["third"], textvariable=var3, state="readonly", width=12)
        dropdown3.grid(row=1, column=2, padx=5)
        self.dropdown_vars["third"] = var3
        self.dropdown_widgets.append(dropdown3)

        def update_dependent_dropdowns(event=None):
            selected = var1.get()
            # Update second dropdown
            dropdown2['values'] = dependent_options[selected]["second"]
            var2.set(dependent_options[selected]["second"][0])
            # Update third dropdown
            dropdown3['values'] = dependent_options[selected]["third"]
            var3.set(dependent_options[selected]["third"][0])

        # Bind selection change on first dropdown
        dropdown1.bind("<<ComboboxSelected>>", update_dependent_dropdowns)


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
            second_val = self.dropdown_vars.get("second")
            third_val = self.dropdown_vars.get("third")
            print(second_val.get(), third_val.get())
            exostats = classitemtostats(second_val.get(), third_val.get())
            print(exostats)

            if isinstance(exostats, str):
                result = exostats
            else: 
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

        sorted = sorter(fitStats(stats, exostats))
        
        for poss, pad in sorted:
            output.append(convert(poss))
            output.append(pad.tolist())
        return output
    
    def func_exotic_armor(self, stats):
        output = []
        sorted = sorter(fitExoArmor(stats))
        for poss, pad in sorted:
            output.append(convertExo(poss))
            output.append(pad.tolist())
        return output
    
    def func_no_exotic(self, stats):
        output = []
        sorted = sorter(fitLegArmor(stats))
        
        for poss, pad in sorted:
            output.append(convert(poss))
            output.append(pad.tolist())
        return output

if __name__ == "__main__":
    app = SliderUI()
    app.mainloop()

    
    


