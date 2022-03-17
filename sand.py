import concurrent.futures as threading
from time import sleep, process_time
from tracemalloc import start
import objects

start = process_time()

agent = objects.Agent()

print(process_time()- start)