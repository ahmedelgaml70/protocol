"""Find a wall-clock EVM block range with read-only timestamp binary search."""


def block_timestamp(rpc, number):
    block = rpc.rpc("eth_getBlockByNumber", [hex(number), False])
    if not isinstance(block, dict) or not isinstance(block.get("timestamp"), str):
        raise ValueError(f"Block {number}: timestamp unavailable")
    return int(block["timestamp"], 16)


def start_block_for_hours(rpc, latest, earliest, hours):
    """First block >= tip_timestamp minus requested hours, capped at deployment.

    Assumes canonical EVM block timestamps are nondecreasing across block number.
    Executes O(log(blocks)) read-only eth_getBlockByNumber requests.
    """
    if not (0 < hours <= 24 * 30):
        raise ValueError("hours must be > 0 and <= 720")
    if earliest > latest:
        raise ValueError("earliest block after tip")
    latest_time = block_timestamp(rpc, latest)
    cutoff = latest_time - int(hours * 3600)
    lo, hi = earliest, latest
    if block_timestamp(rpc, lo) >= cutoff:
        return lo
    while lo < hi:
        mid = (lo + hi) // 2
        if block_timestamp(rpc, mid) < cutoff:
            lo = mid + 1
        else:
            hi = mid
    return lo
