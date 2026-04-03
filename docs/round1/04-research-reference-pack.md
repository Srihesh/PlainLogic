# Research Reference Pack (Think Big, Build Rigor)

Use this pack to design an original environment grounded in proven research patterns.
Use ideas, not copied tasks.

## A. Core Agent-Environment Design

1. ReAct
  - Citation: Yao et al., ICLR 2023.
  - Use: step-by-step reasoning plus action.
  - Implementation move: keep structured trajectory logs and reward useful intermediate transitions.

2. Toolformer
  - Citation: Schick et al., NeurIPS 2023.
  - Use: tool/action invocation as model behavior.
  - Implementation move: define explicit action schemas and strict parser-safe action formats.

3. Reflexion
  - Citation: Shinn et al., NeurIPS 2023 workshop track.
  - Use: self-correction loops from feedback.
  - Implementation move: include penalties for repeating failed actions and bonus for corrected retries.

## B. Benchmark and Evaluation Rigor

1. SWE-bench
  - Citation: Jimenez et al., ICLR 2024.
  - Use: deterministic, replayable evaluation.
  - Implementation move: fixture-based graders and run-to-run consistency tests.

2. WebArena
  - Citation: Zhou et al., 2023.
  - Use: long-horizon realistic tasks.
  - Implementation move: easy/medium/hard progression with dependency and policy constraints.

3. ALFWorld
  - Citation: Shridhar et al., ICLR 2021.
  - Use: stateful interaction and grounded transitions.
  - Implementation move: explicit world state updates and strict done criteria.

## C. Reward Design and Safety

1. Potential-Based Reward Shaping
  - Citation: Ng, Harada, Russell, ICML 1999.
  - Use: dense shaping without changing optimal policy under conditions.
  - Implementation move: progress potential function with bounded shaping.

2. Reward Hacking Risks
  - Citation: Amodei et al., Concrete Problems in AI Safety, 2016.
  - Use: prevent objective gaming.
  - Implementation move: disallow easy exploit loops, add invalid-action costs, and monitor suspicious trajectories.

3. Process Supervision Trends
  - Use: reward components mapped to trajectory quality, not only terminal success.
  - Implementation move: split score into policy compliance, progress, and efficiency components.

## D. LLM Post-Training Context (For Design Judgment)

1. DeepSeekMath / GRPO-style reporting
  - Citation: Shao et al., 2024.
  - Use: stable policy optimization with grouped comparisons.
  - Implementation move: design tasks where relative quality between attempts is measurable.

2. Preference Learning family (DPO and related)
  - Use: preference signals in addition to scalar rewards.
  - Implementation move: prepare optional pairwise trajectory metadata for future extension.

## E. Paper-to-Environment Mapping Template

For each design decision, write one line in README:

1. Decision
2. Which paper informed it
3. How it was adapted
4. Why it remains deterministic

Example:

- Decision: medium task includes multi-incident dependency graph.
- Reference: WebArena long-horizon structure.
- Adaptation: synthetic city operations domain.
- Determinism: fixed fixture and seeded event order.

## F. Additional Web-Verified References (High Value)

1. WebArena: A Realistic Web Environment for Building Autonomous Agents
  - Citation: Zhou et al., arXiv:2307.13854 (2023/2024 revision).
  - Link: https://arxiv.org/abs/2307.13854
  - Why useful: realistic long-horizon task design with reproducibility emphasis.
  - Implementation move: keep your task interfaces realistic, but grading deterministic.

2. Concrete Problems in AI Safety
  - Citation: Amodei et al., arXiv:1606.06565 (2016).
  - Link: https://arxiv.org/abs/1606.06565
  - Why useful: reward hacking and objective misspecification framing.
  - Implementation move: explicitly test loop exploits and malformed action exploits.

3. When is Tree Search Useful for LLM Planning? It Depends on the Discriminator
  - Citation: Chen et al., arXiv:2402.10890 (ACL 2024).
  - Link: https://arxiv.org/abs/2402.10890
  - Why useful: advanced search may be slower with little gain unless discriminator quality is high.
  - Implementation move: prioritize efficient reranking/heuristic fallback over expensive tree search in baseline.

4. Voyager: An Open-Ended Embodied Agent with Large Language Models
  - Citation: Wang et al., arXiv:2305.16291 (2023).
  - Link: https://arxiv.org/abs/2305.16291
  - Why useful: curriculum + reusable skill library pattern for open-ended improvement.
  - Implementation move: add reusable action templates and progression from easy to hard fixtures.

5. Improving Factuality and Reasoning in Language Models through Multiagent Debate
  - Citation: Du et al., arXiv:2305.14325 (2023).
  - Link: https://arxiv.org/abs/2305.14325
  - Why useful: disagreement-based verification can improve reliability.
  - Implementation move: optional dual-policy check mode for hard tasks (primary policy + verifier policy).

6. Large Language Models Are Human-Level Prompt Engineers (APE)
  - Citation: Zhou et al., arXiv:2211.01910 (2022/2023 revision).
  - Link: https://arxiv.org/abs/2211.01910
  - Why useful: prompt/instruction search as measurable optimization loop.
  - Implementation move: tune task instruction templates with score-based prompt selection.

7. Evaluating Frontier Models for Dangerous Capabilities
  - Citation: Phuong et al., arXiv:2403.13793 (2024).
  - Link: https://arxiv.org/abs/2403.13793
  - Why useful: structured capability evaluation methodology.
  - Implementation move: include red-team trajectories and failure-mode test suite in evaluation artifacts.

## Practical Rule

Use research to strengthen:

1. state/action design
2. grader rigor
3. reward shaping discipline
4. anti-exploit hardening

Never use research to justify:

1. copied benchmark tasks
2. renamed public environments
3. non-reproducible scoring behavior
