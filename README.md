# MiniHPC QuickSort Benchmark

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

---

## Overview

This project demonstrates efficient implementation and benchmarking of **Parallel** and **Serial QuickSort algorithms** in Python. It showcases practical HPC techniques such as process-level parallelism, memory profiling, performance optimization for sorting large datasets, and benchmarking.

- **Serial QuickSort:** A clean recursive implementation of QuickSort.
- **Parallel QuickSort:** Uses Python's `concurrent.futures.ProcessPoolExecutor` to speed up sorting by parallelizing top-level partitions.
- **Benchmarking:** Compares runtime and memory consumption of serial and parallel implementations on large arrays.
- **Memory Profiling:** Integrates `memory_profiler` to measure peak memory usage during sorting.

---

## Features

- Parallelizes QuickSort at the top partition level with minimal overhead.
- Uses adaptive thresholds to decide when to parallelize based on input size.
- Efficient merging of sorted chunks when applicable.
- Detailed benchmarking with time and memory usage metrics.
- Modular design for easy extension or integration.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Packages listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
