import tkinter as tk
from wizard.wizard import Wizard

def main():
    root = tk.Tk()
    root.title("Kreator Postaci D&D 5e")
    root.geometry("800x600")

    app = Wizard(root)
    app.pack(expand=True, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
