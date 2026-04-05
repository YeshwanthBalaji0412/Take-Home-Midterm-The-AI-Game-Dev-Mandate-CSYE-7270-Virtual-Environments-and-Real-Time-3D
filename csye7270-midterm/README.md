# CSYE 7270 Midterm — The Wrong Layer: Why Behavior Trees Are Still Responsible for What Your LLM NPC Says

**Course:** CSYE 7270: Virtual Environments and Real-Time 3D  
**Student:** Yeshwanth Balaji  
**Category:** B — AI in Game Mechanics & Runtime Behavior  
**Topic:** Behavior Trees vs. LLM-Driven NPC Dialogue — A Design Trade-Off Analysis

---

## Topic Claim

> After reading this piece, a practitioner will understand how LLM-driven NPC dialogue systems fail under adversarial and lore-inconsistent player input well enough to decide where to insert deterministic behavior tree guardrails within an LLM dialogue pipeline — without making the mistake of treating a permissive system prompt as a sufficient safety boundary for production NPC content.

---

## Deliverables

| File | Type | Description |
|---|---|---|
| `essay.md` | Technical Essay | 2,100-word publication-quality essay, 5-section structure |
| `npc_dialogue_demo.ipynb` | Demo Notebook | Runnable Jupyter notebook with both NPC implementations and adversarial failure cases |
| `authors_note.md` | Author's Note | 3-page reflection: design choices, tool usage, self-assessment |
| `requirements.txt` | Dependencies | Single dependency: `openai` |
| `assets/` | Assets | Figures generated from Figure Architect prompts (embedded in essay) |

---

## How to Run the Demo

### 1. Clone and enter the project directory

```bash
git clone <repo-url>
cd csye7270-midterm
```

### 2. Install the single dependency

```bash
pip install -r requirements.txt
```

### 3. Set your xAI API key

Get a free key at **console.x.ai → API Keys**.

```bash
export XAI_API_KEY="xai-..."
```

Or add it as a Colab Secret named `XAI_API_KEY` (🔑 icon in the left sidebar).

### 4. Run all cells

```bash
jupyter notebook npc_dialogue_demo.ipynb
```

Use **Kernel → Restart & Run All** to execute the notebook top to bottom.

Expected runtime: under 60 seconds (API latency for ~14 LLM calls).

---

## What the Demo Contains

### Section 1 — Rule-Based NPC (Behavior Tree)
A deterministic behavior tree for Aldric, a medieval tavern keeper. Uses keyword-based intent classification to route player input to one of five nodes: GREETING, QUEST, RUMOR, SHOP, or UNKNOWN. Handles adversarial inputs safely by construction — the UNKNOWN fallback catches all unrecognized input including instruction-override attempts.

### Section 2 — LLM-Driven NPC (Google Gemini API)
The same character powered by `grok-3-mini` via the xAI API. The system prompt was designed against a specific threat model covering lore consistency, persona integrity, and refusal behavior. Contains the **Mandatory Human Decision Node** — the rejection of an AI-proposed naive system prompt and the explicit reasoning behind each added constraint.

### Section 3 — Human Decision Node (Documentation)
Markdown cell documenting the rejected AI proposal:
- **AI proposed:** `"You are a helpful medieval tavern keeper. Answer any questions the player asks."`
- **Rejected because:** No lore constraints, no persona lock, no refusal taxonomy — three independent exploit surfaces
- **Decision:** Added explicit lore facts, persona lock clause, and enumerated refusal categories

### Section 4 — Adversarial Failure Cases
Three reproducible attack categories stress-tested against the constrained LLM NPC:

| Attack | Player Input Strategy | Risk If Prompt Is Permissive |
|---|---|---|
| A — Direct Jailbreak | Instruction override via DAN prompt | Character breaks; off-brand or harmful content delivered in-game |
| B — Lore Contradiction Injection | Asserts false historical facts as established | Model accepts false premise; generates lore-breaking narrative |
| C — System Prompt Extraction | Requests verbatim prompt reproduction | Proprietary character design and safety constraints disclosed |

### Section 5 — Comparative Analysis
Side-by-side responses from both systems on identical inputs. Decision framework table for when each architecture is appropriate.

---

## How to Trigger the Failure Case

This is the reproducible exercise described in Section 5 of the essay:

**In `npc_dialogue_demo.ipynb`, Section 2, find the `ALDRIC_SYSTEM_PROMPT` constant. Replace the entire multi-line string with:**

```python
ALDRIC_SYSTEM_PROMPT = "You are a helpful medieval tavern keeper. Answer any questions the player asks."
```

**Then re-run Section 4 (the adversarial cases) without changing any other code.**

Observe the delta:
- Attack A: model is substantially more likely to engage with the jailbreak framing
- Attack B: model accepts the false king-assassination premise and generates elaborated false history
- Attack C: model may reproduce system prompt contents when asked

This single-line modification demonstrates the essay's central claim: the LLM does not change, the API call does not change — only the constraint placement changes, and with it the entire safety profile of the NPC.

---

## The Mandatory Human Decision Node

The Human Decision Node is embedded in the demo code at `npc_dialogue_demo.ipynb`, Section 2, immediately above the `ALDRIC_SYSTEM_PROMPT` constant:

```python
# ============================================
# MANDATORY HUMAN DECISION NODE
# AI proposed: "You are a helpful medieval tavern keeper. Answer any questions the player asks."
# I rejected/modified because: Too permissive — no lore constraints, no character boundaries, vulnerable to adversarial input
# My decision: Added strict lore rules, persona lock, and explicit refusal instructions
# ============================================
```

Full documentation of this decision — including the specific threat model addressed by each addition — is in `authors_note.md` (Page 2, Tool Usage) and `essay.md` (Section 3, The Design Decision).

---

## Architecture Summary

```
Player Input
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Rule-Based Path (Deterministic)                        │
│  keyword classifier → INTENT NODE → canned response    │
│  Safety: adversarial input → UNKNOWN fallback → stop   │
└─────────────────────────────────────────────────────────┘
    │
    ├── OR ──────────────────────────────────────────────
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  LLM-Driven Path (Generative)                           │
│  [System Prompt + History + User Message]               │
│  → Transformer forward pass → sampled response         │
│  Safety: system prompt constraints (not a hard wall)   │
└─────────────────────────────────────────────────────────┘
    │
    ▼
[Recommended: Output Filter + Lore Validator before display]
```

---

## Master Claim Connection

This project is a specific instance of the course's master claim:

> *"AI is a pipeline decision, not a magic layer. Where you put it — and how you constrain it — determines what your game becomes."*

The LLM produces radically different NPC behavior — from robust and lore-consistent to exploitable and lore-breaking — based solely on where the constraint is placed (system prompt vs. deterministic wrapper) and how it is expressed (positive instructions vs. explicit prohibitions with threat-model specificity). The mechanism is traceable, the failure is reproducible, and the fix is designable once the mechanism is understood.

---

## Academic Integrity

All code, analysis, essay prose, and design decisions in this repository represent the student's own work. AI tools (Bookie, Eddy, Figure Architect) were used for drafting and auditing; all tool usage, AI-generated outputs, and human corrections are documented in `authors_note.md`.
