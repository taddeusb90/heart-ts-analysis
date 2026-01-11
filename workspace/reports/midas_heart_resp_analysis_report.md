# MIDAS Heart/Resp Analysis Handover Report

## Overview
This report summarizes the full pipeline setup, notebook implementation, parameter decisions, results, limitations, and file locations for the MIDAS motion time-series analysis project. It is meant to allow another researcher/assistant to continue the work without re-deriving context.

Project goal: separate respiratory and cardiac motion, detect beats, and assess whether signals cluster into four ground-truth groups (control, doxo, empa, empa_doxo) without label leakage.

---

## Repo structure and key files

- Data: `./data/*.csv` (18 total files)
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
- **Actual frame rate is 18 fps** (overrides time column).
- In notebook: `FRAME_RATE_FPS = 18.0` and `USE_FRAME_RATE = True`.
- Time series are rebuilt as `time_s = np.arange(len(signal)) / fps`.

### Implications at 18 fps
- Heart rate target: 270–310 bpm ⇒ 4.5–5.2 Hz.
- At 18 fps, only ~3–4 samples per beat.
- **Conclusion**: beat morphology is under-sampled → beat-shape clustering is unreliable.

---

## Pipeline implemented in notebook

### 1) Spectrum inspection (Welch PSD)
- PSD computed for inspection and HR estimation.
- This is **reliable** at low fps for detecting the dominant heart peak.

### 2) Respiration vs heart separation
- Two methods:
  - FFT masking (`SEPARATION_METHOD = "fft"`)
  - Zero-phase Butterworth band-pass (optional)
- Current bands:
  - Respiration: `RESP_BAND_HZ = (0.1, 2.0)`
  - Heart: `HEART_BAND_HZ = (4.0, 6.5)`

### 3) Respiratory cycle timing (new)
- Detects peaks/troughs in smoothed respiration to estimate:
  - Full cycle duration (peak-to-peak)
  - Inhalation duration (trough → peak)
  - Exhalation duration (peak → trough)
- Parameters:
  - `RESP_MIN_PERIOD_S = 0.5`
  - `RESP_SMOOTH_S = 0.3`
  - `RESP_PROMINENCE_FACTOR = 1.0`

### 4) Beat detection
- Heart-band Hilbert envelope
- Smoothed envelope and robust prominence (median + 1.5×MAD)
- Refractory period derived from max BPM

### 5) Beat window extraction
- Fixed-length resampling per beat
- `RESAMPLE_LEN = 256`

### 6) Features + clustering
- **Unsupervised** clustering on beat-level features (MiniROCKET + KMeans/HDBSCAN)
- **k-Shape** beat-shape clustering (included but explicitly labeled unreliable at 18 fps)
- **Record-level clustering** (aggregate beats per recording)
- **Record-level features** (resp power, heart power, PSD HR, HRV proxy)

### 7) Visualizations and saving
- All plots are saved automatically to `./outputs/figures`.

---

## Ground-truth groups (from filenames)

Label mapping used **only for evaluation**:
- `control*` → `control`
- `doxo*` and `doxo_re*` → `doxo`
- `empa*` → `empa`
- `empa_doxo*` and `preconditionare_empa_doxo*` → `empa_doxo`

Clustering never uses these labels.

---

## Results summary (18 fps)

### Reliable outputs
- **PSD-based HR estimates** are within expected range:
  - Mean ≈ 265.8 bpm, median ≈ 264.1 bpm, max ≈ 309 bpm.
- Respiration component shows periodic signal; cycle timing can be extracted.

### Weak outputs (expected at 18 fps)
- Beat-level clustering metrics are near zero (ARI/NMI ≈ 0).
- k-Shape clustering weak (shape is under-sampled).

### Record-level clustering
- Some signal present but modest:
  - Record-level KMeans on beat features: ARI ~0.10, NMI ~0.29, best alignment ~0.56.
  - Record-level KMeans on band-power/PSD/HRV features: ARI ~−0.04, NMI ~0.20.

**Interpretation**: With 18 fps, only PSD HR + record-level features are reliable. Beat-shape clustering should be considered exploratory at best.

---

## Saved figures

Location: `./outputs/figures/`

Key files:
- `psd_control(I.1).png`
- `fft_decomposition_control(I.1).png`
- `separation_fft_control(I.1).png`
- `beat_detection_control(I.1).png`
- `decomposition_by_category_fft.png`
- `beat_detection_by_category_fft.png`
- `resp_cycles_by_category_fft.png`
- `embedding_labels_vs_clusters.png`

---

## Gemini analysis (visual inspection)

Gemini was used to analyze plots. It noted:
- Respiration appears periodic and well isolated.
- Heart/resp overlap appears minimal.
- Beat detection peaks align well.

Caveat: Gemini described embeddings as well separated, but **quantitative metrics do not confirm** this. Do not rely on visual embedding separation alone.

---

## Known limitations

- 18 fps sampling rate under-samples cardiac morphology.
- Beat-shape clustering and morphology comparisons are unreliable.
- FFT masking can introduce ringing; zero-phase filtering is preferred if signal quality allows.
- Embeddings can look separated even when metrics are poor.

---

## Recommendations for next steps

1) If possible, obtain higher-fps data (60+ fps) for reliable morphology.
2) If stuck at 18 fps, focus on:
   - PSD HR estimates
   - Resp cycle timing
   - Record-level spectral features
3) If ventilator rate is known, set a **narrow respiration band-pass** around that rate to get a cleaner sinusoid.
4) Consider adding a summary table by group (mean resp cycle, mean PSD HR).

---

## How to run

```bash
poetry install
poetry run jupyter notebook
```

Open: `notebooks/heart_midas_pipeline.ipynb`

---

## Key parameters in notebook

- `FRAME_RATE_FPS = 18.0`
- `RESP_BAND_HZ = (0.1, 2.0)`
- `HEART_BAND_HZ = (4.0, 6.5)`
- `MIN_BPM = 270`, `MAX_BPM = 310`
- `REFRACTORY_S = 0.9 * (60 / MAX_BPM)`
- `BEAT_WINDOW_S = (0.3 * (60 / MIN_BPM), 0.7 * (60 / MIN_BPM))`
- `ENV_SMOOTH_S = 0.08`
- `RESAMPLE_LEN = 256`
- `RESP_MIN_PERIOD_S = 0.5`, `RESP_SMOOTH_S = 0.3`

---

## Files modified/created in this work session

- `notebooks/heart_midas_pipeline.ipynb`
- `outputs/figures/*.png`
- `pyproject.toml`, `poetry.toml`, `.python-version`, `.env`
- `AGENTS.md`, `workspace/GOAL.md`
- `workspace/reports/midas_heart_resp_analysis_report.md` (this report)

---

## Handover notes

- The pipeline is stable and reproducible.
- The biggest blocker is sampling rate — morphology-based clustering is not reliable at 18 fps.
- Record-level features and PSD-based HR are currently the strongest signals.

