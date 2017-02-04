from threading import Thread
from os import listdir

class CountWords(Thread):
  def __init__(self):
    super(CountWords, self).__init__()

  def run(self):
    files = listdir("./lib")
    print(files)


def main():
  word_counter = CountWords()
  word_counter.start()

if __name__ == '__main__':
  main()