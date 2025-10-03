import tkinter as tk
from view.menu_view import MenuView

def main():
    root = tk.Tk()
    MenuView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
