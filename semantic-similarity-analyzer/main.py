import nltk
from nltk.corpus import wordnet as wn
from nltk.metrics.distance import edit_distance
from collections import Counter
import re

# Завантаження ресурсів WordNet
nltk.download('wordnet')

# Вивід персональної інформації
def print_personal_info():
    print("Ім'я: Владислава")
    print("Прізвище: Сірко")
    print("Проєкт: Аналіз семантичної подібності")

# Виведення визначень слова
def print_definitions(word):
    synsets = wn.synsets(word)
    for i, synset in enumerate(synsets):
        print(f"Визначення {i+1} слова {word}: {synset.definition()}")

# Гіпоніми та гіпероніми
def print_hyponyms_hypernyms(word):
    synsets = wn.synsets(word)
    for synset in synsets:
        hyponyms = synset.hyponyms()
        hypernyms = synset.hypernyms()
        print(f"\nСлово {word} — {synset.name()}")
        print("Гіпоніми:",  [lemma.name().replace('_', ' ') for hypo in hyponyms for lemma in hypo.lemmas()])
        print("Гіпероніми:", [lemma.name().replace('_', ' ') for hyper in hypernyms for lemma in hyper.lemmas()])

# Спільний гіперонім
def find_common_hypernym(word1, word2):
    syn1 = wn.synsets(word1, 'n')[0]
    syn2 = wn.synsets(word2, 'n')[0]
    common = syn1.lowest_common_hypernyms(syn2)
    if common:
        lemma = common[0].lemmas()[0].name().replace('_', ' ')
        print(f"Спільний гіперонім для {word1} і {word2}: {lemma}")

# Метрики семантичної подібності
def print_similarity_metrics(word1, word2):
    syn1 = wn.synsets(word1, 'n')[0]
    syn2 = wn.synsets(word2, 'n')[0]
    print("Path Similarity:", syn1.path_similarity(syn2))
    print("Wu–Palmer Similarity:", syn1.wup_similarity(syn2))
    print("Leacock–Chodorow Similarity:", syn1.lch_similarity(syn2))

# Відстані Левенштейна та Дамерау–Левенштейна
def print_edit_distances(w1, w2):
    print("Відстань Левенштейна:", edit_distance(w1, w2))
    print("Відстань Дамерау–Левенштейна:", edit_distance(w1, w2, transpositions=True))

# Пошук схожих слів у файлі
def find_similar_words(word, file_path, top_n=4):
    with open(file_path, 'r') as f:
        words = f.read().splitlines()
    distances = [(w, edit_distance(word, w)) for w in words]
    distances.sort(key=lambda x: x[1])
    print(f"\nТоп {top_n} найближчих слів до '{word}':")
    for i, (w, dist) in enumerate(distances[:top_n], 1):
        print(f"{i}. {w} (Дистанція: {dist})")

# Аналіз тексту і збереження частот
def analyze_text_file(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read().lower()
    words = re.findall(r'\b\w+\b', text)
    freq = Counter(words)
    with open(output_file, 'w') as f_out:
        for word, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
            f_out.write(f"{word}\n")

def main():
    print_personal_info()
    word1, word2 = "cat", "rat"

    print("\nВизначення слів:")
    print_definitions(word1)
    print_definitions(word2)

    print("\nГіпоніми та гіпероніми:")
    print_hyponyms_hypernyms(word1)
    print_hyponyms_hypernyms(word2)

    print("\nСпільний гіперонім:")
    find_common_hypernym(word1, word2)

    print("\nМетрики семантичної подібності:")
    print_similarity_metrics(word1, word2)

    print("\nВідстані між словами:")
    print_edit_distances(word1, word2)

    # Пошук схожих слів
    user_input = input("\nВведіть англійське слово для пошуку подібних: ")
    find_similar_words(user_input, "1-1000.txt")

    # Аналіз тексту
    analyze_text_file("edgeworth-parents.txt", "sorted_words.txt")
    print("\nАналіз завершено. Перевірте файл 'sorted_words.txt'.")

if __name__ == "__main__":
    main()