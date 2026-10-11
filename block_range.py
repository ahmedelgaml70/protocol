"""Select an on-chain time window without querying pruned early-history blocks."""


def block_timestamp(rpc, number):
    block = rpc.rpc("eth_getBlockByNumber", [hex(number), False])
    if not isinstance(block, dict) or not isinstance(block.get("timestamp"), str):
        raise ValueError(f"Block {number}: timestamp unavailable")
    return int(block["timestamp"], 16)


def start_block_for_hours(rpc, latest, earliest, hours):
    """First block >= tip timestamp - hours, respecting earliest eligible block.

    Start at the tip and grow the backward search exponentially. This avoids
    querying genesis (which free RPC endpoints may have pruned), and then
    binary-searches the *recent* bracket. Works with fast and slower EVM chains.
    Explicitly fails when even the requested recent range is unavailable.
    """
    if not (0 < hours <= 720):
        raise ValueError("hours must be > 0 and <= 720")
    if earliest < 0 or earliest > latest:
        raise ValueError("invalid earliest/latest block")
    cutoff = block_timestamp(rpc, latest) - int(hours * 3600)
    if earliest == latest:
        return earliest
    high = latest
    step = 1
    while True:
        candidate = max(earliest, latest - step)
        if block_timestamp(rpc, candidate) < cutoff:
            low = candidate
            break
        if candidate == earliest:
            return earliest
        step *= 2
    while low < high:
        middle = (low + high) // 2
        if block_timestamp(rpc, middle) < cutoff:
            low = middle + 1
        else:
            high = middle
    return low
