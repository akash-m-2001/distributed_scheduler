from fastapi import FastAPI
import time
import json
import os

STATE_FILE = "office/state.json"
def save_state():
    state = {
        "task_queue": task_queue,
        "current_task": current_task,
        "workers": workers,
        "dead_letter_queue": dead_letter_queue,
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)



def load_state():
    global task_queue, current_task, workers, dead_letter_queue

    if not os.path.exists(STATE_FILE):
        return

    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    except json.JSONDecodeError:
        print("State file corrupted or empty. Starting fresh.")
        return

    task_queue = state.get("task_queue", [])
    current_task = state.get("current_task", None)
    workers = state.get("workers", {})
    dead_letter_queue = state.get("dead_letter_queue", [])



app = FastAPI()

task_queue = [
    {"id": "hello_task", "retries": 0, "max_retries": 3}
]

current_task = None

# worker_id -> last_heartbeat_time
workers = {}
dead_letter_queue = []

load_state()
HEARTBEAT_TIMEOUT = 10  # seconds


@app.get("/")
def health():
    return {"status": "office running"}


@app.post("/heartbeat")
def heartbeat(worker_id: str):
    workers[worker_id] = time.time()
    save_state()
    return {"status": "heartbeat received"}


@app.get("/workers")
def list_workers():
    now = time.time()
    alive = []
    dead = []

    for worker_id, last_seen in workers.items():
        if now - last_seen < HEARTBEAT_TIMEOUT:
            alive.append(worker_id)
        else:
            dead.append(worker_id)

    return {"alive": alive, "dead": dead}


@app.get("/request_task")
def request_task():
    global current_task

    if current_task is None and task_queue:
        current_task = task_queue.pop(0)
        save_state()
        return {"task": current_task}

    return {"task": None}

@app.get("/state")
def state():
    return {
        "queue": task_queue,
        "current_task": current_task,
        "workers": workers,
    }

@app.post("/report_done")
def report_done(task: str):
    global current_task
    current_task = None
    save_state()
    return {"status": f"{task} completed"}
