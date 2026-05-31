"""
═══════════════════════════════════════════════════════════════
Why Do Customers Leave? — Telco Churn Analysis Dashboard
═══════════════════════════════════════════════════════════════
Framework : SCQR (Situation → Complication → Question → Resolution)
           + Pyramid Principle (Level 1 → Level 2 → Level 3)
Author    : [Nama Kamu]
Dataset   : IBM Telco Customer Churn (Kaggle — hassanelfattmi)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Telco Churn · SCQR Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

C = {
    'churn': '#E74C3C', 'retain': '#27AE60', 'neutral': '#2980B9',
    'warn': '#F39C12', 'dark': '#2C3E50', 'joined': '#8E44AD',
    'crit': '#8B0000', 'bg': '#F8F9FA', 'muted': '#6c757d',
}
PAL = ['#2980B9', '#27AE60', '#F39C12', '#E74C3C', '#8E44AD', '#1ABC9C']
LAYOUT = dict(
    font=dict(family="DM Sans, sans-serif", size=13),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=40, r=40, t=50, b=40),
    hoverlabel=dict(bgcolor='white', font_size=12),
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="st-"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding-top: 1.2rem; max-width: 1200px; }
h1 { font-weight: 700 !important; letter-spacing: -0.02em; }
.scqr-box { padding: 1rem 1.3rem; border-radius: 0 10px 10px 0; margin: 0.5rem 0; font-size: 0.95rem; line-height: 1.55; }
.scqr-s { background: #E8F4FD; border-left: 5px solid #2980B9; }
.scqr-c { background: #FFF3CD; border-left: 5px solid #F39C12; }
.scqr-q { background: #F8D7DA; border-left: 5px solid #E74C3C; font-style: italic; font-size: 1.1rem; font-weight: 600; }
.scqr-r { background: #D4EDDA; border-left: 5px solid #27AE60; font-weight: 500; }
.scqr-tag { display: inline-block; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.7; margin-bottom: 0.2rem; }
.pyr-l1 { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 1.3rem 1.5rem; border-radius: 12px; margin: 1rem 0; font-size: 1.05rem; line-height: 1.6; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }
.pyr-l1 b { color: #F39C12; }
.pyr-l2 { background: #f1f3f5; padding: 0.9rem 1.2rem; border-radius: 8px; border-left: 3px solid #2980B9; margin: 0.4rem 0; font-size: 0.92rem; }
.pyr-l2-title { font-weight: 700; color: #2C3E50; margin-bottom: 0.2rem; }
.kpi-card { background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 12px; padding: 1.1rem 1.3rem; border-left: 4px solid #2980B9; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.kpi-card.churn { border-left-color: #E74C3C; }
.kpi-card.revenue { border-left-color: #F39C12; }
.kpi-card.good { border-left-color: #27AE60; }
.kpi-val { font-size: 1.8rem; font-weight: 700; line-height: 1; margin: 0.25rem 0; font-family: 'JetBrains Mono', monospace; }
.kpi-label { font-size: 0.75rem; color: #6c757d; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
.hyp-badge { display: inline-block; padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; background: #d4edda; color: #155724; }
.divider { border-top: 1.5px solid #dee2e6; margin: 1.8rem 0 1.2rem; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

@st.cache_data
def load():
    df = pd.read_csv("data/master_churn.csv")
    with open("data/metadata.json") as f:
        meta = json.load(f)
    return df, meta

try:
    df, meta = load()
except FileNotFoundError:
    st.error("Data files not found. Place `master_churn.csv` and `metadata.json` in `data/`.")
    st.stop()

kpi = meta['kpi']
hyp = meta['hypotheses']
churned = df[df['is_churned'] == 1]
retained = df[df['is_churned'] == 0]
overall_cr = df['is_churned'].mean()


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def scqr(s=None, c=None, q=None, r=None):
    if s: st.markdown(f'<div class="scqr-box scqr-s"><div class="scqr-tag">Situation</div><br>{s}</div>', unsafe_allow_html=True)
    if c: st.markdown(f'<div class="scqr-box scqr-c"><div class="scqr-tag">Complication</div><br>{c}</div>', unsafe_allow_html=True)
    if q: st.markdown(f'<div class="scqr-box scqr-q"><div class="scqr-tag">Question</div><br>"{q}"</div>', unsafe_allow_html=True)
    if r: st.markdown(f'<div class="scqr-box scqr-r"><div class="scqr-tag">Resolution — Pyramid Level 1</div><br>{r}</div>', unsafe_allow_html=True)

def pyramid_l2(title, text):
    st.markdown(f'<div class="pyr-l2"><div class="pyr-l2-title">{title}</div>{text}</div>', unsafe_allow_html=True)

def kpi_card(label, value, css=""):
    st.markdown(f'<div class="kpi-card {css}"><div class="kpi-label">{label}</div><div class="kpi-val">{value}</div></div>', unsafe_allow_html=True)

def divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def churn_bar(data, col, title, horizontal=False):
    grp = data.groupby(col)['is_churned'].agg(['mean','count']).reset_index()
    grp.columns = [col, 'rate', 'n']
    grp['pct'] = (grp['rate']*100).round(1)
    grp['clr'] = grp['rate'].apply(lambda x: C['churn'] if x > overall_cr else C['retain'])
    grp = grp.sort_values('rate', ascending=True if horizontal else False)
    if horizontal:
        fig = go.Figure(go.Bar(y=grp[col], x=grp['pct'], orientation='h', marker_color=grp['clr'],
            text=grp.apply(lambda r: f"{r['pct']:.1f}% (n={r['n']:,})", axis=1), textposition='outside', textfont=dict(size=11)))
        fig.add_vline(x=overall_cr*100, line_dash='dash', line_color='gray', opacity=0.4,
                      annotation_text=f"Avg {overall_cr*100:.1f}%", annotation_font_size=10)
    else:
        fig = go.Figure(go.Bar(x=grp[col], y=grp['pct'], marker_color=grp['clr'],
            text=grp.apply(lambda r: f"{r['pct']:.1f}%<br>n={r['n']:,}", axis=1), textposition='outside', textfont=dict(size=11)))
        fig.add_hline(y=overall_cr*100, line_dash='dash', line_color='gray', opacity=0.4,
                      annotation_text=f"Avg {overall_cr*100:.1f}%", annotation_font_size=10)
    fig.update_layout(title=title, showlegend=False, **LAYOUT)
    return fig


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 📊 Telco Churn Analysis")
    st.caption("SCQR + Pyramid Principle")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Executive Summary",
        "📈 Where is Churn?",
        "⏱ When Do They Leave?",
        "💰 How Much Do We Lose?",
        "🛡 What Protects Them?",
        "📝 What Locks Them In?",
        "🎯 Who Should We Save?",
        "⚠ Can We Predict It?",
        "❓ Why Do They Leave?",
        "🔍 Customer Lookup",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:#999'><b>Framework:</b> SCQR + Pyramid<br><b>Author:</b> [Nama Kamu]<br><b>Date:</b> April 2026</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════

if page == "🏠 Executive Summary":
    st.markdown("# Why Do Customers Leave?")
    st.caption("Telco Customer Churn Analysis — SCQR Executive Briefing")
    scqr(
        s="Perusahaan telco ini melayani <b>7,043 pelanggan</b> di California dengan total revenue <b>$21.4M</b>, menawarkan layanan internet (Fiber/DSL/Cable), phone, dan berbagai add-on services.",
        c="<b>26.5% pelanggan churn</b> (1,869 dari 7,043) — mengakibatkan revenue leakage <b>$3.68M</b> (17.2% total revenue). Yang lebih mengkhawatirkan: pelanggan yang churn justru membayar <b>lebih mahal</b> ($74/bulan vs $61/bulan). Tanpa pemahaman granular tentang siapa, kapan, dan mengapa mereka pergi, strategi retention tetap generik dan tidak efisien.",
        q="Faktor apa yang paling mendorong churn, segmen mana yang harus diprioritaskan, dan intervensi apa yang paling cost-effective?",
        r="Tiga intervensi prioritas berdasarkan 5 hipotesis yang <b>seluruhnya terkonfirmasi</b>: <b>(1)</b> Migrasi kontrak Month-to-Month → tahunan (churn drops 45.8% → 6.2%), <b>(2)</b> Service bundling TechSupport + OnlineSecurity untuk Fiber Optic (Δ = 16pp), <b>(3)</b> Onboarding redesign untuk 12 bulan pertama (47.4% churn terkonsentrasi di sini). Fokus pada <b>1,947 pelanggan High Value / High Risk</b> dengan $2.9M revenue at risk."
    )
    divider()
    st.markdown("##### Pyramid Level 2 — Key Metrics")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi_card("Total Customers", f"{kpi['total_customers']:,}")
    with c2: kpi_card("Churn Rate", f"{kpi['churn_rate_pct']}%", "churn")
    with c3: kpi_card("Revenue Lost", f"${kpi['revenue_lost']:,.0f}", "revenue")
    with c4: kpi_card("Churned", f"{kpi['churned']:,}", "churn")
    with c5: kpi_card("Satisfaction (Churn)", f"{kpi['avg_satisfaction_churned']}/5", "churn")
    divider()
    st.markdown("##### Pyramid Level 2 — All 5 Hypotheses Confirmed")
    cols = st.columns(5)
    for i, (hid, h) in enumerate(hyp.items()):
        with cols[i]:
            st.markdown(f"**{hid}** <span class='hyp-badge'>✓ {h['status']}</span><br><span style='font-size:0.88rem'>{h['label']}</span><br><span style='font-size:0.78rem;color:#555'>{h['detail']}</span>", unsafe_allow_html=True)
    divider()
    st.markdown("##### Pyramid Level 3 — Evidence")
    ca, cb = st.columns(2)
    with ca:
        fig = px.pie(df, names='customer_status', hole=0.5, color='customer_status', color_discrete_map={'Stayed':C['retain'],'Churned':C['churn'],'Joined':C['joined']})
        fig.update_layout(title="Customer Status", **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        st.plotly_chart(churn_bar(df, 'contract', 'Churn Rate by Contract Type'), use_container_width=True)
    divider()
    st.markdown("##### Resolution → Action Plan")
    c1,c2,c3 = st.columns(3)
    with c1: pyramid_l2("🟢 Quick Win (0–30 hari)", "Migrasi 3,610 pelanggan MTM ke kontrak tahunan. Diskon 10–15% + auto-payment setup. Target: 20% konversi → save ~$650K/tahun.")
    with c2: pyramid_l2("🟡 Mid-Term (1–3 bulan)", "Bundle TechSupport + OnlineSecurity gratis 3 bulan untuk 3,035 pelanggan Fiber Optic. Target: reduce churn dari 40.7% ke <25%.")
    with c3: pyramid_l2("🔴 Long-Term (3–6 bulan)", "Redesign onboarding: check-in otomatis bulan 1, 3, 6, 12. Implement risk scoring (r=0.657) sebagai early warning system.")


elif page == "📈 Where is Churn?":
    st.markdown("# 📈 Where is Churn Concentrated?")
    scqr(
        s="Perusahaan memiliki pelanggan tersebar di berbagai tipe kontrak (MTM, 1yr, 2yr), internet service (Fiber/DSL/Cable), dan metode pembayaran — masing-masing dengan behavior berbeda.",
        c="Churn rate keseluruhan <b>26.5%</b> ternyata <b>tidak merata</b>: beberapa segmen memiliki churn rate mendekati 50%, sementara segmen lain hanya 5–7%. Strategi retention generik gagal menangkap perbedaan ini.",
        q="Di segmen mana churn paling terkonsentrasi, dan segmen mana yang relatif aman?",
        r="Churn terkonsentrasi di tiga segmen: <b>Month-to-Month</b> (45.8%), <b>Fiber Optic</b> (40.7%), dan <b>Electronic check</b> (45.3%). Sebaliknya, pelanggan kontrak tahunan (6.2%), DSL (18.6%), dan auto-payment (16.0%) jauh lebih stabil."
    )
    divider()
    st.markdown("##### Level 2 — Churn Breakdown by Key Dimensions")
    ca, cb = st.columns(2)
    with ca:
        pyramid_l2("A. Contract type = pembeda terbesar", "MTM 45.8% vs Two Year 2.6%. Tanpa lock-in, tidak ada barrier to exit.")
        st.plotly_chart(churn_bar(df, 'contract', 'By Contract Type'), use_container_width=True)
    with cb:
        pyramid_l2("B. Internet type = sinyal value gap", "Fiber Optic 40.7% — tertinggi meski harga juga tertinggi.")
        st.plotly_chart(churn_bar(df, 'internet_type', 'By Internet Type'), use_container_width=True)
    ca, cb = st.columns(2)
    with ca:
        pyramid_l2("C. Tenure = lifecycle vulnerability", "Pelanggan baru (0–6 bulan) paling rentan.")
        st.plotly_chart(churn_bar(df, 'tenure_segment', 'By Tenure Segment'), use_container_width=True)
    with cb:
        pyramid_l2("D. Payment method = commitment proxy", "Electronic check 45.3% — manual = low friction to leave.")
        st.plotly_chart(churn_bar(df, 'payment_method', 'By Payment Method', horizontal=True), use_container_width=True)
    divider()
    st.markdown("##### Level 3 — Explore Any Variable")
    cat_cols = [c for c in df.columns if df[c].dtype == 'object' and 2 <= df[c].nunique() <= 15 and c not in ['customer_id','churn_reason','city','country','state']]
    sel = st.selectbox("Pilih variabel:", cat_cols, index=cat_cols.index('contract'))
    st.plotly_chart(churn_bar(df, sel, f'Churn Rate by {sel.replace("_"," ").title()}'), use_container_width=True)


elif page == "⏱ When Do They Leave?":
    st.markdown("# ⏱ When in the Lifecycle Do They Leave?")
    scqr(
        s="Customer lifecycle bervariasi dari 0 hingga 72 bulan. Perusahaan belum memiliki pemetaan kapan dalam perjalanan pelanggan churn paling mungkin terjadi.",
        c="Pelanggan di <b>≤12 bulan pertama churn 47.4%</b>, sementara >12 bulan hanya 17.1%. Hampir separuh pelanggan baru hilang dalam tahun pertama.",
        q="Kapan tepatnya critical window terjadi, dan bagaimana survival curve pelanggan?",
        r="<b>H3 ✓ CONFIRMED</b> (χ²=708.78, p=3.68e-156): 12 bulan pertama adalah danger zone. Survival curve drop tajam di bulan 1–6. <b>ROI tertinggi ada di onboarding, bukan winback.</b>"
    )
    divider()
    st.markdown("##### Level 2 — Supporting Evidence")
    pyramid_l2("A. Distribusi tenure churned vs retained sangat berbeda", "Churned terkonsentrasi di 0–15 bulan. Retained tersebar merata di 20–72 bulan.")
    ca, cb = st.columns(2)
    with ca:
        fig = go.Figure()
        for lbl, clr, nm in [(0, C['retain'], 'Retained'), (1, C['churn'], 'Churned')]:
            fig.add_trace(go.Histogram(x=df[df['is_churned']==lbl]['tenure'], nbinsx=36, opacity=0.5, marker_color=clr, name=nm, histnorm='probability density'))
        fig.add_vline(x=12, line_dash='dash', line_color=C['warn'], annotation_text='12-mo mark')
        fig.update_layout(title='Tenure Distribution', barmode='overlay', xaxis_title='Tenure (months)', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        t_ch = df.groupby('tenure')['is_churned'].mean().reset_index()
        t_ch.columns = ['tenure', 'rate']
        t_ch['roll'] = t_ch['rate'].rolling(3, center=True).mean()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=t_ch['tenure'], y=t_ch['rate']*100, marker_color=C['neutral'], opacity=0.25, name='Actual'))
        fig.add_trace(go.Scatter(x=t_ch['tenure'], y=t_ch['roll']*100, line=dict(color=C['churn'], width=3), name='3-mo rolling'))
        fig.update_layout(title='Churn Rate by Tenure', xaxis_title='Tenure (months)', yaxis_title='Churn Rate (%)', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    pyramid_l2("B. Survival curve — half-life pelanggan", "Proporsi aktif menurun tajam di bulan awal, lalu melambat.")
    tmax = int(df['tenure'].max())
    surv = pd.DataFrame({'mo': range(1, tmax+1), 'surv': [(df['tenure'] >= t).mean() for t in range(1, tmax+1)]})
    fig = go.Figure(go.Scatter(x=surv['mo'], y=surv['surv'], fill='tozeroy', fillcolor='rgba(41,128,185,0.08)', line=dict(color=C['neutral'], width=3)))
    fig.add_hline(y=0.5, line_dash='dash', line_color=C['churn'], annotation_text='50% survival')
    fig.update_layout(title='Customer Survival Curve', xaxis_title='Month', yaxis_title='Proportion Still Active', yaxis_tickformat='.0%', **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    divider()
    st.markdown("##### Level 3 — Statistical Test")
    c1,c2,c3 = st.columns(3)
    with c1: kpi_card("Early (≤12mo)", "47.4%", "churn")
    with c2: kpi_card("Later (>12mo)", "17.1%", "good")
    with c3: kpi_card("Chi-sq p-value", "3.68e-156", "")
    st.success("**H3 ✓ CONFIRMED:** Early tenure churn 2.8× higher than later tenure.")


elif page == "💰 How Much Do We Lose?":
    st.markdown("# 💰 How Much Revenue Are We Losing?")
    scqr(
        s="Total revenue <b>$21.4M</b> dari 7,043 pelanggan. Revenue terdistribusi tidak merata — sebagian kecil pelanggan menghasilkan porsi besar.",
        c="Churn mengakibatkan <b>$3.68M revenue leakage</b> (17.2%). Paradoks: pelanggan yang churn membayar <b>$74.44/bulan</b> — <b>21% lebih tinggi</b> dari retained ($61.27). Kita kehilangan pelanggan paling bernilai.",
        q="Seberapa besar dampak finansial churn, dan dari segmen mana revenue paling banyak bocor?",
        r="Revenue leakage <b>$3.68M</b> terkonsentrasi pada pelanggan high-value. Perbedaan monthly charges signifikan (Mann-Whitney p=3.31e-54). <b>Churn bukan masalah headcount — ini wealth destruction pada pelanggan premium.</b>"
    )
    divider()
    st.markdown("##### Level 2 — Revenue Breakdown")
    c1,c2,c3 = st.columns(3)
    with c1: kpi_card("Total Revenue", f"${kpi['total_revenue']:,.0f}")
    with c2: kpi_card("Revenue Retained", f"${kpi['total_revenue']-kpi['revenue_lost']:,.0f}", "good")
    with c3: kpi_card("Revenue Lost", f"${kpi['revenue_lost']:,.0f}", "churn")
    ca, cb = st.columns(2)
    with ca:
        pyramid_l2("A. Churned customers membayar lebih mahal", f"Avg churned ${kpi['avg_monthly_churned']}/mo vs retained ${kpi['avg_monthly_retained']}/mo.")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=retained['monthly_charges'], nbinsx=30, opacity=0.5, marker_color=C['retain'], name='Retained', histnorm='probability density'))
        fig.add_trace(go.Histogram(x=churned['monthly_charges'], nbinsx=30, opacity=0.5, marker_color=C['churn'], name='Churned', histnorm='probability density'))
        fig.update_layout(title='Monthly Charges Distribution', barmode='overlay', xaxis_title='Monthly Charges ($)', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        pyramid_l2("B. Revenue bocor terbesar dari pelanggan baru", "Early tenure menyumbang porsi besar revenue lost.")
        rev_seg = churned.groupby('tenure_segment')['total_revenue'].sum().reset_index()
        fig = px.bar(rev_seg, x='tenure_segment', y='total_revenue', color_discrete_sequence=[C['warn']], text=rev_seg['total_revenue'].apply(lambda x: f'${x:,.0f}'))
        fig.update_traces(textposition='outside')
        fig.update_layout(title='Revenue Lost by Tenure Segment', xaxis_title=None, yaxis_title='Revenue Lost ($)', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("##### Level 3 — CLTV Comparison")
    fig = go.Figure()
    fig.add_trace(go.Box(y=churned['cltv'], name='Churned', marker_color=C['churn'], boxmean=True))
    fig.add_trace(go.Box(y=retained['cltv'], name='Retained', marker_color=C['retain'], boxmean=True))
    fig.update_layout(title='CLTV: Churned vs Retained', **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


elif page == "🛡 What Protects Them?":
    st.markdown("# 🛡 What Services Protect Against Churn?")
    scqr(
        s="Perusahaan menawarkan 8+ layanan add-on: Online Security, Tech Support, Device Protection, Streaming TV/Movies/Music, Unlimited Data, Multiple Lines.",
        c="Tanpa TechSupport: churn <b>31.2%</b> (vs 15.2%). Tanpa OnlineSecurity: <b>31.3%</b> (vs 14.6%). Δ ~16pp. Fiber Optic — produk premium — justru churn tertinggi <b>40.7%</b>.",
        q="Layanan mana yang berfungsi sebagai retention moat, dan mengapa Fiber Optic justru berisiko tinggi?",
        r="<b>H2 ✓ H4 ✓ CONFIRMED.</b> TechSupport & OnlineSecurity = retention tools terkuat (Δ ~16pp). Setiap tambahan service = churn lebih rendah. Fiber Optic paradox: high price + high churn = <b>value gap</b>. <b>Value-added services bukan cost center — mereka retention tools.</b>"
    )
    divider()
    st.markdown("##### Level 2 — Service Impact")
    svc_cols = ['online_security','online_backup','device_protection','premium_tech_support','streaming_tv','streaming_movies','streaming_music','unlimited_data']
    rows = []
    for col in svc_cols:
        if col in df.columns:
            y = df[df[col]=='Yes']['is_churned'].mean()*100
            n = df[df[col]=='No']['is_churned'].mean()*100
            rows.append({'service': col.replace('_',' ').title(), 'With':y, 'Without':n, 'Delta':n-y})
    si = pd.DataFrame(rows).sort_values('Delta', ascending=True)
    pyramid_l2("A. Every service reduces churn — protection services have biggest impact", "TechSupport Δ=16pp, OnlineSecurity Δ=16.7pp.")
    fig = go.Figure()
    fig.add_trace(go.Bar(y=si['service'], x=si['Without'], orientation='h', name='Without', marker_color=C['churn'], opacity=0.7))
    fig.add_trace(go.Bar(y=si['service'], x=si['With'], orientation='h', name='With', marker_color=C['retain'], opacity=0.7))
    fig.update_layout(title='Churn: With vs Without Each Service', barmode='group', xaxis_title='Churn Rate (%)', **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    ca, cb = st.columns(2)
    with ca:
        pyramid_l2("B. More services = lower churn", "Stickiness grows with adoption.")
        sc = df.groupby('n_services')['is_churned'].agg(['mean','count']).reset_index()
        fig = go.Figure(go.Bar(x=sc['n_services'], y=sc['mean']*100, marker_color=C['neutral'],
            text=sc.apply(lambda r: f"{r['mean']*100:.0f}%<br>n={r['count']:,}", axis=1), textposition='outside'))
        fig.add_hline(y=overall_cr*100, line_dash='dash', line_color='gray', opacity=0.4)
        fig.update_layout(title='Churn by # of Services', xaxis_title='Active Services', yaxis_title='Churn %', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        pyramid_l2("C. Fiber Optic paradox", "Premium price ≠ premium retention. Butuh bundling strategy.")
        st.plotly_chart(churn_bar(df, 'internet_type', 'Churn by Internet Type'), use_container_width=True)


elif page == "📝 What Locks Them In?":
    st.markdown("# 📝 What Commitment Mechanisms Work?")
    scqr(
        s="Tiga tipe kontrak: Month-to-Month, One Year, Two Year. Empat metode bayar. Lima promotional offer (A–E) plus 'No Offer'.",
        c="MTM churn <b>45.8%</b> vs yearly <b>6.2%</b> — rasio <b>7.4×</b>. E-check <b>45.3%</b> vs auto-pay <b>16.0%</b>. Tanpa friction to exit, pelanggan pergi mudah.",
        q="Mekanisme commitment apa yang paling efektif, dan bagaimana interaksinya dengan tenure?",
        r="<b>H1 ✓ H5 ✓ CONFIRMED.</b> Contract = lever #1 (7.4× difference). Auto-pay = 2.8× lower. Contract × tenure: MTM tetap tinggi di SEMUA tenure — ini masalah <b>structural commitment</b>, bukan lifecycle."
    )
    divider()
    st.markdown("##### Level 2 — Commitment Mechanisms")
    ca, cb = st.columns(2)
    with ca:
        pyramid_l2("A. Contract = strongest lever", "MTM 45.8%, One Year 11.3%, Two Year 2.6%.")
        st.plotly_chart(churn_bar(df, 'contract', 'By Contract'), use_container_width=True)
    with cb:
        pyramid_l2("B. Payment = engagement proxy", "Manual (E-check 45.3%) vs auto (16.0%). Automation creates inertia.")
        st.plotly_chart(churn_bar(df, 'payment_method', 'By Payment Method', horizontal=True), use_container_width=True)
    pyramid_l2("C. Contract × Tenure: MTM stays high regardless of tenure", "Even 3+ year MTM customers have high churn — it's about lock-in, not familiarity.")
    fig = go.Figure()
    for ct in df['contract'].unique():
        sub = df[df['contract']==ct]
        bins = pd.cut(sub['tenure'], bins=range(0,78,6))
        tc = sub.groupby(bins, observed=False)['is_churned'].mean()*100
        fig.add_trace(go.Scatter(x=list(range(len(tc))), y=tc.values, mode='lines+markers', name=ct, line=dict(width=3)))
    fig.update_layout(title='Churn Over Time by Contract', xaxis_title='Tenure (6-mo bins)', yaxis_title='Churn %', **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("##### Level 3 — Offer Analysis")
    st.plotly_chart(churn_bar(df, 'offer', 'Churn by Promotional Offer'), use_container_width=True)


elif page == "🎯 Who Should We Save?":
    st.markdown("# 🎯 Who Should We Prioritize for Retention?")
    scqr(
        s="Tidak semua pelanggan sama. Monthly charges $18–$119. Beberapa high-value bundling 5+ services, lain low-value layanan minimal.",
        c="Budget retention terbatas. $1 untuk retain pelanggan $18/bulan ≠ $1 untuk pelanggan $100/bulan. Butuh <b>prioritisasi value × risk</b>.",
        q="Segmen mana yang harus mendapat prioritas retention tertinggi?",
        r="<b>High Value / High Risk: 1,947 pelanggan</b>, churn <b>57.9%</b>, revenue at risk <b>$2.94M</b>. Avg $88/bulan, satisfaction hanya 2.6/5. <b>Priority #1 — high-paying but deeply dissatisfied.</b>"
    )
    divider()
    st.markdown("##### Level 2 — 2×2 Value × Risk Matrix")
    seg = df.groupby('segment_2x2').agg(n=('is_churned','count'), rate=('is_churned','mean'), avg_mo=('monthly_charges','mean'), avg_ten=('tenure','mean'), avg_sat=('satisfaction_score','mean'), tot_rev=('total_revenue','sum')).reset_index()
    seg['pct'] = (seg['rate']*100).round(1)
    seg['rar'] = (seg['tot_rev']*seg['rate']).round(0)
    cmap = {'High Value / High Risk':C['churn'], 'Low Value / High Risk':C['warn'], 'High Value / Low Risk':C['retain'], 'Low Value / Low Risk':C['neutral']}
    icons = {'High Value / High Risk':'🔥', 'Low Value / High Risk':'⚠️', 'High Value / Low Risk':'✅', 'Low Value / Low Risk':'💤'}
    cols = st.columns(4)
    for i, (_, r) in enumerate(seg.sort_values('rate', ascending=False).iterrows()):
        with cols[i]:
            ic = icons.get(r['segment_2x2'], '')
            css = 'churn' if r['segment_2x2']=='High Value / High Risk' else 'revenue' if 'High Risk' in r['segment_2x2'] else 'good' if 'High Value' in r['segment_2x2'] else ''
            kpi_card(f"{ic} {r['segment_2x2']}", f"{r['pct']}% churn", css)
            st.caption(f"n={r['n']:,} · ${r['rar']:,.0f} at risk · sat {r['avg_sat']:.1f}/5")
    ca, cb = st.columns(2)
    with ca:
        fig = px.scatter(df.sample(min(3000,len(df)), random_state=42), x='monthly_charges', y='risk_score', color='segment_2x2', color_discrete_map=cmap, opacity=0.25, labels={'monthly_charges':'Monthly Charges ($)','risk_score':'Risk Score'})
        fig.update_layout(title='Value × Risk Scatter', legend=dict(font=dict(size=9)), **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        ss = seg.sort_values('pct', ascending=True)
        fig = go.Figure(go.Bar(y=ss['segment_2x2'], x=ss['pct'], orientation='h', marker_color=[cmap.get(s,'gray') for s in ss['segment_2x2']],
            text=ss.apply(lambda r: f"{r['pct']}% · ${r['rar']:,.0f} at risk", axis=1), textposition='outside'))
        fig.update_layout(title='Churn & Revenue at Risk', xaxis_title='Churn Rate (%)', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("##### Level 3 — Segment Detail")
    st.dataframe(seg[['segment_2x2','n','pct','avg_mo','avg_ten','avg_sat','rar']].rename(columns={'segment_2x2':'Segment','n':'Customers','pct':'Churn %','avg_mo':'Avg Monthly ($)','avg_ten':'Avg Tenure (mo)','avg_sat':'Satisfaction','rar':'Rev at Risk ($)'}).sort_values('Churn %', ascending=False), use_container_width=True, hide_index=True)


elif page == "⚠ Can We Predict It?":
    st.markdown("# ⚠ Can We Predict Who Will Churn?")
    scqr(
        s="Kita sudah tahu faktor-faktor churn. Pertanyaannya: bisa kah digabung menjadi satu composite risk score yang proaktif mengidentifikasi pelanggan at-risk?",
        c="Saat ini tidak ada early warning system. Intervensi dilakukan <b>reaktif</b> — setelah pelanggan sudah menunjukkan niat pergi atau bahkan sudah churn.",
        q="Bisakah kita membangun risk scoring system yang membedakan pelanggan berisiko dari yang aman?",
        r="<b>Ya.</b> Composite risk score (6 variabel) menghasilkan <b>r = 0.657</b> (good discriminator, p ≈ 0). Tier 'Critical': actual churn <b>80.3%</b> vs 'Low Risk' hanya <b>2.9%</b>. <b>Siap diimplementasikan sebagai automated early warning.</b>"
    )
    divider()
    st.markdown("##### Level 2 — Risk Scoring Evaluation")
    risk = df.groupby('risk_label', observed=False).agg(n=('is_churned','count'), rate=('is_churned','mean'), avg_mo=('monthly_charges','mean'), avg_sat=('satisfaction_score','mean'), tot_rev=('total_revenue','sum')).reset_index()
    risk['pct'] = (risk['rate']*100).round(1)
    risk['rar'] = (risk['tot_rev']*risk['rate']).round(0)
    rcol = [C['retain'], C['warn'], C['churn'], C['crit']]
    pyramid_l2("A. Risk score cleanly separates tiers", "Low 2.9% → Medium 15.6% → High 19.8% → Critical 80.3%. Monotonic = good discriminator.")
    ca, cb = st.columns(2)
    with ca:
        fig = go.Figure(go.Bar(x=risk['risk_label'], y=risk['pct'], marker_color=rcol[:len(risk)],
            text=risk.apply(lambda r: f"{r['pct']}%<br>n={r['n']:,}", axis=1), textposition='outside'))
        fig.update_layout(title='Actual Churn by Risk Label', yaxis_title='Churn %', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        fig = go.Figure(go.Bar(x=risk['risk_label'], y=risk['rar'], marker_color=rcol[:len(risk)],
            text=risk['rar'].apply(lambda x: f'${x:,.0f}'), textposition='outside'))
        fig.update_layout(title='Revenue at Risk by Label', yaxis_title='Rev at Risk ($)', **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    pyramid_l2("B. Critical tier: satisfaction sangat rendah (2.1/5)", "Dissatisfaction = main driver di tier ini.")
    fig = go.Figure()
    for rl, clr in zip(risk['risk_label'], rcol):
        sub = df[df['risk_label']==rl]['satisfaction_score']
        if len(sub)>0: fig.add_trace(go.Histogram(x=sub, name=rl, marker_color=clr, opacity=0.45, histnorm='probability density'))
    fig.update_layout(title='Satisfaction by Risk Tier', barmode='overlay', xaxis_title='Satisfaction (1–5)', **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("##### Level 3 — Score Components & Validation")
    pyramid_l2("Risk score = sum of", "Contract MTM (+3) · Tenure ≤12mo (+2) · Tenure 13–24 (+1) · No protection (+1) · E-check (+1) · Satisfaction ≤2 (+2) · Fiber Optic (+1)")
    c1,c2 = st.columns(2)
    with c1: kpi_card("Point-biserial r", "0.657", "good")
    with c2: kpi_card("p-value", "≈ 0", "good")
    st.dataframe(risk[['risk_label','n','pct','avg_mo','avg_sat','rar']].rename(columns={'risk_label':'Risk','n':'N','pct':'Churn %','avg_mo':'Avg Monthly ($)','avg_sat':'Satisfaction','rar':'Rev at Risk ($)'}), use_container_width=True, hide_index=True)


elif page == "❓ Why Do They Leave?":
    st.markdown("# ❓ Why Do They Actually Leave?")
    scqr(
        s="Dataset ini memiliki keunggulan langka: <b>explicit churn reasons</b>. Setiap pelanggan yang churn memiliki churn_category (high-level) dan churn_reason (granular).",
        c="Dari 1,869 churned, alasan terbesar: <b>Competitor (45.0%)</b>, Attitude (16.8%), Dissatisfaction (16.2%). Hampir setengah churn didorong <b>competitive pressure</b>, bukan hanya internal failure.",
        q="Apa root cause utama churn, dan bagaimana hubungannya dengan satisfaction?",
        r="<b>Competitor = #1 driver (45%)</b> — pelanggan pindah karena harga, perangkat, atau speed lebih baik. Tapi Dissatisfaction + Attitude (33% combined) <b>bisa dicegah secara internal</b>. Satisfaction score = prediktor tunggal terkuat (<b>r = −0.755</b>)."
    )
    divider()
    st.markdown("##### Level 2 — Churn Reason Breakdown")
    ca, cb = st.columns(2)
    with ca:
        pyramid_l2("A. High-level categories", "Competitor (45%), Attitude (16.8%), Dissatisfaction (16.2%), Price (11.3%), Other (10.7%).")
        cat = churned['churn_category'].value_counts().reset_index()
        cat.columns = ['category','count']
        cat = cat[cat['category']!='Not Applicable']
        fig = px.bar(cat, y='category', x='count', orientation='h', color='count', color_continuous_scale='OrRd',
            text=cat.apply(lambda r: f"{r['count']} ({r['count']/len(churned)*100:.1f}%)", axis=1))
        fig.update_traces(textposition='outside')
        fig.update_layout(title='Churn Category', coloraxis_showscale=False, xaxis_title='Count', yaxis_title=None, **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        pyramid_l2("B. Top 10 specific reasons", "Granular root causes — competitor offers, support attitude, pricing.")
        reas = churned['churn_reason'].value_counts().head(10).reset_index()
        reas.columns = ['reason','count']
        reas = reas[reas['reason']!='Not Applicable']
        fig = px.bar(reas[::-1], y='reason', x='count', orientation='h', color_discrete_sequence=[C['churn']], text='count')
        fig.update_traces(textposition='outside')
        fig.update_layout(title='Top 10 Specific Reasons', xaxis_title='Count', yaxis_title=None, **LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("##### Level 3 — Satisfaction × Category")
    cat_sat = churned[churned['churn_category']!='Not Applicable']
    fig = px.box(cat_sat, x='churn_category', y='satisfaction_score', color='churn_category', color_discrete_sequence=PAL)
    fig.update_layout(title='Satisfaction by Churn Category', showlegend=False, xaxis_title=None, yaxis_title='Satisfaction (1–5)', **LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


elif page == "🔍 Customer Lookup":
    st.markdown("# 🔍 Customer Risk Assessment")
    st.markdown("Search any customer for full profile and risk tier.")
    search = st.text_input("Customer ID:", placeholder="e.g. 0002-ORFBO")
    if search:
        match = df[df['customer_id'].str.contains(search, case=False, na=False)]
        if len(match) == 0:
            st.warning(f"No match for '{search}'")
        else:
            if len(match) > 1: st.info(f"{len(match)} matches — showing first.")
            cu = match.iloc[0]
            c1,c2,c3,c4 = st.columns(4)
            with c1: kpi_card("Customer ID", cu['customer_id'])
            with c2: kpi_card("Status", cu['customer_status'], 'churn' if cu['is_churned']==1 else 'good')
            with c3: kpi_card("Risk", str(cu.get('risk_label','N/A')), 'churn' if str(cu.get('risk_label','')) in ['High Risk','Critical'] else '')
            with c4: kpi_card("Segment", cu.get('segment_2x2','N/A'))
            divider()
            c1,c2,c3 = st.columns(3)
            with c1:
                st.markdown("**Demographics**")
                st.markdown(f"- Gender: {cu['gender']}\n- Age: {cu['age']} ({cu.get('age_group','N/A')})\n- Married: {cu['married']}\n- Dependents: {cu['dependents']} ({cu['number_of_dependents']})\n- Senior: {cu['senior_citizen']}")
            with c2:
                st.markdown("**Account & Services**")
                st.markdown(f"- Tenure: {cu['tenure']} mo ({cu.get('tenure_segment','N/A')})\n- Contract: {cu['contract']}\n- Internet: {cu.get('internet_type','N/A')}\n- Payment: {cu['payment_method']}\n- Services: {cu.get('n_services','N/A')} active\n- Protection: {'Yes' if cu.get('has_protection',0)==1 else 'No'}")
            with c3:
                st.markdown("**Financials & Scores**")
                st.markdown(f"- Monthly: ${cu['monthly_charges']:.2f}\n- Total Revenue: ${cu['total_revenue']:,.2f}\n- CLTV: {cu['cltv']:,}\n- Satisfaction: {cu['satisfaction_score']}/5\n- Churn Score: {cu['churn_score']}\n- Risk Score: {cu.get('risk_score','N/A')}")
            if cu['is_churned']==1:
                st.error(f"**Churn Reason:** {cu.get('churn_category','N/A')} — {cu.get('churn_reason','N/A')}")
    else:
        st.markdown("##### Or browse by Risk Label:")
        rf = st.multiselect("Filter:", ['Low Risk','Medium Risk','High Risk','Critical'], default=['Critical'])
        if rf:
            filt = df[df['risk_label'].isin(rf)].sort_values('risk_score', ascending=False)
            st.dataframe(filt[['customer_id','customer_status','risk_label','segment_2x2','tenure','contract','monthly_charges','satisfaction_score','total_revenue']].head(50), use_container_width=True, hide_index=True)
            st.caption(f"Showing {min(50,len(filt))} of {len(filt):,} customers")
