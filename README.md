# Distributed Job Scheduler (Fault-Tolerant)

A minimal distributed job scheduler demonstrating core distributed-systems concepts:
heartbeats, failure detection, task retries, dead-letter queues, and persistent
control-plane state.

## Features
- Centralized control plane
- Stateless workers with heartbeats
- Failure detection and task requeue
- Retry limits with dead-letter queue
- Persistent scheduler state (crash recovery)
- At-least-once execution semantics

## Architecture
- **Office (Control Plane)**: owns state and scheduling decisions
- **Workers**: execute tasks and send heartbeats
- **State Persistence**: scheduler state stored on disk

## How It Works
1. Workers register via heartbeats
2. Office assigns tasks
3. Worker failures detected via heartbeat timeout
4. Tasks retried or moved to dead-letter queue
5. State survives scheduler restarts

## Running Locally

### 1. Start the control plane

uvicorn office.office:app --reload
### 2. Start a worker
python worker/worker.py

### 3. Observe state

http://127.0.0.1:8000/state

http://127.0.0.1:8000/dead

### Failure Scenarios

Kill worker mid-task → task retried

Exceed retry limit → task moves to dead-letter queue

Restart scheduler → state recovered

### Guarantees

At-least-once execution

No silent task loss

Bounded retries

### Future Extensions

Priority queues

Backoff strategies

Multiple concurrent tasks

External state store (Redis / etcd)
