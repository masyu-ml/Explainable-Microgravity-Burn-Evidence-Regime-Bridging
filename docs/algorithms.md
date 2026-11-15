# Mathematical and Algorithmic Methodology

The mathematical statements below describe EMBER's scientific design and prior archived model families. They are **not universal laws of flame equivalence**, nor proofs that the newest live code has been independently verified.

## 1. Mixed-type retrieval (weighted Gower, kNN-style selection)

A scenario is represented by available attributes:

**x = [M, G, O₂, P, U, r, L]**

M = material; G = geometry; O₂ = oxygen concentration; P = pressure; U = airflow; r = specimen radius (where applicable); L = pyrolysis or specimen length.

The weighted similarity is:

**S(i,j) = [Σₖ₌₁ᵖ wₖ · δᵢⱼₖ · sᵢⱼₖ] / [Σₖ₌₁ᵖ wₖ · δᵢⱼₖ]**

- wₖ: selected weight for attribute k
- δᵢⱼₖ: indicator that k can be compared
- sᵢⱼₖ: attribute-level similarity
- p: number of attributes

For a numerical variable:

**sᵢⱼₖ = max(0, 1 − |xᵢₖ − xⱼₖ| / Rₖ)**

For a categorical variable: **sᵢⱼₖ = 1** if the values match and **0** otherwise.

Values not present in both records are excluded from the numerator and denominator. If no features are comparable, the algorithm must report **insufficient comparability** rather than claiming strong scientific similarity; a numerical zero may be used internally with that limitation reported. Material and geometry can be used as hard eligibility gates before ranking.

### Retrieval pseudocode

```text
Input: scenario X, NASA evidence catalog D, family F, neighbor count k
1. Validate scenario units and required inputs.
2. Filter D to source records eligible for family F.
3. Enforce material and geometry restrictions where specified.
4. For each eligible record:
   a. Select comparable attributes.
   b. Compute categorical/numerical similarities.
   c. Compute weighted Gower score.
   d. Preserve missing-source flags and per-feature contributions.
5. Sort by score; select top k eligible records.
6. Return ranked records with original NASA source IDs and condition labels.
```

**Important:** This is nearest-neighbor-style *retrieval*, not a separately trained kNN classification model. Gower similarity is **not** probability or proof of equivalence. Exact production weights and normalization ranges depend on the original source configuration.

## 2. Bayesian logistic ignition reference

A limited BASS-II PMMA-rod protocol subset has **19 audited observations**, comprising **16 positive** and **3 negative** records.

**P(y = 1 | O₂, β) = 1 / [1 + exp(−(β₀ + β₁ · O₂))]**

**p(β | D) = p(D | β) · p(β) / p(D)**

**P(y* = 1 | O₂*, D) = ∫ P(y* = 1 | O₂*, β) · p(β | D) dβ**

The documented oxygen-associated slope has a nonnegative-support prior. These expressions describe a protocol-specific probabilistic analysis, not a general ignition model for Earth, the Moon or Mars.

### Reported leave-one-out evaluation

| Metric | Reported value | Meaning |
| --- | ---: | --- |
| ROC AUC | 0.9792 | Ranking discrimination in leave-one-out evaluation |
| Brier score | 0.0696 | Mean squared probability error |
| Log loss | 0.2429 | Probabilistic error with greater penalty on confident mistakes |

**BS = (1/N) · Σᵢ₌₁ᴺ (pᵢ − yᵢ)²**

**LL = −(1/N) · Σᵢ₌₁ᴺ [yᵢ · ln(pᵢ) + (1 − yᵢ) · ln(1 − pᵢ)]**

These metrics come from a small, imbalanced sample. They are not independently validated cross-gravity physics scores. Do not invent an F1-score without a verified threshold, predictions and confusion matrix.

## 3. Material-specific physics bridging

The archived model registry includes six adapters: thick PMMA concurrent flow, PMMA rod, SIBAL concurrent thin fabric, Kimwipes thin sheet, LDPE insulated wire and thin PMMA Narrow Channel Apparatus analogy. Each adapter has its own applicability conditions.

### Thick PMMA mixed convection

**Fr = U_f² / (g · Lₚ)**

**Uₘ = U_f · (P/P₀) · [1 + (g · Lₚ/U_f²)²]^(¼)**

This formula requires source-specific units, pressure reference and nonzero airflow for the displayed algebraic form. Matching Uₘ does not prove equivalent ignition or flame spread.

### PMMA rod stretch

**a_raw = 3U / (2r)**

**B = A_tube / (A_tube − A_rod)**

**a_forced = a_raw · B · √(r/r₀)**

**a_buoyant = K · √(g/r)**

**a_total = a_forced + a_buoyant**

The coefficient K and reference radius r₀ follow source-specific assumptions. a_total is a **calculated stretch rate (s⁻¹)**, not directly an ignition probability, NASA observation or flame-spread rate.

## 4. Inverse regime comparison

**x* = argmin₍ₓ∈Ω₎ [D(Φ(x), Φ(xₜ)) + λ · C(x)]**

x*: proposed comparison scenario; xₜ: target scenario; Ω: eligible domain; Φ: physical fingerprint; D: mismatch measure; C: constraint penalty; λ: weighting parameter.

A numerically close fingerprint does not establish identical transport, chemistry, material pyrolysis or full flame behavior across gravity regimes.

## 5. Scientific abstention

```text
Input: scenario X, model registry M, evidence catalog D
1. Validate variables and units.
2. Select material/geometry model.
3. Check oxygen, pressure, airflow, gravity, specimen, and domain restrictions.
4. If model is unsupported: return OUT_OF_DOMAIN_ABSTENTION.
5. Compute supported physical fingerprint.
6. Search for valid constrained comparison scenarios.
7. If no justified match: return NO_VALIDATED_BRIDGE.
8. Otherwise return source-scoped quantities, units, residuals and limitations.
```

**OUT_OF_DOMAIN_ABSTENTION:** no support for computing the selected physical model at the requested input.

**NO_VALIDATED_BRIDGE:** a fingerprint may be computable but a scientifically justified cross-regime comparison is not established.

Neither status proves that a NASA experiment for the scenario does not exist.
