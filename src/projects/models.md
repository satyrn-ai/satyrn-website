---
title: Satyrn Models
description: "Small models for routine Python development, trained on community-owned data with a tight feedback loop to Satyrn Engine."
---

Small models need help for routine Python development. We want to grow a team
that ships up-to-date small models that work well with common Python frameworks — trained
on data owned by us, for us, with a tight feedback loop to [Satyrn Engine](engine.md).

**Try it now** on our [Hugging Face community](https://huggingface.co/satyrn-ai):

- [Qwen3.8-27B-py3.15](https://huggingface.co/satyrn-ai/Qwen3.8-27B-py3.15)
- [Ornith-1.5-9B](https://huggingface.co/satyrn-ai/Ornith-1.5-9B-py3.15)

## Overview

Satyrn Models focuses on fine-tuning small language models that run locally on
a developer's laptop. The goal is practical: models that understand Python well
enough to assist with everyday coding tasks — refactoring, debugging, writing tests — without
sending your code to the cloud.

Python evolves fast. New language features, standard library changes, and framework
updates arrive every release. A model trained on stale data gives stale advice.
We keep our models current by maintaining a tight feedback loop: when Python or a major
framework ships a new version, we regenerate datasets, retrain, and validate — so the
models you run locally reflect the Python you actually write.

## How We Work

The training pipeline lives in the [satyrn-models](https://github.com/satyrn-ai/satyrn-models)
repository and consists of two main components:

- **Dataset generation** — the `satyrn-dataset` CLI builds corpora from Python documentation and source code.
- **Fine-tuning** — the `satyrn-unsloth` CLI handles model training using Unsloth for efficient fine-tuning.

Training follows a three-stage pipeline, building on one another:

1. **CPT** (Continued Pretraining) — train on raw Python documentation and source text.
2. **SFT** (Supervised Fine-Tuning) — train on prompt/response pairs generated from real Python code.
3. **RL** (Reinforcement Learning) — train on a reward signal to improve response quality.

Datasets are currently available for **Python 3.14** and **Python 3.15**, covering
both CPT (raw text from CPython documentation) and SFT (prompt/response pairs generated from real code).

Experiments and spikes that explore new directions live alongside the main pipeline,
keeping the core workflow clean while encouraging iteration.

## Next Steps

- Expand dataset coverage to more Python frameworks and libraries.
- Complete the RL (Reinforcement Learning) stage of the pipeline.
- Establish a regular release cadence for model updates tied to Python version releases.
- Bring on more contributors — we want to teach folks how to do this work and grow the team.
- Partner with industry sponsors for GPU compute, so we can train more models without asking contributors to pay out of pocket.

## How to Join

If you want to help build models that work for Python developers, [get involved](../get-involved.md).
We need help with dataset curation, training experiments, evaluation, and more.
