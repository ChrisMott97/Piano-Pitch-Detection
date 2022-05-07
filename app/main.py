from scipy.fft import fft
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy import stats
from tqdm import tqdm
import pickle
from pathlib import Path

from utility import get_windows, process_fundamental, plot_comparison, plot_real_comparison
from yin import augmented_detect_pitch_CMNDF
from fft import cents

def process(filename, fft_only=False):
  sample_rate, data = wavfile.read(filename)
  windows = get_windows(data)

  processed_yin = []
  processed_fft = []

  for window_start, window_end in tqdm(windows):
    data = data.astype(np.float64)
    data_window = data[window_start: window_end]

    processed_fft.append(cents(data_window, sample_rate))

    if fft_only:
      continue

    window_size = int(10 / 2000 * 16000)
    bounds = [20, 1000]
    pitches = []
    length = (data_window.shape[0] // (window_size + 3))
    for i in tqdm(range(length)):
      pitches.append(
        augmented_detect_pitch_CMNDF(
          data_window,
          window_size,
          i * window_size,
          sample_rate,
          bounds
        )
      )
    pitch_median = np.median(pitches)
    pitch_mode = stats.mode(pitches)[0][0]
    fundamental = pitch_mode
    
    print()
    print(pitch_median)
    print(pitch_mode)

    frequency_properties = process_fundamental(fundamental)
    processed_yin.append(frequency_properties)

  if fft_only:
    return processed_fft
  return processed_fft, processed_yin

def process_cache(base_file):
  path_to_file = f"{base_file}.p"
  path = Path("saved/midi/" + path_to_file)
  if path.is_file():
    with open (path, 'rb') as fp:
      processed_fft, processed_yin = pickle.load(fp)
  else:
    processed_fft, processed_yin = process(f"tests/{base_file}.wav")
    with open(f"saved/midi/{base_file}.p", 'wb') as fp:
      pickle.dump((processed_fft, processed_yin), fp)
  return processed_fft, processed_yin

def fft_cache(base_file):
  file_name = f"saved/real/{base_file}.p"
  path = Path(file_name)
  if path.is_file():
    with open(path, 'rb') as fp:
      midi, real, untuned = pickle.load(fp)
  else:
    midi = process(f"tests/{base_file}.wav", fft_only=True)
    real = process(f"tests/p1/{base_file}.wav", fft_only=True)
    untuned = process(f"tests/ensemble/{base_file}.wav", fft_only=True)
    with open(f"saved/real/{base_file}.p", "wb") as fp:
      pickle.dump((midi, real, untuned), fp)
  return midi, real, untuned


if __name__ == "__main__":
  # base_file = "potc13"
  # base_truth = ["A2", "C3", "D3", "E3", "F3", "G3"]

  # processed_fft, processed_yin = process_cache(base_file)
  # plot_comparison(processed_fft, processed_yin, base_truth, "potc", "Pirates")

  base_file = "basic"
  base_truth = ["C4", "D4", "E4", "F4", "G4"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Single C scale notes in the middle of the piano.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Comparing Pianos\nSingle C scale notes in the middle of the piano.")


  base_file = "chromatic"
  base_truth = ["C4", "C#4", "D4", "D#4", "E4"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Single chromatic notes in the middle of the piano.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Single chromatic notes in the middle of the piano.")

  base_file = "arp"
  base_truth = ["C4", "E4", "G4", "C5"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Single C triad arpeggio notes in the middle of the piano.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Single C triad arpeggio notes in the middle of the piano.")

  base_file = "octaves"
  base_truth = ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Octave C notes full piano range.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Octave C notes full piano range.")

  base_file = "low arp"
  base_truth = ["C1", "E1", "G1", "C2"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Single C triad arpeggio notes at the bottom of the piano.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Single C triad arpeggio notes at the bottom of the piano.")

  base_file = "high arp"
  base_truth = ["C7", "E7", "G7", "C8"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Single C triad arpeggio notes at the top of the piano.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Single C triad arpeggio notes at the top of the piano.")

  base_file = "singles"
  base_truth = ["C1", "D2", "E3", "F4", "G5", "A6", "B7"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "C scale notes played multiple times over all octaves.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "C scale notes played multiple times over all octaves.")

  base_file = "lengths"
  base_truth = ["C4", "G4", "E4", "B4", "D4"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Notes of multiple lengths in the middle of the piano.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Notes of multiple lengths in the middle of the piano.")

  base_file = "chords"
  base_truth = ["C4", "E4", "G4"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Arpeggiated then blocked C triad chord in the middle of the piano.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Arpeggiated then blocked C triad chord in the middle of the piano.")

  base_file = "sustain"
  base_truth = ["C4", "D4", "E4", "F4", "G4"]

  processed_fft, processed_yin = process_cache(base_file)
  plot_comparison(processed_fft, processed_yin, base_truth, "Single C scale notes in the middle of the piano with sustain.")

  midi, real, untuned = fft_cache(base_file)
  plot_real_comparison(midi, real, untuned, base_truth, "Single C scale notes in the middle of the piano with sustain.")

  # plt.show(block=True)