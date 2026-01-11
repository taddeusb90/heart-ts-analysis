# GOAL

## Mission
Build a clear, reproducible pipeline that separates respiratory motion from cardiac motion in MIDAS time-series data from rats, detects heart beats on the isolated cardiac component, and groups signals into four conditions (control, doxo, doxo+epa, other) using time-series representations.

This document is the single source of truth. Keep `AGENTS.md` and any plan files in sync whenever the goal or constraints change.

## Guiding Philosophy
- Treat this GOAL as the North Star for every task.
- Use spectrum-guided, zero-phase filtering before complex decomposition.
- Prefer minimal, strong baselines (MiniROCKET) before exotic models.
- Reroute the plan when assumptions fail; do not stall.
- Prevent leakage by validating per animal/recording.
- Log parameter choices and rationale for reproducibility.

## North Star Outcomes
- Reliable separation of respiratory and cardiac components without phase distortion.
- Stable beat detection with plausible heart rates and low false positives.
- Reproducible features and group assignments for the four conditions.
- A documented baseline classifier and an exploratory clustering option.
- Clear artifacts: outputs, parameters, and a summary report.

## Capability Pillars

### Orchestration
- A deterministic pipeline that runs PSD -> filtering -> beat detection -> features -> grouping.

### Knowledge Fabric
- Store rationale, parameters, and observations under `./workspace/notes/` and `./workspace/reports/`.
- Populate `./workspace/references/` as references are introduced.

### Automated Research-to-Code
- TODO: define the canonical code location and scripts for the pipeline.

### Evolutionary Self-Optimization
- TODO: no evolution loop is implemented yet; add if needed.

### Contract and Guardrail Systems
- Enforce zero-phase filtering, refractory-period peak picking, and leakage control.
- Validate inputs/outputs and keep provenance of each derived signal.

## Implementation Anchors

### Codebase homes
- No implementation packages or source directories detected yet.
- TODO: choose and document a code home (e.g., `./src/`, `./scripts/`, or notebooks).

### Data and workspace layout
- Data input: `./data/*.csv` (control/doxo/empa/empa_doxo/preconditionare_empa_doxo).
- Planning hub: `./workspace/` with brainstorming, notes, reports, and integrations.

### Knowledge and memory systems
- No MCP/memory services are configured (TODO if added later).

### Progress tracking
- TODO: add `./workspace/PLAN.md` and `./workspace/PLAN_PROGRESS.md`.

### Testing and validation
- No test suite detected; define validation checks for filters, peaks, and grouping.

### Command surface and guardrails
- No `.agents/commands/` directory found (TODO).
- Follow sandbox/approval policies and avoid destructive commands.

## Reference Exploration Map

- `./workspace/references/`: empty (add reference briefs when available).
- `./workspace/research-projects/`: empty (add submodules if needed).
- `./workspace/resources-for-comparison/`: place comparative materials and baselines.

