import sqlite3

# Підключаємося до бази даних SQLite
conn = sqlite3.connect('word_frequencies.db')

# Функція для підрахунку лексем у таблиці тексту
def count_lexemes(table_name):
    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor = conn.execute(query)
    result = cursor.fetchone()[0]
    return result

# Таблиці текстів
texts = ['text1', 'text2', 'text3', 'text4']

# Підрахунок лексем для кожного тексту
lexeme_counts = {}
for text in texts:
    lexeme_counts[text] = count_lexemes(text)

# Виведення результатів
for text, count in lexeme_counts.items():
    print(f"Кількість лексем у {text}: {count}")

# Закриваємо з'єднання з базою даних
conn.close()