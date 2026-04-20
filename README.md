# Asyncio Notes (Python)

## Overview
- `asyncio` is used for **concurrent programming** in Python  
- Best suited for **I/O-bound tasks** (API calls, DB queries, file operations)  
- Not suitable for **CPU-bound tasks** (use multiprocessing instead)  

---

## 🔹 Core Concepts

### Coroutines
- Defined using `async def`  
- Can be **paused and resumed**  

### Coroutine Execution
- Calling a coroutine does **not execute it immediately**  
- Returns a **coroutine object**  

### Await
- Used to **execute a coroutine**  
- Can only be used inside an `async` function  

### Event Loop
- Core engine of asyncio  
- Runs coroutines using **cooperative multitasking**  
- Switches execution when a coroutine hits `await` 

---

## 🔹 Running Async Code
- Use `asyncio.run()` to start execution  
- It creates and manages the event loop  

---

## 🔹 Concurrency Utilities

### asyncio.gather()
- Runs multiple coroutines concurrently  
- Returns results as a list  (blocking)

### asyncio.create_task()
- Schedules a coroutine to run in the background  

---

## Important Rules
- `await` can only be used inside `async def`  
- Asyncio provides **concurrency, not parallelism**  
- Avoid blocking calls like `time.sleep()`  
- Use `asyncio.sleep()` instead  

---