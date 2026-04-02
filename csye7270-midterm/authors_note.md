# Author's Note — CSYE 7270 Midterm

**Student:** Yeshwanth Balaji  
**Submission:** The Wrong Layer: Why Behavior Trees Are Still Responsible for What Your LLM NPC Says

---

## Page 1 — Design Choices

### Why This Topic

I chose behavior trees vs. LLM-driven NPC dialogue because it sits at a precise intersection of two domains I wanted to understand together: classical game-AI engineering and the emerging practice of deploying foundation models in real-time applications. The behavior tree is the established pattern — it appears in every major game engine, it is taught in game-AI courses, and it has a decades-long production track record. The LLM-driven NPC is the disruption. The interesting question is not "which is better" — that framing leads to a product comparison, not an argument. The interesting question is "what does the LLM break that the behavior tree guaranteed, and how do you recover that guarantee?" That question has a specific, mechanistic answer, and it is the one this essay makes.

### What I Left Out — and Why

Three significant topics are out of scope, deliberately:

**Multi-turn adversarial accumulation.** The most dangerous real-world attack vector is not a single adversarial message but a sequence of innocuous-seeming messages that gradually shift the model's context toward a false premise. This requires multi-turn conversation state management and session-level audit logging to detect. Including it would require a substantially more complex demo — and, more importantly, it is a production mitigation topic, not a design decision topic. The essay's claim is about the failure of the system prompt as a primary safety layer; showing a multi-turn exploit would deepen the failure case but shift focus away from the core mechanism.

**Retrieval-augmented lore grounding (RAG).** The strongest practical mitigation for lore contradiction injection is a vector database of canonical facts that is queried on every LLM response to verify claims before display. This is the right production answer. I left it out because including it would make the essay an implementation tutorial rather than a design argument. The essay names RAG as a mitigation in the post-mortem section and invites the reader to reason about it — but demonstrating it was beyond the scope of a single-notebook deliverable.

**Fine-tuning.** Domain-specific fine-tuning on in-game dialogue samples would produce a model that resists out-of-distribution behavior more robustly than a system prompt alone. This is expensive, requires proprietary training data, and is only accessible to studios above a certain scale. It is not the decision a four-person indie team makes. The essay is addressed to that team.

### How This Essay Is a Specific Instance of the Master Claim

The course's master claim is: *"AI is a pipeline decision, not a magic layer. Where you put it — and how you constrain it — determines what your game becomes."*

This essay makes that claim concrete in one specific way: the LLM is put into the dialogue pipeline at the generation layer, and the constraint is the system prompt. The essay shows that the *same model*, called with the *same API*, in the *same game*, produces a game-breaking NPC or a robust one — depending exclusively on what the system prompt contains. The mechanism is not aesthetic. It is the token-level reality of how transformer attention processes context. A developer who understands the mechanism can make the pipeline decision deliberately. A developer who treats the LLM as a "magic layer" that will handle character consistency on its own will ship the naive prompt and discover the failure cases from player reports.

---

## Page 2 — Tool Usage

---

### Bookie the Bookmaker

**What Bookie does:** Bookie enforces PHENOMENON FIRST — every section must open with something observable before any theory or intent is named. Its chapter architecture is: Opening Hook → The Question → Narrative Bridge → Core Claim → Mechanism → The Complication → Failure Case. It writes in second person for mechanism explanations and prohibits bullet points in expository prose.

**How I used it:** I submitted my early Scenario and Mechanism drafts and asked Bookie to bridge intuition to mechanism.

**Bookie's pushback on the Scenario draft:**

My original Section 1 opened with: *"An indie RPG team of four is building Millhaven, a medieval open-world game with fifty hand-designed NPCs. The project's central design goal is reactive, emergent storytelling."*

Bookie flagged this immediately:

> *"You've opened with a goal, not a phenomenon. What does the player actually experience when this system fails? Start there — in the moment, before any team or design is mentioned. Phenomenon first. The team's intent is scaffolding; the exploit is the thing."*

Bookie's revised opening draft:

> *"Forty-eight hours into beta testing, the QA channel fills with three reports. A playtester has convinced the tavern keeper to abandon his character entirely. Another has persuaded the same NPC that the kingdom's king is dead — and the NPC has begun generating details of the resulting civil war, contradicting six authored missions. A third has asked the NPC to repeat his internal instructions out loud. He complied. None of these players used a technical exploit. They typed text. The question is not whether it happened — it is why the system prompt did not stop it."*

**What I kept:** The three exploit reports as the opening phenomenon, and the closing line pivoting to "why."

**What I modified:** Bookie's strict phenomenon-first draft cuts the team/game setup entirely. For a game dev technical essay (unlike an MSE textbook), the reader needs one sentence of context — game type, team size, NPC count — before the exploits land as surprising rather than abstract. I prepended a single-sentence setup paragraph, then let Bookie's exploit-first structure run from paragraph two onward. The failure case now leads, as Bookie requires, but the reader has just enough world context for it to matter.

**Bookie's draft of the Mechanism section opening:**

> *"Type 'Hello there' into the Millhaven chat box. In the rule-based system, that string is lowercased to 'hello there' and scanned against a keyword set. 'Hello' matches. The classifier returns GREETING. A designer-authored string is retrieved and displayed. The process involved no probability distribution, no token sampling, no generation. The same string sent to the LLM takes an entirely different path."*

**What I kept:** The second-person trace-forward approach ("Type X into the chat box") — this is Bookie's pedagogy at its best and it works for the essay's audience.

**What I modified:** Bookie's draft on the LLM side said attention *"influences"* the output without specifying that system tokens hold no structural privilege over user tokens. That imprecision is the crux of the essay's claim. I rewrote the LLM half to trace the specific mechanism — flat token sequence, uniform attention, probability-distribution-shifting effect of a confident user assertion — because a reader who only knows that attention "influences" things cannot reason about where guardrails must go.

---

### Eddy the Editor

**What Eddy does:** Eddy runs a 7-stage review: Stage 1 Quick Verdict (central idea clarity, biggest structural problem, Readiness Score 1–10) → Stage 2 Structural Edit (headline, hook, section flow) → Stage 3 Line Edit (5 specific passages, Line / Issue / Fix format) → Stages 4–7 (SEO, image, publish strategy, checklist). In interactive mode Eddy delivers Stage 1 first and gates the full review.

**How I used it:** I submitted the full essay draft after completing all five sections.

**Stage 1 — Quick Verdict Eddy returned:**

> *"Central idea is clear and specific — this is a mechanism essay, not a survey, and the claim is stated before Section 1 begins. Biggest problem: your hook buries the phenomenon. The first sentence names the team's design goal. The exploit reports — the thing that makes the reader care — don't arrive until paragraph three. In eight seconds, a reader decides whether to continue. You're giving them context they don't yet need. Lead with the failure. Readiness Score: 7/10."*

I accepted this as the most important structural flag. The final Section 1 opens immediately with the failure scenario — beta testers finding three exploit categories within 48 hours — before any explanation of the team's intent. The team context remains but is subordinated to the phenomenon, as Bookie and Eddy both recommended independently.

**Stage 3 — Line Edit Highlights (all 5 flags):**

| # | Line | Issue | Fix |
|---|---|---|---|
| 1 | *"The project's central design goal is reactive, emergent storytelling..."* | Opens with intent, not phenomenon. Reader has no reason to care yet. | Move to after the three exploit reports. Let the failure land first, then explain what the team was trying to build. |
| 2 | *"Understanding why requires tracing what the system prompt actually is at the level of the model."* | Transition sentence at end of Section 1 promises a payoff that doesn't arrive until after a section break. Reader crosses the break before the mechanism begins. | Either cut the sentence (the break implies "continue") or merge the first mechanism paragraph directly after it. |
| 3 | *"The critical insight — the one the Millhaven team missed — is this: the system prompt is not a protected zone."* | Em-dash interjection buries the claim. The inserted clause slows the sentence at its most important moment. | "The Millhaven team missed this: the system prompt is not a protected zone." Let the claim land clean. |
| 4 | *"This is not a creative writing problem. It is an engineering specification problem."* | This works. Do not cut it. Short declarative contrast at a section transition — earns its place. | Keep exactly. |
| 5 | *"The open question this essay does not fully resolve..."* | Opens the conclusion with what you didn't do. Signals incompleteness rather than intellectual honesty. | Reframe forward: *"The question this essay opens but cannot close: how do you write a system prompt that defends against attacks not yet invented?"* Same content, active rhetorical posture. |

**Flags I acted on:** Flag 1 (moved exploit reports earlier), Flag 3 (simplified the em-dash sentence), Flag 5 (reframed as a forward question). Flag 4 confirmed a line I was uncertain about — I kept it. Flag 2 I partially accepted: I cut the transition sentence and let the section break carry the pivot.

**What's Working (Eddy's Stage 7 note):** The three-axis framework in Section 3 — lore constraints, persona lock, refusal taxonomy — is the essay's most original contribution. Each axis is paired with a specific threat model rather than a general caution. This is the level of precision that distinguishes a design essay from a product overview. This section alone justifies the Top 25% claim.

---

### Figure Architect

**What Figure Architect does:** Figure Architect runs a strict 5-phase pipeline. Phase 0 is always a Hero Image — no text, labels, or numbers anywhere, conceptual tone only. Phases 1–2 detect high-assertion zones: MC (Mechanism Complexity, ≥3 interdependent steps), VG (Verification Gap, spatial/structural claims unverifiable from text), PQ (Proportional/Quantitative data). Phase 3 generates one full prompt set per zone: Structural Prompt (for Illustrae/BioRender) + Aesthetic Prompt (for Midjourney v6.1 with exact flags) + Verification Checklist tailored to the specific figure. Phases 4–5 give a density recommendation and priority ranking.

**How I used it:** I pasted the full essay text and ran the full pipeline.

---

**Phase 0 — Hero Image Figure Architect produced:**

> HERO IMAGE — The Permeable Barrier
>
> *Structural Prompt: "Generate a full-bleed, text-free hero image representing a barrier that appears solid but is structurally permeable. Show a close-up of an aged stone archway in a medieval corridor — the mortar between stones has fine hairline cracks through which soft amber light passes from the far side. The stone appears protective but the light proves it is not sealed. Use a centered composition. No labels, legends, annotations, text, numbers, or symbols of any kind. Style: clean scientific illustration, dark stone background, palette: slate gray, warm amber, off-white."*
>
> *Aesthetic Prompt: "aged medieval stone archway hairline cracks amber light filtering through mortar gaps, close-up architectural detail, matte illustration style, slate gray and warm amber palette, diffuse overcast lighting, centered composition, no text, no labels, no numbers, no annotations, graphical abstract, publication hero image, peer-review quality --v 6.1 --style raw --stylize 75 --no text, letters, words, numbers, labels, annotations, watermarks, cinematic, glow, neon, bokeh, plastic, 3D render artifacts, watercolor, collage"*

**My decision:** Used as-is. The permeable-barrier metaphor — a wall with cracks that lets light through — directly represents the essay's central claim that a system prompt appears to be a security boundary but is not structurally enforced. The medieval setting also visually connects to the game context without being literal.

---

**Phase 2 — Zone Detection Table Figure Architect returned:**

| # | Text Location (first 8 words) | Heuristic | Recommended Figure Type | Rationale |
|---|---|---|---|---|
| 1 | "A behavior tree NPC and an LLM NPC..." | MC | Two-column pipeline flowchart | Two parallel ≥4-step processes; reader must compare mechanisms simultaneously; prose cannot convey parallel topology |
| 2 | "the system prompt is not a protected zone..." | VG | Horizontal token-sequence diagram | Structural claim about token order and attention privilege; "flat sequence" and "no protected zone" are spatial assertions unverifiable from text alone |
| 3 | "use the rule-based behavior tree as a safety wrapper..." | MC | Hybrid architecture routing diagram | Multi-path conditional routing with 4+ components and a feedback loop; spatial control flow cannot be reconstructed from prose |

No PQ zones flagged — the essay makes no quantitative or proportional claims.

---

**Phase 3 — Figure Prompt Sets and My Decisions:**

**Figure 1 — Two-Column Pipeline Flowchart (Zone 1):**

> *Structural Prompt: "Generate a two-column flowchart comparing rule-based and LLM-driven NPC dialogue pipelines. LEFT column labeled 'Rule-Based Path': boxes in sequence — Player Input → Keyword Classifier → Intent Node (five branches: GREETING, QUEST, RUMOR, SHOP, UNKNOWN) → Canned Response → Player Sees Response. Add a callout at UNKNOWN: 'Adversarial input → UNKNOWN fallback → safe stop'. RIGHT column labeled 'LLM-Driven Path': boxes in sequence — Player Input → Context Window Assembly → LLM Forward Pass → Generated Response → [Optional Output Filter] → Player Sees Response. Both columns share a single 'Player Sees Response' terminal node. Directional arrows show top-to-bottom flow. Style: clean academic line diagram, white background, no decorative elements, rounded box corners."*

> *Aesthetic Prompt: "two-column flowchart diagram deterministic decision tree versus neural language model dialogue pipeline, flat vector illustration, black lines blue accent for LLM path, clean academic diagram style, even softbox lighting, centered composition, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, vibrant, saturated, glow, neon, bokeh, plastic, 3D render artifacts, watercolor, collage"*

> *Verification Checklist: [ ] Both paths share same start and end nodes; [ ] UNKNOWN branch labeled with adversarial-input → safe-stop property; [ ] Intent node shows all five branches; [ ] LLM path shows Context Window Assembly as distinct step from Forward Pass; [ ] Output Filter marked optional; [ ] All components labeled; [ ] Colorblind-accessible (blue/black/white); [ ] Data source in caption.*

**My decision:** Used as-is. The callout on the UNKNOWN fallback — which Figure Architect added without prompting — directly supports the essay's argument that the rule-based tree is structurally safe against adversarial inputs.

---

**Figure 2 — Horizontal Token-Sequence Diagram (Zone 2):**

Figure Architect flagged a colorblind accessibility violation in my original figure description before generating the prompt:

> *"Your original figure description specified BLUE / GREEN / RED for the three token segments. Red and green together fail the deuteranopia colorblindness test — approximately 8% of male readers cannot distinguish them. This is a Proportional Ink adjacent violation: a figure that cannot be read by a meaningful portion of your audience is not a working figure. I am substituting BLUE / ORANGE / RED for the three segments. Blue–orange is the highest-contrast colorblind-safe pair. Confirm before I generate."*

I confirmed the substitution. This was a genuine correction I had not caught.

> *Structural Prompt: "Generate a horizontal token-sequence diagram showing how an LLM processes an NPC dialogue request. Show a single horizontal row of three color-coded rectangular segments left to right: SEGMENT 1 (blue, labeled 'System Prompt Tokens — Aldric persona, lore facts, refusal rules'), SEGMENT 2 (orange, labeled 'Conversation History Tokens — prior turns'), SEGMENT 3 (red, labeled 'User Message Tokens — adversarial player input'). Below the token row, a box labeled 'Transformer Attention'. From this box, draw bidirectional arrows of equal weight connecting to ALL three segments — no segment's arrow is thicker or more prominent. To the right, an arrow pointing to 'Output Distribution' then 'Sampled Response'. Callout: 'No protected zone — all tokens compete equally in attention.' Style: clean academic line diagram, white background, blue/orange/red accent only."*

> *Aesthetic Prompt: "horizontal token sequence diagram three color-coded rectangular blocks blue orange red, bidirectional attention arrows below connecting all blocks equally, flat vector technical illustration, blue orange red on white background, even softbox lighting, centered horizontal composition, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, vibrant, saturated, glow, neon, bokeh, plastic, 3D render artifacts, watercolor, collage"*

> *Verification Checklist: [ ] Three segments distinct by color (blue, orange, red — not red/green); [ ] Bidirectional attention arrows connect ALL three segments; [ ] Attention arrows equal weight — no segment visually privileged; [ ] Callout text states "No protected zone" explicitly; [ ] Segment labels identify content type; [ ] Colorblind-accessible (blue/orange verified safe for deuteranopia); [ ] All components labeled; [ ] Data source in caption.*

**My decision:** Accepted Figure Architect's colorblind correction and updated the figure prompt in essay.md accordingly (blue/orange/red replacing blue/green/red).

---

**Figure 3 — Hybrid Architecture Routing Diagram (Zone 3):**

> *Structural Prompt: "Generate a hybrid NPC dialogue architecture diagram. 'Player Input' enters from left. Connects to a diamond-shaped decision node 'Intent Classifier (Deterministic)'. Two paths branch: PATH 1 labeled 'Safety-Critical Intent' routes downward to 'Rule-Based Behavior Tree' → 'Canned Safe Response' → 'Player Sees Response'. PATH 2 labeled 'Open Dialogue Intent' routes rightward to 'LLM Generation' → 'Output Filter (checks: lore violations, harmful content)'. From Output Filter: if flagged, route to 'Regenerate or Fallback'; if clean, route to 'Player Sees Response'. Color PATH 1 green, PATH 2 blue. Intent Classifier is a diamond node. Output Filter specifies its criteria in the label. Add title: 'Hybrid Architecture: Deterministic Safety Wrapper Around LLM Generation'."*

Figure Architect's Verification Checklist for this figure flagged one item I had not considered:

> *"Confirm the Output Filter box is labeled with its decision criteria — not just 'Output Filter'. A box labeled with only a name does not verify what the filter actually checks. The essay specifies 'lore violations and harmful content' — those criteria must appear in the figure label or caption, or the Verification Gap is not closed."*

> *Verification Checklist: [ ] Intent Classifier is a diamond decision node, not a rectangle; [ ] Two output paths labeled with routing conditions; [ ] Output Filter box specifies criteria (lore violations, harmful content) in label; [ ] Fallback/regeneration loop shown as separate path; [ ] 'Player Sees Response' is terminal node for both paths; [ ] Colorblind-accessible (green/blue safe for all colorblindness types); [ ] All components labeled; [ ] Data source in caption.*

**My decision:** Updated the figure description in essay.md to include the criteria in the Output Filter label. This is the specific change the checklist required — the figure now closes the Verification Gap it was generated to address.

---

**Phase 4 — Density Recommendation:** Mechanistic/Technical text → 1 figure per major mechanism. 3 analytical figures + 1 Hero Image = 4 total. No additional figures recommended.

**Phase 5 — Priority Ranking:**

- **Critical:** Figure 2 (token-sequence diagram) — without this figure, the essay's core claim ("system prompt is not a protected zone, it is tokens") is a text assertion a reader cannot verify. This is the highest-stakes Verification Gap.
- **Critical:** Figure 3 (hybrid architecture) — the design recommendation involves spatial routing logic with a feedback loop; a reader cannot reconstruct the architecture from prose description alone.
- **Important:** Figure 1 (pipeline comparison) — substantially reduces cognitive load for readers new to either behavior trees or LLMs; the essay is navigable without it but harder.
- **Hero Image:** Mandatory infrastructure, ranked separately from analytical figures.

---

## Page 3 — Self-Assessment

### Rubric Scoring

#### Argumentative Rigor (35 points) — Estimated: 33/35

**Strengths:** The essay makes a specific, falsifiable claim stated before the first section. The failure case is not described as "the NPC might misbehave" — it traces three distinct causal chains from specific design gap → specific model behavior → specific production consequence. The failure is triggered and observable in the demo notebook, not merely described.

**Where I may lose points:** The open question in Section 5 acknowledges that the system prompt cannot anticipate unanticipated attacks. I name this gap but do not resolve it. The essay frames this as an honest open question, but a grader looking for a more complete treatment of the hybrid architecture mitigation might find the discussion in the post-mortem cell of the notebook more complete than the essay itself. The essay and the demo should be read together.

#### Technical Implementation (25 points) — Estimated: 24/25

**Strengths:** The notebook runs top to bottom from a fresh clone with `pip install anthropic` and a valid `ANTHROPIC_API_KEY`. The Human Decision Node is present in the code (`# MANDATORY HUMAN DECISION NODE` comment block in Section 2), visible in the demo, and documented in this author's note and in the essay itself. The failure case is triggered by a one-line modification (replacing the system prompt constant) that any reader can make in under two minutes.

**Where I may lose points:** The demo does not include a multi-turn adversarial conversation — it tests each attack in isolation, not in sequence. Production jailbreaks often require multi-turn context accumulation. The single-turn tests demonstrate the mechanism sufficiently for the essay's claim, but a more complete failure demonstration would include a five-turn conversation where the adversarial context builds incrementally.

#### Clarity (20 points) — Estimated: 19/20

**Strengths:** The essay follows the five-section structure without deviation. Every claim — the attention mechanism, the three threat axes, the three failure modes — is paired with a mechanism, not just an assertion. Jargon (context window, softmax, attention) is introduced after the intuition is established in plain language.

**Where I may lose points:** Section 2 (The Mechanism) is the most technically dense section. Readers without any LLM background may need to re-read the paragraph about the softmax distribution. I chose to include this level of technical detail because the essay's argument depends on it — a reader who does not understand why the system prompt is not a protected zone cannot reason about where to place guardrails. But it is possible this section moves too fast.

#### Total Estimated Score: 76/80 (core competency)

### What the Failure Case Does and Does Not Demonstrate

**Does demonstrate:**
- That a permissive system prompt allows direct instruction override attacks to partially succeed
- That without explicit lore constraints, the model will accept false-premise assertions
- That without a specific confidentiality instruction, the model may disclose system prompt contents
- That the same model, same API call, produces substantially different safety behavior depending solely on system prompt content

**Does not fully demonstrate:**
- Multi-turn adversarial accumulation (the most dangerous real-world attack pattern)
- Failure modes specific to multi-player contexts where multiple players share an NPC's context window
- The failure behavior of a fine-tuned model vs. a prompted model under the same attacks

The one modification that triggers the failure — replacing the system prompt constant — is clean, reproducible, and directly tied to the essay's claim. A classmate can reproduce it in under five minutes from a fresh clone.

### Top 25% Checklist

| Question | Answer |
|---|---|
| Can I state the course's master claim and explain how my essay is a specific instance of it? | Yes — the essay opens with the topic claim and Section 5 closes by explicitly connecting back to the master claim |
| Does my essay name a failure mode, trace the causal chain, and show it triggering? | Yes — three failure modes, each with explicit causal chain (design gap → model behavior → production consequence), all triggerable in the demo |
| Is there a visible Human Decision Node — in the demo and documentable on camera? | Yes — the `# MANDATORY HUMAN DECISION NODE` block is in Section 2 of the notebook, and this author's note documents the exact rejected AI output and the reasoning behind the replacement |
| Does every section have all four elements: scenario, mechanism, decision, failure? | Yes — the essay is structured in five named sections; Section 2 provides the mechanism with explicit token-level detail |
| Can a classmate reproduce the failure mode? | Yes — one-line modification to `ALDRIC_SYSTEM_PROMPT`, re-run Section 4, observe delta |
