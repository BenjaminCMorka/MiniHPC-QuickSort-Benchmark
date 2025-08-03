import multiprocessing
from concurrent.futures import ProcessPoolExecutor

_global_pool = None
_pool_initialized = False

def _init_pool():
    """init global pool one time"""
    global _global_pool, _pool_initialized
    if not _pool_initialized:
        
        num_workers = min(4, multiprocessing.cpu_count())  
        _global_pool = ProcessPoolExecutor(max_workers=num_workers)
        _pool_initialized = True
    return _global_pool

def partition(arr):
    """partition func"""
    if len(arr) <= 1:
        return [], arr, []
    
    # three median pivot
    first, middle, last = arr[0], arr[len(arr)//2], arr[-1]
    pivot = sorted([first, middle, last])[1]
    
    left = []
    mid = []
    right = []
    
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            mid.append(x)
        else:
            right.append(x)
    
    return left, mid, right

def _quicksort_sequential(arr):
    """sequential quicksort for small arrays"""
    if len(arr) <= 1:
        return arr
    
    left, mid, right = partition(arr)
    return _quicksort_sequential(left) + mid + _quicksort_sequential(right)

def _parallel_sort_worker(arr):
    """worker function that sorts a chunk sequentially"""
    return _quicksort_sequential(arr)

def parallel_quicksort(arr):
    """
    parallel quicksort, efficiency considered by:
    1. only parallelize at the top level
    2. use seq sorting for all sub problems
    3. minimize process creation overhead
    """
    if len(arr) <= 1:
        return arr
    
    # use seq for small arrs
    if len(arr) < 100000:
        return _quicksort_sequential(arr)
    
    try:
        pool = _init_pool()
        

        left, mid, right = partition(arr)
        
        # only use parallelism if both sides  big enough
        min_parallel_size = 50000  
        
        if len(left) >= min_parallel_size and len(right) >= min_parallel_size:
            # if both sides large use 2 workers
            futures = [
                pool.submit(_parallel_sort_worker, left),
                pool.submit(_parallel_sort_worker, right)
            ]
            left_sorted = futures[0].result()
            right_sorted = futures[1].result()
        elif len(left) >= min_parallel_size or len(right) >= min_parallel_size:
            # if one side large use 1 worker for it
            if len(left) >= min_parallel_size:
                left_future = pool.submit(_parallel_sort_worker, left)
                right_sorted = _quicksort_sequential(right)
                left_sorted = left_future.result()
            else:
                right_future = pool.submit(_parallel_sort_worker, right)
                left_sorted = _quicksort_sequential(left)
                right_sorted = right_future.result()
        else:
            # just sequential if both sdes small
            left_sorted = _quicksort_sequential(left)
            right_sorted = _quicksort_sequential(right)
        
        return left_sorted + mid + right_sorted
        
    except Exception:
        # falls back to sequential if parallel fails
        return _quicksort_sequential(arr)

def cleanup_pool():
    """clean global pool"""
    global _global_pool, _pool_initialized
    if _global_pool:
        _global_pool.shutdown(wait=True)
        _global_pool = None
        _pool_initialized = False

# exit cleanuppp
import atexit
atexit.register(cleanup_pool)
