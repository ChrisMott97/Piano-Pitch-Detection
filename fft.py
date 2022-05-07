from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from utility import process_fundamental
import numpy as np

def cents(data, rate):
  t = 1/rate

  samples = data.shape[0]

  fft_out = fft(data)
  fft_freq = fftfreq(samples, t)
  pos_fft_out = np.abs(fft_out)
  pos_fft_out_half = pos_fft_out[:(data.shape[0] // 8)]
  peaks = find_peaks(pos_fft_out_half, prominence=100000)
  
  points = list(zip(peaks[0], pos_fft_out_half[peaks[0]]))

  fundamental = fft_freq[max(points, key=lambda item:item[1])[0]]
  properties = process_fundamental(fundamental)

  return properties