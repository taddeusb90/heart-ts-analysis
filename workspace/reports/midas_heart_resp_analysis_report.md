# MIDAS Heart/Resp Analysis Handover Report

## Overview
This report summarizes the full pipeline setup, notebook implementation, parameter decisions, results, limitations, and file locations for the MIDAS motion time-series analysis project. It is meant to allow another researcher/assistant to continue the work without re-deriving context.

Project goal: separate respiratory and cardiac motion, detect beats, and assess whether signals cluster into four ground-truth groups (control, doxo, empa, empa_doxo) without label leakage.

---

## Repo structure and key files

- Data: `./data/*.csv` (18 files)
- Notebook: `./notebooks/heart_midas_pipeline.ipynb`
- Outputs (saved plots): `./outputs/figures/*.png`
- Environment config:
  - `pyproject.toml`, `poetry.toml` (Poetry setup, in-project `.venv`)
  - `.python-version` (pyenv version = 3.11.13)
  - `.env` (DATA_DIR, NOTEBOOKS_DIR)
- Orientation: `AGENTS.md`, `workspace/GOAL.md`

---

## Data assumptions and frame rate

- MIDAS motion detection derived from video.
- **Actual frame rate is 60 fps** (overrides time column).
- Notebook setting: `FRAME_RATE_FPS = 60.0`, `USE_FRAME_RATE = True`.
- Time series are rebuilt as `time_s = np.arange(len(signal)) / fps`.

---

## Ground-truth groups (from filenames)

Label mapping used **only for evaluation**:
- `control*` → `control`
- `doxo*` and `doxo_re*` → `doxo`
- `empa*` → `empa`
- `empa_doxo*` and `preconditionare_empa_doxo*` → `empa_doxo`

Clustering never uses these labels.

---

## Pipeline implemented in notebook

### 1) Spectrum inspection (Welch PSD)
- PSD computed for inspection and HR estimation.
- HR is estimated from the **heart-band PSD peak** after separation.

### 2) Respiration vs heart separation
- **Methodology update**: Respiration is isolated first using a fixed band-pass (70-80 bpm). The **Heart component is derived from the residual** (Signal - Respiration) to ensure complete removal of respiratory motion, followed by a band-pass filter (270-310 bpm) to isolate cardiac activity.
- Two methods:
  - FFT masking
  - Zero-phase Butterworth band-pass (current default)
- Current bands:
  - Respiration: **fixed band-pass** from 70–80 bpm
  - Heart: `HEART_BAND_HZ = (MIN_BPM/60, MAX_BPM/60)` → (4.5–5.17 Hz)

### 3) Respiratory cycle timing
- Detects peaks/troughs in smoothed respiration to estimate:
  - Full cycle duration (peak-to-peak)
  - Inhalation duration (trough → peak)
  - Exhalation duration (peak → trough)

**Ventilator target**:
- Controlled at **70–80 cycles/min**.
- Notebook setting: `RESP_BPM_RANGE = (70.0, 80.0)`.
- Resp band uses a **narrow band-pass** locked to the range.

### 4) Beat detection
- Heart-band signal normalized by MAD and used for peak detection.
- Refractory period derived from max BPM.

### 5) Beat window extraction
- Fixed-length resampling per beat.
- `RESAMPLE_LEN = 256`.

### 6) Features + clustering
- **Unsupervised** clustering on beat-level features (MiniROCKET + KMeans/HDBSCAN)
- **k-Shape** beat-shape clustering
- **Record-level clustering** (aggregate beats per recording)
- **Record-level features** (resp power, heart power, PSD HR, HRV proxy)

### 7) Visualizations and saving
- All plots are saved automatically to `./outputs/figures`.

---

## Results summary (60 fps, RESP_BPM_RANGE=70–80)

### Heart rate estimates
- **PSD HR (bpm)**: mean **286.0**, median **283.0**, min **273.5**, max **307.9**
- **Peak HR (bpm)**: mean **291.6**, median **300.0**, min **276.9**, max **300.0**

These align with the expected 270–310 bpm range.

### Respiratory cycle timing (fixed range)
- Expected cycle at 75 bpm ≈ **0.80 s**.
- Measured cycle delta vs expected: mean **−0.01 s**, min **−0.04 s**, max **+0.03 s**.

This indicates respiration is now locked to the ventilator range as intended.

### Beat extraction and clustering
- Total beat windows: **873** (shape length 256)
- Supervised MiniROCKET Group CV accuracy: **~0.20 ± 0.09**

**Unsupervised beat-level clustering** (weak signal):
- KMeans ARI 0.011, NMI 0.012, alignment 0.315
- HDBSCAN ARI 0.002, NMI 0.004, alignment 0.346
- k-Shape ARI 0.001, NMI 0.003, alignment 0.276

**Record-level clustering**:
- Record-level KMeans (beat features): ARI −0.074, NMI 0.155, alignment 0.389
- Record-level KMeans (spectral features): ARI 0.074, NMI 0.308, alignment 0.500

**Interpretation**: Beat-level clustering remains weak. Record-level spectral features are the most stable unsupervised signal, though still modest.

---

## Saved figures

Location: `./outputs/figures/`

Key files:
- `psd_control(I.1).png`
- `fft_decomposition_control(I.1).png`
- `separation_filter_control(I.1).png` (or `separation_fft_*` depending on method)
- `beat_detection_control(I.1).png`
- `decomposition_by_category_filter.png` (or fft variant)
- `beat_detection_by_category_filter.png` (or fft variant)
- `resp_cycles_by_category_filter.png` (or fft variant)
- `embedding_labels_vs_clusters.png`

---

## Known limitations

- Beat-level clustering does not clearly separate treatment groups.
- Embedding visuals may look separated even when ARI/NMI is low.

---

## Recommendations for next steps

1) If labels are available and classification is desired, use **supervised MiniROCKET** rather than clustering.
2) For unsupervised work, prefer **record-level spectral features** (PSD HR, band power, HRV proxy).
3) If morphology-based separation is critical, collect higher-resolution signals or use multi-channel references.

---

## How to run

```bash
poetry install
poetry run jupyter notebook
```

Open: `notebooks/heart_midas_pipeline.ipynb`

---

## Key parameters in notebook (current)

- `FRAME_RATE_FPS = 60.0`
- `RESP_BPM_RANGE = (70.0, 80.0)`
- `RESP_BAND_HZ = (0.1, 2.0)` (fallback if range not set)
- `MIN_BPM = 270`, `MAX_BPM = 310`
- `HEART_BAND_HZ = (4.5, 5.17)`
- `REFRACTORY_S = 0.85 * (60 / MAX_BPM)`
- `ENV_SMOOTH_S = 0.05`
- `RESAMPLE_LEN = 256`

---

## Files modified/created in this work session

- `notebooks/heart_midas_pipeline.ipynb`
- `outputs/figures/*.png`
- `workspace/reports/midas_heart_resp_analysis_report.md` (this report)

---

## Handover notes

- **Pipeline Update**: The separation logic now explicitly defines the Heart component as the residual of the signal after removing the fixed respiratory band (70-80 bpm).
- Heart-rate estimation is now within expected bounds (270-310 bpm).
- Respiratory extraction is locked to the fixed ventilator range (70–80 bpm).
- Unsupervised clustering does not show strong separation; record-level spectral features remain the most reliable signal.

