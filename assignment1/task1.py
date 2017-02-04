from threading import Thread
from os import listdir
from re import sub, split

class CountWords(Thread):
  def __init__(self):
    super(CountWords, self).__init__()

  def run(self):
    hist = {}
    texts = listdir('./lib')
    for text in texts:
      with open('./lib/' + text) as book:
        for line in book.readlines():
          only_words = sub(r'[^a-zA-Z\s]+', ' ', line)
          split_words = split(r'\s+', only_words.strip())
          for split_word in split_words:
            word = split_word.lower()
            hist[word] = hist.get(word, 0) + 1
        print(hist)
        return

def main():
  word_counter = CountWords()
  word_counter.start()

if __name__ == '__main__':
  main()