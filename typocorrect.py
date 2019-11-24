def deleteAll(s: str, stringsToDelete: list):
    for strToReplace in stringsToDelete:
        s = s.replace(strToReplace, ' ')
    return s


def levenshteinDistance(s1: str, s2: str, insertCost: int = 1, deleteCost: int = 1, replaceCost: int = 1):
    M = len(s1)
    N = len(s2)
    D = [[0 for j in range(N + 1)] for i in range(M + 1)]
    for i in range(M + 1):
        D[i][0] = i * deleteCost
    for j in range(N + 1):
        D[0][j] = j * insertCost
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if s1[i - 1] != s2[j - 1]:
                D[i][j] = min(D[i - 1][j] + deleteCost,
                              D[i][j - 1] + insertCost,
                              D[i - 1][j - 1] + replaceCost)
            else:
                D[i][j] = D[i - 1][j - 1]
    return D[M][N]


def typoCorrect(word: str, correctDict: dict, requiredDistance: int = 2) -> str:
    previousDistance = requiredDistance + 1
    correction = ""
    for correctWord in correctDict.keys():
        currentDistance = levenshteinDistance(word, correctWord, 1, 1, 1)
        if currentDistance < previousDistance and currentDistance <= requiredDistance:
            correction = correctWord
            previousDistance = currentDistance
        elif currentDistance == previousDistance and currentDistance <= requiredDistance and \
                correctDict[correctWord] > correctDict.get(correction, 0):
            correction = correctWord

        if word[:len(correctWord)] == correctWord:
            if word[len(correctWord):] in correctDict.keys() and previousDistance > 1:
                correction = word[:len(correctWord)] + " " + word[len(correctWord):]
                previousDistance = 1
            elif typoCorrect(word[len(correctWord):], correctDict, requiredDistance - 1) in correctDict.keys() \
                    and previousDistance > requiredDistance:
                correction = word[:len(correctWord)] + " " + typoCorrect(word[len(correctWord):], correctDict,
                                                                         requiredDistance - 1)
                previousDistance = levenshteinDistance(word, correction)
        elif word[len(word) - len(correctWord):] == correctWord:
            if word[:len(word) - len(correctWord)] in correctDict.keys() and previousDistance > 1:
                correction = word[:len(word) - len(correctWord)] + " " + word[len(word) - len(correctWord):]
                previousDistance = 1
            elif typoCorrect(word[:len(word) - len(correctWord)], correctDict, requiredDistance - 1) \
                    in correctDict.keys() and previousDistance > requiredDistance:
                correction = typoCorrect(word[:len(word) - len(correctWord)], correctDict, requiredDistance - 1) + " " \
                             + word[len(word) - len(correctWord):]
                previousDistance = levenshteinDistance(word, correction)

    if correction == "":
        return word
    else:
        return correction


correctDict = {}  # Частота корректных словоформ
correctDictFile = open("dict1.txt", 'r')
correctDictText = correctDictFile.readlines()
correctDictFile.close()
for i in correctDictText:
    i = i.split()
    correctDict.update({i[0]: int(i[1])})

textfile = open("brain271.txt", 'r')
text = textfile.read()
textfile.close()

text = deleteAll(text, ['!', '?', ',', ';', '.', ':', '«', '»', '(', ')']).lower()  # Преобразования
while text.find("  ") >= 0:
    text = text.replace("  ", " ")

words = {}  # Частота для каждой словоформы
for word in text.split():
    word = word.lower()
    if word != '':
        c = words.get(word, 0) + 1
        words.update({word: c})

print("2.1. Количество словоформ: ", sum(words.values()))
print("2.2. Количество разных словоформ: ", len(words.keys()))

countInDict = 0
potentialTypos = []
print("Потенциальные ошибки:")
for word in words.keys():
    if word in correctDict.keys():
        countInDict += words[word]
    else:
        potentialTypos.append(word)
potentialTypos = sorted(potentialTypos, key=lambda x: words[x], reverse=True)

print("2.3. Количество словоформ из словаря: ", countInDict)
print("3.1. Количество потенциальных ошибок: ", sum(words.values()) - countInDict)

corrections = {}
print("Исправление потенциальных ошибок:")
for word in potentialTypos:
    correction = typoCorrect(word, correctDict, 2)
    corrections.update({word: correction})
    if correction == word:
        print(word, "не найдено", sep=' - ')
    else:
        print(word, corrections[word], levenshteinDistance(word, corrections[word], 1, 1, 1), sep=' - ')

for word in corrections.keys():
    text = text.replace(word, corrections[word])

words = {}  # Частота для каждой словоформы
for word in text.split():
    word = word.lower()
    if word != '':
        c = words.get(word, 0) + 1
        words.update({word: c})

print("4.1. Количество словоформ: ", sum(words.values()))
print("4.2. Количество разных словоформ: ", len(words.keys()))

countInDict = 0
for word in words.keys():
    if word in correctDict.keys():
        countInDict += words[word]

print("4.3. Количество словоформ из словаря: ", countInDict)

outputfile = open("output.txt", 'w')
outputfile.write(text)
outputfile.close()
