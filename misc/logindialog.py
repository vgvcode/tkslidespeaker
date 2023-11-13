import tkinter as tk
from tkinter import simpledialog

class LoginDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Username:").grid(row=0)
        tk.Label(master, text="Password:").grid(row=1)

        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        return self.username_entry  # Focus on the username entry initially

    def apply(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        #print("Username:", self.username)
        #print("Password:", self.password)
        self.result = (username, password)
        # You can perform authentication or any other action with the entered values here

def show_login_dialog():
    dialog = LoginDialog(root, title="Login")
    result = dialog.result
    if result:
        # "OK" button clicked
        username, password = result
        #print("Username:", username)
        #print("Password:", password)
        # Perform authentication or any other action with the entered values
        return True
    else:
        # "Cancel" button clicked or dialog closed without entering values
        # print("Login canceled")
        return False

# Create the main window
root = tk.Tk()
root.title("Login Dialog Example")

# Create a button to trigger the login dialog
login_button = tk.Button(root, text="Login", command=show_login_dialog)
login_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()

# import tkinter as tk
# from tkinter import simpledialog

# def show_login_dialog():
#     # Create a simple dialog with two input fields
#     username = simpledialog.askstring("Login", "Enter your username:")
#     password = simpledialog.askstring("Login", "Enter your password:", show='*')

#     # Print the entered values (you might want to perform authentication here)
#     print("Username:", username)
#     print("Password:", password)

# # Create the main window
# root = tk.Tk()
# root.title("Login Dialog Example")

# # Create a button to trigger the login dialog
# login_button = tk.Button(root, text="Login", command=show_login_dialog)
# login_button.pack(pady=20)

# # Start the Tkinter event loop
# root.mainloop()
