import random
import time
import csv
import logging
import matplotlib.pyplot as plt
from serial_quicksort import quicksort as serial_qs
from parallel_quicksort import parallel_quicksort as parallel_qs

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def benchmark(func, arr):
    start = time.perf_counter()
    func(arr.copy())
    return time.perf_counter() - start

def run_benchmark_suite():
    sizes = [100_000, 500_000, 1_000_000, 3_000_000, 5_000_000]
    runs_per_size = 3
    results = []

    print(f"{'Size':>10} | {'Method':>10} | {'Run':>3} | {'Time (s)':>10}")
    print("-" * 45)

    for size in sizes:
        for run in range(1, runs_per_size + 1):
            arr = [random.randint(0, 10_000_000) for _ in range(size)]

            # Serial
            serial_time = benchmark(serial_qs, arr)
            print(f"{size:10,} | {'Serial':>10} | {run:3} | {serial_time:10.4f}")
            results.append([size, "Serial", run, serial_time])

            # Parallel
            parallel_time = benchmark(parallel_qs, arr)
            print(f"{size:10,} | {'Parallel':>10} | {run:3} | {parallel_time:10.4f}")
            results.append([size, "Parallel", run, parallel_time])

    # Write results to CSV
    csv_file = "benchmark_results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Array Size", "Method", "Run", "Time (s)"])
        writer.writerows(results)
    print(f"\nResults saved to {csv_file}")

    # Aggregate averages for plotting
    avg_results = {}
    for size, method, run, time_taken in results:
        key = (size, method)
        avg_results.setdefault(key, []).append(time_taken)
    avg_results = {k: sum(v)/len(v) for k,v in avg_results.items()}

    # Prepare plot data
    sizes_sorted = sorted(set([size for size, method in avg_results.keys()]))
    serial_times = [avg_results[(size, "Serial")] for size in sizes_sorted]
    parallel_times = [avg_results[(size, "Parallel")] for size in sizes_sorted]

    # Plot
    plt.figure(figsize=(10,6))
    plt.plot(sizes_sorted, serial_times, marker='o', label='Serial QuickSort')
    plt.plot(sizes_sorted, parallel_times, marker='o', label='Parallel QuickSort')
    plt.xlabel("Array Size")
    plt.ylabel("Average Time (seconds)")
    plt.title("QuickSort Performance: Serial vs Parallel")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("benchmark_plot.png")
    plt.show()
    print("Plot saved as benchmark_plot.png")

if __name__ == "__main__":
    run_benchmark_suite()
