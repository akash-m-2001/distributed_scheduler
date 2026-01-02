import requests
import time
import threading
import uuid

OFFICE_URL = "http://127.0.0.1:8000"
WORKER_ID = str(uuid.uuid4())


def send_heartbeat():
    while True:
        try:
            requests.post(
                f"{OFFICE_URL}/heartbeat",
                params={"worker_id": WORKER_ID},
                timeout=2,
            )
            print("Heartbeat sent")
        except Exception:
            print("Heartbeat failed")

        time.sleep(3)


def main():
    print(f"Worker started with id {WORKER_ID}")

    heartbeat_thread = threading.Thread(
        target=send_heartbeat, daemon=True
    )
    heartbeat_thread.start()

    response = requests.get(f"{OFFICE_URL}/request_task").json()
    task = response.get("task")

    if task:
        print(f"Received task: {task}")
        time.sleep(5)
        print("Task done")
        requests.post(
            f"{OFFICE_URL}/report_done",
            params={"task": task},
        )
    else:
        print("No task available")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
