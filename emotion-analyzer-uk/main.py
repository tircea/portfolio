import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd
import sqlite3
import stanza
from collections import Counter

# Завантаження моделі
stanza.download('uk')
nlp = stanza.Pipeline('uk')

# Кольори
BG_COLOR = "#262220"  # Темний фон загального вікна
PANEL_BG = "#F7F1F0"  # Фон для текстових блоків
TEXT_COLOR = "#262220"
BUTTON1_COLOR = "#C3A6A0"
BUTTON2_COLOR = "#A15C38"
FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

# Переклад POS-тегів
pos_translation = {
    'ADJ': 'прикметник', 'ADP': 'прийменник', 'ADV': 'прислівник',
    'AUX': 'допоміжне дієслово', 'CCONJ': 'сурядний сполучник',
    'DET': 'визначник', 'INTJ': 'вигук', 'NOUN': 'іменник',
    'NUM': 'числівник', 'PART': 'частка', 'PRON': 'займенник',
    'PROPN': 'власна назва', 'PUNCT': 'розділовий знак',
    'SCONJ': 'підрядний сполучник', 'SYM': 'символ',
    'VERB': 'дієслово', 'X': 'невизначене',
}

# Завантаження словника емоцій
def load_emotion_dict(path='tone-dict-uk.tsv'):
    df = pd.read_csv(path, sep='\t', header=None, names=['word', 'tone'])
    return df.set_index('word')['tone'].to_dict()

emotion_dict = load_emotion_dict()

# Аналіз тексту
def analyze_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Помилка", "Будь ласка, введіть або завантажте текст.")
        return

    doc = nlp(text)
    word_pos = [(word.text.lower(), word.upos) for sentence in doc.sentences for word in sentence.words]
    df = pd.DataFrame(word_pos, columns=["Слово", "POS"])
    df["Частина мови"] = df["POS"].map(pos_translation)
    df.dropna(inplace=True)

    total = len(df)
    coverage = df['Частина мови'].value_counts(normalize=True) * 100

    # Емоційні слова
    freqs = Counter([word for word, pos in word_pos])
    positive, negative = [], []
    for word, freq in freqs.items():
        tone = emotion_dict.get(word)
        if tone is not None:
            if tone > 0:
                positive.append((word, freq))
            elif tone < 0:
                negative.append((word, freq))

    # Збереження в БД
    conn = sqlite3.connect("emotion_words.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS PositiveWords (word TEXT, frequency INTEGER)")
    cursor.execute("DELETE FROM PositiveWords")
    cursor.executemany("INSERT INTO PositiveWords VALUES (?, ?)", sorted(positive, key=lambda x: -x[1])[:10])
    cursor.execute("CREATE TABLE IF NOT EXISTS NegativeWords (word TEXT, frequency INTEGER)")
    cursor.execute("DELETE FROM NegativeWords")
    cursor.executemany("INSERT INTO NegativeWords VALUES (?, ?)", sorted(negative, key=lambda x: -x[1])[:10])
    conn.commit()
    conn.close()

    # Вивід
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, f"Загальна кількість слів: {total}\n\n")
    result_output.insert(tk.END, "Покриття тексту за частинами мови:\n")
    for pos, percent in coverage.items():
        result_output.insert(tk.END, f"{pos}: {percent:.2f}%\n")

    result_output.insert(tk.END, "\nНайчастотніші позитивні слова:\n")
    for word, freq in sorted(positive, key=lambda x: -x[1])[:10]:
        result_output.insert(tk.END, f"{word}: {freq}\n")

    result_output.insert(tk.END, "\nНайчастотніші негативні слова:\n")
    for word, freq in sorted(negative, key=lambda x: -x[1])[:10]:
        result_output.insert(tk.END, f"{word}: {freq}\n")

# Завантаження тексту з файлу
def load_text_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, f.read())

# Створення вікна
window = tk.Tk()
window.title("Аналіз частин мови та емоційного тону")
window.configure(bg=BG_COLOR)
window.geometry("900x700")

tk.Label(window, text="Введіть або вставте текст для аналізу:",
         bg=BG_COLOR, fg="white", font=("Segoe UI", 11, "bold")).pack(pady=(10, 4))

# Біле поле для вводу
text_input = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=12,
                                       font=FONT_MAIN, bg=PANEL_BG, fg=TEXT_COLOR)
text_input.pack(pady=4)

# Кнопки
btn_frame = tk.Frame(window, bg=BG_COLOR)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Завантажити .txt", font=FONT_BOLD,
          bg="#C3A6A0", fg="white", activebackground="#a68b88",
          activeforeground="white", relief="ridge", bd=2,
          command=load_text_file).pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame, text="Аналізувати текст", font=FONT_BOLD,
          bg="#C3A6A0", fg="white", activebackground="#a68b88",
          activeforeground="white", relief="ridge", bd=2,
          command=analyze_text).pack(side=tk.LEFT, padx=10)

tk.Label(window, text="Результати аналізу:", bg=BG_COLOR,
         fg="white", font=("Segoe UI", 11, "bold")).pack(pady=(20, 4))

# Біле поле для результатів
result_output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=18,
                                          font=FONT_MAIN, bg=PANEL_BG, fg=TEXT_COLOR)
result_output.pack()

window.mainloop()