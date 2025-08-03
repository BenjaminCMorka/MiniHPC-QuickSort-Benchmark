import random
import time
from memory_profiler import memory_usage
import csv
from serial_quicksort import quicksort
from parallel_quicksort import parallel_quicksort

def profile_memory_and_time(func, arr):
    # run func and measure peak memory and elapsed time
    start_time = time.time()
    mem_usage = memory_usage((func, (arr,)), max_iterations=1, interval=0.1)
    elapsed = time.time() - start_time
    peak_mem = max(mem_usage) - min(mem_usage)
    return elapsed, peak_mem

def run_benchmarks():
    sizes = [100000, 300000, 500000, 700000]
    results = []

    print(f"{'Size':>8} | {'Method':>10} | {'Time (s)':>10} | {'Peak Mem (MB)':>14}")
    print("-" * 50)

    for size in sizes:
        arr = [random.randint(0, 1000000) for _ in range(size)]

        # serial quicksort
        elapsed, peak_mem = profile_memory_and_time(lambda a: quicksort(a), arr.copy())
        print(f"{size:8} | {'Serial':>10} | {elapsed:10.4f} | {peak_mem:14.4f}")
        results.append([size, "Serial", elapsed, peak_mem])

        # parallel quicksort
        elapsed, peak_mem = profile_memory_and_time(parallel_quicksort, arr.copy())
        print(f"{size:8} | {'Parallel':>10} | {elapsed:10.4f} | {peak_mem:14.4f}")
        results.append([size, "Parallel", elapsed, peak_mem])


    with open("memory_benchmark_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Array Size", "Method", "Elapsed Time (s)", "Peak Memory Usage (MB)"])
        writer.writerows(results)

    print("\nresults saved to memory_benchmark_results.csv")

if __name__ == "__main__":
    run_benchmarks()
