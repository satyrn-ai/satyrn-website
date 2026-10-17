---
title: Satyrn Models on Hugging Face
date: 2026-09-29
authors:
  - postrational
description: "The first AI models to support Python 3.15, released on its release date. Small, local, fine-tuned models for routine Python development."
---

Today we are releasing the first open-weight AI model to support Python 3.15, on its
release date.

<!-- more -->

Hi, I'm Michał Karzyński, team lead for the Satyrn Models team. This is our first Satyrn
Models deliverable, helping us deliver "AI Our Way" by supporting routine Python development
on reasonable computers.

Let me tell you a bit about it and about us.

## The models

We've launched our [Hugging Face community](https://huggingface.co/satyrn-ai) with two
fine-tuned models:

- **[Qwen3.8-27B-py3.15](https://huggingface.co/satyrn-ai/Qwen3.8-27B-py3.15)** — a 27B parameter model targeting **32 GB laptops**.
- Ornith 1.5 9B for **16 GB laptops** is also being worked on.  
- Both are fine-tuned to support Python 3.15 and Python 3.14.

These are, to the best of our knowledge, the only open-weight models on Earth that know Python
3.15. We've confirmed this by checking the training cutoff dates of other popular models —
it *appears* that none of them include the Python 3.15 release.

The bigger idea here isn't just the models — it's the team and the open process behind
them. This is what "AI Our Way" looks like in practice: a community-owned, transparent
training pipeline that anyone can follow, contribute to, and trust.

## What this is and isn't

**What this is:** We are fine-tuning existing open-weight models on community-owned Python
datasets. The goal is practical assistance for everyday coding tasks — refactoring,
debugging, writing tests — running locally on your laptop without sending your code to the
cloud.

**What this isn't:** This is not full training from scratch. We're not building foundation
models. We're taking models that already understand language and code, and specializing them
on current Python so they give current advice.

Also: this isn't production-ready quite yet. We're just starting on this journey.

## How to use it

The first model is available on Hugging Face and can be run locally with any compatible
inference tool. Visit our [Satyrn Models project page](../../projects/models.md) for more information.

## How we did it

Our training pipeline lives in the
[satyrn-model](https://github.com/satyrn-ai/satyrn-model) repository and follows a three
stage process:

1. **CPT (Continued Pretraining)** — we train on raw Python documentation and source text,
   so the model learns the language as it's actually written.
2. **SFT (Supervised Fine-Tuning)** — we train on prompt and response pairs generated from
   real Python code, teaching the model to assist with developer tasks.
3. **RL (Reinforcement Learning)** — we train on a reward signal to improve response
   quality. This stage is still in progress.

Datasets are built from Python documentation and source code using our
[satyrn-dataset](https://github.com/satyrn-ai/satyrn-model) CLI, covering Python 3.14 and
3.15. Fine-tuning uses [Unsloth](https://github.com/unslothai/unsloth) for efficiency,
keeping compute costs low enough that contributors don't need industrial GPU budgets.

## What's next

We want more people involved. Both experienced model trainers and regular developers willing
to learn — we'll teach you. We're also looking for industrial partners: if your
organization can donate GPU compute, that would directly accelerate this work.

Our roadmap includes:

- Expanding dataset coverage to more Python frameworks and libraries.
- Completing the RL stage of the pipeline by generating good verifiable coding tasks.
- Growing our datasets to include realistic examples of agentic work, including reasoning, tool calling, etc.
- Establishing a regular release cadence tied to Python version releases.
- Growing the team and teaching others how to do this work.
- Coming up with and testing novel ideas about tuning models to be our best locally running assistants.

## Conclusion

This is just the beginning, we started only 2 months ago. The real deliverable isn't just two model
weights — it's proof that a community can move fast, work openly, and ship something useful on the same day
Python ships. We're building this for us, by us. If that resonates, [get involved](../../get-involved.md).
