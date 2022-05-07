from cProfile import label
from pydoc import visiblename
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=10)

def create_baseline(limit=False):
  letters = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
  octaves = range(9)
  notes = []
  for octave in octaves:
    for letter in letters:
      notes.append(f"{letter}{octave}")
  a0 = notes.index("A0")
  c8 = notes.index("C8")
  if limit:
    return notes[a0:c8+1]
  return notes

def moving_average(x, w):
  return np.convolve(x, np.ones(w), 'valid') / w

def process_fundamental(f):
  notes = create_baseline()
  exponent = np.log(f/440)/np.log(2**(1/12))
  a4 = notes.index('A4')
  half_steps = round(exponent)
  tuned_fundamental = round(440 * ((2**(1/12))**half_steps), 2)
  note = notes[a4 + half_steps]
  cents = round(1200 * np.log2 (f / tuned_fundamental), 2)
  return note, cents, f

def get_windows(data):
    samples = data.shape[0]
    # t = 1/rate
    # length_secs = samples/rate
    max_vol_sample = np.where(data == np.amax(data))[0][0]
    max_vol = data[max_vol_sample]

    # zero negative data
    data = [max(0, x) for x in data]
    avg = moving_average(data, 5000)
    # plt.plot(data)
    avg = (avg - np.min(avg)) / (np.max(avg) - np.min(avg))
    # avg = preprocessing.normalize([avg])[0]
    # print(avg)
    # plt.plot(avg)
    peaks = find_peaks(avg, prominence=0.05)[0]
    note_windows = []
    gap_size = 0.5

    # plt.scatter(peaks, avg[peaks])
    # plt.show()
    diffs = []
    for i in range(1, len(peaks)+1):
        if i == len(peaks):
            # note_windows.append((peaks[i-1], len(avg)-1))
            diffs.append((len(avg)-1) - peaks[i-1])
            break
        diff = peaks[i] - peaks[i-1]
        diffs.append(diff)
    min_diff = min(diffs)

    for i in range(1, len(peaks)+1):
        # diff = peaks[i] - peaks[i-1]
        up_to = peaks[i-1] + int(min_diff * gap_size)
        note_windows.append((peaks[i-1], up_to))
    
    return note_windows

def plot_comparison(processed_fft, processed_yin,truth, title):
  yin_notes = []
  fft_notes = []
  yin_cents = []
  fft_cents = []
  for note, wrong, _ in processed_yin:
    yin_notes.append(note)
    yin_cents.append(wrong)
  for note, wrong, _ in processed_fft:
    fft_notes.append(note)
    fft_cents.append(wrong)
  
  base_notes = create_baseline()
  quantified_width = list(range(len(base_notes)))
  inharmonicity_curve = [0.0003*(x-(len(base_notes)//2))**3 for x in quantified_width]

  print("Plotting")
  plt.grid(True)
  plt.plot(base_notes, inharmonicity_curve, label="Inharmonicity Curve")
  plt.vlines(truth, -50, 50, linestyles="--", label="Correct Notes")
  # notes = np.array(notes)
  # cents_out = np.array(cents_out)
  min_length = min(len(yin_notes), len(fft_notes))
  if len(yin_notes) == len(fft_notes):
    for i in range(len(yin_notes)):
      if yin_notes[i] == fft_notes[i]:
        plt.plot([yin_notes[i], fft_notes[i]], [yin_cents[i],fft_cents[i]], 'k-')
  # for i in range(min_length):
  #   close_notes = [yin_notes[i]]
  #   note_index = base_notes.index(yin_notes[i])
  #   close_notes.append(base_notes[note_index+1])
  #   close_notes.append(base_notes[note_index-1])
  #   # plt.plot(np.array([yin_notes, fft_notes]).T, np.array([yin_cents,fft_cents]).T, 'k-', label="Yin & FFT Agree")
  #   if fft_notes[i] in close_notes:
  #     plt.plot([yin_notes[i], fft_notes[i]], [yin_cents[i],fft_cents[i]], 'k-')
  plt.scatter(yin_notes, yin_cents, c='g', label="Yin")
  plt.scatter(fft_notes, fft_cents, c='r', label="FFT")
  plt.ylim([-50,50])
  plt.yticks(np.arange(-50, 50, 10))
  print("Showing")
  plt.title(f"Comparing FFT and Yin Algorithms\n{title}\nTruth Notes: {truth}")
  plt.xlabel("Notes")
  plt.ylabel("Cents")
  plt.legend()
  # plt.savefig(f"graphs/{output_filename}.png")
  plt.show()

def plot_real_comparison(midi, real, untuned, truth, title):
  midi_notes = []
  midi_cents = []
  real_notes = []
  real_cents = []
  untuned_notes = []
  untuned_cents = []

  for note, wrong, _ in midi:
    midi_notes.append(note)
    midi_cents.append(wrong)

  for note, wrong, _ in real:
    real_notes.append(note)
    real_cents.append(wrong)
  
  for note, wrong, _ in untuned:
    untuned_notes.append(note)
    untuned_cents.append(wrong)

  
  base_notes = create_baseline()
  quantified_width = list(range(len(base_notes)))
  inharmonicity_curve = [0.0003*(x-(len(base_notes)//2))**3 for x in quantified_width]

  print("Plotting")
  plt.grid(True)
  plt.plot(base_notes, inharmonicity_curve, label="Inharmonicity Curve")
  plt.vlines(truth, -50, 50, linestyles="--", label="Correct Notes")
  # notes = np.array(notes)
  # cents_out = np.array(cents_out)
  # if len(yin_notes) == len(fft_notes):
  #   for i in range(len(yin_notes)):
  #     if yin_notes[i] == fft_notes[i]:
  #       plt.plot([yin_notes[i], fft_notes[i]], [yin_cents[i],fft_cents[i]], 'k-')
  # for i in range(min_length):
  #   close_notes = [yin_notes[i]]
  #   note_index = base_notes.index(yin_notes[i])
  #   close_notes.append(base_notes[note_index+1])
  #   close_notes.append(base_notes[note_index-1])
  #   # plt.plot(np.array([yin_notes, fft_notes]).T, np.array([yin_cents,fft_cents]).T, 'k-', label="Yin & FFT Agree")
  #   if fft_notes[i] in close_notes:
  #     plt.plot([yin_notes[i], fft_notes[i]], [yin_cents[i],fft_cents[i]], 'k-')
  plt.scatter(midi_notes, midi_cents, c='g', label="MIDI", alpha=0.7)
  plt.scatter(real_notes, real_cents, c='r', label="Tuned Piano", alpha=0.7)
  plt.scatter(untuned_notes, untuned_cents, c='b', label="Less Tuned Piano", alpha=0.7)
  plt.ylim([-50,50])
  plt.yticks(np.arange(-50, 50, 10))
  print("Showing")
  plt.title(f"Comparing Pianos\n{title}\nTruth Notes: {truth}")
  plt.xlabel("Notes")
  plt.ylabel("Cents")
  plt.legend()
  # plt.savefig(f"graphs/{output_filename}.png")
  plt.show()