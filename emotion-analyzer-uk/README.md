# 📝 Емоційний аналіз українських поетичних текстів

## Опис
Ця програма виконує автоматизований **морфологічний** та **емоційний аналіз** українських текстів. Користувач може вставити власний текст або обрати текстовий файл, після чого програма:
- визначає частини мови для кожного слова (через `Stanza`),
- обчислює покриття тексту частинами мови,
- виконує **лематизацію** (`pymorphy3`),
- зіставляє слова зі **словником емоційного тону**,
- виділяє позитивні й негативні слова,
- зберігає результати в SQLite-базу,
- будує кругову діаграму,
- виводить **топ-10 позитивних** і **топ-10 негативних** слів.

---

## Технології
- Python 
- Stanza
- Pandas
- Pymorphy3
- SQLite3
- Matplotlib
- Tkinter

---

## Запуск

1. Встановити бібліотеки:
```bash
pip install stanza pandas pymorphy3 matplotlib
```

2. Завантажити модель Stanza:
```python
import stanza
stanza.download('uk')
```

3. Запустити програму:
```bash
python main.py
```

---

## Вхідні дані

- Вставлений текст або .txt-файл
- Емоційний словник: tone-dict-uk.tsv


