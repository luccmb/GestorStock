import customtkinter as ctk
from src.login import LoginWindow
from src.inventory import InventoryWindow

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.show_login()

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginWindow(self.root, self.show_inventory)

    def show_inventory(self, username):
        for widget in self.root.winfo_children():
            widget.destroy()
        InventoryWindow(self.root, username, self.show_login)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()