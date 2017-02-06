from threading import Thread, Semaphore
from os import listdir
from re import sub, split
from timeit import Timer
import matplotlib.pyplot as plt

class CountWords(Thread):
  def __init__(self, hist, readers, hist_sem, readers_sem, thread_cond):
    super(CountWords, self).__init__()
    self.hist = hist
    self.readers = readers
    self.readers_sem = readers_sem
    self.hist_sem = hist_sem
    self.thread_cond = thread_cond

  def run(self):
    local_hist = {}
    while True:
      # Get the next line from the current reader
      self.readers_sem.acquire()
      remaining_readers = len(self.readers)
      line = None
      if remaining_readers > 0:
        line = self.readers[0].readline()
        if (not line):
          self.readers[0].close()
          self.readers[:] = self.readers[1:]
          remaining_readers -= 1
      self.readers_sem.release()

      # If all of the readers have been exhausted...
      if (not line and remaining_readers == 0):
        # ...it's time to write to the global histogram
        self.hist_sem.acquire()
        for (word, count) in local_hist.items():
          self.hist[word] = self.hist.get(word, 0) + count
        if (self.thread_cond['idle'] == self.thread_cond['num'] - 1):
          # If this thread is the last one alive, write to the file
          self.write_to_file(self.hist)
        else:
          # Otherwise, increment the number of idle threads and release the lock
          self.thread_cond['idle'] += 1
        self.hist_sem.release()
        return

      # If there's more to count, keep adding to the local histogram.
      only_words = sub(r"[^a-zA-Z'\s]+", ' ', line)
      split_words = split(r'\s+', only_words.strip())
      for split_word in split_words:
        if (split_word != ''):
          word = split_word.lower()
          local_hist[word] = local_hist.get(word, 0) + 1

  def write_to_file(self, hist, out='out.txt'):
    with open(out, 'w') as out_file:
      for (word, count) in hist.items():
        out_file.write("{}: {}\n\n".format(word, count))

def main(num_threads = 10):
  thread_cond = {
    'num': int(num_threads),
    'idle': 0
  }
  hist = {}
  hist_sem = Semaphore(1)
  readers_sem = Semaphore(1)

  readers = [open('./lib/' + name) for name in listdir('./lib')]
  word_counters = [CountWords(hist, readers, hist_sem, readers_sem, thread_cond) for _ in range(thread_cond['num'])]
  for thread in word_counters:
    thread.start()
  for thread in word_counters:
    thread.join()

if __name__ == '__main__':
  num_threads_data = []
  timing_data = []
  for num_threads in range(1,5):
    t = Timer('main({})'.format(num_threads), "from __main__ import main")
    timed = t.timeit(10)/10
    num_threads_data.append(num_threads)
    timing_data.append(timed)
    print("{} threads: {}".format(num_threads, timed))
  plt.plot(num_threads_data, timing_data)
  plt.show()