# ResilienceOS

ResilienceOS is a deterministic city emergency operations simulator for OpenEnv-style agent training.

## Documentation map

1. docs/index.md
2. docs/contracts.md
3. docs/paper_to_code_mapping.md
4. docs/submission_notes.md
5. docs/submission_manifest.md
6. docs/final_gate_check.md
7. docs/gemini_sanity_checks.md

## Real-world motivation

ResilienceOS simulates a city emergency operations workflow where incidents compete for limited resources under policy constraints.
This targets realistic long-horizon coordination instead of toy interactions.

## What is implemented

1. Deterministic fixtures for easy, medium, and hard tasks.
2. Typed action and observation contracts.
3. Deterministic grading in [0.0, 1.0].
4. Anti-loop and invalid-action penalties.
5. Baseline runner using a deterministic heuristic policy.
6. API server endpoints: health, reset, step, state.
7. Round 1 inference script with policy modes: heuristic, model, hybrid.

## Action schema

Action fields:

1. action_type
2. incident_id
3. resource_id
4. payload

Supported action types:

1. classify_incident
2. request_missing_fields
3. assign_resource
4. reroute_resource
5. escalate_to_regional
6. activate_shelter
7. defer_with_justification
8. close_incident

## Observation schema

Observation fields:

1. task
2. step
3. remaining_steps
4. incidents
5. resources
6. policy
7. last_result

## Task progression

1. easy
	- Single incident with clear optimal policy path.
2. medium
	- Multi-incident prioritization under limited resources.
3. hard
	- Cascading incident handling with escalation and shelter constraints.

## Grading and reward shaping

Final score combines:

1. policy alignment
2. objective progress
3. efficiency

Score formula:

1. score = 0.45 * policy_alignment + 0.45 * objective_progress + 0.10 * efficiency
2. final_score = clamp(score - exploit_penalty, 0.0, 1.0)

Step rewards include:

1. progress gain
2. policy bonus
3. invalid-action penalty
4. loop penalty

## Local setup

1. Create and activate a Python environment.
2. Install package.

```bash
python -m pip install -e .
```

3. Run baseline report.

```bash
python scripts/baseline_inference.py --seed 7 --output outputs/baseline_report.json
```

4. Run determinism check.

```bash
python scripts/determinism_check.py
```

## API server run

```bash
uvicorn resilienceos.server:app --host 0.0.0.0 --port 8000
```

## Round 1 inference script

Recommended hackathon variables:

1. HF_TOKEN
2. OPENAI_BASE_URL=https://router.huggingface.co/v1
3. MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

Also supported:

1. OPENAI_API_KEY (if you choose OpenAI billing path)

```bash
python scripts/inference_round1.py --seed 7 --policy heuristic --output outputs/round1_inference_report.json
```

No paid OpenAI key is required if your Hugging Face token has available router credits.

## Docker

```bash
docker build -t resilienceos:round1 .
docker run --rm resilienceos:round1
```

## Reproducibility notes

1. Use fixed seed for comparison runs.
2. Determinism check compares two full task sweeps.
3. Graders are bounded and deterministic by design.

## Baseline score table (seed 7)

1. easy: 1.000000
2. medium: 1.000000
3. hard: 1.000000
4. aggregate: 1.000000

## Submission artifact checklist

1. outputs/baseline_report.json
2. outputs/deterministic_replay_report.txt
3. outputs/docker_build_log.txt
4. outputs/local_validate_log.txt
5. outputs/deployment_healthcheck.txt
6. docs/submission_manifest.md
7. docs/final_gate_check.md
8. outputs/eval_matrix_report.json
9. outputs/red_team_report.json
10. docs/gemini_sanity_checks.md
11. outputs/all_outputs_dump.txt

## Paper-backed features applied in code

1. Deterministic reproducible environment and long-horizon tasks
	- Inspired by WebArena style realism + reproducibility.
	- Applied in fixtures and seeded task design.
2. Reward-hacking and exploit resistance checks
	- Inspired by Concrete Problems in AI Safety.
	- Applied in invalid-action penalties, loop tracking, and red-team eval script.
3. Efficiency-first planning policy
	- Inspired by findings that expensive search is not always worth it without strong discriminators.
	- Applied via heuristic baseline and hybrid fallback policy mode.
4. Capability and failure-mode evaluation mindset
	- Inspired by frontier capability evaluation frameworks.
	- Applied via explicit red-team scenario checks and evaluation artifact generation.

## Research traceability

Paper-to-code mapping:

1. docs/paper_to_code_mapping.md

Run red-team safety evaluation:

```bash
python scripts/red_team_eval.py
```

## Policy evaluation matrix

Generate a compact comparison report across available policies:

```bash
python scripts/eval_matrix.py
```

Output:

1. outputs/eval_matrix_report.json

## Submission notes

Use this summary while filling hackathon form fields:

1. docs/submission_notes.md

## Build submission bundle

Create a ready-to-upload artifact folder and zip:

```bash
bash scripts/build_submission_bundle.sh
```

Outputs:

1. outputs/submission_bundle/
2. outputs/submission_bundle.zip