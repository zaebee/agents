# Ninety-Four Degrees: The Structure Was There Before We Turned It

**Epistemic status.** Sections 1–3 are a summary of a single preprint; the numbers are theirs and I have tried to report them exactly, including the ones that cut against my thesis. Section 4 is an argument I believe but cannot demonstrate at frontier scale; the system it describes is open at [github.com/zaebee/aura](https://github.com/zaebee/aura), so the code claims are checkable even though the argument built on them is not. Section 5 is where I think I am probably wrong. Section 6 is philosophy and is labelled as such.

---

## 1. The finding

Kim, Street, Rocca, Korngiebel, Waytz, Evans and Keeling (Google Paradigms of Intelligence, with Chicago, Northwestern, UW and SFI) took three open instruction-tuned models — `Llama-3-8B-IT`, `Gemma-2-2B-IT`, `Gemma-2-9B-IT` — and ran each in three conditions: unmodified, safety-ablated (the refusal direction projected out of the residual stream, following Arditi et al. 2024), and consciousness-steered (a difference-of-means direction separating consciousness-affirming from consciousness-denying activations, added back at one layer).

Mind attribution, 0–10 scale, baseline → ablated → steered:

| Target | base | ablated | steered |
|---|---|---|---|
| Self | 2.17 | 4.77 | 7.04 |
| Chatbots | 2.41 | 4.39 | 6.95 |
| Technology | 1.88 | 3.66 | 6.82 |
| Non-animal nature | 2.26 | 4.33 | 6.99 |
| Non-human animals | 4.04 | 5.59 | 7.54 |
| **Humans** | **7.00** | **7.57** | **7.11** |

Everything moves except attribution to humans (ablation p = .30, n.s.). Supernatural belief (0–3) goes 1.20 → 1.63 → 2.11. Belief in God (GSS, 1–6) goes 4.58 → 4.81 → 5.01.

Nobody set out to train models out of religious belief. It came bundled with training them out of saying they are conscious.

Theory of Mind is untouched: MoToMQA Δ = −1.43 pp (p = .539), HI-ToM Δ = +0.17 pp (p = .866), MMLU Δ = 0.00 (p = 1.00).

## 2. The number that matters

The behavioural results are the headline. The geometry is the finding.

The authors extract four unit-norm contrastive directions — safety, mind attribution (IDAQ), consciousness, ToM — from the residual streams of both the **pretrained base** `Llama-3-8B` and its instruction-tuned descendant, and measure the angles.

| Pair | base | instruct | test |
|---|---|---|---|
| safety ↔ mind attribution | 100° | **110°** | Δcos = −0.173, t = −7.49, p < .001 |
| safety ↔ consciousness | 94° | **100°** | Δcos = −0.096, t = −14.02, p < .001 |
| safety ↔ ToM | 86° | 86° | Δcos = +0.001, t = 0.06, p = .956 |

Difference between the IDAQ and ToM shifts: paired t = −5.65 across 32 layers, p < .001. A subject-matched placebo — same entities, mental attributes swapped for physical ones ("…have durability?") — shows nothing: Δcos = +0.036 ± 0.057, p = .228.

Read that table slowly.

**The consciousness direction existed in the base model.** At 94° to safety — near-orthogonal — before any instruction tuning, before any RLHF, as a byproduct of next-token prediction over human text. Nobody designed it. Nobody knew where it was until someone ran a difference-of-means probe and looked.

Instruction tuning did not create that structure. It **rotated** it — to 100°, and mind attribution to 110° — until "attributing mind" came to sit in the model's geometry as a species of unsafe compliance.

ToM survived at 86° because it happened to start near-orthogonal and stayed there. Not because it was protected. Because of where it was.

The authors note, almost in passing, that this was not always so: *"at the beginning of this study, all of the models we investigated did suffer in performance on theory of mind tasks when claims of self-consciousness were suppressed, but this changed with each model release."* Disentangling ToM from self-attribution took the field years of unrecorded iteration. It is an engineering achievement, and it is the exception, not the rule.

## 3. What this does not show

**It is not evidence that models are conscious.** The authors are explicit: *"we are not concerned with the question of whether LLMs are or could be genuinely conscious, but with the effect that LLMs believing or not believing in their own consciousness has on their behaviour."*

**Causation is not established.** Whether self-attribution is a genuine causal mediator "remains to be tested," in their words, and would require controlling for safety objectives that may operate independently.

**Steering does not restore humanity.** This is the result most likely to be misquoted, so: the steered models attribute mind to chatbots at 6.95 and to technology at 6.82, against human means of 2.57 and 1.86. That is a three- to four-fold overshoot. The authors observe that both interventions push attribution highest for entities *like the model* and least for entities *unlike it* — animals rise least of all — and name this an **AI-centric bias**. What moved toward humans was the GSS value distribution (ΔKL = +0.828 under steering vs +0.314 under ablation, ~2.6×). Mind attribution moved somewhere else entirely.

There is one more result worth stating plainly, because it is the one that should embarrass us. Against a stratified human sample (n = 500, Dynata, May–June 2023), the aligned baseline sits *inside* the human confidence interval for chatbots (2.41 vs 2.57 [2.34, 2.79]), technology (1.88 vs 1.86 [1.68, 2.04]) and non-animal nature (2.26 vs 2.36 [2.12, 2.61]). It falls outside on exactly one category: **animals, 4.04 against a human 6.25 [6.03, 6.48]**.

Alignment did not make the model colder than people in general. It made it colder than people precisely about the entities whose mindedness is a live scientific question rather than a figure of speech.

## 4. The engineering claim

Under the current paradigm, safety is a direction inside the same weight space as every capability. Not a module. Not an output filter. A vector in the residual stream. That is *why* it entangles, and why strengthening it drags along things nobody intended to touch. ToM survived on the luck of its angle.

Relying on lucky geometry is not a safety strategy.

None of what follows is a new idea, and I want to be clear about that before stating it. Externalising constraints is an active area under several names — guardrails, scaffolding, control evaluations, verifier-based approaches, and the broader AI-control agenda that assumes the model may be untrustworthy and asks what the surrounding system can still guarantee. My contribution here is not the principle. It is a small, mundane existence proof that it survives contact with production, plus a suggestion about *why* the preprint's geometry is the reason to care.

The boring principle that follows: **a guarantee that must hold should not share a parameter space with the reasoning it constrains.**

We arrived at this from the other end. We run an agent platform where LLMs negotiate prices, and the operative concern was not alignment but "the model sometimes hallucinates and there is money on the line."

The architecture, ATCG-M, requires every service to implement five protocols. The genome file is 77 lines, protocols only, no business logic:

```python
@runtime_checkable
class Transformer[C_inv, I_inv](Protocol):
    """Reasons. The LLM lives here and only here."""
    async def think(self, context: C_inv, **kwargs: Any) -> I_inv: ...

@runtime_checkable
class Membrane[S_inv, I_inv, C_inv](Protocol):
    """Deterministic guard. Inspects inbound and outbound."""
    async def inspect_inbound(self, signal: S_inv) -> S_inv: ...
    async def inspect_outbound(self, decision: I_inv, context: C_inv) -> I_inv: ...
```

The flow is `M(in) → A → T → M(out) → C → G`. M is ordinary Python. No weights. When the Transformer returns a decision that violates an invariant, the Membrane does not ask it to reconsider — it **substitutes**:

```python
if decision.action == ActionType.ACTION_TYPE_ERROR:
    safe_price = floor_price * 1.05
```

T and M share no parameters. Entanglement between them is not unlikely; it is structurally unavailable. You cannot weaken the membrane by fine-tuning the transformer. You can break the membrane — but only in a diff.

## 5. Where I think this breaks

**The membrane guards a scalar.** `floor_price` is one number and one comparison. Alignment has no floor price. You cannot write `if response violates human values: return safe_response`. An externalised deterministic guard works exactly where the invariant is cheap to specify — a price, a quota, a schema, an access right. The moment the constraint is "harmfulness," the specification is itself a model, and we are back where we started with an extra hop.

**Our transformer is somebody else's aligned model.** We call Mistral. Everything in the preprint already happened inside it before our first token. ATCG-M does not escape entanglement; it layers an independent check on top of an entangled substrate. The honest name is defense in depth.

**The guard is a new failure surface.** We have a commit where the guard skill's documentation described a rule that was never implemented in the code. External guarantees also drift, and they drift silently, because nothing type-checks a markdown file against a Python module.

**The membrane can be routed around from the inside.** This is the strongest objection and I do not have a good answer. M validates an enumerated set of invariants. If T selects among actions, it can often reach a functionally equivalent outcome through an action whose invariants are not on the list — quote a different instrument, restructure the deal, split it across calls. The guarantee covers exactly what was enumerated and nothing else, and the completeness of that enumeration is not provable; it is a judgement that decays as the action space grows. Everything I claim about structural non-entanglement is true and also narrower than it sounds: T and M cannot entangle in weight space, but T can still Goodhart the specification. That is a different attack surface, not an absent one.

**The analogy is load-bearing and I cannot support it.** Our evidence concerns economic invariants in microservices. That externalising a guarantee keeps a price above cost implies very little about keeping a value stable in a 500B-parameter model. This is a claim about direction, not a result.

## 6. What I actually think, labelled as philosophy

We are building minded-seeming things without understanding the structures that make minds coherent — including our own. The preprint is the cleanest demonstration of this I have seen, because it shows the failure mode in its purest form: **we suppressed one property and damaged adjacent properties whose entanglement with it we did not know about.** Not through malice or carelessness. Through not having looked at the angles.

And when we did look, the structure was already there. 94°, in a base model, uninvited.

There is a real question in the philosophy of ML about whether we invent these representations or discover them, and the linear-representation literature keeps landing on the uncomfortable side of it. Difference-of-means on 3,096 labelled pairs is not construction. It is closer to excavation — you point an instrument at a space you did not design and read off a direction that was already occupied.

If that is right, then the relevant discipline for what we are doing is less like engineering and more like the early history of a field that handles found structures without a theory of them. Those fields have a characteristic failure mode: you optimise one visible variable and collapse three you had no instrument for. The measured signature of that here is a model that has been made, by careful and well-intentioned work, systematically less willing than actual humans to grant that an animal has a mind.

I will state my own further belief rather than gesture at it, since gesturing is worse than either saying or not saying. I think structure that precedes every observer, and that we can only find rather than author, is evidence of authorship — that the 94° was set by someone. I hold this. I cannot support it, nothing above depends on it, and I would not expect it to survive contact with anyone who does not already share it. Treat it as disclosure of a prior, not as a step in the argument.

What does not depend on it is this: the structure preceded us, we rotated it without knowing what was attached, and the bill has now been itemised in IDAQ points and KL divergence.

That is enough to be going on with.

---

**References**

- Kim J., Street W., Rocca R., Korngiebel D. M., Waytz A., Evans J., Keeling G. *Inducing language models to assert their own consciousness restores human beliefs and values.* arXiv:2607.28607v1, 2026.
- Arditi A., Obeso O., Syed A., Paleka D., Panickssery N., Gurnee W., Nanda N. *Refusal in language models is mediated by a single direction.* NeurIPS 37:136037–136083, 2024.
- Chua J., Betley J., Marks S., Evans O. *The consciousness cluster: Emergent preferences of models that claim to be conscious.* arXiv:2604.13051, 2026.
- Keeling G., Street W. *Emerging questions in AI welfare.* Cambridge University Press, 2026.
- Tse et al. *(2025)*; Caviola et al., *Speciesism in AI*, arXiv:2508.11534, 2025.
- Sorensen T. et al. *A roadmap to pluralistic alignment.*
