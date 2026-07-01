"""
style.py
--------
Custom CSS injected into the Streamlit app for a modern,
finance-dashboard look: rounded cards, soft shadows, and a
clean color palette.
"""

CUSTOM_CSS = """
<style>
    :root {
        --ft-bg: #f5f7fb;
        --ft-card: #ffffff;
        --ft-text: #111827;
        --ft-muted: #6b7280;
        --ft-border: #eef0f4;
        --ft-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
        --ft-sidebar-bg: #111827;
        --ft-sidebar-text: #e5e7eb;
        --ft-sidebar-sub: #9ca3af;
        --ft-button-bg: #3b82f6;
        --ft-button-hover: #2563eb;
        --ft-button-text: #ffffff;
        --ft-input-bg: #ffffff;
        --ft-input-border: #d1d5db;
        --ft-budget-ok-bg: #ecfdf5;
        --ft-budget-ok-border: #10b981;
        --ft-budget-ok-text: #065f46;
        --ft-budget-warn-bg: #fffbeb;
        --ft-budget-warn-border: #f59e0b;
        --ft-budget-warn-text: #92400e;
        --ft-budget-danger-bg: #fef2f2;
        --ft-budget-danger-border: #ef4444;
        --ft-budget-danger-text: #991b1b;
    }

    html[data-theme="dark"], body[data-theme="dark"] {
        --ft-bg: #0f172a;
        --ft-card: #111827;
        --ft-text: #f8fafc;
        --ft-muted: #94a3b8;
        --ft-border: #1f2937;
        --ft-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
        --ft-sidebar-bg: #0b1120;
        --ft-sidebar-text: #f8fafc;
        --ft-sidebar-sub: #94a3b8;
        --ft-button-bg: #2563eb;
        --ft-button-hover: #1d4ed8;
        --ft-button-text: #ffffff;
        --ft-input-bg: #111827;
        --ft-input-border: #334155;
        --ft-budget-ok-bg: #0f766e33;
        --ft-budget-ok-border: #14b8a6;
        --ft-budget-ok-text: #d1fae5;
        --ft-budget-warn-bg: #78350f33;
        --ft-budget-warn-border: #f59e0b;
        --ft-budget-warn-text: #fde68a;
        --ft-budget-danger-bg: #7f1d1d33;
        --ft-budget-danger-border: #ef4444;
        --ft-budget-danger-text: #fecaca;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --ft-bg: #0f172a;
            --ft-card: #111827;
            --ft-text: #f8fafc;
            --ft-muted: #94a3b8;
            --ft-border: #1f2937;
            --ft-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
            --ft-sidebar-bg: #0b1120;
            --ft-sidebar-text: #f8fafc;
            --ft-sidebar-sub: #94a3b8;
            --ft-button-bg: #2563eb;
            --ft-button-hover: #1d4ed8;
            --ft-button-text: #ffffff;
            --ft-input-bg: #111827;
            --ft-input-border: #334155;
            --ft-budget-ok-bg: #0f766e33;
            --ft-budget-ok-border: #14b8a6;
            --ft-budget-ok-text: #d1fae5;
            --ft-budget-warn-bg: #78350f33;
            --ft-budget-warn-border: #f59e0b;
            --ft-budget-warn-text: #fde68a;
            --ft-budget-danger-bg: #7f1d1d33;
            --ft-budget-danger-border: #ef4444;
            --ft-budget-danger-text: #fecaca;
        }
    }

    /* ---------- Global ---------- */
    .stApp {
        background-color: var(--ft-bg);
        color: var(--ft-text);
    }

    #MainMenu, footer { visibility: hidden; }

    section[data-testid="stSidebar"] {
        background-color: var(--ft-sidebar-bg);
    }
    section[data-testid="stSidebar"] * {
        color: var(--ft-sidebar-text) !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #ffffff !important;
    }

    /* ---------- Headings ---------- */
    h1, h2, h3 {
        color: var(--ft-text);
        font-weight: 700;
    }

    /* ---------- Summary Cards ---------- */
    .metric-card {
        background: var(--ft-card);
        border-radius: 16px;
        padding: 22px 20px;
        box-shadow: var(--ft-shadow);
        border: 1px solid var(--ft-border);
        text-align: left;
        transition: transform 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .metric-icon {
        font-size: 26px;
        margin-bottom: 6px;
    }
    .metric-label {
        color: var(--ft-muted);
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-value {
        color: var(--ft-text);
        font-size: 26px;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Accent bars per card type */
    .card-blue   { border-left: 5px solid #3b82f6; }
    .card-green  { border-left: 5px solid #10b981; }
    .card-orange { border-left: 5px solid #f59e0b; }
    .card-purple { border-left: 5px solid #8b5cf6; }

    /* ---------- Generic content card ---------- */
    .content-card {
        background: var(--ft-card);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--ft-shadow);
        border: 1px solid var(--ft-border);
        margin-bottom: 20px;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        border: none;
        background-color: var(--ft-button-bg);
        color: var(--ft-button-text);
        transition: background-color 0.15s ease;
    }
    .stButton > button:hover {
        background-color: var(--ft-button-hover);
        color: var(--ft-button-text);
    }

    /* ---------- Inputs ---------- */
    .stTextInput input, .stNumberInput input, .stDateInput input,
    .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        border-radius: 10px !important;
        background-color: var(--ft-input-bg) !important;
        color: var(--ft-text) !important;
        border: 1px solid var(--ft-input-border) !important;
    }

    /* ---------- Budget alert ---------- */
    .budget-ok {
        background: var(--ft-budget-ok-bg);
        border: 1px solid var(--ft-budget-ok-border);
        color: var(--ft-budget-ok-text);
        padding: 14px 18px;
        border-radius: 12px;
        font-weight: 600;
    }
    .budget-warn {
        background: var(--ft-budget-warn-bg);
        border: 1px solid var(--ft-budget-warn-border);
        color: var(--ft-budget-warn-text);
        padding: 14px 18px;
        border-radius: 12px;
        font-weight: 600;
    }
    .budget-danger {
        background: var(--ft-budget-danger-bg);
        border: 1px solid var(--ft-budget-danger-border);
        color: var(--ft-budget-danger-text);
        padding: 14px 18px;
        border-radius: 12px;
        font-weight: 600;
    }

    /* ---------- Sidebar brand ---------- */
    .sidebar-brand {
        font-size: 22px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 0;
    }
    .sidebar-sub {
        font-size: 12px;
        color: var(--ft-sidebar-sub) !important;
        margin-bottom: 20px;
    }
</style>
"""


def inject_custom_css(st):
    """Apply the custom CSS to the given Streamlit module instance."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_metric_card(st, icon, label, value, css_class="card-blue"):
    """Render a single styled summary/metric card."""
    st.markdown(
        f"""
        <div class="metric-card {css_class}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
