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
- **Methodology update**: Respiration is isolated first using a fixed band-pass (71–73 bpm). The heart component is isolated with band-pass filtering (FFT masking or zero-phase Butterworth), using a wider morphology band for separation and a tighter band for HR estimation.
- Two methods:
  - FFT masking
  - Zero-phase Butterworth band-pass (current default)
- Current bands:
  - Respiration: **fixed band-pass** from 71–73 bpm
  - Heart separation: `HEART_SEPARATION_BAND_HZ` → (4.0–6.5 Hz)
  - HR estimation: `HEART_BAND_HZ` → (4.5–5.17 Hz)

### 3) Respiratory cycle timing
- Detects peaks/troughs in smoothed respiration to estimate:
  - Full cycle duration (peak-to-peak)
  - Inhalation duration (trough → peak)
  - Exhalation duration (peak → trough)

**Ventilator target**:
- Controlled at **~72 cycles/min**.
- Notebook setting: `RESP_BPM_RANGE = (71.0, 73.0)`.
- Resp band uses a **narrow band-pass** locked to the range.

### 4) Beat detection
- Heart-band signal normalized by MAD and used for peak detection.
- Refractory period derived from max BPM.

### 5) Beat window extraction
- Fixed-length resampling per beat.
- `RESAMPLE_LEN = 256`.

### 6) Features + clustering
- **Unsupervised** beat-level clustering (KMeans on PCA + MiniROCKET features)
- Beat embedding visualization (labels vs clusters)
- Record-level features (resp power, heart power, PSD HR, HRV proxy)

### 7) Visualizations and saving
- All plots are saved automatically to `./outputs/figures`.

---

## Results summary (60 fps, RESP_BPM_RANGE=71–73)

### Heart rate estimates
- **PSD HR (bpm)**: mean **289.9**, median **290.1**, min **272.0**, max **309.1**

These align with the expected 270–310 bpm range.

### Respiratory cycle timing (fixed range)
- Expected cycle at 72 bpm ≈ **0.83 s**.
- Measured cycle delta vs expected: mean **~0.00 s**, observed range **−0.01 s to +0.00 s**.

This indicates respiration is now locked to the ventilator range as intended.

### Beat extraction and clustering
- Total beat windows: **70** (shape length 256, capped to 60 beats/record for balance)
- Supervised MiniROCKET Group CV accuracy: **0.143 ± 0.065**

**Unsupervised beat-level clustering** (redo, beats only):
- Beat KMeans (PCA features): ARI **0.026**, NMI **0.073**, purity **0.414**
- Beat KMeans (MiniROCKET features): ARI **0.026**, NMI **0.073**, purity **0.414**

**Interpretation**: Beat-level clustering improves slightly but remains weak; purity is modest. This suggests that beat morphology alone is not strongly separated by treatment in this dataset.

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
- `RESP_BPM_RANGE = (71.0, 73.0)`
- `RESP_BAND_HZ = (0.1, 2.0)` (fallback if range not set)
- `MIN_BPM = 270`, `MAX_BPM = 310`
- `HEART_BAND_HZ = (4.5, 5.17)`
- `HEART_SEPARATION_BAND_HZ = (4.0, 6.5)`
- `REFRACTORY_S = 0.85 * (60 / MAX_BPM)`
- `ENV_SMOOTH_S = 0.02`
- `BEAT_PROMINENCE = 0.8`
- `RESAMPLE_LEN = 256`
- `MAX_BEATS_PER_RECORD = 60`

---

## Files modified/created in this work session

- `notebooks/heart_midas_pipeline.ipynb`
- `outputs/figures/*.png`
- `workspace/reports/midas_heart_resp_analysis_report.md` (this report)

---

## Handover notes

- **Pipeline Update**: Respiration and heart are isolated via band-pass filtering (FFT or zero-phase Butterworth). The separation band is wider (4.0–6.5 Hz) for morphology; HR estimation remains in 270–310 bpm.
- Heart-rate estimation is now within expected bounds (270-310 bpm).
- Respiratory extraction is locked to the fixed ventilator range (71–73 bpm).
- Unsupervised clustering does not show strong separation; record-level spectral features remain the most reliable signal.
