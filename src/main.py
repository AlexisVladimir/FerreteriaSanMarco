from ttkbootstrap import Window
from src.views.main_view import MainView

def main():
    root = Window(themename="flatly")
    app = MainView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
''''
# src/main.py
import ttkbootstrap as ttk
from src.views.login_view import LoginView

def show_main_view(root):
    # Limpia la ventana actual y carga la vista principal
    for widget in root.winfo_children():
        widget.destroy()
    from src.views.main_view import MainView
    MainView(root)

def main():
    root = ttk.Window(themename="flatly")
    # Se pasa una función callback que se llamará al autenticarse exitosamente.
    login_view = LoginView(root, on_success=lambda user: show_main_view(root))
    root.mainloop()

if __name__ == "__main__":
    main()

'''