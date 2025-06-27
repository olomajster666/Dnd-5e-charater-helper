import tkinter as tk
import os
from state.character_state import CharacterState
import subprocess

from .has_steps import HasSteps


class StepCharacterSheet(tk.Frame):
    def __init__(self, master, state, wizard : HasSteps):
        super().__init__(master)
        self.state = state
        self.wizard = wizard

        tk.Label(self, text="Podgląd karty postaci:", font=("Arial", 16)).pack(pady=10)
        self.preview_text = tk.Text(self, height=20, width=80)
        self.preview_text.pack(pady=10)

        self.update_preview()
        tk.Button(self, text="Eksportuj do PDF", command=self.export_to_pdf).pack(pady=10)

    def update_preview(self):
        state = self.state.data
        class_data = state.get("class", {})
        background_data = state.get("background", {})
        # Handle proficiencies as a list directly
        proficiencies = state.get("proficiencies", [])
        preview = f"""DUNGEONS & DRAGONS
Klasa i Poziom: {class_data.get('name', {}).get('pl', 'Brak')}
Tło: {background_data.get('name', {}).get('pl', 'Brak')}
Imię Gracza: {state.get('name', 'Brak')}
Rasa: {state.get('race', 'Brak')}
Wyrównanie: {state.get('alignment', 'Brak')}
Punkty Doświadczenia: {state.get('experience_points', 0)}
Wyposażenie: {', '.join(state.get('equipment', [])) or 'Brak'}
Umiejętności: {', '.join(proficiencies) or 'Brak'}
Czarostwo: {', '.join(state.get('spells', [])) or 'Brak'}"""
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)

    def export_to_pdf(self):
        state = self.state.data
        class_data = state.get("class", {})
        background_data = state.get("background", {})
        proficiencies = state.get("proficiencies", [])
        latex_content = r"""
\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[polish]{babel}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

% Preamble for D&D character sheet styling
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\rhead{Dungeons \& Dragons}
\lhead{Karta Postaci}
\usepackage{enumitem}
\usepackage{booktabs}

\begin{document}

\begin{center}
{\Large DUNGEONS \& DRAGONS}\\[0.5cm]
{\Large Karta Postaci}\\[1cm]
\end{center}

\begin{tabular}{ll}
\toprule
Klasa i Poziom & {class_data.get('name', {}).get('pl', 'Brak')}\\[0.1cm] \\
Tło & {background_data.get('name', {}).get('pl', 'Brak')}\\[0.1cm] \\
Imię Gracza & {state.get('name', 'Brak')}\\[0.1cm] \\
Rasa & {state.get('race', 'Brak')}\\[0.1cm] \\
Wyrównanie & {state.get('alignment', 'Brak')}\\[0.1cm] \\
Punkty Doświadczenia & {state.get('experience_points', 0)}\\[0.1cm] \\
\end{tabular}

\section*{Wyposażenie}
\begin{itemize}
    \item {', '.join(state.get('equipment', [])) or 'Brak'}
\end{itemize}

\section*{Umiejętności}
\begin{itemize}
    \item {', '.join(proficiencies) or 'Brak'}
\end{itemize}

\section*{Czarostwo}
\begin{itemize}
    \item {', '.join(state.get('spells', [])) or 'Brak'}
\end{itemize}

% Placeholder for image if provided
{image_placeholder}

\end{document}
""".format(
    class_data=class_data,
    background_data=background_data,
    state=state,
    proficiencies=proficiencies,
    image_placeholder=r"\section*{Obrazek}" if state.get("image_path") else ""
)

        with open("character_sheet.tex", "w", encoding="utf-8") as f:
            f.write(latex_content)

        try:
            subprocess.run(["latexmk", "-pdf", "character_sheet.tex"], check=True)
            os.startfile("character_sheet.pdf")
        except subprocess.CalledProcessError as e:
            tk.messagebox.showerror("Błąd", f"Nie udało się wygenerować PDF: {e}")
        except FileNotFoundError:
            tk.messagebox.showerror("Błąd", "latexmk nie jest zainstalowany. Zainstaluj TeX Live.")