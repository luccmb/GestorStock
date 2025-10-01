import customtkinter as ctk
from .database import Database

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()
        self.build_gui()

    def build_gui(self):
        self.root.title("GestorStock - Login")
        self.root.geometry("400x300")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(self.frame, text="Iniciar Sesión", font=("Arial", 20))
        self.label_title.pack(pady=10)

        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="Usuario")
        self.entry_username.pack(pady=10, padx=20, fill="x")

        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Contraseña", show="*")
        self.entry_password.pack(pady=10, padx=20, fill="x")

        self.button_login = ctk.CTkButton(self.frame, text="Iniciar Sesión", command=self.login)
        self.button_login.pack(pady=10)

        self.button_register = ctk.CTkButton(self.frame, text="Registrar Nuevo Usuario", command=self.register)
        self.button_register.pack(pady=5)

        self.label_message = ctk.CTkLabel(self.frame, text="", text_color="red")
        self.label_message.pack(pady=5)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if self.db.verify_user(username, password):
            self.label_message.configure(text="¡Login exitoso!", text_color="green")
            self.root.after(1000, lambda: self.on_login_success(username))
        else:
            self.label_message.configure(text="Usuario o contraseña incorrectos", text_color="red")

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username and password:
            if self.db.add_user(username, password):
                self.label_message.configure(text="Usuario registrado con éxito", text_color="green")
            else:
                self.label_message.configure(text="El usuario ya existe", text_color="red")
        else:
            self.label_message.configure(text="Por favor, completa todos los campos", text_color="red")