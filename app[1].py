"""
Client Portfolio Reporting Tool
Author: Mustafa Hussain
Description: Automated portfolio performance reporting dashboard for institutional clients.
             Generates AUM breakdowns, benchmark comparisons, and client-level analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BlackRock | Client Portfolio Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .stApp {
        background: #0a0e1a;
        color: #e8eaf0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0d1220;
        border-right: 1px solid #1e2a40;
    }

    /* Header banner */
    .header-banner {
        background: linear-gradient(135deg, #0d1220 0%, #0f2040 50%, #0a1830 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 28px 36px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header-title {
        font-size: 26px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.3px;
        margin: 0;
    }

    .header-sub {
        font-size: 13px;
        color: #5a7a9a;
        margin-top: 4px;
        font-family: 'IBM Plex Mono', monospace;
    }

    .br-badge {
        background: #ff0000;
        color: white;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 1.5px;
    }

    /* Metric cards */
    .metric-card {
        background: #0d1628;
        border: 1px solid #1e2e45;
        border-radius: 10px;
        padding: 22px 24px;
        transition: border-color 0.2s;
    }

    .metric-card:hover {
        border-color: #2e5080;
    }

    .metric-label {
        font-size: 11px;
        font-weight: 500;
        color: #4a6a8a;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 10px;
        font-family: 'IBM Plex Mono', monospace;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: #e8eaf0;
        line-height: 1;
    }

    .metric-delta {
        font-size: 12px;
        margin-top: 8px;
        font-family: 'IBM Plex Mono', monospace;
    }

    .positive { color: #00c896; }
    .negative { color: #ff5252; }
    .neutral  { color: #5a7a9a; }

    /* Section headers */
    .section-header {
        font-size: 13px;
        font-weight: 500;
        color: #4a6a8a;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding-bottom: 10px;
        border-bottom: 1px solid #1e2e45;
        margin-bottom: 18px;
        font-family: 'IBM Plex Mono', monospace;
    }

    /* Table styling */
    .stDataFrame {
        border: 1px solid #1e2e45 !important;
        border-radius: 8px;
    }

    /* Insight box */
    .insight-box {
        background: #091525;
        border-left: 3px solid #0050a0;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 13.5px;
        color: #8aaecc;
        line-height: 1.6;
    }

    /* Chart container */
    .chart-container {
        background: #0d1628;
        border: 1px solid #1e2e45;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* Tag pill */
    .tag-pill {
        display: inline-block;
        background: #0f2040;
        border: 1px solid #1e3a5f;
        color: #4a9ade;
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 6px;
        font-family: 'IBM Plex Mono', monospace;
    }

    /* Divider */
    hr { border-color: #1e2e45 !important; }

    /* Streamlit overrides */
    .stSelectbox > div > div { background: #0d1628; border-color: #1e2e45; color: #e8eaf0; }
    .stMultiSelect > div > div { background: #0d1628; border-color: #1e2e45; }
    label { color: #8aaecc !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/portfolio_data.csv", parse_dates=["Date"])
    df["Excess_Return"] = df["Daily_Return"] - df["Benchmark_Return"]
    df["Active_Gain_Loss"] = df["AUM"] * df["Excess_Return"]
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# ─────────────────────────────────────────────
#  SIDEBAR — FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 24px 0;'>
        <span style='font-size:18px; font-weight:600; color:#e8eaf0;'>⚡ Portfolio Analytics</span><br>
        <span style='font-size:11px; color:#4a6a8a; font-family: IBM Plex Mono;'>CLIENT REPORTING SUITE v2.1</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">FILTERS</div>', unsafe_allow_html=True)

    all_clients = sorted(df["Client"].unique().tolist())
    selected_clients = st.multiselect(
        "Client Account", all_clients, default=all_clients,
        help="Select one or more institutional clients"
    )

    all_assets = sorted(df["Asset_Class"].unique().tolist())
    selected_assets = st.multiselect(
        "Asset Class", all_assets, default=all_assets
    )

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max
    )

    st.markdown("---")
    st.markdown('<div class="section-header">REPORT</div>', unsafe_allow_html=True)
    report_mode = st.radio(
        "View Mode",
        ["Executive Summary", "Client Deep Dive", "Fund Analytics"],
        index=0
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#2e4560; font-family: IBM Plex Mono; line-height: 1.7;'>
    DATA: iShares ETF Universe<br>
    PERIOD: Jan 2024<br>
    CURRENCY: USD<br>
    BUILD: Mustafa Hussain
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FILTER DATA
# ─────────────────────────────────────────────
if len(date_range) == 2:
    start_d, end_d = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_d, end_d = df["Date"].min(), df["Date"].max()

if not selected_clients:
    selected_clients = all_clients
if not selected_assets:
    selected_assets = all_assets

fdf = df[
    df["Client"].isin(selected_clients) &
    df["Asset_Class"].isin(selected_assets) &
    (df["Date"] >= start_d) &
    (df["Date"] <= end_d)
].copy()

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <div>
        <div class="header-title">Client Portfolio Reporting Dashboard</div>
        <div class="header-sub">INSTITUTIONAL CLIENT SERVICES  ·  iSHARES ETF PLATFORM  ·  LIVE ANALYTICS</div>
    </div>
    <div class="br-badge">BLACKROCK</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPI METRICS
# ─────────────────────────────────────────────
total_aum    = fdf.groupby(["Client","Fund","Date"])["AUM"].last().groupby(["Client","Fund"]).last().sum()
total_return = (fdf["Daily_Return"] * fdf["AUM"]).sum() / fdf["AUM"].sum() * 100
bench_return = (fdf["Benchmark_Return"] * fdf["AUM"]).sum() / fdf["AUM"].sum() * 100
alpha        = total_return - bench_return
num_funds    = fdf["Fund"].nunique()
num_clients  = fdf["Client"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

for col, label, val, delta, is_pct in zip(
    [col1, col2, col3, col4, col5],
    ["TOTAL AUM", "PORTFOLIO RETURN", "BENCHMARK RETURN", "ACTIVE ALPHA", "ACTIVE FUNDS"],
    [f"${total_aum/1e6:.1f}M", f"{total_return:.3f}%", f"{bench_return:.3f}%", f"{alpha:+.4f}%", str(num_funds)],
    [f"{num_clients} clients", "Weighted avg", "vs S&P 500 proxy", "Outperforming" if alpha > 0 else "Underperforming", f"{num_clients} clients"],
    [False, True, True, True, False]
):
    sign_class = "positive" if (is_pct and alpha > 0) else ("negative" if (is_pct and alpha < 0) else "neutral")
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{val}</div>
        <div class="metric-delta {sign_class}">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHARTS ROW 1
# ─────────────────────────────────────────────
chart_col1, chart_col2 = st.columns([3, 2])

with chart_col1:
    st.markdown('<div class="section-header">AUM TREND BY CLIENT</div>', unsafe_allow_html=True)
    aum_trend = (
        fdf.groupby(["Date", "Client"])["AUM"]
        .sum().reset_index()
    )
    fig_trend = px.area(
        aum_trend, x="Date", y="AUM", color="Client",
        color_discrete_sequence=["#0066cc", "#00aaff", "#0033aa"],
        template="plotly_dark"
    )
    fig_trend.update_layout(
        paper_bgcolor="#0d1628", plot_bgcolor="#0d1628",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(font=dict(color="#8aaecc", size=11), bgcolor="rgba(0,0,0,0)"),
        yaxis=dict(tickprefix="$", tickformat=".2s", gridcolor="#1e2e45", color="#5a7a9a"),
        xaxis=dict(gridcolor="#1e2e45", color="#5a7a9a"),
        height=300,
        hovermode="x unified",
        font=dict(family="IBM Plex Mono")
    )
    fig_trend.update_traces(line_width=2)
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.markdown('<div class="section-header">AUM BY ASSET CLASS</div>', unsafe_allow_html=True)
    asset_aum = fdf.groupby("Asset_Class")["AUM"].sum().reset_index()
    fig_pie = px.pie(
        asset_aum, values="AUM", names="Asset_Class",
        color_discrete_sequence=["#0066cc", "#0099ff", "#003388"],
        template="plotly_dark", hole=0.6
    )
    fig_pie.update_layout(
        paper_bgcolor="#0d1628", plot_bgcolor="#0d1628",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(font=dict(color="#8aaecc", size=11), bgcolor="rgba(0,0,0,0)"),
        height=300,
        font=dict(family="IBM Plex Mono")
    )
    fig_pie.update_traces(textfont_color="white", textfont_size=12)
    st.plotly_chart(fig_pie, use_container_width=True)

# ─────────────────────────────────────────────
#  CHARTS ROW 2 — PERFORMANCE vs BENCHMARK
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">PORTFOLIO vs BENCHMARK — DAILY RETURN ANALYSIS</div>', unsafe_allow_html=True)

perf_chart_col1, perf_chart_col2 = st.columns([3, 2])

with perf_chart_col1:
    daily_perf = (
        fdf.groupby("Date").apply(
            lambda x: pd.Series({
                "Portfolio_Return": (x["Daily_Return"] * x["AUM"]).sum() / x["AUM"].sum() * 100,
                "Benchmark_Return": (x["Benchmark_Return"] * x["AUM"]).sum() / x["AUM"].sum() * 100
            })
        ).reset_index()
    )
    daily_perf["Alpha"] = daily_perf["Portfolio_Return"] - daily_perf["Benchmark_Return"]

    fig_perf = go.Figure()
    fig_perf.add_trace(go.Scatter(
        x=daily_perf["Date"], y=daily_perf["Portfolio_Return"],
        name="Portfolio", line=dict(color="#0099ff", width=2.5),
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_perf.add_trace(go.Scatter(
        x=daily_perf["Date"], y=daily_perf["Benchmark_Return"],
        name="Benchmark", line=dict(color="#ff6600", width=2, dash="dot"),
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_perf.add_trace(go.Bar(
        x=daily_perf["Date"], y=daily_perf["Alpha"],
        name="Alpha", marker_color=["#00c896" if v > 0 else "#ff5252" for v in daily_perf["Alpha"]],
        opacity=0.6, yaxis="y2"
    ))
    fig_perf.update_layout(
        paper_bgcolor="#0d1628", plot_bgcolor="#0d1628",
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(title="Return (%)", gridcolor="#1e2e45", color="#5a7a9a", tickformat=".3f"),
        yaxis2=dict(title="Alpha (%)", overlaying="y", side="right", color="#5a7a9a", showgrid=False),
        xaxis=dict(gridcolor="#1e2e45", color="#5a7a9a"),
        legend=dict(font=dict(color="#8aaecc", size=11), bgcolor="rgba(0,0,0,0)"),
        height=300,
        font=dict(family="IBM Plex Mono", color="#8aaecc"),
        hovermode="x unified"
    )
    st.plotly_chart(fig_perf, use_container_width=True)

with perf_chart_col2:
    st.markdown('<div class="section-header">FUND PERFORMANCE SUMMARY</div>', unsafe_allow_html=True)
    fund_perf = (
        fdf.groupby("Fund").apply(lambda x: pd.Series({
            "Avg Return (%)": round((x["Daily_Return"] * x["AUM"]).sum() / x["AUM"].sum() * 100, 4),
            "Alpha (%)": round(((x["Daily_Return"] - x["Benchmark_Return"]) * x["AUM"]).sum() / x["AUM"].sum() * 100, 4),
            "AUM ($M)": round(x.groupby("Date")["AUM"].sum().iloc[-1] / 1e6, 2)
        }))
        .reset_index()
        .sort_values("AUM ($M)", ascending=False)
    )
    fund_perf["Fund"] = fund_perf["Fund"].str.replace("iShares ", "", regex=False)

    fig_bar = px.bar(
        fund_perf, x="Alpha (%)", y="Fund", orientation="h",
        color="Alpha (%)",
        color_continuous_scale=[[0, "#ff5252"], [0.5, "#1e2e45"], [1, "#00c896"]],
        template="plotly_dark"
    )
    fig_bar.update_layout(
        paper_bgcolor="#0d1628", plot_bgcolor="#0d1628",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#1e2e45", color="#5a7a9a"),
        yaxis=dict(color="#8aaecc", tickfont=dict(size=10)),
        coloraxis_showscale=False,
        height=300,
        font=dict(family="IBM Plex Mono")
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
#  CLIENT BREAKDOWN TABLE
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">CLIENT ACCOUNT SUMMARY</div>', unsafe_allow_html=True)

client_summary = (
    fdf.groupby("Client").apply(lambda x: pd.Series({
        "AUM ($M)": round(x.groupby("Date")["AUM"].sum().iloc[-1] / 1e6, 2),
        "Funds Held": x["Fund"].nunique(),
        "Asset Classes": ", ".join(sorted(x["Asset_Class"].unique())),
        "Avg Daily Return (%)": round((x["Daily_Return"] * x["AUM"]).sum() / x["AUM"].sum() * 100, 4),
        "Avg Benchmark (%)": round((x["Benchmark_Return"] * x["AUM"]).sum() / x["AUM"].sum() * 100, 4),
        "Active Alpha (%)": round(((x["Daily_Return"] - x["Benchmark_Return"]) * x["AUM"]).sum() / x["AUM"].sum() * 100, 4)
    }))
    .reset_index()
    .sort_values("AUM ($M)", ascending=False)
)

def style_alpha(val):
    if isinstance(val, float):
        color = "#00c896" if val > 0 else "#ff5252" if val < 0 else "#8aaecc"
        return f"color: {color}; font-weight: 500"
    return ""

styled = (
    client_summary.style
    .applymap(style_alpha, subset=["Active Alpha (%)"])
    .format({"AUM ($M)": "${:,.2f}M", "Avg Daily Return (%)": "{:.4f}%",
             "Avg Benchmark (%)": "{:.4f}%", "Active Alpha (%)": "{:+.4f}%"})
    .set_properties(**{"background-color": "#0d1628", "color": "#e8eaf0",
                        "border": "1px solid #1e2e45", "font-family": "IBM Plex Mono",
                        "font-size": "13px"})
    .set_table_styles([{"selector": "th", "props": [
        ("background-color", "#091525"), ("color", "#4a6a8a"),
        ("font-size", "11px"), ("text-transform", "uppercase"),
        ("letter-spacing", "1px"), ("border", "1px solid #1e2e45")
    ]}])
)
st.dataframe(client_summary, use_container_width=True)

# ─────────────────────────────────────────────
#  ANALYST INSIGHTS
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-header">AUTOMATED ANALYST INSIGHTS</div>', unsafe_allow_html=True)

best_client = client_summary.loc[client_summary["Active Alpha (%)"].idxmax(), "Client"]
best_alpha  = client_summary["Active Alpha (%)"].max()
worst_fund  = fund_perf.loc[fund_perf["Alpha (%)"].idxmin(), "Fund"]

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown(f"""
    <div class="insight-box">
        🏆 <strong>Top Performing Client:</strong> {best_client} is generating the highest active alpha
        at <strong style="color:#00c896">{best_alpha:+.4f}%</strong> above benchmark on an AUM-weighted basis.
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    equity_aum = fdf[fdf["Asset_Class"]=="Equity"]["AUM"].sum()
    total_a = fdf["AUM"].sum()
    st.markdown(f"""
    <div class="insight-box">
        📊 <strong>Equity Concentration:</strong> Equity holdings represent
        <strong style="color:#0099ff">{equity_aum/total_a*100:.1f}%</strong> of total AUM across all client
        portfolios — above the 60% typical institutional threshold.
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    days_positive = (daily_perf["Alpha"] > 0).sum()
    total_days = len(daily_perf)
    st.markdown(f"""
    <div class="insight-box">
        📈 <strong>Batting Average:</strong> Portfolios outperformed benchmark on
        <strong style="color:#00c896">{days_positive}/{total_days} trading days</strong>
        ({days_positive/total_days*100:.0f}% hit rate) — indicating consistent active management value.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color: #2e4560; font-size: 11px; font-family: IBM Plex Mono; padding: 12px 0;'>
    CLIENT PORTFOLIO REPORTING TOOL  ·  BUILT BY MUSTAFA HUSSAIN  ·  MS BUSINESS ANALYTICS · ST. FRANCIS COLLEGE  ·  2024
    <br><br>
    <span class='tag-pill'>Python</span>
    <span class='tag-pill'>Streamlit</span>
    <span class='tag-pill'>Plotly</span>
    <span class='tag-pill'>Pandas</span>
    <span class='tag-pill'>iShares ETF Data</span>
    <span class='tag-pill'>Portfolio Analytics</span>
</div>
""", unsafe_allow_html=True)
