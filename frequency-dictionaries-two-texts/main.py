import tokenize_uk
import pymorphy3
import json
import sys
from collections import Counter

from sqlLib import SQL
from funcs import extractTextPDF, parseWords, divide_into_samples, list_chunk

def checkTables(db):
    f = open('tables.json', encoding="utf-8")
    data = json.load(f)
    for tableName in data:
        tableParams = data[tableName]
        if not db.table_exists(tableName):
            db.createTable(tableName, tableParams)
            print("Creating table", tableName)


morph = pymorphy3.MorphAnalyzer(lang='uk')
if len(sys.argv) < 2:
    print("Usage: python main.py <filename>\nExample: python main.py text1.pdf\n")
    exit()

fileText = sys.argv[1]
print("Start reading file")
try:
    if fileText.split(".")[-1] == "pdf":
        text = extractTextPDF(fileText)
    else:
        f = open(fileText, "r", encoding="utf-8")
        text = f.read()
except:
  print("File not found!")
  exit()

db = SQL(fileText+'.frequency_dict.db')
checkTables(db)
print("File readed")
words = tokenize_uk.tokenize_uk.tokenize_words(text)
print("Parsing words...")
result, parsedWords, chastiMovi = parseWords(words, morph)

chastiMoviStart = list_chunk(chastiMovi, 20_000)[0] 
viborka = list_chunk(result, 20_000)[0]

chastiMovi = list(divide_into_samples(chastiMoviStart))
chastiMovi = [Counter(chastMovi) for chastMovi in chastiMovi]

samples = list(divide_into_samples(viborka))
sample_frequencies = [Counter(sample) for sample in samples]

print("Inserting values into ЧС_словоформ and ЧС_лем table...")
for cur_word in set(viborka):
    freqs = []
    parsedWord = parsedWords[cur_word]
    for sample_freq in sample_frequencies:
        sample_freq = dict(sample_freq)
        if cur_word in sample_freq:
            freq = sample_freq[cur_word]
        else:
            freq = 0
        freqs.append(freq)
    req = """
    INSERT INTO ЧС_словоформ (словоформа, обща_частота, підв_1, підв_2, підв_3, підв_4, підв_5, підв_6, підв_7, підв_8, підв_9, 
                            підв_10, підв_11, підв_12, підв_13, підв_14, підв_15, підв_16, підв_17, підв_18, підв_19, підв_20) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = [cur_word, sum(freqs)] + freqs
    db.executeSql(req, params)
    normalForm = parsedWord.normal_form
    params = [normalForm, sum(freqs)] + freqs

    data = db.fetch("SELECT * from ЧС_лем where лема=?", [normalForm])

    if data:
        data = list(data)
        data.pop(0)
        newFreqs = ([sum(freqs)] + freqs)
        newFreqs = [x + y for x, y in zip(newFreqs, data)]
        db.executeSql("""
        UPDATE ЧС_лем SET обща_частота = ?, підв_1 = ?, підв_2 = ?, підв_3 = ?, підв_4 = ?, підв_5 = ?, підв_6 = ?, підв_7 = ?, підв_8 = ?, підв_9 = ?, 
                            підв_10 = ?, підв_11 = ?, підв_12 = ?, підв_13 = ?, підв_14 = ?, підв_15 = ?, підв_16 = ?, підв_17 = ?, підв_18 = ?, 
                            підв_19 = ?, підв_20 = ? WHERE лема = ?;
        """, newFreqs+[normalForm])
    else:
        req = """
        INSERT INTO ЧС_лем (лема, обща_частота, підв_1, підв_2, підв_3, підв_4, підв_5, підв_6, підв_7, підв_8, підв_9, 
                                підв_10, підв_11, підв_12, підв_13, підв_14, підв_15, підв_16, підв_17, підв_18, підв_19, підв_20) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.executeSql(req, params)
    

print("Inserting values into ЧС_частмови table...")

for chastMovi in set(chastiMoviStart):
    freqs = []
    for chastiMoviFreq in chastiMovi:
        chastiMoviFreq = dict(chastiMoviFreq)
        if chastMovi not in chastiMoviFreq:
            freq = 0
        else:
            freq = chastiMoviFreq[chastMovi]

        freqs.append(freq)
    
    req = """
    INSERT INTO ЧС_частмови (pos, обща_частота, підв_1, підв_2, підв_3, підв_4, підв_5, підв_6, підв_7, підв_8, підв_9, 
                            підв_10, підв_11, підв_12, підв_13, підв_14, підв_15, підв_16, підв_17, підв_18, підв_19, підв_20) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = [chastMovi, sum(freqs)] + freqs
    db.executeSql(req, params)