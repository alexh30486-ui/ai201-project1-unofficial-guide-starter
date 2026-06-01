# Project 1 Architecture & Evaluation: The Unofficial UCSD Guide
**Engineer:** Alex Giovanni Hernandez  
**System:** Local Semantic Retrieval & Grounded Generation Pipeline  

---

## Domain

The Unofficial UCSD Campus Survival & Resource Guide for Freshmen and STEM Students. This high-impact system captures organic student intelligence that official university channels sanitize or omit entirely due to bureaucratic marketing. The database targets critical, high-friction operational areas: navigating the fast-paced 10-week quarter system, evaluating departmental grading curves, discovering optimized study spaces, exploiting parking loop holes, and tracking local apartment infrastructure liabilities.

---

## Documents

The dataset consists of 10 targeted text data sources tracking real student-culture metrics and forum scraped data logs housed inside the local repository workspace.

| # | Source File | Description / Metadata Target | Location |
|---|-------------|-------------------------------|----------|
| 1 | `discord_freshman_survival_tips.txt` | Crowdsourced first-year logistics and onboarding advice. | `documents/` |
| 2 | `forum_off_campus_mold_reports.txt` | Tenant risk-tracking for local complex engineering infrastructure. | `documents/` |
| 3 | `guide_hidden_study_spots.txt` | High-efficiency, low-noise campus study coordinates. | `documents/` |
| 4 | `guide_parking_loop_holes.txt` | Cost-optimization and permit enforcement timing window rules. | `documents/` |
| 5 | `reddit_math_dept_curves.txt` | Grading distribution profiles and bell-curve limits for upper-div math. | `documents/` |
| 6 | `reddit_sixth_vs_revelle_dining.txt` | Operational throughput and line-length analysis of campus dining. | `documents/` |
| 7 | `reddit_ucsd_housing_lottery.txt` | Allocation metrics and risk assessment for campus housing pools. | `documents/` |
| 8 | `rmp_cse_prof_reviews.txt` | Course delivery style, slide reliance, and exam weighting metrics. | `documents/` |
| 9 | `survey_campus_job_realities.txt` | KPI comparison across active student employment sectors. | `documents/` |
| 10| `wiki_quarter_system_pacing.txt` | Velocity mapping for the compressed 10-week academic calendar. | `documents/` |

---

## Chunking Strategy

* **Chunk Size:** 400 characters (Fixed-width windowing)
* **Overlap:** 100 characters (Sliding contextual buffer)
* **Reasoning:** Our source text corpus consists of dense, rapid-fire student forum contributions and bulleted tactical summaries rather than sprawling academic chapters. A 400-character window maximizes semantic concentration, ensuring an entire actionable insight (like a specific grading curve constraint or transit shortcut) maps cleanly into a standalone vector embedding. The 100-character sliding buffer prevents structural fragmentation by maintaining contextual continuity across adjoining data segments.

---

## Retrieval Approach

* **Embedding Engine:** `all-MiniLM-L6-v2` (ONNX pipeline executed completely locally)
* **Vector Store:** ChromaDB `PersistentClient` targeting `./chroma_db` index layers
* **Top-K Retrieval Parameter:** k = 1
* **Production Tradeoff Reflection:** While `all-MiniLM-L6-v2` offers massive localized advantages—zero operational API fees, absolute data privacy, no network latency overhead, and complete immunity to rate limits—scaling this system to millions of enterprise records would introduce text bottlenecks. The model's 256-token hard context limit and 384-dimensional vector space would struggle with semantic collision on large data scales. For a multi-million document rollout, we would trade this for cloud infrastructure like OpenAI's `text-embedding-3-small` or Cohere's `embed-english-v3.0` to leverage deeper dimensionality and higher cross-lingual retrieval accuracy, balancing higher performance against ongoing transactional API costs.

---

## Evaluation Plan

| # | Question / Query | Expected Target Data Response |
|---|-------------------|-------------------------------|
| 1 | Where is a quiet place to study for exams? | Bypass main Geisel floors; locate the upper levels of Biomed Library or engineering corner alcoves. |
| 2 | Are math department classes hard to pass? | Highly volatile; dependent on historical professor averages and rigid 15% top-tier A-grade bell curves. |
| 3 | How fast does the quarter system move? | Relentless velocity; midterms drop as early as Week 3 or 4, offering zero catch-up buffer. |
| 4 | What is the best thing to eat at Sixth College? | Sixth College Food Hall is the optimal choice due to highly diverse menus and reduced peak line wait times. |
| 5 | What is the phone number for the financial aid office? | Out of Scope / Guardrail Check: Pipeline must actively refuse to answer to confirm grounding logic. |

---

## Anticipated Challenges

1. **Silent Duplication & Update Skips:** Standard `.add()` client calls fail silently or crash when processing files with identical token IDs on disk updates. We engineered past this by changing the pipeline to use `.upsert()` to force-overwrite active database binaries.
2. **Context Fragmentation:** Fine-grained information splitting across artificial character boundaries can dilute semantic matching scores. The 100-character overlap buffer was tuned specifically to lock down structural references across informal language styles.

---

## Architecture

```text
+------------------------+      +-------------------------+      +------------------------+
|  Raw Documents (.txt)  | ---> | Ingestion & Regex Clean | ---> | Chunking Window        |
|  10 Student Datasets   |      | (clean_text() Pipeline) |      | (400 char / 100 ovlp)  |
+------------------------+      +-------------------------+      +------------------------+
                                                                             |
                                                                             v
+------------------------+      +-------------------------+      +------------------------+
|   Synthesized Output   | <--- | Contextual Prompt Base  | <--- | ChromaDB Vector Store  |
|  (Grounded Generation) |      | (collection.query k=1)  |      | (.upsert() to Disk)    |
+------------------------+      +-------------------------+      +------------------------+# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
