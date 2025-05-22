import tkinter as tk
from tkinter import messagebox, ttk
import random

class GrammarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Граматика італійської мови")
        self.correct_answers = 0
        self.total_questions = 0
        self.font_main = ("Arial", 12)
        self.font_bold = ("Arial", 12, "bold")

        self.setup_interface()

    def setup_interface(self):
        self.notebook = ttk.Notebook(self.root)
        self.frame_theory = ttk.Frame(self.notebook)
        self.frame_test = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_theory, text="Теорія")
        self.notebook.add(self.frame_test, text="Тест")
        self.notebook.pack(expand=True, fill="both")

        self.create_theory_tab()
        self.create_test_tab()

    def create_theory_tab(self):
        theory_text = (
            "В італійській мові дієслова змінюються за часами, особами та числами. "
            "Основні часи: Presente (теперішній) і Imperfetto (минулий незавершений).\n\n"
            "Presente описує дію, що триває зараз або має постійний характер. "
            "Наприклад: Parlo italiano (Я розмовляю італійською).\n\n"
            "Imperfetto передає незавершену або повторювану дію в минулому. "
            "Наприклад: Parlavo con lui ogni giorno (Я розмовляв з ним щодня). "
            "Закінчення: -vo, -vi, -va, -vamo, -vate, -vano.\n"
        )
        label = tk.Label(self.frame_theory, text=theory_text, wraplength=550, justify="left", font=self.font_main)
        label.pack(pady=20, padx=20)

    def create_test_tab(self):
        self.verb_forms = {
            "1 особа однини (Presente)": "parlo",
            "2 особа однини (Presente)": "parli",
            "3 особа однини (Presente)": "parla",
            "1 особа множини (Presente)": "parliamo",
            "2 особа множини (Presente)": "parlate",
            "3 особа множини (Presente)": "parlano",
            "1 особа однини (Imperfetto)": "parlavo",
            "2 особа однини (Imperfetto)": "parlavi",
            "3 особа однини (Imperfetto)": "parlava",
            "1 особа множини (Imperfetto)": "parlavamo",
            "2 особа множини (Imperfetto)": "parlavate",
            "3 особа множини (Imperfetto)": "parlavano"
        }

        self.question_label = tk.Label(self.frame_test, text="", font=self.font_main)
        self.question_label.pack(pady=20)

        self.radio_var = tk.StringVar()
        self.radio_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(self.frame_test, text="", variable=self.radio_var, value="", font=self.font_main)
            btn.pack(anchor="w")
            self.radio_buttons.append(btn)

        self.submit_button = tk.Button(self.frame_test, text="Відповісти", command=self.check_answer, font=self.font_bold)
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(self.frame_test, text="", font=self.font_main)
        self.score_label.pack(pady=5)

        self.next_button = tk.Button(self.frame_test, text="Наступне питання", command=self.generate_question, font=self.font_main)
        self.next_button.pack(pady=5)

        self.generate_question()

    def generate_question(self):
        self.correct_question, self.correct_answer = random.choice(list(self.verb_forms.items()))
        self.question_label.config(text=f"{self.correct_question} для дієслова 'parlare':")
        self.radio_var.set("")

        all_answers = list(self.verb_forms.values())
        incorrect_answers = random.sample([a for a in all_answers if a != self.correct_answer], 3)
        options = [self.correct_answer] + incorrect_answers
        random.shuffle(options)

        for btn, answer in zip(self.radio_buttons, options):
            btn.config(text=answer, value=answer)

    def check_answer(self):
        selected = self.radio_var.get()
        if not selected:
            messagebox.showwarning("Увага", "Будь ласка, оберіть варіант відповіді.")
            return

        self.total_questions += 1
        if selected == self.correct_answer:
            self.correct_answers += 1
            messagebox.showinfo("Результат", "Правильно!")
        else:
            messagebox.showerror("Результат", f"Ні, правильна відповідь: {self.correct_answer}")

        self.update_score()
        self.generate_question()

    def update_score(self):
        self.score_label.config(
            text=f"Правильних відповідей: {self.correct_answers} із {self.total_questions}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = GrammarApp(root)
    root.mainloop()