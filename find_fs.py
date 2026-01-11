
import numpy as np
import pandas as pd
from scipy.signal import welch
import glob

def find_correct_fs():
    files = sorted(glob.glob("data/*.csv"))
    filepath = files[0]
    df = pd.read_csv(filepath)
    signal = df.iloc[:, 1].to_numpy()
    
    # Assume target resp is 71 BPM (1.183 Hz)
    target_hz = 71.0 / 60.0
    
    # We found that at 60 FPS, the peak was at ~0.86 Hz (found via 52 BPM / 60)
    # peak_idx / N * 60 = 0.86
    # We want peak_idx / N * FS_new = 1.183
    # FS_new = 60 * (1.183 / 0.86)
    
    # Let's verify peak location in normalized units (cycles per sample)
    f, pxx = welch(signal, fs=1.0, nperseg=min(len(signal), 1024))
    mask = (f > 0.01) & (f < 0.1) # search low frequencies
    peak_freq_norm = f[mask][np.argmax(pxx[mask])]
    
    # target_hz = peak_freq_norm * FS_new
    fs_new = target_hz / peak_freq_norm
    
    print(f"Detected Resp Peak (norm): {peak_freq_norm:.5f} cycles/sample")
    print(f"Target Resp Frequency: {target_hz:.5f} Hz (71 BPM)")
    print(f"Calculated Correct FS: {fs_new:.2f} FPS")

if __name__ == "__main__":
    find_correct_fs()
