# Chapter 9: The Trouble with Distributed Systems

## Core Idea
A distributed system can fail partially. One node can fail while another continues. A message can be delayed, lost, duplicated, or delivered after a timeout. A clock can be wrong, and a process can pause while it still holds a lease. Correct designs treat these conditions as normal parts of the system model.

The chapter separates safety from liveness. Safety means that nothing bad happens, such as two leaders accepting writes. Liveness means that something good eventually happens, such as a request completing. A design must state both properties and the assumptions that support them.

## Frameworks Introduced

- **Partial failure model**
  - **When to use**: Use it as the default model for networked services.
  - **How**: Assume each component can fail independently. Define what a caller can know after a timeout. Do not treat an absent response as proof that the remote operation did not happen.

- **Timeouts under unbounded delay**
  - **When to use**: Use timeouts to bound waiting, not to prove remote failure.
  - **How**: Set a deadline, return or retry after it, and make the operation safe if the original request later completes. Monitor queueing and tail latency because delays vary with load.

- **Physical and logical time**
  - **When to use**: Use monotonic clocks for elapsed-time measurement. Use time-of-day clocks for calendar timestamps. Use logical clocks for causal ordering.
  - **How**: Keep clock uncertainty visible. Do not infer causality from wall-clock timestamps without a bounded clock error.

- **Leases and fencing**
  - **When to use**: Use a lease when one node needs temporary authority. Use fencing when an old holder can continue after its lease expires.
  - **How**: Give each lease holder a monotonically increasing fencing token. Make the protected resource reject requests with an older token.

- **Byzantine fault model**
  - **When to use**: Use it when nodes may lie, send conflicting messages, or act maliciously.
  - **How**: Add authenticated messages, redundancy, and a protocol designed for Byzantine behavior. Do not use crash-fault assumptions for an adversarial environment.

- **Formal and deterministic testing**
  - **When to use**: Use model checking for small state spaces and deterministic simulation for many message and fault schedules.
  - **How**: Specify safety and liveness properties. Inject faults. Control random seeds and event order. Reproduce a failing schedule.

## Key Concepts

- **Partial failure**: A component fails while other components continue running.
- **Network partition**: A communication break that separates system components.
- **Timeout**: A local decision to stop waiting after a deadline.
- **Unbounded delay**: A model in which a message can take an arbitrarily long time.
- **Monotonic clock**: A clock that measures elapsed time without moving backward.
- **Time-of-day clock**: A clock tied to a calendar that can jump due to synchronization.
- **Clock skew**: The difference between clocks on different machines.
- **Process pause**: A delay in which a process stops executing while the process remains alive.
- **Lease**: A time-limited grant of authority.
- **Fencing token**: A value that lets a resource reject stale lease holders.
- **Safety**: A property that says a bad event never occurs.
- **Liveness**: A property that says a desired event eventually occurs.

## Mental Models

- Treat every timeout as an uncertainty boundary. The remote result may exist even when the caller has stopped waiting.
- Treat a clock reading as an estimate with an error interval, not as universal truth.
- Treat a lease as insufficient until the resource enforces fencing.
- Treat a process pause as a failure from the perspective of time-sensitive authority.
- Treat a distributed algorithm as correct only under an explicit system model.

## Anti-patterns

- **Assume a timeout proves failure**: The request may have committed before the response was delayed.
- **Use TCP as an end-to-end correctness guarantee**: TCP detects some connection failures, but applications still face delays, retries, and process failures.
- **Use wall-clock timestamps to order events**: Clock skew and clock jumps can reverse event order.
- **Let a lease holder write without a fencing token**: A paused old process can write after a new holder starts.
- **Treat a majority as truth in every setting**: A majority can agree on a false result when nodes can lie or when the failure model differs.
- **Test only the healthy path**: Many distributed bugs require a rare message order or a process pause.

## Code Examples

```javascript
while (true) {
  request = getIncomingRequest();
  // Ensure that the lease always has at least 10 seconds remaining
  if (lease.expiryTimeMillis - System.currentTimeMillis() < 10000) {
    lease = lease.renew();
  }
  if (lease.isValid()) {
    process(request);
  }
}
```

- **What it demonstrates**: A lease loop checks local validity, but the protected resource still needs fencing to reject stale work.

## Reference Tables

| Assumption | Permitted conclusion | Required caution |
|---|---|---|
| Response arrived | The remote operation produced a response | The operation may have committed earlier |
| Timeout expired | The caller stopped waiting | The operation may still run or complete |
| Connection closed | The path failed at some point | The remote process state remains unknown |
| Clock timestamp is `t` | One machine observed `t` | Other clocks and causal order may differ |

| Property | Meaning | Typical violation |
|---|---|---|
| Safety | Nothing bad happens | Two leaders accept writes |
| Liveness | Something good eventually happens | A lock never becomes available |

## Worked Example

A worker obtains a ten-second lease and pauses for garbage collection. The lease expires. Another worker obtains a new lease and starts processing. The first worker resumes and sends a delayed write. A lease check inside the old process cannot stop that write because the process holds stale local state.

The resource must compare a fencing token from each worker with the latest accepted token. The old worker's request then fails even if its process believes that its lease remains valid.

## Key Takeaways

1. Model networks, clocks, and processes as unreliable.
2. Make retries safe because a timeout does not cancel remote work.
3. Use monotonic clocks for durations and logical clocks for causal order.
4. Fence every time-limited authority at the resource boundary.
5. State safety and liveness separately.
6. Use fault injection and deterministic schedules to expose rare failures.

## Connects To

- **Chapter 6**: Replication lag and failover depend on timeouts and partial failure.
- **Chapter 8**: Distributed transactions must survive coordinator and participant failure.
- **Chapter 10**: Consensus formalizes agreement under crash and network faults.
- **Chapter 13**: End-to-end correctness handles uncertainty that local components cannot resolve.
