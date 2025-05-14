import nltk
import random
import matplotlib.pyplot as plt
from nltk.corpus import movie_reviews
from nltk import FreqDist
from nltk.classify import NaiveBayesClassifier, SklearnClassifier
from nltk.classify.util import accuracy
from sklearn.svm import SVC

# Завантаження корпусу
nltk.download('movie_reviews')

print("=== Сентимент-аналіз фільмових відгуків ===")
print("Завантаження даних...")

# Отримання списку відгуків та їх категорій
reviews = []
for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        review_words = list(movie_reviews.words(fileid))
        reviews.append((review_words, category))

random.shuffle(reviews)

# Формування частотного словника (без пунктуації)
all_words = [word.lower() for word in movie_reviews.words() if word.isalpha()]
all_words_freq = FreqDist(all_words)

# Функція: побудова графіка частотних слів
def plot_top_words(freq_dist, n=20):
    top_words = freq_dist.most_common(n)
    words = [w for w, _ in top_words]
    counts = [c for _, c in top_words]

    plt.figure(figsize=(12, 6))
    plt.bar(words, counts)
    plt.title(f"Топ {n} найчастотніших слів у корпусі movie_reviews")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Опція: показати топ-слів
show_graph = input("Бажаєте побачити графік найчастотніших слів у корпусі? (так/ні): ").strip().lower()
if show_graph == 'так':
    print("\n🔎 Цей графік демонструє 20 найуживаніших слів у корпусі англомовних фільмових відгуків з NLTK (movie_reviews).")
    plot_top_words(all_words_freq)

# Слова, які можна обрати для аналізу
available_words = ["good", "bad", "practical", "fun", "boring"]
print("\nОберіть слово для аналізу з цього списку:")
print(", ".join(available_words))
selected_word = input("Введіть слово: ").strip().lower()

# Перевірка, чи слово з доступного списку
if selected_word not in available_words:
    print("❌ Слово не з доступного списку. Завершення програми.")
    exit()

# Частота слова в усьому корпусі, позитивних і негативних відгуках
total_count = all_words_freq[selected_word]
positive_reviews = [w.lower() for w in movie_reviews.words(categories='pos')]
negative_reviews = [w.lower() for w in movie_reviews.words(categories='neg')]
pos_count = FreqDist(positive_reviews)[selected_word]
neg_count = FreqDist(negative_reviews)[selected_word]

# Вивід статистики
print(f"\nСлово «{selected_word}» загалом зустрічається: {total_count} раз(ів)")
print(f"У позитивних відгуках: {pos_count}")
print(f"У негативних відгуках: {neg_count}")

# Побудова ознак для класифікаторів
word_features = list(all_words_freq)[:3600]
def find_features(document_words):
    words = set(w.lower() for w in document_words if w.isalpha())
    return {w: (w in words) for w in word_features}

featuresets = [(find_features(words), category) for (words, category) in reviews]
random.shuffle(featuresets)
train_set, test_set = featuresets[:1800], featuresets[1800:]

# Навчання Naive Bayes
classifier = NaiveBayesClassifier.train(train_set)
nb_accuracy = accuracy(classifier, test_set) * 100
print(f"\n Точність класифікатора Naive Bayes: {nb_accuracy:.2f}%")

# Навчання SVC
svc_classifier = SklearnClassifier(SVC(kernel='linear'))
svc_classifier.train(train_set)
svc_accuracy = accuracy(svc_classifier, test_set) * 100
print(f" Точність класифікатора SVC: {svc_accuracy:.2f}%")

# Побудова графіка точності
def plot_accuracy(nb_acc, svc_acc):
    classifiers = ['Naive Bayes', 'SVC']
    accuracies = [nb_acc, svc_acc]

    plt.figure(figsize=(6, 4))
    plt.bar(classifiers, accuracies, color=['skyblue', 'lightgreen'])
    plt.ylabel('Точність (%)')
    plt.title('Порівняння класифікаторів')
    plt.ylim(0, 100)
    for i, acc in enumerate(accuracies):
        plt.text(i, acc + 1, f"{acc:.2f}%", ha='center')
    plt.tight_layout()
    plt.show()

# Опція: показати графік порівняння класифікаторів
show_acc = input("\nБажаєте побачити графік точності класифікаторів? (так/ні): ").strip().lower()
if show_acc == 'так':
    plot_accuracy(nb_accuracy, svc_accuracy)

# Збереження результатів
with open("results.txt", "w", encoding="utf-8") as f:
    f.write("Результати сентимент-аналізу\n")
    f.write(f"Слово: {selected_word}\n")
    f.write(f"Загальна частота: {total_count}\n")
    f.write(f"У позитивних: {pos_count}\n")
    f.write(f"У негативних: {neg_count}\n")
    f.write(f"Точність Naive Bayes: {nb_accuracy:.2f}%\n")
    f.write(f"Точність SVC: {svc_accuracy:.2f}%\n")

print("\n Аналіз завершено. Результати збережено у файл 'results.txt'.")