# Why Do Customers Leave? — Telco Churn Diagnostic Analysis

> **A descriptive-and-diagnostic analysis of customer churn in a telecommunications dataset, structured around the McKinsey 6-Step problem-solving process and communicated using the Pyramid Principle.**
>
> *Mining Engineer · Data Practitioner · Business & Strategy Consultant*

---

## TL;DR

From 7,043 telco customers, **26.5% churned** — driving **$3.68M in revenue leakage** (17.2% of total revenue of $21.4M). All five tested hypotheses were statistically confirmed (p < 0.05). The single largest priority segment is **1,947 High-Value / High-Risk customers** with a 57.9% churn rate and **$2.94M of revenue at risk**.

Three intervention levers, ordered by actionability:
1. **Contract migration** — Month-to-Month churn 45.8% vs yearly 6.2% (χ² = 1,414; p ≈ 0)
2. **Service bundling** — TechSupport reduces churn by 16.0pp; OnlineSecurity by 16.7pp
3. **Onboarding redesign** — 47.4% of churn happens in the first 12 months of tenure

---

## Repository Contents

| File / Folder | What it is |
|---|---|
| `notebooks/Telco_Churn_Analysis_Portfolio.ipynb` | Full analysis — problem framing → data cleaning → EDA → segmentation → risk profiling → synthesis |
| `app/streamlit_app.py` | Interactive Streamlit app for exploring churn drivers and segment-level revenue at risk |
| `data/raw/` | Six relational CSV tables from the IBM Telco Customer Churn dataset (Kaggle) |
| `data/powerbi/` | Cleaned exports ready for Power BI: master table, KPI summary, segment summary, risk evaluation, churn reasons, metadata |
| `outputs/` | Saved charts (`.png`) used in the notebook and the Streamlit app |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

---

## Quick Start

```bash
# Clone
git clone https://github.com/Reinaldis/Telco-Churn-Data-Analysis-Portfolio.git
cd Telco-Churn-Data-Analysis-Portfolio

# Set up environment
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Option 1 — Run the notebook
jupyter notebook notebooks/Telco_Churn_Analysis_Portfolio.ipynb

# Option 2 — Launch the Streamlit app
streamlit run app/streamlit_app.py
```

> **Note on data paths:** the notebook was originally authored in Google Colab and reads from `/content/`. If running locally, either place the six CSVs at `/content/` or change `DATA_PATH` in Section 2.2 to `./data/raw/`.

---

## What This Project Demonstrates

### For technical reviewers
- **End-to-end analytical workflow** — six raw relational tables → merged master (7,043 × 60) → cleaned → segmented → profiled → exported for downstream BI
- **Hypothesis-driven testing** — five pre-registered hypotheses, each tested with the appropriate statistical method (Chi-square for categorical associations, Mann-Whitney U for distribution differences, point-biserial correlation for binary-vs-continuous relationships)
- **Custom risk scoring model** — additive risk score validated as a "good discriminator" (point-biserial r = 0.657 against actual churn), comparable to the dataset's native `churn_score` (r = 0.661)
- **Reproducible exports** — Power-BI-ready CSVs + JSON metadata for analytical traceability

### For business and strategy readers
- **Structured problem framing** — applies the McKinsey 6-Step process (Define → Disaggregate → Prioritize → Workplan → Analyze → Synthesize)
- **Executive synthesis** — full Pyramid Principle structure (Bottom Line → MECE supporting arguments → evidence table → action plan with timeframes and expected impact)
- **Decision-ready segmentation** — 2×2 Value × Risk matrix that translates 7,043 individual customers into four named, actionable segments

---

## Methodology Notes & Honest Limitations

This section is intentionally placed before "Key Findings" because methodological context shapes how the findings should be read.

1. **Descriptive and diagnostic, not predictive.** The objective is to understand *why* churn happens, not to score individual customers for likelihood of churn. Building a true predictive model (logistic regression / gradient boosting) is a separate exercise.

2. **Correlation is not causation.** All five confirmed hypotheses describe *associations*. The recommended interventions (contract migration, service bundling, onboarding redesign) are reasonable on causal grounds, but their actual impact should be validated via controlled A/B testing.

3. **`satisfaction_score` is a cautionary variable.** The dataset's `satisfaction_score` shows the strongest correlation with churn (r = −0.755). However, this score appears to be collected post-hoc — meaning it may be a *consequence* of the churn decision as much as a predictor of it. The same caveat applies to the dataset's built-in `churn_score`. The custom risk score in Section 6 was built deliberately from *behavioral and contractual variables only* (tenure, contract type, payment method, service adoption, etc.) so its discriminative power (r = 0.657) is not driven by leakage from satisfaction data.

4. **Cross-sectional, single-state data.** The dataset is a snapshot of California customers. There is no time-series dimension to detect trend changes, and findings should not be assumed to generalize to other geographies or time periods without validation.

5. **No SMOTE / synthetic oversampling was used.** This is a deliberate methodological stance: synthetic samples can produce variable combinations that do not correspond to plausible customer profiles, which damages the interpretability of downstream findings. Class imbalance is handled descriptively, not engineered away.

---

## Key Findings (with supporting statistics)

| # | Finding | Metric | Statistical Test |
|---|---|---|---|
| 1 | Overall churn rate | 26.5% (1,869 / 7,043) | — |
| 2 | Month-to-Month vs yearly churn ratio | **7.4×** (45.8% vs 6.2%) | Chi-square: χ² = 1,414; p ≈ 0 |
| 3 | TechSupport impact on churn | **−16.0pp** (31.2% → 15.2%) | Chi-square: χ² = 190; p = 2.9e-43 |
| 4 | OnlineSecurity impact on churn | **−16.7pp** (31.3% → 14.6%) | Chi-square: χ² = 206; p = 1.2e-46 |
| 5 | Fiber Optic churn rate | **40.7%** (highest of all internet types) | — |
| 6 | Early-tenure churn (≤12 months) | **47.4%** vs 17.1% later | Chi-square: χ² = 709; p = 3.7e-156 |
| 7 | Electronic check vs auto-payment | **45.3%** vs 16.0% churn | — |
| 8 | Revenue lost to churn | **$3,684,460** (17.2% of total) | Mann-Whitney U: p = 3.3e-54 |
| 9 | Top stated churn category | **Competitor (45.0%)** | — |
| 10 | Custom risk score discrimination | point-biserial r = 0.657 | p ≈ 0 |
| 11 | High-Value / High-Risk priority segment | **1,947 customers, 57.9% churn** | — |

---

## Frameworks Applied

This project deliberately demonstrates how three consulting frameworks structure an analytical deliverable:

- **McKinsey 6-Step Problem-Solving** governs the macro structure of the notebook — from problem definition (Section 1) through synthesis (Section 7).
- **Pyramid Principle** governs the executive summary and Section 7 — bottom-line conclusion first, then MECE supporting arguments, then evidence.
- **SCQR (Situation–Complication–Question–Resolution)** governs the narrative inside each section header — establishing context before findings.

---

## Tech Stack

`Python` · `Pandas` · `NumPy` · `SciPy` · `Matplotlib` · `Seaborn` · `Plotly` · `Streamlit` · `Power BI` (downstream)

---

## Bagian Naratif (Bahasa Indonesia)

### Kenapa proyek ini?

Churn adalah salah satu metrik bisnis paling mudah diukur tapi paling sulit diintervensi dengan benar. Banyak analisis churn berhenti di "berapa persen pelanggan yang pergi" — padahal pertanyaan yang relevan untuk leadership adalah: *segmen mana yang harus diprioritaskan, lever mana yang paling actionable, dan berapa estimasi revenue yang bisa diselamatkan*.

Proyek ini dibangun untuk menunjukkan bagaimana satu pertanyaan bisnis sederhana — *kenapa pelanggan pergi?* — bisa dipecah secara terstruktur menggunakan kerangka kerja konsultasi (McKinsey 6-Step), dianalisis dengan rigor statistik (lima hipotesis pre-registered, masing-masing diuji dengan metode yang sesuai), lalu disintesiskan kembali menggunakan Pyramid Principle ke dalam bentuk rekomendasi yang siap dibawa ke ruang rapat.

### Apa yang ingin saya tunjukkan lewat repo ini

Tiga hal, yang sengaja dipisahkan supaya bisa dievaluasi independen:

1. **Cara berpikir** — apakah problem framing-nya MECE? Apakah hipotesis dipilih berdasarkan logic tree, bukan ditebak? Apakah ada workplan eksplisit sebelum analisis dimulai?
2. **Eksekusi teknis** — apakah data cleaning didokumentasikan? Apakah uji statistik yang dipilih sesuai dengan jenis variabelnya? Apakah custom risk score divalidasi, atau hanya di-claim?
3. **Komunikasi hasil** — apakah executive summary bisa berdiri sendiri? Apakah rekomendasi punya konteks waktu (quick win vs long-term) dan estimasi dampak? Apakah limitasi disampaikan jujur, atau disembunyikan?

### Catatan tentang dataset

Dataset IBM Telco Customer Churn dari Kaggle dipilih karena strukturnya relasional (enam tabel terpisah), yang membuat tahap data engineering lebih realistis dibanding dataset single-table biasa. Dataset ini juga mengandung kolom `satisfaction_score` dan `churn_score` bawaan — namun, sebagaimana dijelaskan di section *Methodology Notes* di atas, dua variabel ini saya treat dengan hati-hati karena kemungkinan besar bersifat post-hoc, sehingga custom risk score di Section 6 sengaja dibangun *tanpa* menggunakan kedua variabel tersebut.

### Konteks domain

Proyek ini berada di domain telco, bukan di mining/energi yang menjadi fokus utama pekerjaan saya. Namun, kerangka analitis dan struktur komunikasinya identik dengan yang saya gunakan untuk pekerjaan domain utama saya — perbedaan domain hanya mengubah konten, bukan cara berpikir. Repo ini sengaja saya pertahankan karena dataset publik memungkinkan reviewer mereproduksi setiap langkah analisis secara independen.

---

## Reproducibility Checklist

- [x] All raw data included (`data/raw/`)
- [x] All transformations explicit in notebook (no hidden manual edits)
- [x] All statistical tests cite both test statistic and p-value
- [x] All charts saved to `outputs/` with consistent naming
- [x] Power BI exports timestamped and versioned via `analysis_metadata.json`
- [x] Custom risk score formula transparent (additive scoring rule documented in Section 5)
- [x] Methodology limitations stated explicitly before findings

---

## License

Code in this repository is released under the MIT License. The IBM Telco Customer Churn dataset is publicly available on Kaggle under its own terms — please refer to the [original Kaggle page](https://www.kaggle.com/datasets/hassanelfattmi/why-do-customers-leave-can-you-spot-the-churners) for dataset licensing.

---

## Contact

**Reinaldi Santoso**
*Mining Engineer · Data Practitioner · Business & Strategy Consultant*

[LinkedIn] · [Email] · [Portfolio site]

> *"Where mining expertise meets data intelligence and business strategy."*
