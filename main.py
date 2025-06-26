import tkinter as tk

from menu.start_menu import StartMenu

def main():
    root = tk.Tk()
    root.title("Kreator Postaci D&D 5e")
    root.geometry("800x600")

    app = StartMenu(root)
    app.pack(expand=True, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
