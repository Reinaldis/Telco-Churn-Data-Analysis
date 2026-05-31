# Decisions Log

> A record of methodological and analytical decisions made during this project. Each entry follows the format **Context → Decision → Consequence → Alternatives Considered**. The purpose is to make the reasoning behind the analysis auditable — not to defend every choice, but to make trade-offs visible.

---

## Format

Each decision is tagged with a status:
- 🟢 **Active** — decision currently in force
- 🟡 **Superseded** — replaced by a later decision (linked)
- 🔴 **Reversed** — tried and rolled back, with reasoning

---

## D-001 — Frame the analysis as descriptive-and-diagnostic, not predictive

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Project Identity & Executive Summary

### Context
The IBM Telco Customer Churn dataset is commonly used for predictive modeling tutorials (logistic regression, XGBoost, neural nets). The dataset also contains a built-in `churn_score` column, which makes a predictive task even more tempting.

### Decision
Frame this project explicitly as **descriptive-and-diagnostic**, not predictive. The objective is to explain *why* churn happens and *which segments* matter, not to score individual customers for likelihood of churn.

### Consequence
- The notebook does not build a logistic regression, gradient boosting, or any ML classifier.
- The custom risk score in Section 6 is an additive heuristic, evaluated by discriminative correlation (point-biserial r), not by AUC-ROC or precision/recall.
- A separate, follow-up project would be needed for a true predictive model.

### Alternatives Considered
- **Build a full predictive pipeline** — rejected because it duplicates one of the most saturated tutorial topics online and would not differentiate the analytical thinking from the technique.
- **Hybrid (descriptive + small predictive model)** — rejected to keep the narrative tight; mixing descriptive and predictive framings in one notebook tends to muddle the conclusions.

---

## D-002 — Apply McKinsey 6-Step as the macro structure

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 1 (Problem Framing)

### Context
Most data analysis notebooks open directly with `pd.read_csv` and EDA. This is efficient for technical readers but invisible to business reviewers who want to know *what question is being answered* before seeing any chart.

### Decision
Open with a full Problem Framing section that applies the McKinsey 6-Step process: Define → Disaggregate (MECE logic tree) → Prioritize (hypotheses) → Workplan → Analyze → Synthesize.

### Consequence
- The first ~10% of the notebook contains no code and no data — only structured business reasoning.
- Hypotheses (H1–H5) are explicitly pre-registered before any chart is drawn, which makes the subsequent "all five confirmed" result less suspicious of post-hoc storytelling.
- Section 7 closes the loop by mapping each finding back to the hypotheses defined in Section 1.

### Alternatives Considered
- **EDA-first, framing-second** — rejected because it inverts the consulting principle of *answer first, work backward to evidence*.

---

## D-003 — Pre-register five hypotheses before EDA

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 1.3

### Context
Without pre-registered hypotheses, EDA tends to drift toward whatever produces the most striking chart, and "findings" become post-hoc rationalizations of patterns spotted in the data.

### Decision
Five hypotheses (H1–H5) covering contract type, service adoption, tenure, internet type, and payment method are written down in Section 1.3 *before any data is loaded*. Each hypothesis specifies expected direction and the variable to test.

### Consequence
- All five were ultimately confirmed (p < 0.05). This is a result worth flagging cautiously — it could mean the hypotheses were too easy, or that the dataset's structure is well-aligned with telco industry priors.
- The final synthesis (Section 7) reports each hypothesis with its statistical test result, so the reader can verify the claim was tested, not asserted.

### Alternatives Considered
- **Test 10–15 hypotheses to cover more ground** — rejected because multiple-comparisons inflation would require Bonferroni or FDR correction, which adds noise without proportional insight. Five focused hypotheses test the most actionable levers.

---

## D-004 — Treat `satisfaction_score` and `churn_score` as suspect leakage variables

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 4.6, Section 6, Limitations

### Context
The dataset includes a `satisfaction_score` (1–5) and a `churn_score` (0–100). Naive analysis would show satisfaction has the strongest correlation with churn (r = −0.755), and `churn_score` would dominate any feature importance plot.

### Decision
- Report the satisfaction-churn correlation honestly, but flag in the limitations section that satisfaction may be measured post-hoc (i.e., after the churn decision was made), which would make it a *consequence* of churn intent, not an independent cause.
- Build the custom risk score in Section 6 using **only behavioral and contractual variables** — tenure, contract type, payment method, service adoption, internet type — and *not* satisfaction or `churn_score`.
- Compare the custom risk score (r = 0.657) against the dataset's `churn_score` (r = 0.661) to show the heuristic is competitive without using suspect variables.

### Consequence
- The custom risk score's discriminative power is defensible because it cannot be accused of feature leakage.
- The headline finding "satisfaction has the strongest correlation with churn" is reported but appropriately caveated.
- A reviewer who notices the satisfaction-leakage concern will find it pre-empted, which builds trust.

### Alternatives Considered
- **Drop satisfaction from the analysis entirely** — rejected because the correlation is genuinely informative *if* properly framed; hiding it would be dishonest.
- **Include satisfaction in the risk score** — rejected because it would inflate apparent performance via leakage.

---

## D-005 — Do not use SMOTE or any synthetic oversampling

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Methodology (general)

### Context
With a 26.5% / 73.5% class split, the data is mildly imbalanced. The reflex in many tutorials is to apply SMOTE to balance the classes.

### Decision
No synthetic oversampling. Class imbalance is handled descriptively (reporting churn rates within segments rather than aggregate accuracy) and, if a predictive model were built later, would be addressed via `class_weight` or `scale_pos_weight`.

### Consequence
- All reported metrics (churn rates by segment, statistical tests) reflect the actual data distribution, not a synthetic one.
- This is a methodological stance carried over from operational/sensor data domains, where SMOTE can produce physically impossible combinations. For categorical customer data, the risk is less severe, but the principle of preferring honest validation over engineered balance still applies.

### Alternatives Considered
- **SMOTE on the merged master table** — rejected for the reasons above.
- **Random undersampling of the majority class** — rejected because it discards real data.

---

## D-006 — Validate the custom risk score with point-biserial correlation, not AUC

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 6

### Context
The custom risk score is a continuous score (0 to ~10) intended to discriminate between churned and retained customers. The standard metric for such a task is AUC-ROC.

### Decision
Use point-biserial correlation (r) between the risk score and the binary churn outcome, with p-value, as the primary validation metric.

### Consequence
- Point-biserial r = 0.657, p ≈ 0 — interpretable as "good discriminator" by conventional thresholds (|r| > 0.3 = moderate; > 0.5 = good).
- This aligns with the descriptive-not-predictive framing (D-001) — the goal is to show the score *separates* churn from non-churn, not to optimize a classification threshold.

### Alternatives Considered
- **AUC-ROC** — would have been equally valid and more familiar to ML reviewers; the trade-off is that AUC implies a predictive use case, which contradicts D-001. Point-biserial is more honest about the descriptive intent.
- **Confusion matrix at a chosen threshold** — rejected because it presupposes a decision rule, which is downstream of this analysis.

---

## D-007 — Define risk score weights from prior knowledge, not from data fitting

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 6

### Context
The risk score adds integer weights based on factors known to be associated with churn (Month-to-Month contract = +3, satisfaction ≤ 2 = +2, etc.). These weights could have been derived from a logistic regression's coefficients fitted on the same data.

### Decision
Weights are assigned heuristically based on the *magnitude of churn rate differences observed in Section 4 EDA*, not by fitting any model. The score is interpretable as a transparent additive rule.

### Consequence
- The score is fully auditable — anyone can recompute it by hand from the rules in Section 5.
- It does not overfit to the dataset (the weights are not optimized).
- The risk score is competitive with the dataset's built-in `churn_score` despite this simplicity, which is itself the finding.

### Alternatives Considered
- **Fit a logistic regression and use coefficients as weights** — rejected because it shifts the project from descriptive to predictive and obscures the heuristic clarity.

---

## D-008 — Use Mann-Whitney U for monthly charges comparison, not t-test

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 4.3

### Context
Comparing monthly charges between churned and retained customers requires a hypothesis test for distribution difference. The default reflex is a two-sample t-test.

### Decision
Use Mann-Whitney U test (non-parametric).

### Consequence
- The test does not assume normality, which monthly charges does not satisfy (visible bimodality in the distribution histogram).
- The reported p-value (3.31e-54) is robust to the distributional shape.

### Alternatives Considered
- **t-test** — would have produced a similarly small p-value but would be technically inappropriate given the distribution.
- **Welch's t-test** — addresses unequal variances but not non-normality.

---

## D-009 — Use Chi-square for all categorical-vs-churn associations

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Sections 4.2, 4.4, 4.5

### Context
Multiple hypotheses involve a categorical predictor (contract type, payment method, internet type, etc.) vs the binary churn outcome.

### Decision
Use Pearson Chi-square test of independence (`scipy.stats.chi2_contingency`) for all such associations.

### Consequence
- Consistent statistical reporting across hypotheses (each finding cites χ² statistic, degrees of freedom, p-value).
- Large sample size (n = 7,043) means even small associations are statistically significant — so effect sizes (percentage point differences) are always reported alongside p-values.

### Alternatives Considered
- **Fisher's exact test** — overkill for sample sizes this large; computationally expensive without added benefit.
- **Logistic regression with categorical predictors** — would have produced odds ratios but adds modeling overhead for what is meant to be a screening analysis.

---

## D-010 — Build a 2×2 Value × Risk segmentation matrix using median splits

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 5

### Context
The end-user of this analysis is a Revenue Operations or Customer Success team that needs to *prioritize* — they cannot give equal retention attention to all 7,043 customers. The analysis needs to translate findings into discrete, actionable segments.

### Decision
Build a 2×2 matrix splitting customers by:
- **Value** — median split on `monthly_charges`
- **Risk** — median split on the custom risk score

This yields four named segments: High Value / High Risk (the priority), High Value / Low Risk (the moat), Low Value / High Risk (likely-to-churn but low-value), Low Value / Low Risk (stable but unprofitable).

### Consequence
- The 1,947 "High Value / High Risk" customers ($2.94M revenue at risk) become the headline number for prioritization recommendations.
- Median split is a deliberate simplification — it produces approximately balanced cell sizes and is easy to explain in a single sentence.

### Alternatives Considered
- **K-means clustering** — rejected because the resulting clusters would not be interpretable as Value × Risk and would require explanation of cluster characteristics.
- **Quartile-based 4×4 matrix (16 segments)** — rejected because granularity exceeds what a retention team can act on; the marginal segments would be too small to support distinct strategies.
- **Tercile splits (3×3 = 9 segments)** — considered, but the 2×2 communicates the priority more directly. The trade-off is that customers near the median are forced into a binary tier; this is acknowledged.

---

## D-011 — Export Power-BI-ready CSVs rather than build the BI dashboard inside the notebook

**Status:** 🟢 Active
**Date:** March 2026
**Section:** Section 8

### Context
The notebook produces enough chart material to suggest building a full Power BI dashboard. But mixing two tools in one repo creates confusion about what the canonical output is.

### Decision
The notebook produces *export-ready* CSV and JSON files (`data/powerbi/`) with cleaned, segmented, and annotated data. The Power BI dashboard is a separate deliverable, downstream of the notebook.

### Consequence
- The notebook's responsibility ends at "clean data + analytical findings + ready exports." The dashboard is a separate concern.
- The exports include a `analysis_metadata.json` with timestamps and hypothesis results, so the dashboard can display analytical context, not just numbers.

### Alternatives Considered
- **Build interactive charts inside the notebook only (Plotly)** — partially done (Plotly imports are present), but a notebook does not replace a dashboard for stakeholder consumption.
- **No exports — leave the notebook self-contained** — rejected because real-world consulting deliverables almost always flow downstream into a BI tool.

---

## D-012 — Pair the notebook with a Streamlit app rather than a static HTML report

**Status:** 🟢 Active
**Date:** March 2026
**Section:** `app/streamlit_app.py`

### Context
The notebook is long and assumes the reader will scroll top-to-bottom. A reviewer who wants to *explore* the findings (filter by segment, change thresholds, look at one chart at a time) cannot do that in a notebook.

### Decision
Build a Streamlit app on top of the cleaned master table, exposing the headline findings and the segmentation matrix as an interactive dashboard.

### Consequence
- Two complementary deliverables: the notebook is *the analysis*, the app is *the exploration tool*.
- The README has to do dual-audience framing because notebook reviewers and app users have different expectations.

### Alternatives Considered
- **Static HTML report (e.g., nbconvert to HTML)** — rejected because it loses interactivity and adds no value over the notebook itself.
- **Power BI dashboard as the only interactive layer** — rejected because Power BI requires the reviewer to have access and willingness to open a `.pbix` file or sign into Power BI Service. Streamlit deploys to a public URL.

---

## D-013 — Bilingual README (English primary, Indonesian narrative section)

**Status:** 🟢 Active
**Date:** May 2026
**Section:** `README.md`

### Context
The repo is shared with two audiences: international recruiters / technical reviewers (English-default) and Indonesian colleagues / domestic professional network (Indonesian-comfortable). Single-language README would underserve one group.

### Decision
- English for all technical content, structure, methodology, findings, code documentation.
- A dedicated Indonesian narrative section ("Bagian Naratif") near the end that explains *why this project exists* and *what it is meant to demonstrate*, in Bahasa Indonesia.

### Consequence
- The README is longer than typical, but the Indonesian section is positioned late enough that international readers can ignore it without losing technical content.
- This pattern is repeated across other artifacts in the portfolio (LinkedIn carousels, deck narratives use Indonesian; code, model outputs, technical artifacts use English).

### Alternatives Considered
- **English only** — rejected because the most relevant near-term professional network is Indonesian.
- **Indonesian only** — rejected because GitHub portfolio is internationally visible and most technical conventions are English-default.
- **Two separate README files (`README.md`, `README.id.md`)** — considered; might be revisited if the Indonesian section grows beyond ~25% of the document.

---

## Open Questions (not yet decided)

These are items where a decision is pending or where the current choice should be re-examined.

- **OQ-1** — Should the dataset's `satisfaction_score` correlation analysis be re-run *with the variable removed*, to show the analysis still stands? Currently planned as a follow-up commit; would strengthen D-004 considerably.
- **OQ-2** — Should the action plan ROI estimates ("save ~$650K revenue/year") be reframed as "potential revenue protected, subject to A/B validation"? Currently flagged in the README limitations but not in the notebook itself.
- **OQ-3** — Should the notebook be split into modular Python scripts (`src/data_loader.py`, `src/eda.py`, `src/risk_scoring.py`) for engineering polish? Trade-off: cleaner code structure vs single-file portfolio readability. Currently deferred.

---

*Last updated: May 2026*
