#!/usr/bin/python
# Previous line tells the shell to execute
# the Python interpreter, and pass this
# file as an argument to it.

from threading import Semaphore, Thread

BUF_SIZE = 3

# We won't preallocate space
# in this implementation; we
# can use the list like a queue
buffer = []

# Initialize Semaphores
mutex = Semaphore(1)
empty = Semaphore(BUF_SIZE)
full  = Semaphore(0)

def main():
    # Create Threads
    # ('target' is the function to
    #  call upon execution of thread)
    pthread = Thread(target=producer)
    cthread = Thread(target=consumer)

    # Start Threads
    pthread.start()
    cthread.start()

    # Join Threads
    pthread.join()
    cthread.join()

def producer():
    # Null-terminate list and iterate
    for charm in CHARMS + [None]:
        empty.acquire()
        mutex.acquire()
        # Begin Critical Section

        if charm:
            print 'Producing: %s' % charm

        buffer.append(charm)

        # End Critical Section
        mutex.release()
        full.release()

def consumer():
    while True:
        full.acquire()
        mutex.acquire()
        # Begin Critical Section

        charm = buffer.pop(0)

        # Null termination Check
        if not charm:
            return

        print 'Consuming: %s' % charm

        # End Critical Section
        mutex.release()
        empty.release()

# Our Charm Objects
class LuckyCharm(object):

    def __init__(self, name, ansi_color, setting):
        self.values = (setting, ansi_color, name)

    def __str__(self):
        return "\033[%d;%dm%s\033[0m" % self.values

CHARMS = [
    LuckyCharm('PINK HEART',       35, 1),
    LuckyCharm('ORANGE STAR',      33, 0),
    LuckyCharm('YELLOW MOON',      33, 1),
    LuckyCharm('GREEN CLOVER',     32, 0),
    LuckyCharm('BLUE DIAMOND',     34, 1),
    LuckyCharm('PURPLE HORSESHOE', 35, 0),
    LuckyCharm('RED BALLOON',      31, 0)
]

# Python incantation to
# call 'main()' on
# execution of script
if __name__ == '__main__':
    main()
