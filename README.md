# ⚡ Mini Project - Concurrent Page Fetcher with Python

**What if you had to fetch 20 web pages? Would you wait for each one to finish before starting the next?**

Imagine you're building a tool that collects information from 20 different websites. Your first approach is simple: visit one website, wait for its response, and then move to the next.

But here's the problem: most of the time, your program isn't actually doing anything. It's just waiting for websites to respond.

And if one website is unusually slow, everything behind it has to wait too.

**There has to be a better way.**

That's exactly what this project explores.

## 🚀 About the Project

**Concurrent Page Fetcher** is a Python mini-project that demonstrates how to fetch multiple web pages efficiently using `asyncio` and `HTTPX`.

Instead of waiting for one request to finish before starting another, we can start multiple requests concurrently and let their network operations overlap.

But speed isn't everything. This project also explores how to:

- Control the number of simultaneous requests.
- Handle slow websites using timeouts.
- Compare sequential and concurrent execution.
- Measure the performance difference through benchmarking.

The goal is to understand how asynchronous programming makes network-bound applications faster and more resilient.

## 📸 Project Snippet


<img width="1561" height="906" alt="Screenshot (374)" src="https://github.com/user-attachments/assets/b2b96cb2-5a7d-449e-801b-4bab6c482998" />
<img width="1920" height="1080" alt="Screenshot (375)" src="https://github.com/user-attachments/assets/c18009b5-68bc-4696-b635-e3011d9ece98" />

The screenshot shows a benchmark run comparing the different fetching strategies.

## ✨ Features

| Feature                  | Description                                                                     |
| ------------------------ | ------------------------------------------------------------------------------- |
| Single Page Fetching     | Fetches a URL, checks its HTTP status and returns the response body length.     |
| Concurrent Fetching      | Uses `asyncio.gather()` to fetch multiple URLs concurrently.                  |
| Concurrency Control      | Uses `asyncio.Semaphore` to limit simultaneous requests.                      |
| Timeout Handling         | Prevents individual slow requests from waiting indefinitely.                    |
| Performance Benchmarking | Compares sequential fetching against concurrent fetching with different limits. |
| Offline Testing          | Uses HTTPX's in-memory transport to test functionality without internet access. |

## 📂 Project Structure

```text
.
├── speed_run.py       # Core asynchronous fetching functions
├── benchmark.py       # Sequential vs concurrent benchmarks
├── test_speed_run.py  # Offline test cases
├── requirements.txt   # Project dependencies
└── README.md
```

## ⚙️ How It Works

The project implements four main functions in `speed_run.py`:

**1. `fetch_one(url)`**

Fetches a single URL asynchronously, checks the HTTP response status and returns the URL along with the number of characters in its response body.

**2. `fetch_all(urls)`**

Uses `asyncio.gather()` to execute multiple fetching tasks concurrently. Results are returned in the same order as the input URLs.

**3. `fetch_all_limited(urls, limit)`**

Uses `asyncio.Semaphore` to control concurrency. For example, a limit of 3 ensures that no more than three requests are active at once.

**4. `fetch_all_safe(urls, timeout)`**

Adds a timeout to individual requests. If a request takes too long, its result contains `None` instead of the response body length. Other HTTP and network errors are allowed to propagate.

## 📊 Benchmarking

The project includes `benchmark.py` to compare four execution strategies:

1. **Sequential:** Fetches URLs one after another.
2. **Concurrent:** Fetches all URLs concurrently without an application-level concurrency limit.
3. **Concurrent (Limit 3):** Allows a maximum of three simultaneous requests.
4. **Concurrent (Limit 10):** Allows a maximum of ten simultaneous requests.

By default, the benchmark fetches 20 Python documentation pages.

You can also provide your own URLs.

**Note:** Benchmark results depend on network conditions, server response times and the websites being accessed. Concurrent execution does not guarantee faster results in every situation.

## 🛠️ Tech Stack

- Python 3.10+
- asyncio
- HTTPX
- pytest

## 💻 Getting Started

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd concurrent-page-fetcher
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the environment**

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

## 🧪 Run Tests

Run the test suite using:

```bash
python -m pytest -q
```

The tests use an in-memory HTTPX transport, so an internet connection is not required.

## ⚡ Run the Benchmark

Run the benchmark using the default set of URLs:

```bash
python benchmark.py
```

Or provide custom URLs:

```bash
python benchmark.py https://example.com https://www.python.org
```

The benchmark reports the number of successfully fetched pages and the elapsed time for each execution strategy.

**Note:** An internet connection is required for benchmarking. HTTP errors and network failures are reported rather than counted as successful fetches.

## 🎯 What I Learned

Through this project, I explored:

- How asynchronous programming works in Python.
- The difference between sequential and concurrent execution.
- How `asyncio.gather()` manages multiple coroutines.
- How semaphores control concurrency.
- How to handle timeouts in asynchronous applications.
- How to benchmark and test network-based code.

---
