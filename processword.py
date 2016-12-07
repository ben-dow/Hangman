import random
import linecache

class Hangman:
    def __init__(self,wrd):
        self.word = wrd
        self.wordindex = self.indexWord(self.word)

        self.word_display = []
        for i in range(0,len(self.word)):
            self.word_display.append(" ")

        self.geuss_display = []
        self.geusses_wrong = 0

    def indexWord(self, word):
        wordindex = dict()
        for i in range(0,len(word.strip())):
            if word[i].upper() in wordindex:
                wordindex[word[i].upper()].append(i)
            else:
                wordindex[word[i].upper()] = [i]
        return wordindex
    def processGeuss(self, letter):
        if letter.strip().upper() in self.word or letter.lower() in self.word:
            return True
        else:
            self.geusses_wrong += 1
            self.geuss_display.append(letter)
            return False

    def build_word(self,letter):
        idx = self.wordindex[letter.upper()]
        for i in idx:
            self.word_display[i] = letter.upper()

class Files:
    def __init__(self,filename):
        self.lines = 0
        self.filename = filename
        for line in open(filename):
            self.lines += 1

    def determineWord(self):
        randomnum = random.randint(0,self.lines)
        line = linecache.getline(self.filename,randomnum)
        return line.strip().upper()
