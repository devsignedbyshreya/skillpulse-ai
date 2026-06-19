import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from queries import *
from components import metric_card

import os
from dotenv import load_dotenv

load_dotenv()

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="SkillPulse AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# THEME  –  Deep navy + Indigo #6366F1
# =====================================

ACCENT       = "#6366F1"          # indigo
ACCENT_DIM   = "rgba(99,102,241,0.13)"
ACCENT_GLOW  = "rgba(99,102,241,0.35)"
ACCENT_BORDER= "rgba(99,102,241,0.28)"
ACCENT_HOVER = "#6366F1"
BG_BASE      = "#080C14"
BG_SURFACE   = "#0D1525"
BG_CARD      = "#131C30"
BG_SIDEBAR   = "#070B12"

st.markdown(f"""
<style>

/* ── Root tokens ── */
:root {{
    --bg-base:       {BG_BASE};
    --bg-surface:    {BG_SURFACE};
    --bg-card:       {BG_CARD};
    --bg-card-hover: #1A2540;
    --accent:        {ACCENT};
    --accent-dim:    {ACCENT_DIM};
    --accent-glow:   {ACCENT_GLOW};
    --accent-border: {ACCENT_BORDER};
    --green:         #10B981;
    --green-dim:     rgba(16,185,129,0.12);
    --text-primary:  #E8EAF0;
    --text-secondary:#8892A4;
    --text-muted:    #46506A;
    --border:        rgba(255,255,255,0.06);
    --radius:        6px;
    --font:          -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

/* ── Global ── */
html, body, .stApp {{
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {BG_SIDEBAR} !important;
    border-right: 1px solid var(--border) !important;
}}
/* nav radio pills */
[data-testid="stSidebar"] .stRadio > div {{
    gap: 2px !important;
}}
[data-testid="stSidebar"] .stRadio label {{
    color: var(--text-secondary) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 9px 14px !important;
    border-radius: var(--radius) !important;
    border: 1px solid transparent !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    cursor: pointer !important;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    color: var(--text-primary) !important;
    background: rgba(99,102,241,0.08) !important;
    border-color: var(--accent-border) !important;
}}
[data-testid="stSidebar"] .stRadio label[data-checked="true"],
[data-testid="stSidebar"] .stRadio input:checked + div {{
    color: var(--accent) !important;
    background: var(--accent-dim) !important;
    border-color: var(--accent-border) !important;
}}
/* hide default radio circles */
[data-testid="stSidebar"] .stRadio input {{ display: none !important; }}

/* ── Page headings ── */
h1 {{
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
    line-height: 1.25 !important;
}}
h2, h3 {{
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}

/* ── KPI cards ── */
.kpi-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent);
    border-radius: var(--radius);
    padding: 20px 22px;
    min-height: 100px;
}}
.kpi-label {{
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 8px;
}}
.kpi-value {{
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

/* ── Insight cards ── */
.insight-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
}}
.insight-row {{
    display: flex;
    justify-content: space-between;
    font-size: 0.875rem;
    border-bottom: 1px solid var(--border);
    padding: 8px 0;
}}
.insight-row:last-child {{ border-bottom: none; }}
.insight-key   {{ color: var(--text-secondary); font-weight: 500; }}
.insight-value {{ color: var(--text-primary);   font-weight: 600; }}

/* ── Section Header ───────────────────────────── */

.section-wrapper {{
    margin-top: 28px;
    margin-bottom: 24px;
}}

.section-title {{
    color: #F8FAFC;
    font-size: 1.65rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-bottom: 6px;
}}

.section-description {{
    color: #8892A4;
    font-size: 0.88rem;
    line-height: 1.5;
    margin-bottom: 14px;
}}

.section-divider {{
    height: 1px;
    background: rgba(255,255,255,0.08);
    width: 100%;
}}


/* ── Live status badge ── */
.status-bar {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--green-dim);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 0.79rem;
    font-weight: 500;
    color: var(--green);
    margin-bottom: 22px;
}}
.pulse-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    flex-shrink: 0;
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%   {{ box-shadow: 0 0 0 0   rgba(16,185,129,0.6); }}
    70%  {{ box-shadow: 0 0 0 6px rgba(16,185,129,0); }}
    100% {{ box-shadow: 0 0 0 0   rgba(16,185,129,0); }}
}}

/* ── Streamlit metric tiles ── */
[data-testid="stMetric"] {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 14px 18px !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    color: var(--text-muted) !important;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-variant-numeric: tabular-nums !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
}}
[data-testid="stSelectbox"] svg {{ color: var(--text-secondary) !important; }}

/* ── Text input ── */
[data-testid="stTextInput"] input {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    padding: 10px 14px !important;
    font-size: 0.9rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
}}

/* ── Primary button ── */
.stButton > button {{
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 8px 20px !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.02em !important;
}}
.stButton > button:hover {{
    background: {ACCENT_HOVER} !important;
    box-shadow: 0 0 14px var(--accent-glow) !important;
    transform: translateY(-1px) !important;
}}
/* Secondary / clear button */
.stButton > button[kind="secondary"] {{
    background: var(--bg-card) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
}}
.stButton > button[kind="secondary"]:hover {{
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    box-shadow: none !important;
    transform: none !important;
}}

/* ── Code block ── */
.stCodeBlock code {{
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-size: 0.82rem !important;
    color: #a5b4fc !important;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {ACCENT_BORDER} !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}}

/* ── Plotly chart blocks ── */
[data-testid="stPlotlyChart"] {{
    border: 1px solid rgba(99,102,241,0.40);
    border-radius: 12px;
    overflow: hidden;
    background: #0D1525;
    transition: all 0.2s ease;
}}

[data-testid="stPlotlyChart"]:hover{{
    border-color: #818CF8;
    box-shadow:
        0 0 0 1px rgba(129,140,248,0.35),
        0 0 30px rgba(129,140,248,0.25);
}}

/* ── Divider ── */
hr {{
    border-color: var(--border) !important;
    margin: 28px 0 !important;
}}

/* ── Alert / info ── */
.stAlert {{
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
}}
div[data-baseweb="notification"] {{
    background: var(--bg-card) !important;
}}

/* ── Chat bubbles ── */
.chat-block {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 22px;
    margin-bottom: 14px;
}}
.chat-user {{
    border-left: 3px solid #38BDF8;
    background: rgba(56,189,248,0.07);
}}
.chat-bot {{
    border-left: 3px solid var(--accent);
    background: var(--accent-dim);
}}
.chat-role {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
}}
.chat-role.user {{ color: #38BDF8; }}
.chat-role.bot  {{ color: var(--accent); }}
.chat-text      {{ font-size: 0.9rem; line-height: 1.6; color: var(--text-primary); }}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: var(--accent) !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg-base); }}
::-webkit-scrollbar-thumb {{ background: #1A2540; border-radius: 3px; }}

/* ── Download button ── */
.stDownloadButton > button {{
    background: var(--bg-card) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    font-size: 0.82rem !important;
}}
.stDownloadButton > button:hover {{
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}}

/* ── Caption ── */
[data-testid="stCaptionContainer"] {{
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
}}

/* Ask button alignment */
div[data-testid="column"]:last-child .stButton {{
    margin-top: 28px !important;
}}

div[data-testid="column"]:last-child .stButton button {{
    height: 46px !important;
}}
</style>
""", unsafe_allow_html=True)
# =====================================
# CHART THEME  –  Indigo palette
# =====================================

# All charts share indigo as primary; secondary shades keep visual coherence
PRIMARY_CHART_COLOR = "#6366F1"
HOVER_CHART_COLOR = "#818CF8"

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor=BG_SURFACE,
    plot_bgcolor=BG_SURFACE,
    font=dict(family="Inter, sans-serif", color="#8892A4", size=12),
    title_font=dict(family="Inter, sans-serif", color="#E8EAF0", size=13),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.07)",
        tickcolor="rgba(255,255,255,0.07)",
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.07)",
        tickcolor="rgba(255,255,255,0.07)",
        tickfont=dict(size=11),
    ),
    margin=dict(l=20, r=20, t=44, b=20),
    hoverlabel=dict(
        bgcolor="#1A2540",
        bordercolor="#818CF8",
        font_color="#FFFFFF",
        font_size=14
    ),
    bargap=0.3,
)

def styled_bar(df, x, y, title="", text=None, color=None, horizontal=False):
    """Consistently styled Plotly bar with indigo palette."""
    color = PRIMARY_CHART_COLOR
    kwargs = dict(
        x=y if horizontal else x,
        y=x if horizontal else y,
        orientation="h" if horizontal else "v",
        color_discrete_sequence=[color],
    )
    if text:
        kwargs["text"] = text
    fig = px.bar(df, **kwargs, title=title)
    fig.update_traces(
        marker=dict(
            color=PRIMARY_CHART_COLOR,
            line=dict(
                color="#818CF8",
                width=1
            )
        ),
        opacity=0.90,
        textfont=dict(
            size=10,
            color="#E8EAF0"
        ),
        textposition="outside" if not horizontal else "auto",
        hovertemplate=
            "<b>%{x}</b><br>" +
            "Value: %{y}<extra></extra>"
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="",
        legend_title_text=""
    )
    return fig

# =====================================
# HELPERS
# =====================================

def section(title, description=None):

    st.markdown(
        f"""
        <div class="section-wrapper">
            <div class="section-title">{title}</div>
            <div class="section-description">{description or ""}</div>
            <div class="section-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def kpi(label, value):
    st.markdown(
        f"""<div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{value}</div>
            </div>""",
        unsafe_allow_html=True,
    )

# =====================================
# LOAD DATA
# =====================================

@st.cache_data(
    ttl=60,
    show_spinner=False
)
def load_dashboard_data():
    return {
        "skills":        get_top_skills(),
        "roles":         get_top_roles(),
        "countries":     get_country_distribution(),
        "health":        get_pipeline_health(),
        "emerging":      get_emerging_skills(),
        "companies":     get_top_companies(),
        "skill_role":    get_skill_role_demand(),
        "company_skill": get_company_skill_demand(),
        "country_skill": get_country_skill_mapping(),
    }

loading_container = st.empty()

loading_container.markdown("""
<div style="
padding:12px 16px;
background:#0f2d3a;
border:1px solid #1e4d61;
border-radius:12px;
color:#22d3ee;
font-weight:600;
">
🔄 Updating live job market insights...
</div>
""", unsafe_allow_html=True)

data = load_dashboard_data()

loading_container.empty()
skills        = data["skills"]
roles         = data["roles"]
countries     = data["countries"]
health        = data["health"]
emerging      = data["emerging"]
companies     = data["companies"]
skill_role    = data["skill_role"]
company_skill = data["company_skill"]
country_skill = data["country_skill"]

skills["share_pct"] = (
    skills["job_count"] / skills["job_count"].sum() * 100
).round(1)

try:
    all_skills = get_all_skills()
except Exception:
    all_skills = skills

try:
    last_run = (
        pd.to_datetime(
            health.iloc[0]["last_run_time"],
            utc=True
        )
        .tz_convert("Asia/Kolkata")
        .strftime("%d %b %Y")
    )
except Exception:
    last_run = str(health.iloc[0]["last_run_time"])

# =====================================
# SIDEBAR
# =====================================


with st.sidebar:

    # ── Brand ──────────────────────────────────────────
    st.markdown(
        f"""<div style="padding:18px 4px 20px;border-bottom:1px solid rgba(255,255,255,0.06);
                        margin-bottom:0;">
                  <div style="font-size:1.05rem;font-weight:700;color:#E8EAF0;
                              letter-spacing:-0.01em;line-height:1.1;">
                    SkillPulse<span style="color:{ACCENT};"> AI</span>
                  </div>
                  <div style="font-size:0.62rem;color:#46506A;letter-spacing:0.09em;
                              text-transform:uppercase;margin-top:1px;">
                    job Market Intelligence
                  </div>
                </div>
              </div>
            </div>""",
        unsafe_allow_html=True,
    )

    # ── App summary ────────────────────────────────────
    st.markdown(
        f"""<div style="padding:16px 4px 16px;border-bottom:1px solid rgba(255,255,255,0.06);
                        margin-bottom:16px;">
              <p style="font-size:0.78rem;color:#8892A4;line-height:1.65;margin:0;">
                Real-time insights on job market trends track in-demand skills, top roles, hiring companies, 
                and emerging technologies across countries.
              </p>
              <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;">
                <span style="font-size:0.65rem;background:rgba(99,102,241,0.12);
                             border:1px solid {ACCENT_BORDER};border-radius:4px;
                             padding:3px 8px;color:{ACCENT};font-weight:600;">
                  ⚡ Live Data
                </span>
                <span style="font-size:0.65rem;background:rgba(16,185,129,0.1);
                             border:1px solid rgba(16,185,129,0.25);border-radius:4px;
                             padding:3px 8px;color:#10B981;font-weight:600;">
                  🤖 AI-Powered
                </span>
              </div>
            </div>""",
        unsafe_allow_html=True,
    )

    # ── Nav label ──────────────────────────────────────
    st.markdown(
        """<div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;
                       letter-spacing:0.12em;color:#46506A;padding:0 4px;margin-bottom:6px;">
             Navigation
           </div>""",
        unsafe_allow_html=True,
    )

    page = st.radio(
        "",
        [
            "📊  Dashboard",
            "📈  Observability",
            "🤖  AI Assistant"
        ],
        label_visibility="collapsed",
    )
    # normalise to plain names
    page = page.split("  ", 1)[1]

    # ── Stats strip ────────────────────────────────────
    try:
        job_count_fmt  = f"{int(health.iloc[0]['silver_job_count']):,}"
        skill_cnt      = int(health.iloc[0]['unique_skills'])
        country_cnt    = len(countries)
    except Exception:
        job_count_fmt = "—"
        skill_cnt     = "—"
        country_cnt   = "—"

    st.markdown(
        f"""<div style="margin-top:20px;padding:14px 10px;background:{BG_CARD};
                        border:1px solid rgba(255,255,255,0.06);border-radius:6px;">
              <div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;
                          letter-spacing:0.1em;color:#46506A;margin-bottom:10px;">
                Dataset Snapshot
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div>
                  <div style="font-size:1rem;font-weight:700;color:#E8EAF0;
                              font-variant-numeric:tabular-nums;">{job_count_fmt}</div>
                  <div style="font-size:0.65rem;color:#46506A;">Jobs</div>
                </div>
                <div>
                  <div style="font-size:1rem;font-weight:700;color:#E8EAF0;">{skill_cnt}</div>
                  <div style="font-size:0.65rem;color:#46506A;">Skills</div>
                </div>
                <div>
                  <div style="font-size:1rem;font-weight:700;color:#E8EAF0;">{country_cnt}</div>
                  <div style="font-size:0.65rem;color:#46506A;">Countries</div>
                </div>
                <div>
                  <div style="font-size:1rem;font-weight:700;color:{ACCENT};">Live</div>
                  <div style="font-size:0.65rem;color:#46506A;">Status</div>
                </div>
              </div>
            </div>""",
        unsafe_allow_html=True,
    )

    # ── Footer ─────────────────────────────────────────
    st.markdown(
        """
        <div style="margin-top:24px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.06);
                    font-size:0.85rem;color:#46506A;line-height:1.8;">
            Powered by
            <strong style="color:#FF3621;">Databricks</strong>
            &
            <strong style="color:#6366F1;">Adzuna</strong>
            <br>
        </div>
        """,
        unsafe_allow_html=True,
    )
# =====================================
# DASHBOARD
# =====================================

if page == "Dashboard":

    header_html = f"""
    <div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:6px;">
        <div>
            <h1 style="
                margin:0;
                font-size:4rem;
                font-weight:800;
                letter-spacing:-0.04em;
                line-height:1;
            ">
                SkillPulse<span style="color:{ACCENT};"> AI</span>
            </h1>
        </div>
    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)

    # ── Live status badge ───────────────────────────────
    st.markdown(
        f"""<div class="status-bar">
              <div class="pulse-dot"></div>
              Live · Refreshed {last_run}
              &nbsp;·&nbsp;
              {int(health.iloc[0]['silver_job_count']):,} jobs
              &nbsp;·&nbsp;
              {int(health.iloc[0]['unique_skills'])} skills
            </div>""",
        unsafe_allow_html=True,
    )

    # ── KPI row ─────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("Most Demanded Skill",  skills.iloc[0]["skill"])
    with c2:
        kpi("Top Hiring Company",   companies.iloc[0]["company"][:22])
    with c3:
        kpi("Most Active Role",     roles.iloc[0]["job_title"][:22])
    with c4:
        kpi("Jobs Analyzed",        f"{int(health.iloc[0]['silver_job_count']):,}")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Market Snapshot ─────────────────────────────────
    section(
        "Market Snapshot",
        "A quick overview of the most in-demand skills, roles, companies, and countries."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""<div class="insight-card">
                  <div class="insight-row">
                    <span class="insight-key">Top Skill</span>
                    <span class="insight-value">{skills.iloc[0]['skill']}</span>
                  </div>
                  <div class="insight-row">
                    <span class="insight-key">Top Role</span>
                    <span class="insight-value">{roles.iloc[0]['job_title']}</span>
                  </div>
                  <div class="insight-row">
                    <span class="insight-key">Top Company</span>
                    <span class="insight-value">{companies.iloc[0]['company']}</span>
                  </div>
                </div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""<div class="insight-card">
                  <div class="insight-row">
                    <span class="insight-key">Top Country</span>
                    <span class="insight-value">{countries.iloc[0]['country']}</span>
                  </div>
                  <div class="insight-row">
                    <span class="insight-key">Fastest Emerging Skill</span>
                    <span class="insight-value">{emerging.iloc[0]['skill']}</span>
                  </div>
                  <div class="insight-row">
                    <span class="insight-key">Skills Tracked</span>
                    <span class="insight-value">{int(health.iloc[0]['unique_skills'])}</span>
                  </div>
                </div>""",
            unsafe_allow_html=True,
        )

    # ── Dataset Summary ──────────────────────────────────
    section(
        "Dataset Summary",
        "Key metrics from the latest pipeline run and processed job market data."
    )
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Jobs Analyzed",    int(health.iloc[0]["silver_job_count"]))
    d2.metric("Skills Extracted", int(health.iloc[0]["extracted_skills"]))
    d3.metric("Unique Skills",    int(health.iloc[0]["unique_skills"]))
    d4.metric("Countries",        len(countries))

    # ── Top Skills / Roles ───────────────────────────────
    section(
        "Top Skills & Roles",
        "Discover the skills and job roles with the highest demand across the market."
    )
    col1, col2 = st.columns(2)
    with col1:
        fig = styled_bar(
            skills.head(10), x="skill", y="job_count",
            title="Top 10 In-Demand Skills", color=PRIMARY_CHART_COLOR,
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = styled_bar(
            roles.head(10), x="job_title", y="job_count",
            title="Top 10 Job Roles", color=PRIMARY_CHART_COLOR,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Top Companies ────────────────────────────────────
    section(
        "Top Hiring Companies",
        "Organizations posting the highest number of job opportunities."
    )
    fig = styled_bar(
        companies.head(10), x="company", y="job_count",
        title="Companies by Job Volume", color=PRIMARY_CHART_COLOR,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Country Explorer ─────────────────────────────────
    section(
        "Country Explorer",
        "Analyze hiring demand and skill trends across different countries."
    )
    col_sel, _ = st.columns([2, 5])
    with col_sel:
        selected_country = st.selectbox(
            "Country",
            sorted(country_skill["country"].dropna().unique()),
            label_visibility="collapsed",
        )
    country_df = (
        country_skill[country_skill["country"] == selected_country]
        .sort_values("skill_demand", ascending=False)
        .head(10)
    )
    fig = styled_bar(
        country_df, x="skill", y="skill_demand",
        title=f"Top Skills · {selected_country}", color=PRIMARY_CHART_COLOR,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Role Explorer ────────────────────────────────────
    section(
        "Role Explorer",
        "Explore which skills are most frequently requested for specific job roles."
    )
    role_list = sorted(skill_role["job_title"].dropna().astype(str).unique())
    col_sel, _ = st.columns([3, 4])
    with col_sel:
        selected_role = st.selectbox("Role", role_list, label_visibility="collapsed")
    role_df = (
        skill_role[skill_role["job_title"] == selected_role]
        .sort_values("job_count", ascending=False)
        .head(10)
    )
    fig = styled_bar(
        role_df, x="skill", y="job_count",
        title=f"Skills Required · {selected_role}", color=PRIMARY_CHART_COLOR,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Company Explorer ─────────────────────────────────
    section(
        "Company Explorer",
        "View the most sought-after skills for individual companies."
    )
    company_list = sorted(company_skill["company"].dropna().astype(str).unique())
    col_sel, _ = st.columns([3, 4])
    with col_sel:
        selected_company = st.selectbox("Company", company_list, label_visibility="collapsed")
    company_df = (
        company_skill[company_skill["company"] == selected_company]
        .sort_values("job_count", ascending=False)
        .head(10)
    )
    fig = styled_bar(
        company_df, x="skill", y="job_count",
        title=f"Skills Wanted By · {selected_company}", color=PRIMARY_CHART_COLOR,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Skill Explorer ───────────────────────────────────
    section(
        "Skill Explorer",
        "Drill into demand, ranking, and market share for any skill."
    )
    skill_options = sorted(all_skills["skill"].dropna().astype(str).unique())
    col_sel, _ = st.columns([2, 5])
    with col_sel:
        selected_skill = st.selectbox("Skill", skill_options, label_visibility="collapsed")

    skill_info = all_skills[all_skills["skill"] == selected_skill]
    rank_df = (
        skills.sort_values("job_count", ascending=False).reset_index(drop=True)
    )
    rank_df["rank"] = rank_df.index + 1
    try:
        skill_rank = rank_df[rank_df["skill"] == selected_skill]["rank"].iloc[0]
        rank_str = f"#{skill_rank}"
    except IndexError:
        rank_str = "—"

    s1, s2, s3, _ = st.columns([1, 1, 1, 3])
    with s1:
        st.metric("Current Demand", int(skill_info.iloc[0]["job_count"]))
    with s2:
        st.metric("Demand Rank",    rank_str)
    with s3:

        if "share_pct" in skill_info.columns:
            share = skill_info.iloc[0]["share_pct"]
        else:
            share = round(
                skill_info.iloc[0]["job_count"]
                / all_skills["job_count"].sum()
                * 100,
                1
            )

        st.metric(
            "Market Share",
            f"{share}%"
        )

    # ── Emerging Skills ──────────────────────────────────
    section(
        "Fastest Growing Skills",
        "Identify emerging technologies and skills experiencing the highest growth."
    )

    emerging_chart = emerging.sort_values(
        "pct_change",
        ascending=False
    )

    fig = styled_bar(
        emerging_chart.head(10),
        x="skill",
        y="pct_change",
        title="Fastest Growing Skills (%)",
        color=PRIMARY_CHART_COLOR,
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ── Hiring Demand by Country ─────────────────────────
    section(
        "Hiring Demand by Country",
        "Compare job volume and hiring activity across regions."
    )
    fig = styled_bar(
        countries, x="country", y="job_count",
        title="Job Volume by Country", color=PRIMARY_CHART_COLOR,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Pipeline Health ──────────────────────────────────
    section(
        "Pipeline Health",
        "Monitor ingestion, transformation, and skill extraction performance."
    )
    row = health.iloc[0]
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Jobs Processed",   int(row["silver_job_count"]))
    h2.metric("Skills Extracted", int(row["extracted_skills"]))
    h3.metric("Unique Skills",    int(row["unique_skills"]))
    h4.metric("Last Refresh",     last_run)


elif page == "Observability":

    st.markdown(
        f"""
        <h1 style="
            font-size:3rem;
            font-weight:800;
            margin-bottom:0;
        ">
            Observability <span style="color:{ACCENT};">Center</span>
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color:#8892A4;
            font-size:1rem;
            margin-top:-10px;
            margin-bottom:25px;
        ">
            Monitor pipeline health, data quality, drift detection, and operational alerts across the SkillPulse platform.
        </div>
        """,
        unsafe_allow_html=True
    )

    alerts = get_alerts()

    alerts_display = alerts.rename(
        columns={
            "alert_time": "Time",
            "alert_type": "Alert",
            "severity": "Severity",
            "message": "Description"
        }
    )

    section(
        "Active Alerts",
        "Real-time monitoring alerts generated by the pipeline."
    )

    if alerts.empty:

        st.success(
            "No active alerts"
        )

    else:

        def color_severity(val):

            if val == "CRITICAL":
                return "background-color:#ff4b4b"

            elif val == "WARNING":
                return "background-color:#ffa500"

            elif val == "INFO":
                return "background-color:#1f77b4"

            return ""

        st.dataframe(
            alerts.style.map(
                color_severity,
                subset=["severity"]
            ),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---", unsafe_allow_html=True)


    pipeline_history = get_pipeline_history()

    latest = pipeline_history.iloc[-1]

    c1, c2, c3, c4 , c5 = st.columns(5)

    c1.metric(
        "Bronze Jobs",
        f"{latest['bronze_jobs']:,}"
    )

    c2.metric(
        "Silver Jobs",
        f"{latest['silver_jobs']:,}"
    )

    c3.metric(
        "Extracted Skills",
        f"{latest['extracted_skills']:,}"
    )

    c4.metric(
        "Unique Skills",
        f"{latest['unique_skills']:,}"
    )

    if latest["bronze_jobs"] == latest["silver_jobs"]:

        c5.metric(
            "Pipeline Status",
            "Healthy"
        )

    else:

        c5.metric(
            "Pipeline Status",
            "Issue"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    section(
        "Pipeline Health Trend",
        "Track processed job volumes over time and monitor pipeline stability."
    )
    
    fig = px.line(
        pipeline_history,
        x="run_date",
        y=[
            "bronze_jobs",
            "silver_jobs"
        ],
        markers=True
    )

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="",
        legend_title_text=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section(
        "Pipeline Metrics History",
        "Historical record of pipeline execution metrics, including jobs processed and skills extracted."
    )

    st.dataframe(
        pipeline_history,
        use_container_width=True
    )

    skill_history = get_skill_snapshot_history()

    section(
        "Skill Demand Trends",
        "Monitor how demand for individual skills changes across daily snapshots."
    )

    fig = px.line(
        skill_history,
        x="snapshot_date",
        y="job_count",
        color="skill",
        markers=True
    )

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="",
        legend_title_text=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    skill_drift = run_query("""
    WITH skill_daily AS (
        SELECT
            snapshot_date,
            skill,
            job_count,
            LAG(job_count)
            OVER (
                PARTITION BY skill
                ORDER BY snapshot_date
            ) AS prev_count
        FROM skillpulse.gold.gold_skill_daily_snapshot
    )

    SELECT
        skill,
        snapshot_date,
        job_count,
        prev_count,
        ROUND(
            (
                (job_count - prev_count)
                * 100.0
            ) / NULLIF(prev_count,0),
            2
        ) AS pct_change
    FROM skill_daily
    WHERE prev_count IS NOT NULL
    ORDER BY ABS(pct_change) DESC
    LIMIT 20
    """)

    section(
        "Skill Drift Detection",
        "Detect significant changes in skill demand compared to previous pipeline runs."
    )

    drift_display = (
        skill_drift[
            [
                "skill",
                "prev_count",
                "job_count",
                "pct_change"
            ]
        ]
        .rename(
            columns={
                "prev_count": "Previous Count",
                "job_count": "Current Count",
                "pct_change": "% Change"
            }
        )
    )

    st.dataframe(
        drift_display,
        use_container_width=True,
        hide_index=True
    )

    delta_bronze = (
        latest["bronze_jobs"]
        - pipeline_history.iloc[-2]["bronze_jobs"]
    )

    delta_skills = (
        latest["extracted_skills"]
        - pipeline_history.iloc[-2]["extracted_skills"]
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Daily Job Change",
        f"{delta_bronze:+}"
    )

    c2.metric(
        "Daily Skill Change",
        f"{delta_skills:+}"
    )

    section(
        "Emerging Skills",
        "Identify rapidly growing skills with the highest increase in market demand."
    )

    emerging_df = get_emerging_skills()

    emerging_display = (
        emerging_df.rename(
            columns={
                "job_count": "Current Count",
                "prev_count": "Previous Count",
                "pct_change": "% Change"
            }
        )
    )

    st.dataframe(
        emerging_display,
        use_container_width=True,
        hide_index=True
    )

    section(
        "Lakehouse Monitor Status",
        "Current status of Databricks Lakehouse Monitoring, profiling, and drift detection."
    )

    st.success(
        "Bronze Lakehouse Monitor Active | Profile Metrics Available | Drift Tracking Enabled"
    )

    st.info(
        "Profile Metrics Available. Drift metrics will populate as additional historical windows accumulate."
    )

# =====================================
# AI ASSISTANT
# =====================================

elif page == "AI Assistant":

    from genie import ask_genie

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ── Header ───────────────────────────────────────────
    title_col, btn_col = st.columns([6, 1])

    with title_col:
        st.markdown(
            f"""
            <h1 style="
                font-size:3.2rem;
                font-weight:800;
                margin-bottom:0;
                letter-spacing:-0.04em;
            ">
                SkillPulse <span style="color:{ACCENT};">Assistant</span>
            </h1>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "Ask anything about skills, roles, companies, and job market trends. Backed by live job market data."
        )
    with btn_col:
        st.write("")
        st.write("")

        if st.button(
            "Clear Chat",
            type="secondary",
            use_container_width=True
        ):
            st.session_state.chat_history = []
            st.rerun()

    # ── Example prompts ──────────────────────────────────
    section(
        "Example Questions",
        "Try these sample prompts to explore the job market using natural language."
    )
    ex_cols = st.columns(2)
    examples_left  = [
        "Show me the top roles",
        "Which companies hire ML Engineers?",
        "Top skills in Australia",
        "Compare SQL and Python demand",
    ]
    examples_right = [
        "Show me the top skills",
        "Show hiring demand by country",
        "Skills required for Data Engineer roles",
        "Fastest growing skills this month",
    ]
    for col, examples in zip(ex_cols, [examples_left, examples_right]):
        with col:
            for ex in examples:
                st.markdown(
                    f"""<div style="background:{BG_CARD};
                                   border:1px solid rgba(255,255,255,0.06);
                                   border-radius:5px;padding:8px 14px;margin-bottom:7px;
                                   font-size:0.82rem;color:#8892A4;font-family:monospace;
                                   transition:border-color 0.15s;">
                           {ex}
                         </div>""",
                    unsafe_allow_html=True,
                )

    # ── Input ────────────────────────────────────────────
    section(
        "Ask a Question",
        "Ask anything about skills, companies, countries, or hiring trends."
    )

    q_col, btn_col = st.columns([6, 1])

    with q_col:
        question = st.text_input(
            "",
            placeholder="e.g. Which skills are growing fastest in Germany?",
            label_visibility="collapsed",
        )

    with btn_col:
        ask_clicked = st.button(
            "Ask →",
            use_container_width=True
        )

    if ask_clicked and question:
        with st.spinner("Analyzing job market data…"):
            result    = ask_genie(question)
            answer    = result["answer"]
            sql_query = result["sql"]
            chart_df  = None

            if sql_query:
                try:
                    chart_df = run_query(sql_query)
                except Exception as e:
                    st.warning(f"Visualization unavailable: {e}")

            st.session_state.chat_history.append(
                {"question": question, "answer": answer, "data": chart_df}
            )

    # ── Conversation history ─────────────────────────────
    if st.session_state.chat_history:
        section(
            "Conversation",
            "Review your previous questions and generated insights."
        )

        for chat in reversed(st.session_state.chat_history):
            st.markdown(
                f"""<div class="chat-block chat-user">
                      <div class="chat-role user">You</div>
                      <div class="chat-text">{chat['question']}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""<div class="chat-block chat-bot">
                      <div class="chat-role bot">SkillPulse AI</div>
                      <div class="chat-text">{chat['answer']}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

            if chat["data"] is not None:
                df = chat["data"]
                st.dataframe(df, use_container_width=True)

                if len(df.columns) >= 2 and len(df) > 0:
                    try:
                        fig = styled_bar(
                            df.head(10),
                            x=df.columns[0],
                            y=df.columns[1],
                            title=chat["question"],
                            text=df.columns[1],
                            color=PRIMARY_CHART_COLOR,
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        pass

        # ── Export ───────────────────────────────────────
        chat_export = "\n\n".join(
            f"Q: {x['question']}\nA: {x['answer']}"
            for x in st.session_state.chat_history
        )
        st.download_button(
            "📥 Export Conversation",
            chat_export,
            "skillpulse_chat.txt",
        )