import tkinter as tk
from tkinter import scrolledtext, messagebox
import stanza
import pandas as pd

# Завантаження моделі (запускається один раз)
stanza.download('uk')
nlp = stanza.Pipeline('uk')

# Переклад тегів частин мови
pos_translation = {
    'ADJ': 'прикметник',
    'ADP': 'прийменник',
    'ADV': 'прислівник',
    'AUX': 'допоміжне дієслово',
    'CCONJ': 'сурядний сполучник',
    'DET': 'визначник',
    'INTJ': 'вигук',
    'NOUN': 'іменник',
    'NUM': 'числівник',
    'PART': 'частка',
    'PRON': 'займенник',
    'PROPN': 'власна назва',
    'PUNCT': 'розділовий знак',
    'SCONJ': 'підрядний сполучник',
    'SYM': 'символ',
    'VERB': 'дієслово',
    'X': 'невизначене',
}

# Функція аналізу тексту
def analyze_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Помилка", "Будь ласка, введіть текст.")
        return

    doc = nlp(text)
    word_pos = [(word.text, pos_translation.get(word.upos, word.upos)) for sentence in doc.sentences for word in sentence.words]
    df = pd.DataFrame(word_pos, columns=["Слово", "Частина мови"])

    total = len(df)
    coverage = df['Частина мови'].value_counts(normalize=True) * 100
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, f"Загальна кількість слів: {total}\n\n")
    result_output.insert(tk.END, "Покриття тексту за частинами мови:\n")
    for pos, percent in coverage.items():
        result_output.insert(tk.END, f"{pos}: {percent:.2f}%\n")

# Створення вікна
window = tk.Tk()
window.title("Автоматизована класифікація частин мови")
window.geometry("800x600")

tk.Label(window, text="Введіть текст для аналізу:").pack()
text_input = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=15)
text_input.pack(pady=5)

analyze_button = tk.Button(window, text="Аналізувати", command=analyze_text)
analyze_button.pack(pady=10)

result_output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=15)
result_output.pack()

window.mainloop()