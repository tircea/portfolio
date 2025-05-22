import sqlite3
import tkinter as tk
from tkinter import ttk

DB_PATH = 'dictionary.db'

class DictionaryApp:
    def __init__(self, root):
        root.title("Сірко Владислава, 1 група, ЛР №3")
        root.geometry("600x400")
        
        tab_control = ttk.Notebook(root)
        self.tab_dictionary = ttk.Frame(tab_control)
        self.tab_about = ttk.Frame(tab_control)
        tab_control.add(self.tab_dictionary, text="Словник")
        tab_control.add(self.tab_about, text="Про автора")
        tab_control.pack(expand=1, fill="both")
        
        self.setup_about_tab()
        self.setup_dictionary_tab()

        self.conn = sqlite3.connect(DB_PATH)
        self.load_categories()
        self.load_table_data()

    def setup_about_tab(self):
        label_me = tk.Label(self.tab_about, text="Мене звати Сірко Владислава. \nЯ студентка 4-го курсу прикладної лінгвістики, 1 групи.", font=("Arial", 16, "bold"))
        label_me.pack(expand=True)

    def setup_dictionary_tab(self):

        tk.Label(self.tab_dictionary, text="Категорія:", font=("Arial", 12)).pack(pady=10)
        self.category_combo = ttk.Combobox(self.tab_dictionary, state="readonly")
        self.category_combo.pack()
        self.category_combo.bind("<<ComboboxSelected>>", self.update_table_by_category)
        
        table_frame = ttk.Frame(self.tab_dictionary)
        table_frame.pack(expand=True, fill="both", pady=10)
        
        self.table = ttk.Treeview(table_frame, columns=("ID", "Category", "Foreign Word", "Translation"), show="headings")
        self.table.heading("ID", text="ID")
        self.table.heading("Category", text="Категорія")
        self.table.heading("Foreign Word", text="Слово іноземною")
        self.table.heading("Translation", text="Переклад українською")
        self.table.bind("<<TreeviewSelect>>", self.on_table_select)
        self.table.grid(row=0, column=0, sticky="nsew")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.table.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        
        self.selected_label = tk.Label(self.tab_dictionary, text="", font=("Arial", 12))
        self.selected_label.pack(pady=10)

    def load_categories(self):

        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM vocab")
        categories = [row[0] for row in cursor.fetchall()]
        categories.insert(0, "-- Усі категорії --")
        self.category_combo['values'] = categories
        self.category_combo.current(0)  

    def load_table_data(self, category=None):

        cursor = self.conn.cursor()
        query = "SELECT ID, category, foreign_word, translation FROM vocab"
        params = ()
        
        if category and category != "-- Усі категорії --":
            query += " WHERE category = ?"
            params = (category,)
        
        query += " ORDER BY foreign_word COLLATE NOCASE ASC" 
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        for row in self.table.get_children():
            self.table.delete(row)
        
        for row in rows:
            self.table.insert("", "end", values=row)
    
    def update_table_by_category(self, event):

        selected_category = self.category_combo.get()
        self.load_table_data(selected_category)

    def on_table_select(self, event):

        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item)
            foreign_word = item['values'][2]
            translation = item['values'][3]
            self.selected_label.config(text=f"{foreign_word} — {translation}")

    def run(self):
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.mainloop()
        
    def on_close(self):
        self.conn.close()
        root.destroy()

root = tk.Tk()
app = DictionaryApp(root)
app.run()