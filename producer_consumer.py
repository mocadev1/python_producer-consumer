import os
import threading
import time
import random

# Third party modules
import keyboard # Used to finish on Escape pressed key


# Global variables
CAPACITY = 22                           # Buffer capacity
buffer = [' ' for _ in range(CAPACITY)] # Filling the buffer with a -1
in_index = 0                            # Index in which the producer will place the product
out_index = 0                           # Index from which the consumer will take the product

# Declaring Semaphores
mutex = threading.Semaphore()           # Defaults to 1, buffer available 
empty = threading.Semaphore(CAPACITY)   # Empty spaces in the buffer
full = threading.Semaphore(0)           # Products in the buffer


def finish_program():
    """Finish the program aggressively"""
    print('\nYou have pressed Esc key, finishing program...\n')
    # Aggressive way to finish the program but its the way to do it due to Thread's exception handling
    os._exit(0)


# Producer Thread Class
class Producer(threading.Thread):
    def run(self):
        global CAPACITY, buffer, in_index, out_index
        global mutex, empty, full

        while True:
            rand_sleep = round(random.random() * 10, 2) # Sleeping between 1 to 10 sec
            time.sleep(rand_sleep)

            items_to_produce = random.randrange(2, 6) # Picking random number in the range 2-5, top limit (6) excluded

            for _ in range(items_to_produce):
                empty.acquire()
                mutex.acquire()

                self.append()
                in_index = (in_index + 1) % CAPACITY
                show()

                mutex.release()
                full.release()



    def append(self):
        """Puts the product into the buffer"""
        buffer[in_index] = "*"


# Consumer Thread Class
class Consumer(threading.Thread):
    def run(self):
        global CAPACITY, buffer, in_index, out_index, counter
        global mutex, empty, full

        while True:
            rand_sleep = round(random.random() * 10, 2)
            time.sleep(rand_sleep)

            items_to_consume = random.randrange(2, 6) # Picking random number in the range 2-5, top limit (6) excluded

            for _ in range(items_to_consume): 
                full.acquire()
                mutex.acquire()

                self.take()
                out_index = (out_index + 1) % CAPACITY
                show()

                mutex.release()
                empty.release()



    def take(self):
        """Takes the product from the buffer"""
        buffer[out_index] = " "


def show():
    """Just to print the "progress\""""
    hyphen = '-'
    d_hyphen = '--'
    for char in range(CAPACITY):
        print(f'[{buffer[char]}] ', end='') # Prints the spaces on the buffer with its content or whitout it
    print('')
    for _ in range(CAPACITY):
        # The '^' is to center the string in the available space, in this case 
        # it is allways going to be 4 spaces to match the 'spaces' from the 
        # buffer on screen, and also considering the current CAPACITY of the buffer
        print(f'{hyphen:^4}' if _ < 10 else f'{d_hyphen:^4}', end='')
    print('')
    for char in range(CAPACITY):
        print(f'{char + 1:^4}', end='') # To print the space number with the correct width 

    print('\n')
    time.sleep(1) # Just to slow down the view on the console


# Creating Threads
producer = Producer()
consumer = Consumer()

# Starting Threads
producer.start()
consumer.start()

# To finish the program pressing Esc
keyboard.add_hotkey('escape', finish_program)

# Waiting for threads to complete
producer.join()
consumer.join()
