import threading
import random
import time

# Constants
LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Shared buffer
buffer = []
condition = threading.Condition()

# Output files
all_numbers_file = open('all.txt', 'w')
even_numbers_file = open('even.txt', 'w')
odd_numbers_file = open('odd.txt', 'w')

def producer():
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with condition:
            while len(buffer) == BUFFER_SIZE:
                condition.wait()
            buffer.append(num)
            all_numbers_file.write(f'{num}\n')
            condition.notify_all()

def consumer(even: bool):
    while True:
        with condition:
            while not buffer or (even and buffer[-1] % 2 != 0) or (not even and buffer[-1] % 2 == 0):
                if threading.active_count() == 2 and len(buffer) == 0:  
                    return 
                condition.wait()
            num = buffer.pop()
            if even:
                even_numbers_file.write(f'{num}\n')
            else:
                odd_numbers_file.write(f'{num}\n')
            condition.notify_all()

producer_thread = threading.Thread(target=producer)
consumer_thread_even = threading.Thread(target=consumer, args=(False,))  
consumer_thread_odd = threading.Thread(target=consumer, args=(True,))  

producer_thread.start()
consumer_thread_even.start()
consumer_thread_odd.start()

producer_thread.join()
consumer_thread_even.join()
consumer_thread_odd.join()

all_numbers_file.close()
even_numbers_file.close()
odd_numbers_file.close()

print("Program completed.")
