import PyPDF2
import re

def extractTextPDF(name):
    removeChars = [",", ".", "-", "!", "?", "(", ")"]
    result = ""
    pdfFileObj = open(name, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    for pageObj in pdfReader.pages:
        page = pageObj.extract_text()
        result = result + page
    pdfFileObj.close()
    result = result.lower()
    for char in removeChars:
        result = result.replace(char, "")
    
    result = re.sub(r'\s+', r' ', result)
    result = re.sub(r'\s+[цкнгшщхфпрлдчсмтб\'`]\s+', r'', result)    
    return result

def parseWords(words, morph):
    parsedWords = {}
    chastiMovi = []
    result = []
    excluded = ["'", "`"]
    for word in words:
        x = re.match("^[а-ящьюґєії'`]+$", word)
        if x:
            if x.group(0) not in excluded:
                word = x.group(0)
                parsed_word = morph.parse(word)[0]
                if str(parsed_word.tag) != "UNKN" and parsed_word.score > 0.5 and parsed_word.tag.POS:
                    pos = parsed_word.tag.POS.lower()
                    chastiMovi.append(pos)
                    parsedWords[word] = parsed_word
                    result.append(word)
                    
    return result, parsedWords, chastiMovi

def divide_into_samples(tokens, sample_size=1000):
    for i in range(0, len(tokens), sample_size):
        yield tokens[i:i + sample_size]

def list_chunk(clist, n): 
    return [clist[i * n:(i + 1) * n] for i in range((len(clist) + n - 1) // n )]  