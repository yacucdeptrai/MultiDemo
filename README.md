# Báo Cáo Tìm Hiểu Về Đa Luồng và Đa Tiến Trình

## 1. Giới thiệu
Trong lập trình, **đa luồng (multithreading)** và **đa tiến trình (multiprocessing)** là hai kỹ thuật quan trọng để tối ưu hóa hiệu suất xử lý và tận dụng tài nguyên hệ thống, đặc biệt trong các tác vụ yêu cầu thực thi đồng thời. Báo cáo này dựa trên chương trình `complete_system_monitor.py` để phân tích cách triển khai, đo đạc tài nguyên và so sánh hiệu quả của hai kỹ thuật này trên một hệ thống thực tế.

Chương trình được viết bằng Python, sử dụng các thư viện như `threading`, `multiprocessing`, `psutil`, `tabulate`, và `numpy` để thực hiện một tác vụ mẫu (tính tổng các số), giám sát tài nguyên (CPU, RAM), và trình bày kết quả dưới dạng bảng.

## 2. Tổng quan về đa luồng và đa tiến trình

### 2.1. Đa luồng (Multithreading)
- **Khái niệm**: Đa luồng cho phép một tiến trình chạy nhiều luồng (thread) trong cùng không gian bộ nhớ. Mỗi luồng thực hiện một phần công việc độc lập.
- **Ưu điểm**:
  - Chia sẻ bộ nhớ dễ dàng, giảm chi phí giao tiếp.
  - Phù hợp với các tác vụ I/O-bound (như đọc/ghi file, truy cập mạng).
  - Tiết kiệm tài nguyên hơn so với đa tiến trình.
- **Nhược điểm**:
  - Trong Python, **Global Interpreter Lock (GIL)** giới hạn khả năng song song cho các tác vụ CPU-bound (như tính toán nặng).
  - Cần đồng bộ hóa (sử dụng khóa) để tránh xung đột tài nguyên.

### 2.2. Đa tiến trình (Multiprocessing)
- **Khái niệm**: Đa tiến trình tạo ra nhiều tiến trình độc lập, mỗi tiến trình có không gian bộ nhớ riêng và chạy trên một CPU riêng.
- **Ưu điểm**:
  - Tận dụng nhiều CPU, phù hợp với các tác vụ CPU-bound.
  - Không bị giới hạn bởi GIL, đảm bảo song song thực sự.
- **Nhược điểm**:
  - Tiêu tốn nhiều tài nguyên hơn (bộ nhớ, thời gian khởi tạo tiến trình).
  - Giao tiếp giữa các tiến trình phức tạp hơn (cần IPC - Inter-Process Communication).

## 3. Phân tích chương trình `complete_system_monitor.py`

### 3.1. Mô tả chương trình
Chương trình thực hiện một tác vụ mẫu (tính tổng các số từ 1 đến 10,000,000) với 10 tác vụ, sử dụng 4 công nhân (worker) cho cả đa luồng và đa tiến trình. Các tính năng chính bao gồm:
- **Hiển thị thông tin hệ thống**: Hệ điều hành, số CPU, bộ nhớ RAM khả dụng.
- **Theo dõi luồng/tiến trình**: Hiển thị danh sách luồng và tiến trình trước/sau khi thực thi.
- **Đo đạc tài nguyên**: Đo CPU (%), RAM (MB) trung bình trong quá trình thực thi.
- **Trình bày kết quả**: Kết quả được hiển thị trong bảng tổng hợp sau khi tất cả tác vụ hoàn thành.

### 3.2. Cấu trúc chương trình
- **Thư viện**:
  - `threading`, `multiprocessing`: Quản lý luồng và tiến trình.
  - `psutil`: Đo tài nguyên CPU, RAM.
  - `tabulate`: Tạo bảng kết quả.
  - `numpy`: Tính giá trị trung bình của các phép đo.
  - `platform`: Lấy thông tin hệ thống.
- **Các hàm chính**:
  - `compute_sum(n)`: Tính tổng từ 1 đến n, đại diện cho tác vụ CPU-bound.
  - `measure_resources()`: Đo CPU và RAM của tiến trình hiện tại.
  - `display_system_info()`: Hiển thị thông tin hệ thống (OS, CPU, RAM khả dụng).
  - `display_threads()`, `display_processes()`: Liệt kê luồng/tiến trình đang hoạt động.
  - `run_threading(tasks, num_workers)`: Thực hiện tác vụ với đa luồng, sử dụng `ThreadPoolExecutor`.
  - `run_multiprocessing(tasks, num_workers)`: Thực hiện tác vụ với đa tiến trình, sử dụng `ProcessPoolExecutor`.
  - `main()`: Điều phối chương trình, chạy 10 tác vụ với 4 công nhân.

### 3.3. Cách đo đạc tài nguyên
- **CPU**: Sử dụng `psutil.cpu_percent(interval=0.1)` để đo phần trăm sử dụng CPU của hệ thống.
- **RAM**: Sử dụng `process.memory_info().rss` để đo bộ nhớ resident set size (RSS), chuyển sang MB.
- **Thời gian**: Sử dụng `time.time()` để đo thời gian thực thi của mỗi phương pháp.
- Các phép đo được thực hiện sau mỗi tác vụ, sau đó lấy trung bình bằng `numpy.mean`.

### 3.4. Kết quả thực tế
Dựa trên kết quả chạy chương trình trên hệ thống của bạn:

#### Thông tin hệ thống
- **Hệ điều hành**: Windows 11
- **Số lượng CPU**: 20
- **Bộ nhớ RAM khả dụng**: 20.45 GB

#### Hoạt động luồng và tiến trình
- **Trước khi chạy**:
  - Chỉ có một luồng chính (`MainThread`, ID: 4912).
  - Hệ thống có hơn 200 tiến trình đang chạy, bao gồm các tiến trình hệ thống (`svchost.exe`, `csrss.exe`) và ứng dụng người dùng (`Zalo.exe`, `Discord.exe`, `opera.exe`, v.v.).
- **Trong quá trình chạy đa luồng**:
  - Một luồng (`ThreadPoolExecutor-0_0`, ID: 5012) thực hiện tuần tự 10 tác vụ, mỗi tác vụ được báo cáo bắt đầu và hoàn thành.
  - Sau khi hoàn thành, chỉ còn luồng chính (`MainThread`).
- **Trong quá trình chạy đa tiến trình**:
  - Các tiến trình mới được tạo ra, nhưng ID tiến trình được ghi nhận là `6648` (tiến trình chính của chương trình), cho thấy các tác vụ được thực hiện trong tiến trình chính hoặc không ghi nhận đúng ID tiến trình con.
  - Danh sách tiến trình sau khi chạy tương tự như ban đầu, với một số tiến trình mới như `py.exe` (PID: 27764).

#### Kết quả tổng hợp
Kết quả được trình bày trong bảng sau:

| Phương pháp   | Thời gian (giây) | CPU trung bình (%) | RAM trung bình (MB) | ID luồng/tiến trình                                        |
|---------------|------------------|--------------------|---------------------|------------------------------------------------------------|
| Đa luồng      | 2.01             | 2.34               | 38.21               | 4912, 4912, 4912, 4912, 4912, 4912, 4912, 4912, 4912, 4912 |
| Đa tiến trình | 2.04             | 1.54               | 38.78               | 6648, 6648, 6648, 6648, 6648, 6648, 6648, 6648, 6648, 6648 |

#### Phân tích kết quả
1. **Thời gian thực thi**:
   - Đa luồng: 2.01 giây.
   - Đa tiến trình: 2.04 giây.
   - **Nhận xét**: Thời gian thực thi của hai phương pháp gần như tương đương, với đa luồng nhanh hơn một chút (khoảng 0.03 giây). Điều này bất ngờ vì tác vụ là CPU-bound, nơi đa tiến trình thường vượt trội do tránh được GIL. Có thể do số lượng tác vụ (10) và công nhân (4) không đủ lớn để thể hiện sự khác biệt, hoặc hệ thống đã tải nặng với hơn 200 tiến trình.

2. **Sử dụng CPU**:
   - Đa luồng: 2.34%.
   - Đa tiến trình: 1.54%.
   - **Nhận xét**: Mức sử dụng CPU trung bình rất thấp, cho thấy chương trình không tận dụng hết 20 CPU của hệ thống. Đa luồng sử dụng CPU nhiều hơn một chút, có thể do chi phí quản lý luồng trong cùng tiến trình. Đa tiến trình sử dụng ít CPU hơn, có thể do các tiến trình con không được phân bổ hiệu quả trên các CPU.

3. **Sử dụng RAM**:
   - Đa luồng: 38.21 MB.
   - Đa tiến trình: 38.78 MB.
   - **Nhận xét**: Mức sử dụng RAM của hai phương pháp gần giống nhau, với đa tiến trình tiêu tốn nhiều hơn một chút (khoảng 0.57 MB). Điều này phù hợp vì mỗi tiến trình có không gian bộ nhớ riêng, trong khi các luồng chia sẻ bộ nhớ.

4. **ID luồng/tiến trình**:
   - Đa luồng: Tất cả ID là `4912` (luồng chính), cho thấy các tác vụ được thực hiện tuần tự bởi một luồng duy nhất, có thể do GIL hoặc cấu hình `ThreadPoolExecutor`.
   - Đa tiến trình: Tất cả ID là `6648` (tiến trình chính), cho thấy chương trình không ghi nhận đúng ID của các tiến trình con, có thể do lỗi trong hàm `run_multiprocessing` (sử dụng `os.getpid()` trong tiến trình chính thay vì tiến trình con).

## 4. Đánh giá và so sánh

### 4.1. Hiệu suất
- **Đa luồng**: Không hiệu quả như kỳ vọng cho tác vụ CPU-bound do GIL, dẫn đến thực thi tuần tự (như thể hiện qua ID luồng duy nhất). Thời gian thực thi 2.01 giây cho thấy chương trình không tận dụng được song song hóa.
- **Đa tiến trình**: Hiệu suất tương tự đa luồng (2.04 giây), có thể do số lượng tác vụ nhỏ hoặc hệ thống đã tải nặng. Tuy nhiên, đa tiến trình vẫn có tiềm năng vượt trội hơn nếu tăng số tác vụ hoặc tối ưu phân bổ CPU.

### 4.2. Tài nguyên
- **CPU**: Cả hai phương pháp sử dụng CPU rất thấp (<3%), cho thấy hệ thống 20 CPU không được khai thác hiệu quả. Điều này có thể do GIL (đa luồng) hoặc chi phí khởi tạo tiến trình (đa tiến trình).
- **RAM**: Sử dụng RAM gần giống nhau, với đa tiến trình tiêu tốn nhiều hơn một chút do mỗi tiến trình cần bộ nhớ riêng. Tuy nhiên, mức sử dụng RAM (khoảng 38 MB) là rất nhỏ so với 20.45 GB khả dụng.

### 4.3. Ứng dụng thực tế
- **Đa luồng**: Phù hợp hơn cho các ứng dụng I/O-bound, như xử lý yêu cầu mạng hoặc giao diện người dùng. Với tác vụ CPU-bound, đa luồng không hiệu quả trong Python.
- **Đa tiến trình**: Lý tưởng cho các tác vụ CPU-bound như xử lý dữ liệu lớn, tính toán khoa học. Tuy nhiên, cần tối ưu hóa để tận dụng đa lõi CPU.

## 5. Kết luận
Chương trình `complete_system_monitor.py` cung cấp một công cụ hữu ích để nghiên cứu đa luồng và đa tiến trình trong Python. Kết quả thực tế cho thấy:
- **Hiệu suất**: Đa luồng và đa tiến trình có thời gian thực thi tương đương (khoảng 2 giây) do tác vụ nhỏ và GIL giới hạn đa luồng.
- **Tài nguyên**: Cả hai phương pháp sử dụng ít CPU (<3%) và RAM (khoảng 38 MB), cho thấy hệ thống chưa được khai thác hết.
- **Hạn chế**: GIL ảnh hưởng lớn đến đa luồng, và đa tiến trình chưa thể hiện rõ lợi thế do số lượng tác vụ nhỏ hoặc lỗi ghi nhận ID tiến trình con.

## 6. Tài liệu tham khảo
- Python Documentation: `threading`, `multiprocessing`.
- Psutil Documentation: https://psutil.readthedocs.io/
- Tabulate Documentation: https://github.com/astanin/python-tabulate
- Python Concurrent Futures: https://docs.python.org/3/library/concurrent.futures.html