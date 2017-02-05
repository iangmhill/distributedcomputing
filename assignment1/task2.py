from threading import Thread, Semaphore
from os import listdir
from re import sub, split

class CountWords(Thread):
  def __init__(self, hist, readers, hist_sem, readers_sem):
    super(CountWords, self).__init__()
    self.hist = hist
    self.readers = readers
    self.readers_sem = readers_sem
    self.hist_sem = hist_sem

  def run(self):
    while true:
      self.readers_sem.acquire()
      line = self.readers[0].readline()
      if (not line):
        self.readers[:] = self.readers[1:]
        if (len(self.readers) == 0):
          writeDict()
      self.readers_sem.release()



        for line in self.readers[0].readlines():
          only_words = sub(r'[^a-zA-Z\s]+', ' ', line)
          split_words = split(r'\s+', only_words.strip())
          for split_word in split_words:
            word = split_word.lower()
            self.hist[word] = hist.get(word, 0) + 1
    self.writeDict(self.hist)

  def writeDict(self, dict, out='out.txt'):
    f = open(out, 'w')
    for k in dict:
      f.write("{}: {}\n\n".format(k, dict[k]))
    f.close()

def main():
  hist = {}
  processes_sem = Semaphore(5)
  hist_sem = Semaphore(1)
  readers_sem = Semaphore(1)

  readers = [open(name) for name in listdir('./lib')]
  threads = [CountWords(hist, readers, hist_sem, readers_sem) for _ in range(5)]
  word_counter = CountWords()
  word_counter.start()

  # for t in threads (processes_sem.acquire()

  if __name__ == '__main__':
  main()
