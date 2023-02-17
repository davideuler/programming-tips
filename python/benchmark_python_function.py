
Benchmark python function by multi threads

Start 10 threads to benchmark the hello() function.

```
import threading  
import time

def hello(n):  
    print("Hello, how old are you? ", n)  
    
def benchmark():
    start = time.perf_counter()
    thread_list = []
    for _ in range(0, 10):
        t = threading.Thread(target=hello, args=(5,))
        t.start()
        print(f'Active Threads: {threading.active_count()}')
        thread_list.append(t)
    for t in thread_list:
        t.join()
    end = time.perf_counter()
    print(f'Finished in {round(end-start, 2)} second(s)') 
    
```
