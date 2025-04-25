import threading
import multiprocessing
import time
import psutil
import os
import platform
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tabulate import tabulate
import numpy as np

# Khóa để đồng bộ việc in ra thông tin
print_lock = threading.Lock()

# Hàm tính toán mẫu: tính tổng các số từ 1 đến n
def compute_sum(n):
    return sum(range(1, n + 1))

# Hàm đo tài nguyên hệ thống
def measure_resources():
    process = psutil.Process(os.getpid())
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_info = process.memory_info()
    return {
        "cpu_percent": cpu_percent,
        "memory_rss": memory_info.rss / 1024 / 1024  # Chuyển sang MB
    }

# Hàm hiển thị thông tin hệ thống
def display_system_info():
    print("Thông tin hệ thống:")
    print(f"  Hệ điều hành: {platform.system()} {platform.release()}")
    print(f"  Số lượng CPU: {psutil.cpu_count()}")
    print(f"  Bộ nhớ RAM khả dụng: {psutil.virtual_memory().available / (1024 ** 3):.2f} GB")
    print()

# Hàm hiển thị thông tin các luồng đang hoạt động
def display_threads():
    with print_lock:
        print("\nCác luồng đang hoạt động:")
        for thread in threading.enumerate():
            print(f"  Tên luồng: {thread.name}, ID: {thread.ident}, Hoạt động: {thread.is_alive()}")

# Hàm hiển thị thông tin các tiến trình đang hoạt động
def display_processes():
    with print_lock:
        print("\nCác tiến trình đang hoạt động:")
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            print(f"  PID: {proc.info['pid']}, Tên: {proc.info['name']}, Trạng thái: {proc.info['status']}")

# Hàm thực hiện tác vụ với đa luồng
def run_threading(tasks, num_workers):
    start_time = time.time()
    cpu_measurements = []
    memory_measurements = []
    thread_ids = []

    def worker(task_id):
        with print_lock:
            print(f"Luồng {threading.current_thread().name} (ID: {threading.get_ident()}) bắt đầu tác vụ {task_id}")
        compute_sum(10_000_000)
        with print_lock:
            print(f"Luồng {threading.current_thread().name} (ID: {threading.get_ident()}) hoàn thành tác vụ {task_id}")

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for i in range(tasks):
            executor.submit(worker, i)
            thread_ids.append(threading.get_ident())
            resources = measure_resources()
            cpu_measurements.append(resources["cpu_percent"])
            memory_measurements.append(resources["memory_rss"])
            time.sleep(0.1)  # Để quan sát rõ ràng hơn

    end_time = time.time()
    avg_cpu = np.mean(cpu_measurements)
    avg_memory = np.mean(memory_measurements)

    return {
        "time": end_time - start_time,
        "avg_cpu_percent": avg_cpu,
        "avg_memory_mb": avg_memory,
        "thread_ids": thread_ids
    }

# Hàm thực hiện tác vụ với đa tiến trình
def run_multiprocessing(tasks, num_workers):
    start_time = time.time()
    cpu_measurements = []
    memory_measurements = []
    process_ids = []

    def worker(task_id):
        with print_lock:
            print(f"Tiến trình {multiprocessing.current_process().name} (PID: {os.getpid()}) bắt đầu tác vụ {task_id}")
        compute_sum(10_000_000)
        with print_lock:
            print(f"Tiến trình {multiprocessing.current_process().name} (PID: {os.getpid()}) hoàn thành tác vụ {task_id}")

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for i in range(tasks):
            executor.submit(worker, i)
            process_ids.append(os.getpid())
            resources = measure_resources()
            cpu_measurements.append(resources["cpu_percent"])
            memory_measurements.append(resources["memory_rss"])
            time.sleep(0.1)  # Để quan sát rõ ràng hơn

    end_time = time.time()
    avg_cpu = np.mean(cpu_measurements)
    avg_memory = np.mean(memory_measurements)

    return {
        "time": end_time - start_time,
        "avg_cpu_percent": avg_cpu,
        "avg_memory_mb": avg_memory,
        "process_ids": process_ids
    }

# Hàm chính
def main():
    num_tasks = 10
    num_workers = 4

    # Hiển thị thông tin hệ thống ban đầu
    display_system_info()

    print(f"Chạy {num_tasks} tác vụ với {num_workers} công nhân\n")

    # Hiển thị thông tin luồng và tiến trình ban đầu
    display_threads()
    display_processes()

    # Chạy đa luồng
    print("\nBắt đầu đa luồng...")
    thread_results = run_threading(num_tasks, num_workers)
    display_threads()

    # Chạy đa tiến trình
    print("\nBắt đầu đa tiến trình...")
    process_results = run_multiprocessing(num_tasks, num_workers)
    display_processes()

    # Trình bày kết quả dưới dạng bảng
    print("\nKết quả tổng hợp:")
    data = [
        ["Đa luồng", f"{thread_results['time']:.2f}", f"{thread_results['avg_cpu_percent']:.2f}", f"{thread_results['avg_memory_mb']:.2f}", ", ".join(map(str, thread_results['thread_ids']))],
        ["Đa tiến trình", f"{process_results['time']:.2f}", f"{process_results['avg_cpu_percent']:.2f}", f"{process_results['avg_memory_mb']:.2f}", ", ".join(map(str, process_results['process_ids']))]
    ]
    headers = ["Phương pháp", "Thời gian (giây)", "CPU trung bình (%)", "RAM trung bình (MB)", "ID luồng/tiến trình"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()