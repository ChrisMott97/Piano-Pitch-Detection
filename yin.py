import numpy as np

def ACF(f, W, t, lag):
  no_lag = f[t : t + W]
  with_lag = f[lag + t : lag + t + W]
  # print(f"{len(no_lag)} {len(with_lag)}")
  mini = min(len(no_lag), len(with_lag))
  no_lag = no_lag[:mini]
  with_lag = with_lag[:mini]
  return np.sum(no_lag * with_lag)

def DF(f, W, t, lag):
  return ACF(f, W, t, 0) + ACF(f, W, t + lag, 0) - (2 * ACF(f, W, t, lag))

def memo_CMNDF(f, W, t, lag_max):
    running_sum = 0
    vals = []
    for lag in range(0, lag_max):
        if lag == 0:
            vals.append(1)
            running_sum += 0
        else:
            running_sum += DF(f, W, t, lag)
            vals.append(DF(f, W, t, lag) / running_sum * lag)
    return vals

def augmented_detect_pitch_CMNDF(f, W, t, sample_rate, bounds, thresh=0.1):  # Also uses memoization
    CMNDF_vals = memo_CMNDF(f, W, t, bounds[-1])[bounds[0]:]
    sample = None
    for i, val in enumerate(CMNDF_vals):
        if val < thresh:
            sample = i + bounds[0]
            break
    if sample is None:
        sample = np.argmin(CMNDF_vals) + bounds[0]
    return sample_rate / (sample + 1)