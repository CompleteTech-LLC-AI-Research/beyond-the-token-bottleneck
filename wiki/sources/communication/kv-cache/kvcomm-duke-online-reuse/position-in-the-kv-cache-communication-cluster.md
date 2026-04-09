KVCOMM-online addresses **how to make KV operations efficient** — the systems optimization dimension. It's orthogonal to and composable with:
- [[kvcomm-kth-selective|KVComm]]: Could select layers first, then apply offset-based reuse for selected layers
- [[cache-to-cache-semantic-communication|C2C]]: Could apply offset estimation to reduce the fuser's input computation

See [[kv-cache-communication]] for the unified concept page.
