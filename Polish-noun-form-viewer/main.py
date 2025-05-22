import tkinter as tk
from tkinter import ttk
import sqlite3

def connect_to_db():
    global conn
    conn = sqlite3.connect('pol_lab02.s3db')
    cursor = conn.cursor()
    cursor.execute("SELECT sgN FROM tnoun LIMIT 1")
    result = cursor.fetchone()
    if result:
        label_result.config(text=f"Слово: {result[0]}")
    
    cursor.execute("SELECT sgN FROM tnoun WHERE sgN LIKE 'O%' LIMIT 1")
    word_o = cursor.fetchone()
    if word_o:
        label_o_word.config(text=f"Слово на 'O': {word_o[0]}")
    
    cursor.close()

def fill_table():
    cursor = conn.cursor()
    cursor.execute("SELECT id, sgN, sgG FROM tnoun ORDER BY RANDOM() LIMIT 12")
    words = cursor.fetchall()
    
    for row in tree.get_children():
        tree.delete(row)
    
    for idx, (word_id, sgN, sgG) in enumerate(words, start=1):
        sgN = sgN if sgN else "-"
        sgG = sgG if sgG else "-"
        tree.insert('', tk.END, values=(idx, sgN, sgG))
    
    cursor.execute("SELECT sgN FROM tnoun WHERE sgN LIKE 'O%'")
    o_words = [row[0] for row in cursor.fetchall()]
    
    combobox['values'] = o_words
    
    cursor.close()

def combobox_selected(event):
    selected_word = combobox.get()
    label_result.config(text=f"Обране слово: {selected_word}")

window = tk.Tk()
window.title("Сірко Владислава, 1 група, ЛР №2")
window.geometry('800x500')  

#Label
label_result = tk.Label(window, text="Результат SQL-запиту", font=("Arial", 16))
label_result.pack(pady=10)

label_o_word = tk.Label(window, text="Слово на 'O'", font=("Arial", 16))
label_o_word.pack(pady=10)


#Button
button_fill = tk.Button(window, text="Заповнити таблицю", command=fill_table)
button_fill.pack(pady=10)

#ComboBox
combobox = ttk.Combobox(window)
combobox.pack(pady=10)
combobox.bind("<<ComboboxSelected>>", combobox_selected)


frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)

columns = ('#1', '#2', '#3')
tree = ttk.Treeview(
    frame, columns=columns, show='headings',
    yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set
)

tree.heading('#1', text='№')
tree.heading('#2', text='Називний відмінок (sgN)')
tree.heading('#3', text='Родовий відмінок (sgG)')
tree.column('#1', width=50)
tree.column('#2', width=200)
tree.column('#3', width=200)

scrollbar_y.config(command=tree.yview)
scrollbar_x.config(command=tree.xview)

scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
tree.pack(fill=tk.BOTH, expand=True)

connect_to_db()

window.mainloop()