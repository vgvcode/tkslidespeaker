import tkinter as tk
from tkinter import ttk

class ComboBoxModalBox:
    def __init__(self, parent):
        self.parent = parent
        self.result = None

        self.create_widgets()

    def create_widgets(self):
        # Create the modal window
        self.modal_box = tk.Toplevel(self.parent)
        self.modal_box.title("ComboBox Modal Box")

        # Create and populate the combo box
        self.combo_var = tk.StringVar()
        self.combo_box = ttk.Combobox(self.modal_box, textvariable=self.combo_var, values=["Option 1", "Option 2", "Option 3"])
        self.combo_box.grid(row=0, column=0, padx=10, pady=10)

        # Create OK and Cancel buttons
        ok_button = tk.Button(self.modal_box, text="OK", command=self.on_ok)
        cancel_button = tk.Button(self.modal_box, text="Cancel", command=self.on_cancel)

        ok_button.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        cancel_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    def on_ok(self):
        # Get the selected value from the combo box and set the result
        self.result = self.combo_var.get()
        self.modal_box.destroy()

    def on_cancel(self):
        # Set the result to None and close the modal box
        self.result = None
        self.modal_box.destroy()

def main():
    root = tk.Tk()
    root.title("Main Window")

    def open_modal_box():
        modal_box = ComboBoxModalBox(root)
        root.wait_window(modal_box.modal_box)
        if modal_box.result is not None:
            print(f"Selected option: {modal_box.result}")

    open_button = tk.Button(root, text="Open Modal Box", command=open_modal_box)
    open_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
