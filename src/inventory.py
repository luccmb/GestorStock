import customtkinter as ctk
from .database import Database

class InventoryWindow:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.db = Database()
        self.build_gui()

    def build_gui(self):
        self.root.title(f"GestorStock - Bienvenido, {self.username}")
        self.root.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame superior para añadir artículo
        self.frame_add = ctk.CTkFrame(self.root)
        self.frame_add.pack(pady=10, padx=20, fill="x")

        self.entry_name = ctk.CTkEntry(self.frame_add, placeholder_text="Nombre")
        self.entry_name.pack(side="left", padx=5, pady=5)

        self.entry_sku = ctk.CTkEntry(self.frame_add, placeholder_text="SKU")
        self.entry_sku.pack(side="left", padx=5, pady=5)

        self.entry_price = ctk.CTkEntry(self.frame_add, placeholder_text="Precio")
        self.entry_price.pack(side="left", padx=5, pady=5)

        self.entry_quantity = ctk.CTkEntry(self.frame_add, placeholder_text="Cantidad")
        self.entry_quantity.pack(side="left", padx=5, pady=5)

        self.entry_location = ctk.CTkEntry(self.frame_add, placeholder_text="Ubicación")
        self.entry_location.pack(side="left", padx=5, pady=5)

        self.button_add = ctk.CTkButton(self.frame_add, text="Añadir Artículo", command=self.add_item)
        self.button_add.pack(side="left", padx=5, pady=5)

        # Frame para la tabla
        self.frame_table = ctk.CTkFrame(self.root)
        self.frame_table.pack(pady=10, padx=20, fill="both", expand=True)

        # Tabla
        self.tree = ctk.CTkFrame(self.frame_table)  # Usamos Frame como contenedor
        self.tree.pack(fill="both", expand=True)

        # Labels para encabezados
        headers = ["ID", "Nombre", "SKU", "Precio", "Cantidad", "Ubicación", "Acciones"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.tree, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

        self.items = []
        self.load_items()

        # Botón de cerrar sesión
        self.button_logout = ctk.CTkButton(self.root, text="Cerrar Sesión", command=self.on_logout)
        self.button_logout.pack(pady=10)

    def add_item(self):
        name = self.entry_name.get()
        sku = self.entry_sku.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()
        location = self.entry_location.get()

        if name and sku and price and quantity and location:
            try:
                price = float(price)
                quantity = int(quantity)
                if self.db.add_item(name, sku, price, quantity, location):
                    self.load_items()
                    self.clear_entries()
                else:
                    ctk.CTkMessageBox.show_error("Error", "El SKU ya existe")
            except ValueError:
                ctk.CTkMessageBox.show_error("Error", "Precio debe ser número decimal y Cantidad un número entero")
        else:
            ctk.CTkMessageBox.show_error("Error", "Por favor, completa todos los campos")

    def load_items(self):
        # Limpiar tabla
        for widget in self.tree.winfo_children()[len(self.items[0]) if self.items else 7:]:
            widget.destroy()
        self.items = self.db.get_all_items()

        for i, item in enumerate(self.items, start=1):
            for j, value in enumerate(item):
                label = ctk.CTkLabel(self.tree, text=str(value))
                label.grid(row=i, column=j, padx=5, pady=5, sticky="w")
            # Botones de editar y eliminar
            btn_edit = ctk.CTkButton(self.tree, text="Editar", command=lambda x=item: self.edit_item(x))
            btn_edit.grid(row=i, column=len(item), padx=2, pady=2)
            btn_delete = ctk.CTkButton(self.tree, text="Eliminar", command=lambda x=item[0]: self.delete_item(x))
            btn_delete.grid(row=i, column=len(item)+1, padx=2, pady=2)

    def clear_entries(self):
        self.entry_name.delete(0, "end")
        self.entry_sku.delete(0, "end")
        self.entry_price.delete(0, "end")
        self.entry_quantity.delete(0, "end")
        self.entry_location.delete(0, "end")

    def edit_item(self, item):
        id, name, sku, price, quantity, location = item
        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, name)
        self.entry_sku.delete(0, "end")
        self.entry_sku.insert(0, sku)
        self.entry_price.delete(0, "end")
        self.entry_price.insert(0, str(price))
        self.entry_quantity.delete(0, "end")
        self.entry_quantity.insert(0, str(quantity))
        self.entry_location.delete(0, "end")
        self.entry_location.insert(0, location)
        self.button_add.configure(text="Actualizar Artículo", command=lambda: self.update_item(id))

    def update_item(self, id):
        name = self.entry_name.get()
        sku = self.entry_sku.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()
        location = self.entry_location.get()

        if name and sku and price and quantity and location:
            try:
                price = float(price)
                quantity = int(quantity)
                if self.db.update_item(id, name, sku, price, quantity, location):
                    self.load_items()
                    self.clear_entries()
                    self.button_add.configure(text="Añadir Artículo", command=self.add_item)
                else:
                    ctk.CTkMessageBox.show_error("Error", "El SKU ya existe")
            except ValueError:
                ctk.CTkMessageBox.show_error("Error", "Precio debe ser número decimal y Cantidad un número entero")
        else:
            ctk.CTkMessageBox.show_error("Error", "Por favor, completa todos los campos")

    def delete_item(self, id):
        self.db.delete_item(id)
        self.load_items()
        