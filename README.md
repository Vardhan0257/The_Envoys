# The_Envoys

**A verification-first Retrieval-Augmented Generation (RAG) MVP focused on reducing hallucinated claims.**

---

## Overview

**The_Envoys** is a minimal, systems-focused RAG project built to answer one concrete question:

> *Can post-generation claim verification measurably reduce unsupported or hallucinated outputs in LLM-based RAG systems?*

Instead of building a feature-heavy research assistant, this project isolates a **single architectural improvement** — claim-level verification — and evaluates its impact against a naive RAG baseline.

The goal is **measurable improvement**, not UI completeness or agent complexity.

---

## Core Idea

Most RAG systems:

* retrieve text
* generate an answer
* assume correctness

**The_Envoys** treats generation as a *hypothesis*, not a fact.

It enforces:

1. **Structured claim generation**
2. **Explicit claim → evidence mapping**
3. **Independent verification using an NLI model**
4. **Metric-driven comparison against a naive baseline**

---

## Architecture (MVP)

```
PDF → Chunk → Embed → Vector DB
                ↓
            Retrieval (top-k)
                ↓
        ┌───────────────┐
        │ Naive RAG     │
        │ (control)     │
        └───────────────┘

                ↓

        ┌────────────────────────┐
        │ Verified RAG            │
        │ • Structured claims    │
        │ • Claim → chunk IDs    │
        │ • NLI verification     │
        └────────────────────────┘

                ↓
           Metrics & Logs
```

---

## What This Project Is (and Is Not)

### In Scope

* PDF ingestion and chunking
* Vector-based retrieval
* Naive RAG baseline
* Structured claim generation
* Claim-level NLI verification
* Quantitative evaluation (unsupported claim rate, latency, cost)

### Out of Scope

* Multi-agent orchestration
* Knowledge graphs
* Workspace management
* Collaboration features
* UI dashboards
* Fine-tuned models
* Enterprise auth / RBAC

This is intentional.
**Depth > breadth.**

---

## Technology Stack

### Models

* **Generation:** `gpt-4o-mini` (OpenAI API)
* **Embeddings:** `BAAI/bge-small-en-v1.5`
* **Verification:** `microsoft/deberta-v3-base-mnli`

### Backend

* Python
* FastAPI
* PostgreSQL + pgvector
* CPU-only execution

### Libraries

* `sentence-transformers`
* `transformers`
* `PyMuPDF`
* `pandas`
* `numpy`
* `tiktoken`

---

## Repository Structure

```
The_Envoys/
├── app/
│   ├── main.py        # FastAPI entrypoint
│   ├── ingest.py      # PDF ingestion & chunking
│   ├── retrieval.py   # Vector search
│   ├── generate.py    # LLM generation logic
│   ├── verify.py      # NLI verification
│   ├── metrics.py     # Metric computation
│   └── models.py      # DB schema
├── evaluate.py        # Evaluation runner
├── data/              # (ignored) PDFs / eval inputs
├── logs/              # (ignored) metrics & traces
├── requirements.txt
└── README.md
```

---

## Evaluation Methodology

The MVP compares two systems:

| System           | Description                             |
| ---------------- | --------------------------------------- |
| **Naive RAG**    | Vector retrieval + free-form generation |
| **Verified RAG** | Structured claims + NLI verification    |

### Metrics Tracked

* Unsupported claim rate
* Contradicted claim rate
* Retrieval recall@k
* Latency
* Token usage & estimated cost

Evaluation is run over:

* **10 academic PDFs**
* **60 adversarial questions**

  * definitional
  * numeric/table-based
  * contradiction-seeking
  * limited multi-hop

---

## Expected Outcome (Example)

| System       | Unsupported Claim Rate | Avg Latency |
| ------------ | ---------------------- | ----------- |
| Naive RAG    | ~30%                   | ~1.2s       |
| Verified RAG | ~5–10%                 | ~1.9s       |

Numbers will vary — **the delta is what matters**.

---

## Why This Matters

LLMs are probabilistic.
Blind trust is a system design flaw.

**The_Envoys** demonstrates how:

* verification can be separated from generation
* hallucinations can be measured instead of guessed
* AI systems can be engineered, not just prompted

---

## Collaboration Rules

* One feature per branch
* No commits to `main`
* No data or PDFs in repo
* Log failures, don’t hide them
* Metrics > opinions

---

## Status

 **MVP in active development**

Focus:

* correctness
* evaluation
* reproducibility

Not:

* polish
* hype
* feature count

---

### One-line summary

> **The_Envoys** is the smallest RAG system that proves, with data, that claim-level verification reduces hallucinated outputs.
