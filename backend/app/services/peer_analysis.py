import statistics

def peer_deviation(value, peer_values):
    vals=[v for v in peer_values if v is not None]
    if value is None or len(vals)<3:
        return None
    median=statistics.median(vals)
    deviations=[abs(x-median) for x in vals]
    mad=statistics.median(deviations)
    if mad == 0:
        return None
    return (value-median)/(1.4826*mad)
