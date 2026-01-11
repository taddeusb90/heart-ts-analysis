# AGENTS

## Project context
This repo targets time-series analysis of MIDAS motion signals from rats, mixing respiratory and cardiac motion. Data lives in `./data`.

## Primary objective
Build a robust pipeline to:
1) separate respiration vs heart motion,
2) detect heart beats from the isolated heart component,
3) group signals into four conditions (control, doxo, doxo+epa, other) using time-series representations.

## Technical guidance
- Start with frequency-domain inspection (Welch PSD) to set cutoff bands.
- Prefer zero-phase digital filters (`filtfilt`/`sosfiltfilt`) over FFT masking for separation.
- If bands overlap or drift, consider VMD or wavelet decomposition as a second-line method.
- Beat detection: band-pass -> envelope (Hilbert or RMS) -> `find_peaks` with refractory period and prominence.
- For grouping:
  - If labels are known, treat as supervised classification (MiniROCKET + linear classifier as strong baseline).
  - If exploratory, cluster embeddings (MiniROCKET/Wavelet/WST) with k-means or HDBSCAN.
  - If morphology matters, cluster per-beat windows using DTW or k-Shape.

## Constraints & expectations
- Keep methods interpretable and reproducible.
- Avoid leakage: cross-validate by animal/recording, not by beat/window.
- Prefer minimal, clear baselines before adding complexity.

## Deliverables to aim for
- A script/notebook that:
  - computes PSD,
  - performs separation,
  - detects beats,
  - produces features and a basic classifier/clustering run.
- Short report/notes describing parameter choices and observed results.
