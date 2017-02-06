# Assignment 1

## Report (Task 2)

*How did you solve each challenge in task 2? Be specific, add pseudo code if you need to.*

To divide the computational load between multiple threads we decided to create Python file objects for each file to be processed and pass a reference to each of these objects to each thread on initialization. In this way the program break files down by line when allocating document content to threads, and achieving this in a readable manner due to the utilization of built-in functionality. In our solution, an list of file objects are opened by the main() function and references to this list are dispersed to an arbitrary number of threads. The threads then all begin at the first file reading a line at a time, processing that line, then updating their private histograms (word: frequency dictionaries) before reading another line. Regular expression processing was used to isolate words from lines. Once a file has been read, the thread that detected this removes the file object from the head of the list, and threads begin work on the next. Once the file list is empty, threads add their personal data to the shared histogram, and then update a global variable to indicate that they are now inactive. The final thread running can recognize this fact using this variable, and calls the method which writes the public histogram to an output file.


*Did you face any other challenges? How did you solve them?*

Detecting when all threads are idle (in this case that all words had been logged from the last lines of the last file) was the biggest block for us in the logic. We wanted to use a semaphore, since it would make sense to do so, but it also needed to be initialized to a negative value so that each thread could release when it terminated, and the last could acquire and write the histogram. This is not possible with Python's standard semaphors though, and we ended up getting the same functionality with a global variable. This is probably will not be a very sustainable pattern as assignments get more intricate, but for now it provided a quick solution without modifying Python's built-in functionality.

Figuring out how to govern threads' access to the files was also an important challenge. We wanted our threads to be working with as little data at a time as possible to let the scheduler have as much control as possible. Python's generators came in handy here, allowing us to be sure no lines are read twice and that every line is recieved by a thread without much control code at all. In Java, explicit use of `yield` could be used to similar effect.


*Compare the running time of your code in task 1 to that of thread 2 with a single thread. Explain
your results.*




*Calculate the running time of task 2, using a varying number of threads. Start with a single
thread, and keep increasing the number of threads till the running time doesn’t change
(significantly).*




*Create a plot to represent the varying running time with increased number of threads. Explain
your results.*

![multithread runtime plot](./plot.jpg "Optional Title")
