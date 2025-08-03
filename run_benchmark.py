import random
import time
import logging
from serial_quicksort import quicksort as serial_qs
from parallel_quicksort import parallel_quicksort as parallel_qs

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def benchmark(func, arr):
    start = time.perf_counter()
    func(arr.copy())
    return time.perf_counter() - start

def main():
    arr_size = 5_000_000
    logging.info(f"generating array of size: {arr_size:,}")
    test_data = [random.randint(0, 10_000_000) for _ in range(arr_size)]

    logging.info("running serial quicksort...")
    serial_time = benchmark(lambda a: serial_qs(a), test_data)
    logging.info(f"Serial QuickSort completed in {serial_time:.4f} seconds.")

    logging.info("running parallel quickSort...")
    parallel_time = benchmark(parallel_qs, test_data)
    logging.info(f"parallel quickSort completed in {parallel_time:.4f} seconds.")



    print("\n--- Benchmark Summary ---")
    print(f"Serial    : {serial_time:.4f}s")
    print(f"Parallel  : {parallel_time:.4f}s")

    print(f"Speedup (Parallel) : {serial_time / parallel_time:.2f}x")


if __name__ == "__main__":
    main()
