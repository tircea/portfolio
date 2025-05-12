import re
import sqlite3
from collections import Counter
from typing import List, Tuple
import stanza

# Завантаження моделі для української мови
stanza.download("uk")  # Завантажується один раз
nlp = stanza.Pipeline("uk", processors="tokenize,pos,lemma")

def clean_and_tokenize(text: str) -> List[str]:
    # Видалення рядків з "Автор" і номерами текстів
    text = re.sub(r'(?i)Автор\s\d+\s*-.*\n', '', text)
    text = re.sub(r'Текст\s\d+:', '', text)

    # Видалення специфічних символів, залишаючи слова з дефісами і апострофами
    text = re.sub(r'(?<!\w)-(?!\w)', ' ', text)  # Залишає дефіси в словах
    text = re.sub(r'[0-9"%,]', '', text)  # Видаляє % та інші зайві символи
    text = re.sub(r' [-]+', ' ', text)
    text = re.sub(r'[^\wʼ\'\-\s]', ' ', text)  # Зберігає апострофи (ʼ) та дефіси
    text = re.sub(r'--', '', text)  
    text = re.sub(r'\'\'', '', text) 

    # Видалення скорочень типу ст., м., р., тис.
    text = re.sub(r'\b(?:ст|м|р|тис)\.\b', '', text)

    # Заміна зайвих пробілів
    text = re.sub(r'\s+', ' ', text).strip().lower()

    # Токенізація (розбиття на слова)
    tokens = text.split()

    # Фільтрація коротких токенів (менше 2 символів, крім слів через дефіс або апостроф)
    allowed_short_words = {"і", "й", "о", "або"}  # Дозволені короткі слова
    tokens = [token for token in tokens if len(token) > 1 or token in allowed_short_words or '-' in token or 'ʼ' in token]

    return tokens

def get_pos_tags(tokens: List[str]) -> List[Tuple[str, str, str]]:
    doc = nlp(" ".join(tokens))
    pos_tags = []
    for sentence in doc.sentences:
        for word in sentence.words:
            # Зберігаємо оригінальне слово як лему для абревіатур та слів з апострофом
            if word.text.isupper() or 'ʼ' in word.text:
                lemma = word.text
            else:
                lemma = word.lemma
            pos_tags.append((word.text, lemma, word.upos))
    return pos_tags

def save_to_file(tokens: List[str], filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(tokens))

def save_to_database(word_freq: Counter, pos_tags: List[Tuple[str, str, str]], db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Створення таблиці для загального частотного словника
    cursor.execute('''CREATE TABLE IF NOT EXISTS frequency_dict (
                        word TEXT PRIMARY KEY,
                        lemma TEXT,
                        frequency INTEGER,
                        pos TEXT
                      )''')

    # Створення таблиць для іменників, дієслів і прикметників
    cursor.execute('''CREATE TABLE IF NOT EXISTS nouns (
                        word TEXT PRIMARY KEY,
                        lemma TEXT,
                        frequency INTEGER
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS verbs (
                        word TEXT PRIMARY KEY,
                        lemma TEXT,
                        frequency INTEGER
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS adjectives (
                        word TEXT PRIMARY KEY,
                        lemma TEXT,
                        frequency INTEGER
                      )''')

    # Об'єднання частот і частин мови
    word_data = [(word, lemma, freq, pos) for word, lemma, pos in pos_tags for freq in [word_freq[word]]]

    # Додавання даних до загальної таблиці
    cursor.executemany('INSERT OR REPLACE INTO frequency_dict (word, lemma, frequency, pos) VALUES (?, ?, ?, ?)', word_data)

    # Розподіл по таблицях за частинами мови
    for word, lemma, freq, pos in word_data:
        if pos == "NOUN":
            cursor.execute('INSERT OR REPLACE INTO nouns (word, lemma, frequency) VALUES (?, ?, ?)', (word, lemma, freq))
        elif pos == "VERB":
            cursor.execute('INSERT OR REPLACE INTO verbs (word, lemma, frequency) VALUES (?, ?, ?)', (word, lemma, freq))
        elif pos == "ADJ":
            cursor.execute('INSERT OR REPLACE INTO adjectives (word, lemma, frequency) VALUES (?, ?, ?)', (word, lemma, freq))

    conn.commit()
    conn.close()

def main():
    input_file = '/Users/tircea/Desktop/Study/2 сем/Автоматичний аналіз тексту/ПроєктЧС/corpus.txt'  # Змінити на шлях до вашого файлу
    tokenized_file = 'tokenized.txt'
    database_file = 'frequency_dict.db'

    # Зчитування вхідного файлу
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Очищення та токенізація тексту
    tokens = clean_and_tokenize(raw_text)

    # Збереження токенізованого тексту у файл
    save_to_file(tokens, tokenized_file)

    # Отримання частин мови та лем
    pos_tags = get_pos_tags(tokens)

    # Підрахунок частоти слів
    word_freq = Counter(tokens)

    # Збереження частотного словника в базу даних
    save_to_database(word_freq, pos_tags, database_file)

if __name__ == "__main__":
    main()
