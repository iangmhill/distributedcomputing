from threading import Thread, Semaphore
from os import listdir
from re import sub, split

THREAD_COUNT = 5
THREADS_IDLE = 0  # we would like to do this with a negative
                  # semaphore, but couln't in python...

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
        readers[0].close()
        self.readers[:] = self.readers[1:]

        if (len(self.readers) == 0):
          self.hist_sem.acquire()
          self.writeDict(self.hist)
          self.hist_sem.release()

          if(THREADS_IDLE == THREAD_COUNT - 1):
            writeDict()
          else:
            THREADS_IDLE += 1
            return

      self.readers_sem.release()

      only_words = sub(r'[^a-zA-Z\s]+', ' ', line)
      split_words = split(r'\s+', only_words.strip())
      for split_word in split_words:
        word = split_word.lower()
        self.hist[word] = hist.get(word, 0) + 1


  def writeDict(self, dict, out='out.txt'):
    f = open(out, 'w')
    for k in dict:
      f.write("{}: {}\n\n".format(k, dict[k]))
    f.close()

def main():
  hist = {}
  hist_sem = Semaphore(1)
  readers_sem = Semaphore(1)

  readers = [open(name) for name in listdir('./lib')]
  word_counters = [CountWords(hist, readers, hist_sem, readers_sem) for _ in range(THREAD_COUNT)]
  for thread in word_counters:
      thread.start()

  # for t in threads (processes_sem.acquire()

  if __name__ == '__main__':
  main()
