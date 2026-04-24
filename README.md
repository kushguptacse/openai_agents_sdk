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

### OpenAI Agents SDK
#### Agents: 

which are LLMs equipped with instructions and tools

#### Guardrails: 
which enable validation of agent inputs and outputs

#### Handoffs:
Allow one agent to transfer the entire conversation/control to another agent.
The receiving agent becomes the new primary agent and continues execution.
Typically used when responsibility clearly shifts (e.g., routing from a general agent → specialist agent).

Agents-as-tools: 

Agent can also be used as tools.
One agent invokes another agent like a function/tool call.
The called agent executes a task and returns a result.
Control always returns to the original agent after execution.

Tools → control returns to the original agent

Handoffs → control shifts to the new agent

