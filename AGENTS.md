# Heart TS Analysis - Agent Orientation Guide

This guide orients contributors to the heart-ts-analysis workspace. Start with `./workspace/GOAL.md` as the single source of truth; keep this file and plan trackers in sync (TODO: `./workspace/PLAN.md`, `./workspace/PLAN_PROGRESS.md`).

---

## 🎯 PROJECT MISSION

**Goal**: Build a clear, reproducible pipeline that separates respiratory motion from cardiac motion in MIDAS time-series data, detects heart beats on the isolated cardiac component, and groups signals into four conditions (control, doxo, doxo+epa, other) using time-series representations.

**Vision**: A robust, transparent analysis flow that yields trustworthy separation, beat picks, and group-level insights without leakage, and can be extended as new data or labels arrive.

**Core Innovation**: Spectrum-guided, zero-phase separation plus beat-centric representations and strong baselines (MiniROCKET) to quickly reach reliable classification or clustering outcomes.

Primary reference: `./workspace/GOAL.md` (authoritative target and integration blueprint)

### Goal Alignment Policy

- Goal (single source of truth): `./workspace/GOAL.md`.
- Every task must explicitly advance the goal. Sidequests are allowed only if they reduce risk or unblock progress.
- Before starting work, add a one-line "Goal alignment" rationale in your notes or PR description.
- If work conflicts with the goal, reroute and propose an aligned alternative.

### Constraint Policies (Must-Haves)

- **Heart rate target**: detected BPM should fall within **270–310 bpm** (flag deviations and adjust preprocessing or band selection).
- **Respiration target**: respiratory cycles should be **~72 cycles/min** (expect a stable period near **0.83 s**; adjust resp band if drifting).
- **Decomposition expectation**:
  - Respiration is **low‑frequency, near‑sinusoidal, and stable in period** across the clip.
  - Respiration **amplitude should exceed heart** in FFT decomposition plots.
  - Heart band is **higher‑frequency** with **minimal slow envelope drift**; if strong slow modulation appears, treat as leakage.
- **Label integrity**: labels come from filenames and must never be used to bias clustering inputs; only use them for evaluation and reporting.
- **Leakage guard**: keep beat detection/feature extraction independent of labels; validate by animal/recording for any supervised baselines.

---

## 📁 PROJECT STRUCTURE OVERVIEW

### Top-level directories

- `./data/`: Raw MIDAS motion time-series CSVs (control, doxo, empa, empa_doxo, preconditionare_empa_doxo).
- `./workspace/`: Knowledge and planning hub (see substructure below).
- `./AGENTS_old.md`: Legacy orientation draft; superseded by this guide.

### Workspace substructure

- `./workspace/GOAL.md`: North Star mission (keep current).
- `./workspace/agent-research/`: Ideation drafts (`!research` outputs).
- `./workspace/agent-review/`: Pre-implementation reviews (`!review` outputs).
- `./workspace/brainstorming/{sessions,external}/`: Structured sessions and imported transcripts.
- `./workspace/concepts/{extracted,mix,operationalized}/`: Concept library (currently empty).
- `./workspace/deep-research/{reports,sources,oracle}/`: Research outputs and provenance.
- `./workspace/evolution/{artifacts,db,jobs,worktrees}/`: Evolution run artifacts.
- `./workspace/integration/`: Integration designs (currently empty).
- `./workspace/notes/`: Directed findings (currently empty).
- `./workspace/references/`: Reference briefs (currently empty).
- `./workspace/reports/`: Narrative reports (currently empty).
- `./workspace/research-projects/`: Submodule slots (currently empty).
- `./workspace/resources-for-comparison/`: Comparative materials.
- `./workspace/system-design/`: System design docs (currently empty).

---

## 🔬 RESEARCH PROJECTS & REFERENCES

No reference briefs or research submodules are present yet.

- **Knowledge Fabric**: TODO (populate `./workspace/references/`)
- **Agent Orchestration**: TODO
- **CLI/Tooling Foundations**: TODO
- **Evolutionary Systems**: TODO
- **Deep Research**: TODO
- **Guardrails**: TODO

Primary reference remains: `./workspace/GOAL.md`.

---

## 🏗️ SYSTEM ARCHITECTURE

Target pipeline (current repo is data-first; code TBD):

```
Raw CSVs -> PSD (Welch) -> Zero-phase filters (resp/heart)
        -> Heart envelope -> Peak picking -> Beat windows
        -> Feature extraction (MiniROCKET / wavelet / DTW)
        -> Classification or clustering -> Reports
```

Control signals and guardrails:
- Zero-phase filtering to avoid timing shifts.
- Refractory-period peak picking to prevent false beats.
- Cross-validation by animal/recording to prevent leakage.
- Parameter logging for reproducibility (cutoffs, windows, thresholds).

---

## 📚 RESOURCE LOCATIONS

### Master planning & goals
- Goal (authoritative): `./workspace/GOAL.md`
- Master plan: TODO (`./workspace/PLAN.md` missing)
- Plan progress: TODO (`./workspace/PLAN_PROGRESS.md` missing)

### Research & architecture references
- Reference briefs: TODO (`./workspace/references/` empty)
- Research submodules: TODO (`./workspace/research-projects/` empty)

### Brainstorming, notes, and reports
- Brainstorming sessions: `./workspace/brainstorming/sessions/`
- External transcripts: `./workspace/brainstorming/external/`
- Notes: `./workspace/notes/` (empty)
- Reports: `./workspace/reports/` (empty)
- Deep research outputs: `./workspace/deep-research/reports/`

### Commands and automations
- `.agents/commands/`: TODO (directory missing)

---

## 🧠 Working Agreements & Rituals

- Log a one-line "Goal alignment" note before each task.
- Update `./workspace/GOAL.md` when scope or success criteria change.
- Keep artifacts small, cite data sources, and avoid duplicating canonical notes.
- Prefer rerouting plans over stalling when assumptions break.
- Use `/status`, `/review`, and `/approvals` rhythms when available.

---

## ⚙️ Execution Playbook

No build orchestration files were found (no `Cargo.toml`, `package.json`, `Makefile`, `justfile`, or `requirements.txt`).

- TODO: add a README and scripts that define how to run the pipeline.
- TODO: document environment setup (Python version, dependencies).
- Data inputs: `./data/*.csv`.

---

## 🚨 Guardrails & Memory

- AGENTS discovery order: home -> repo root -> cwd; check for `AGENTS.override.md`.
- `./workspace/GOAL.md` is the single source of truth; keep AGENTS/plan files aligned.
- No MCP/memory services are configured yet (TODO: document if added).
- Follow sandbox/approval policies for destructive commands and network access.
