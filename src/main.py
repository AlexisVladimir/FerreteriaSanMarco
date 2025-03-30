from ttkbootstrap import Window
from src.views.main_view import MainView

def main():
    root = Window(themename="flatly")
    app = MainView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
