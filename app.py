import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CONSERVE — Art Preservation Studio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("OpenAI API key not found. Add OPENAI_API_KEY to your .env file.")
    st.stop()

openai_client = OpenAI(api_key=openai_api_key)

# ==================== GLOBAL CSS ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

:root {
    --ink: #0e0e0f;
    --ink-soft: #1a1a1e;
    --ink-mid: #2a2a30;
    --parchment: #f5f0e8;
    --parchment-warm: #ede8dc;
    --parchment-deep: #d8d1c0;
    --gold: #b8963e;
    --gold-light: #d4aa55;
    --gold-muted: #8a6f2e;
    --rust: #8b3a2a;
    --teal: #2a6b6e;
    --teal-light: #3d8c8f;
    --text-primary: #1a1814;
    --text-secondary: #4a453d;
    --text-muted: #7a7268;
    --border: rgba(184,150,62,0.25);
    --border-soft: rgba(184,150,62,0.12);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--parchment) !important;
    font-family: 'Crimson Pro', Georgia, serif;
    color: var(--text-primary);
}

/* Hide streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ===== LANDING PAGE ===== */
.landing-wrap {
    min-height: 100vh;
    background: var(--ink);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}
.landing-texture {
    position: absolute;
    inset: 0;
    background-image: 
        repeating-linear-gradient(0deg, transparent, transparent 60px, rgba(184,150,62,0.04) 60px, rgba(184,150,62,0.04) 61px),
        repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(184,150,62,0.04) 60px, rgba(184,150,62,0.04) 61px);
    pointer-events: none;
}
.landing-ornament {
    width: 1px;
    height: 80px;
    background: linear-gradient(to bottom, transparent, var(--gold), transparent);
    margin-bottom: 48px;
}
.landing-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.35em;
    color: var(--gold-muted);
    text-transform: uppercase;
    margin-bottom: 24px;
}
.landing-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(56px, 8vw, 96px);
    font-weight: 700;
    color: var(--parchment);
    text-align: center;
    line-height: 0.95;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
}
.landing-title em {
    font-style: italic;
    color: var(--gold-light);
}
.landing-sub {
    font-family: 'Crimson Pro', serif;
    font-size: 18px;
    color: rgba(245,240,232,0.5);
    font-style: italic;
    text-align: center;
    margin-bottom: 64px;
    letter-spacing: 0.05em;
}
.landing-divider {
    width: 120px;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
    margin: 40px auto;
}
.landing-features {
    display: flex;
    gap: 48px;
    margin-bottom: 64px;
    flex-wrap: wrap;
    justify-content: center;
}
.landing-feat {
    text-align: center;
    color: rgba(245,240,232,0.4);
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.landing-feat strong {
    display: block;
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 600;
    color: var(--gold-light);
    letter-spacing: normal;
    text-transform: none;
    margin-bottom: 4px;
}

/* ===== HEADER ===== */
.site-header {
    background: var(--ink);
    border-bottom: 1px solid rgba(184,150,62,0.2);
    padding: 20px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.header-logo {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--parchment);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.header-logo span {
    color: var(--gold-light);
}
.header-meta {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    color: var(--gold-muted);
    text-transform: uppercase;
}

/* ===== MAIN LAYOUT ===== */
.main-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 48px 48px 96px;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 !important;
    margin-bottom: 40px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: var(--text-muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 16px 28px !important;
    margin: 0 !important;
    transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--gold) !important;
    background: rgba(184,150,62,0.05) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ===== PAGE TITLE ===== */
.page-title-block {
    margin-bottom: 48px;
    padding-bottom: 32px;
    border-bottom: 1px solid var(--border-soft);
}
.page-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.35em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 12px;
}
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.1;
    letter-spacing: -0.01em;
}
.page-title em {
    font-style: italic;
    color: var(--rust);
}
.page-desc {
    font-family: 'Crimson Pro', serif;
    font-size: 18px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-top: 12px;
    max-width: 640px;
    font-style: italic;
}

/* ===== SECTION LABEL ===== */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
    padding-left: 1px;
}

/* ===== INPUT STYLING ===== */
.stTextArea textarea, .stTextInput input {
    background: white !important;
    border: 1px solid var(--parchment-deep) !important;
    border-radius: 2px !important;
    color: var(--text-primary) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 16px !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(184,150,62,0.08) !important;
}
.stSelectbox > div > div {
    background: white !important;
    border: 1px solid var(--parchment-deep) !important;
    border-radius: 2px !important;
    color: var(--text-primary) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 15px !important;
}
.stFileUploader {
    background: white !important;
    border: 1.5px dashed var(--parchment-deep) !important;
    border-radius: 4px !important;
}
label, .stSelectbox label, .stTextArea label { display: none !important; }

/* ===== FEATURE BADGE ===== */
.feature-badge {
    display: inline-block;
    background: var(--ink-soft);
    color: var(--parchment-deep);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    padding: 8px 16px;
    border-radius: 2px;
    border-left: 3px solid var(--gold);
    margin-top: 12px;
    margin-bottom: 24px;
}

/* ===== ANALYSIS TYPE GRID ===== */
.analysis-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 2px;
    background: var(--parchment-deep);
    border: 1px solid var(--parchment-deep);
    margin-bottom: 32px;
}
.analysis-cell {
    background: white;
    padding: 14px 12px;
    cursor: pointer;
    transition: all 0.15s;
    text-align: center;
}
.analysis-cell:hover { background: var(--parchment-warm); }
.analysis-cell.active { background: var(--ink); }
.analysis-cell .cell-icon { font-size: 20px; margin-bottom: 6px; }
.analysis-cell .cell-name {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-secondary);
    line-height: 1.4;
}
.analysis-cell.active .cell-name { color: var(--parchment); }

/* ===== TEMPERATURE DISPLAY ===== */
.temp-display {
    background: var(--ink);
    border-radius: 3px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    border-left: 4px solid var(--gold);
}
.temp-value {
    font-family: 'Playfair Display', serif;
    font-size: 40px;
    font-weight: 700;
    color: var(--gold-light);
    line-height: 1;
    min-width: 70px;
}
.temp-label {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    color: var(--parchment);
    font-weight: 600;
    margin-bottom: 3px;
}
.temp-desc {
    font-family: 'Crimson Pro', serif;
    font-size: 14px;
    color: rgba(245,240,232,0.55);
    font-style: italic;
    line-height: 1.4;
}

/* ===== PRIMARY BUTTON ===== */
.stButton > button {
    background: var(--ink) !important;
    color: var(--parchment) !important;
    border: 1px solid rgba(184,150,62,0.4) !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    padding: 14px 36px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: var(--gold) !important;
    border-color: var(--gold) !important;
    color: var(--ink) !important;
}

/* ===== CARDS ===== */
.insight-card {
    background: white;
    border: 1px solid var(--parchment-deep);
    border-top: 3px solid var(--gold);
    padding: 28px;
    margin-bottom: 20px;
}
.insight-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.insight-card-body {
    font-family: 'Crimson Pro', serif;
    font-size: 16px;
    color: var(--text-secondary);
    line-height: 1.75;
}

/* ===== PHASE BLOCK ===== */
.phase-block {
    display: grid;
    grid-template-columns: 180px 1fr;
    gap: 0;
    margin-bottom: 2px;
    background: white;
    border: 1px solid var(--parchment-deep);
}
.phase-left {
    background: var(--ink);
    padding: 28px 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.phase-num {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.3em;
    color: var(--gold-muted);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.phase-icon-big { font-size: 32px; margin-bottom: 12px; }
.phase-name {
    font-family: 'Playfair Display', serif;
    font-size: 15px;
    font-weight: 600;
    color: var(--parchment);
    line-height: 1.3;
}
.phase-weeks {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--gold-muted);
    margin-top: 16px;
}
.phase-right { padding: 28px 32px; }
.phase-task {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-soft);
    font-family: 'Crimson Pro', serif;
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.5;
}
.phase-task:last-of-type { border-bottom: none; }
.priority-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 7px;
}
.dot-high { background: var(--rust); }
.dot-medium { background: var(--gold); }
.dot-low { background: var(--teal); }
.phase-milestone {
    margin-top: 20px;
    padding: 14px 18px;
    background: var(--parchment-warm);
    border-left: 3px solid var(--gold);
    font-family: 'Crimson Pro', serif;
    font-size: 14px;
    font-style: italic;
    color: var(--text-secondary);
}
.milestone-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 4px;
    font-style: normal;
}

/* ===== STAT STRIP ===== */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2px;
    background: var(--parchment-deep);
    border: 1px solid var(--parchment-deep);
    margin-bottom: 40px;
}
.stat-cell {
    background: var(--ink);
    padding: 24px 20px;
    text-align: center;
}
.stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--gold-light);
    line-height: 1;
    margin-bottom: 8px;
}
.stat-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.3em;
    color: rgba(245,240,232,0.4);
    text-transform: uppercase;
}

/* ===== RESULTS PAGE ===== */
.result-header {
    background: var(--ink);
    padding: 48px;
    margin-bottom: 0;
    position: relative;
    overflow: hidden;
}
.result-header::before {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 300px; height: 300px;
    border: 1px solid rgba(184,150,62,0.1);
    border-radius: 50%;
}
.result-header::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 400px; height: 400px;
    border: 1px solid rgba(184,150,62,0.06);
    border-radius: 50%;
}
.result-tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 16px;
}
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 700;
    color: var(--parchment);
    line-height: 1.05;
    letter-spacing: -0.02em;
}
.result-title em { color: var(--gold-light); font-style: italic; }
.result-body {
    font-family: 'Crimson Pro', serif;
    font-size: 17px;
    color: rgba(245,240,232,0.6);
    font-style: italic;
    margin-top: 12px;
}

.result-content-wrap {
    background: white;
    border: 1px solid var(--parchment-deep);
    padding: 48px;
}
.result-section-head {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--gold);
    margin: 36px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.result-section-head:first-child { margin-top: 0; }
.result-text {
    font-family: 'Crimson Pro', serif;
    font-size: 17px;
    color: var(--text-secondary);
    line-height: 1.8;
    white-space: pre-wrap;
}

/* ===== QUIZ ===== */
.quiz-wrap {
    background: var(--ink);
    border-radius: 4px;
    padding: 40px;
    margin-bottom: 40px;
}
.quiz-header {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 600;
    color: var(--parchment);
    margin-bottom: 8px;
}
.quiz-sub {
    font-family: 'Crimson Pro', serif;
    font-size: 15px;
    color: rgba(245,240,232,0.5);
    font-style: italic;
    margin-bottom: 32px;
}
.quiz-progress {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
}
.quiz-progress-bar-bg {
    flex: 1;
    height: 2px;
    background: rgba(255,255,255,0.1);
}
.quiz-progress-bar-fill {
    height: 100%;
    background: var(--gold);
    transition: width 0.3s;
}
.quiz-q-text {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    color: var(--parchment);
    font-style: italic;
    margin-bottom: 24px;
    line-height: 1.5;
    padding: 20px 24px;
    background: rgba(255,255,255,0.04);
    border-left: 3px solid var(--gold);
}

/* Radio button overrides in quiz */
.stRadio > div { gap: 8px !important; }
.stRadio label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(184,150,62,0.15) !important;
    border-radius: 2px !important;
    padding: 12px 16px !important;
    color: rgba(245,240,232,0.8) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 15px !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    display: block !important;
}

/* ===== FEATURE GALLERY CARDS ===== */
.feat-card {
    background: white;
    border: 1px solid var(--parchment-deep);
    padding: 28px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.feat-card:hover { border-color: var(--gold); }
.feat-card-head {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 16px;
}
.feat-icon-box {
    width: 44px;
    height: 44px;
    background: var(--ink);
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.feat-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}
.feat-desc {
    font-family: 'Crimson Pro', serif;
    font-size: 15px;
    color: var(--text-muted);
    line-height: 1.5;
}
.feat-cases {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 12px;
}
.case-tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    padding: 4px 10px;
    background: var(--parchment-warm);
    color: var(--text-secondary);
    border-radius: 1px;
}

/* ===== CULTURAL PERIOD HERO ===== */
.period-hero {
    background: var(--ink);
    padding: 36px 40px;
    margin-bottom: 32px;
    border-bottom: 3px solid var(--gold);
    display: flex;
    align-items: center;
    gap: 28px;
}
.period-emoji { font-size: 48px; }
.period-name {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--parchment);
    line-height: 1.1;
}
.period-era {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.25em;
    color: var(--gold);
    text-transform: uppercase;
    margin-top: 6px;
}

/* ===== TECHNIQUE TAGS ===== */
.technique-tag {
    display: inline-block;
    background: var(--ink);
    color: var(--parchment-deep);
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    padding: 7px 14px;
    margin: 4px;
    border-radius: 1px;
}
.work-item {
    font-family: 'Crimson Pro', serif;
    font-size: 16px;
    color: var(--text-secondary);
    padding: 10px 0;
    border-bottom: 1px solid var(--border-soft);
    display: flex;
    align-items: center;
    gap: 12px;
}
.work-item::before {
    content: '—';
    color: var(--gold);
    font-family: 'DM Mono', monospace;
}

/* ===== REC ITEMS ===== */
.rec-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 18px 20px;
    background: white;
    border: 1px solid var(--parchment-deep);
    border-left: 4px solid;
    margin-bottom: 8px;
}
.rec-icon { font-size: 20px; flex-shrink: 0; }
.rec-body { font-family: 'Crimson Pro', serif; font-size: 15px; color: var(--text-secondary); line-height: 1.6; }
.rec-priority {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.25em;
    margin-bottom: 4px;
    text-transform: uppercase;
}

/* ===== SLIDER OVERRIDE ===== */
.stSlider > div { padding: 0 !important; }
.stSlider [data-testid="stSlider"] { padding: 0 !important; }

/* ===== MISC ===== */
.divider-gold {
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
    margin: 40px 0;
}
.spacer { height: 32px; }

/* ===== FEEDBACK ===== */
.feedback-wrap {
    background: var(--parchment-warm);
    border: 1px solid var(--parchment-deep);
    border-top: 3px solid var(--teal);
    padding: 40px;
    margin-top: 48px;
}
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {'name': 'User'}
if 'result_text' not in st.session_state:
    st.session_state.result_text = ""

# ==================== FEATURE DESCRIPTIONS ====================
feature_descriptions = {
    'period': 'Expert restoration guidance for Baroque and Renaissance artworks using historically accurate techniques',
    'cultural': 'Restore and enhance traditional patterns from Mughal, Islamic, Celtic, Asian, and indigenous arts',
    'sculptural': 'Reconstruct eroded or damaged features in sculptures, statues, and three-dimensional artifacts',
    'textile': 'Expert restoration for tapestries, embroidery, historical fabrics, and woven artifacts',
    'abstract': 'Restore contemporary, abstract, expressionist, and modern artworks',
    'manuscript': 'Restore illuminated manuscripts, scrolls, codices, and historical documents',
    'mural': 'Restore wall paintings, cave art, frescoes, and architectural murals',
    'ceramic': 'Restore pottery, porcelain, ceramic vessels, and glazed artifacts',
    'symbol': 'Decode and restore symbolic elements, religious imagery, inscriptions, and cultural icons',
    'educational': 'Create engaging museum descriptions, exhibition content, and educational materials'
}

feature_list = [
    {"key": "period",      "icon": "🎭", "label": "Period Art"},
    {"key": "cultural",    "icon": "🕌", "label": "Cultural Patterns"},
    {"key": "sculptural",  "icon": "🗿", "label": "Sculpture"},
    {"key": "textile",     "icon": "🧵", "label": "Textiles"},
    {"key": "abstract",    "icon": "🎨", "label": "Modern Art"},
    {"key": "manuscript",  "icon": "📜", "label": "Manuscripts"},
    {"key": "mural",       "icon": "🏛️", "label": "Murals"},
    {"key": "ceramic",     "icon": "🏺", "label": "Ceramics"},
    {"key": "symbol",      "icon": "🔯", "label": "Iconography"},
    {"key": "educational", "icon": "🎓", "label": "Education"},
]

def render_header():
    st.markdown("""
    <div class="site-header">
        <div class="header-logo">CON<span>SERVE</span></div>
        <div class="header-meta">Art Preservation Studio &nbsp;·&nbsp; Powered by OpenAI</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== LANDING PAGE ====================
if st.session_state.page == 'landing':
    st.markdown("""
    <div class="landing-wrap">
        <div class="landing-texture"></div>
        <div class="landing-ornament"></div>
        <div class="landing-eyebrow">Cultural Heritage Preservation Studio</div>
        <div class="landing-title">CON<em>SERVE</em></div>
        <div class="landing-sub">Where science meets the ancient art of restoration</div>
        <div class="landing-divider"></div>
        <div class="landing-features">
            <div class="landing-feat"><strong>10</strong>Disciplines</div>
            <div class="landing-feat"><strong>AI</strong>Powered</div>
            <div class="landing-feat"><strong>∞</strong>Heritage</div>
            <div class="landing-feat"><strong>24/7</strong>Available</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Enter the Studio", key="landing_enter"):
            st.session_state.page = 'main'
            st.rerun()

    st.markdown("""
    <div style="background:var(--ink);padding:16px 48px;text-align:center;border-top:1px solid rgba(184,150,62,0.1);">
        <span style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.25em;color:rgba(245,240,232,0.25);text-transform:uppercase;">
            CONSERVE Studio &nbsp;·&nbsp; Cultural Heritage &nbsp;·&nbsp; Powered by OpenAI
        </span>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN APPLICATION ====================
elif st.session_state.page == 'main':
    render_header()

    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Restoration Assistant",
        "Feature Gallery",
        "Cultural Archive",
        "Timeline Planner"
    ])

    # ==================== TAB 1: RESTORATION ASSISTANT ====================
    with tab1:
        st.markdown("""
        <div class="page-title-block">
            <div class="page-eyebrow">Restoration Analysis Engine</div>
            <div class="page-title">Analyse Your <em>Artwork</em></div>
            <div class="page-desc">Submit your artwork for AI-assisted conservation analysis. Provide details and receive expert restoration guidance grounded in historical research.</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown('<div class="section-label">Upload Artwork (Optional)</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="image_upload", label_visibility="collapsed")
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Artwork", use_container_width=True)
            else:
                st.markdown("""
                <div style="height:200px;background:var(--parchment-warm);border:1.5px dashed var(--parchment-deep);display:flex;align-items:center;justify-content:center;margin-top:10px;">
                    <span style="font-family:'Crimson Pro',serif;font-size:15px;color:var(--text-muted);font-style:italic;">drag & drop or click above to upload</span>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-label">Artwork Description</div>', unsafe_allow_html=True)
            artwork_description = st.text_area(
                "",
                placeholder="Describe the artwork: medium, period, visible damage, dimensions, provenance, condition notes...",
                height=200,
                key="description_input",
                label_visibility="collapsed"
            )

        st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

        # Analysis type selector
        st.markdown('<div class="section-label">Analysis Discipline</div>', unsafe_allow_html=True)
        feature_select = st.selectbox(
            "",
            [
                "1. Period-Specific Restoration (Baroque/Renaissance)",
                "2. Cultural Pattern Enhancement (Traditional Arts)",
                "3. Sculptural Reconstruction",
                "4. Textile & Tapestry Repair",
                "5. Abstract & Modern Art Recovery",
                "6. Ancient Manuscript Conservation",
                "7. Mural & Fresco Revival",
                "8. Ceramic & Pottery Reconstruction",
                "9. Symbol & Iconography Interpretation",
                "10. Educational Content Generation"
            ],
            key="feature_select",
            label_visibility="collapsed"
        )
        feature_key = ['period', 'cultural', 'sculptural', 'textile', 'abstract', 'manuscript', 'mural', 'ceramic', 'symbol', 'educational'][int(feature_select[0]) - 1]
        st.markdown(f'<div class="feature-badge">{feature_list[int(feature_select[0])-1]["icon"]} &nbsp;{feature_descriptions[feature_key]}</div>', unsafe_allow_html=True)

        col3, col4, col5 = st.columns(3)
        with col3:
            st.markdown('<div class="section-label">Art Style / Period</div>', unsafe_allow_html=True)
            art_style = st.selectbox("", [""] + [
                "Baroque","Renaissance","Gothic","Neoclassical","Rococo","Romantic",
                "Impressionist","Expressionist","Art Deco","Art Nouveau","Indian Mughal",
                "Indian Rajput","Indian Pahari","Indian Madhubani","Persian Miniature",
                "Islamic Geometric","Byzantine","Japanese Ukiyo-e","Chinese Ming Dynasty",
                "Aboriginal","Egyptian","Greek/Roman Classical"
            ], key="style_input", label_visibility="collapsed")

        with col4:
            st.markdown('<div class="section-label">Damage Type</div>', unsafe_allow_html=True)
            damage_type = st.selectbox("", [""] + [
                "Water damage/stains","Fire damage/smoke residue","Fading from sunlight/UV exposure",
                "Erosion/weathering","Cracks/structural damage","Flaking/peeling paint",
                "Mold/biological growth","Scratches/surface abrasions","Missing sections/losses",
                "Discoloration/yellowing","Torn fabric/textile damage","Broken/fragmented pieces",
                "Oxidation/corrosion","Insect damage","Previous poor restoration"
            ], key="damage_input", label_visibility="collapsed")

        with col5:
            st.markdown('<div class="section-label">Cultural Context</div>', unsafe_allow_html=True)
            cultural_context = st.selectbox("", [""] + [
                "Italian Renaissance","French Baroque","Spanish Colonial","Flemish/Dutch",
                "British Victorian","Indian Mughal","Indian Rajput","Indian Temple Art",
                "Persian/Iranian","Ottoman Turkish","Chinese Imperial","Japanese Edo Period",
                "Egyptian Pharaonic","Greek Classical","Roman Imperial","Byzantine Eastern Orthodox",
                "African Tribal","Native American"
            ], key="context_input", label_visibility="collapsed")

        st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

        # Temperature
        st.markdown('<div class="section-label">Analytical Approach</div>', unsafe_allow_html=True)
        temperature = st.slider("", 0.0, 1.0, 0.6, 0.05, key="temp_slider", label_visibility="collapsed")

        if temperature <= 0.3:
            t_title, t_sub, t_desc = "Strict Historical", "Evidence-Only Mode", "Ultra-precise analysis grounded exclusively in documented historical evidence and proven conservation techniques."
        elif temperature <= 0.5:
            t_title, t_sub, t_desc = "Conservative & Methodical", "Research-Led Approach", "Careful analysis based on historical research and comparative studies, with minimal interpretive speculation."
        elif temperature <= 0.7:
            t_title, t_sub, t_desc = "Balanced Professional", "Art & Science", "The recommended setting — combines rigorous historical grounding with thoughtful, creative interpretation."
        elif temperature <= 0.85:
            t_title, t_sub, t_desc = "Interpretive & Exploratory", "Artistic Reading", "Explores multiple creative possibilities while respecting historical integrity and period conventions."
        else:
            t_title, t_sub, t_desc = "Visionary", "Bold Artistic Interpretation", "Maximum creativity — bold interpretive suggestions that push the boundaries of conventional restoration thinking."

        st.markdown(f"""
        <div class="temp-display">
            <div class="temp-value">{temperature:.2f}</div>
            <div>
                <div class="temp-label">{t_title}</div>
                <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.2em;color:var(--gold-muted);text-transform:uppercase;margin-bottom:6px;">{t_sub}</div>
                <div class="temp-desc">{t_desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

        if st.button("Generate Restoration Analysis", key="generate_btn"):
            if artwork_description:
                with st.spinner("Conducting analysis..."):
                    import time; time.sleep(2)
                    st.session_state.page = 'results'
                    creativity_level = ["highly conservative","conservative and methodical","balanced and professional","creative and exploratory","highly creative and innovative"][min(int(temperature / 0.2), 4)]
                    st.session_state.result_text = f"""COMPREHENSIVE RESTORATION ANALYSIS

ARTWORK DETAILS
{artwork_description}

STYLE/PERIOD: {art_style or 'Not specified'}
DAMAGE TYPE:  {damage_type or 'General wear'}
CULTURAL CONTEXT: {cultural_context or 'Not specified'}
ANALYSIS TYPE: {feature_select}
ANALYTICAL APPROACH: {temperature} — {creativity_level}

─────────────────────────────────────────────────────────

1. HISTORICAL CONTEXT & SIGNIFICANCE

Based on the provided description and the {art_style or 'specified'} period, this artwork represents a significant example of its time. The {cultural_context or 'general'} cultural context suggests traditional techniques and materials commonly employed during this era. Understanding the socio-political environment and artistic patronage structures of the period is essential for an authentic restoration approach.

─────────────────────────────────────────────────────────

2. CONDITION ASSESSMENT

The {damage_type or 'general wear'} presents specific challenges requiring careful consideration:

• Primary concerns include structural integrity and aesthetic coherence
• Surface analysis reveals patterns consistent with environmental exposure
• Original materials and binding media must be preserved wherever possible
• Comprehensive documentation of current state is essential before any intervention

─────────────────────────────────────────────────────────

3. RESTORATION METHODOLOGY

A. Documentation Phase
   — Comprehensive photography (visible light, UV, infrared reflectography)
   — Detailed condition mapping and loss assessment
   — Material sampling and scientific analysis (pigment, substrate, binding media)
   — Historical research and archival provenance study

B. Stabilisation Phase
   — Consolidation of flaking or delaminating paint layers
   — Structural support for fragile substrate
   — Environmental stabilisation and climate control
   — Protection against further deterioration

C. Cleaning Phase
   — Surface cleaning using period-appropriate methods
   — Removal of discoloured varnish or overpainting
   — pH monitoring and controlled solvent testing
   — Gradual approach with constant material assessment

D. Restoration Phase
   — Loss compensation using reversible conservation materials
   — Colour matching to original palette
   — Texture recreation following original {art_style or 'period'} technique
   — Visual integration with surviving original material

─────────────────────────────────────────────────────────

4. MATERIALS & TECHNICAL SPECIFICATIONS

Conservation-grade materials recommended:
• Adhesives: Reversible synthetic polymers (BEVA 371, Paraloid B-72)
• Consolidants: Tested for compatibility with original substrate
• Inpainting media: Watercolours or conservation acrylics (Gamblin)
• Protective coatings: UV-filtering, breathable varnishes (Regalrez)

Period-accurate techniques:
• Brushwork patterns consistent with {art_style or 'period'} conventions
• Layering methodology respecting traditional working sequence
• Colour mixing using knowledge of historical pigment formulations

─────────────────────────────────────────────────────────

5. CULTURAL SENSITIVITY & ETHICAL FRAMEWORK

Following international conservation ethics (ICOM-CC, AIC):
• Minimal intervention — preserve rather than restore where in doubt
• Reversibility of all treatments without risk to original material
• Full documentation of every procedure and decision
• Respect for original artist's intent, not ideals of 'perfection'
• Consultation with cultural heritage specialists and community stakeholders

─────────────────────────────────────────────────────────

6. PREVENTIVE CONSERVATION RECOMMENDATIONS

Environmental Controls:
• Temperature: 18–22°C (64–72°F) with <5°C daily variation
• Relative Humidity: 45–55%, stable
• Illumination: <150 lux for sensitive works; UV filtered
• Air quality: particulate filtered, pollutant-free

─────────────────────────────────────────────────────────

7. CONCLUSION

This analysis recommends a systematic, evidence-based approach to conservation of the submitted work. The {damage_type or 'observed damage'} is addressable through established conservation methodology while preserving the work's integrity, authenticity, and cultural value. All proposed treatments prioritise long-term material stability.

DISCLAIMER: This analysis is advisory only. All physical restoration work must be carried out by certified professional conservators following applicable institutional and ethical guidelines.
"""
                    st.rerun()
            else:
                st.error("Please provide an artwork description to proceed.")

    # ==================== TAB 2: FEATURE GALLERY ====================
    with tab2:
        st.markdown("""
        <div class="page-title-block">
            <div class="page-eyebrow">Capability Overview</div>
            <div class="page-title">Studio <em>Disciplines</em></div>
            <div class="page-desc">Ten specialist disciplines covering the full breadth of art conservation, from ancient manuscripts to contemporary works.</div>
        </div>
        """, unsafe_allow_html=True)

        features = [
            {"icon": "🎭", "title": "Period-Specific Restoration", "desc": "Expert restoration guidance for Baroque and Renaissance artworks using historically accurate techniques", "cases": ["Renaissance portraits with sfumato technique", "Baroque paintings with dramatic chiaroscuro", "Dutch Golden Age realistic lighting", "Rococo delicate pastels and gold leaf"]},
            {"icon": "🕌", "title": "Cultural Pattern Enhancement", "desc": "Restore and enhance traditional patterns from Mughal, Islamic, Celtic, Asian, and indigenous arts", "cases": ["Mughal miniature floral borders", "Islamic geometric tessellations", "Celtic knotwork patterns", "Japanese ukiyo-e wave patterns"]},
            {"icon": "🗿", "title": "Sculptural Reconstruction", "desc": "Reconstruct eroded or damaged features in sculptures, statues, and three-dimensional artifacts", "cases": ["Greek/Roman marble statues", "Indian temple sculptures", "Egyptian hieroglyphic carvings", "Mayan stele reconstructions"]},
            {"icon": "🧵", "title": "Textile & Tapestry Repair", "desc": "Expert restoration for tapestries, embroidery, historical fabrics, and woven artifacts", "cases": ["Medieval tapestries (Bayeux style)", "Chinese silk embroidery", "Indian Banarasi sarees", "Persian carpets"]},
            {"icon": "🎨", "title": "Abstract & Modern Art Recovery", "desc": "Restore contemporary, abstract, expressionist, and modern artworks", "cases": ["Pollock drip paintings", "Rothko color fields", "Abstract impressionism texture recovery", "Minimalist hard-edge works"]},
            {"icon": "📜", "title": "Ancient Manuscript Conservation", "desc": "Restore illuminated manuscripts, scrolls, codices, and historical documents", "cases": ["Book of Kells style illuminations", "Arabic/Persian calligraphy scrolls", "Sanskrit palm leaf manuscripts", "Dead Sea Scrolls preservation"]},
            {"icon": "🏛️", "title": "Mural & Fresco Revival", "desc": "Restore wall paintings, cave art, frescoes, and architectural murals", "cases": ["Ajanta/Ellora cave paintings", "Roman Pompeii frescoes", "Mexican muralism (Diego Rivera style)", "Aboriginal rock art"]},
            {"icon": "🏺", "title": "Ceramic & Pottery Reconstruction", "desc": "Restore pottery, porcelain, ceramic vessels, and glazed artifacts", "cases": ["Chinese Ming dynasty porcelain", "Greek amphoras", "Native American pottery", "Japanese raku ceramics"]},
            {"icon": "🔯", "title": "Symbol & Iconography Interpretation", "desc": "Decode and restore symbolic elements, religious imagery, inscriptions, and cultural icons", "cases": ["Egyptian hieroglyphics", "Christian Byzantine iconography", "Hindu temple symbolism", "Mayan glyph decoding"]},
            {"icon": "🎓", "title": "Educational Content Generation", "desc": "Create engaging museum descriptions, exhibition content, and educational materials", "cases": ["Museum placard content", "Virtual exhibition descriptions", "Educational tour scripts", "Accessibility-friendly art explanations"]}
        ]

        # Knowledge quiz
        import random
        cases = []
        for f in features:
            for case in f['cases']:
                cases.append({"case": case, "feature": f['title']})

        if 'quiz_questions' not in st.session_state:
            pool = cases.copy()
            num_q = min(6, max(3, len(pool)))
            sample = random.sample(pool, num_q)
            titles = [f['title'] for f in features]
            questions = []
            for s in sample:
                correct = s['feature']
                wrongs = [t for t in titles if t != correct]
                choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
                random.shuffle(choices)
                questions.append({'prompt': s['case'], 'correct': correct, 'choices': choices})
            st.session_state.quiz_questions = questions
            st.session_state.q_index = 0
            st.session_state.score = 0

        questions = st.session_state.quiz_questions
        qidx = st.session_state.q_index

        st.markdown("""
        <div class="quiz-wrap">
            <div class="quiz-header">Knowledge Assessment</div>
            <div class="quiz-sub">Match each use case to the correct conservation discipline</div>
        """, unsafe_allow_html=True)

        if qidx < len(questions):
            pct = int((qidx / len(questions)) * 100)
            st.markdown(f"""
            <div class="quiz-progress">
                <span style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(245,240,232,0.4);letter-spacing:0.2em;">{qidx+1} / {len(questions)}</span>
                <div class="quiz-progress-bar-bg"><div class="quiz-progress-bar-fill" style="width:{pct}%"></div></div>
                <span style="font-family:'DM Mono',monospace;font-size:10px;color:var(--gold);letter-spacing:0.1em;">{st.session_state.score} correct</span>
            </div>
            """, unsafe_allow_html=True)

            q = questions[qidx]
            st.markdown(f'<div class="quiz-q-text">"{q["prompt"]}"</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            selected = st.radio('Which conservation discipline best matches this use case?', q['choices'], key=f'choice_{qidx}', label_visibility="collapsed")
            if st.button('Submit Answer', key=f'submit_{qidx}'):
                if selected == q['correct']:
                    st.session_state.score += 1
                    st.success('✓ Correct')
                else:
                    st.error(f"✗ Correct answer: {q['correct']}")
                st.session_state.q_index += 1
                st.rerun()
        else:
            total = len(questions)
            score = st.session_state.score
            pct = int((score / total) * 100)
            st.markdown(f"""
            <div style="text-align:center;padding:32px 0;">
                <div style="font-family:'Playfair Display',serif;font-size:64px;font-weight:700;color:var(--gold-light);">{score}/{total}</div>
                <div style="font-family:'DM Mono',monospace;font-size:11px;letter-spacing:0.3em;color:rgba(245,240,232,0.4);text-transform:uppercase;margin-top:8px;">Assessment Complete · {pct}% Accuracy</div>
            </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button('Retake Assessment', key='quiz_restart'):
                del st.session_state.quiz_questions
                del st.session_state.q_index
                del st.session_state.score
                st.rerun()

        st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="page-eyebrow" style="margin-bottom:20px;">All Ten Disciplines</div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        for i, feature in enumerate(features):
            with (col_a if i % 2 == 0 else col_b):
                cases_html = "".join([f'<span class="case-tag">{c}</span>' for c in feature['cases']])
                st.markdown(f"""
                <div class="feat-card">
                    <div class="feat-card-head">
                        <div class="feat-icon-box">{feature['icon']}</div>
                        <div>
                            <div class="feat-title">{feature['title']}</div>
                            <div class="feat-desc">{feature['desc']}</div>
                        </div>
                    </div>
                    <div class="feat-cases">{cases_html}</div>
                </div>
                """, unsafe_allow_html=True)

    # ==================== TAB 3: CULTURAL ARCHIVE ====================
    with tab3:
        st.markdown("""
        <div class="page-title-block">
            <div class="page-eyebrow">Heritage Knowledge Base</div>
            <div class="page-title">Cultural <em>Archive</em></div>
            <div class="page-desc">Explore the historical context, artistic significance, and conservation considerations for major art traditions from around the world.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Select Art Period or Cultural Tradition</div>', unsafe_allow_html=True)
        insight_type = st.selectbox("", [
            "Renaissance (Italian)", "Baroque (European)", "Rococo (French)",
            "Indian Mughal Art", "Indian Rajput Painting", "Islamic Art & Calligraphy",
            "Japanese Ukiyo-e", "Chinese Ming Dynasty", "Byzantine Art",
            "Egyptian Art", "Greek Classical Art", "Aboriginal Australian Art"
        ], key="cultural_insight_select", label_visibility="collapsed")

        cultural_insights = {
            "Renaissance (Italian)": {"emoji":"🎨","period":"14th–17th Century","background":"The Renaissance marked a cultural rebirth in Europe, emphasising humanism, naturalism, and classical learning. Leonardo da Vinci, Michelangelo, and Raphael revolutionised painting with linear perspective, sfumato, and anatomical precision.","importance":"Renaissance art laid the foundation for Western artistic tradition, shifting from medieval symbolism to representational realism. Its emphasis on individual expression and scientific observation permanently altered how humans understand themselves.","restoration":"Renaissance works demand extreme care due to fragile egg tempera and delicate oil glazing layers. Restoration must preserve gold leaf applications and the subtle tonal balance achieved through layered working methods. Non-invasive imaging is standard before any intervention.","techniques":["Linear Perspective","Sfumato (atmospheric haze)","Chiaroscuro (light/shadow)","Contrapposto stance","Oil glazing layers"],"famous_works":["Mona Lisa","The Last Supper","Sistine Chapel Ceiling","The Birth of Venus"]},
            "Baroque (European)": {"emoji":"✨","period":"17th–18th Century","background":"Baroque emerged as a dramatic, emotional response to the Protestant Reformation. Characterised by intense light effects, movement, and theatrical staging, it served the Catholic Church as a vehicle for devotional awe.","importance":"Baroque art revolutionised emotional expression. Caravaggio, Rembrandt, and Rubens achieved unprecedented drama and psychological depth in their work.","restoration":"Baroque works often feature heavy impasto and intentionally dark varnish layers that create depth. Restoration requires careful staged varnish removal to reveal original pigment while preserving the deliberate tonal architecture.","techniques":["Tenebrism (extreme contrast)","Dynamic, swirling composition","Rich, saturated palette","Psychological intensity","Sculptural drapery"],"famous_works":["The Night Watch","Ecstasy of Saint Teresa","Las Meninas","The Calling of St Matthew"]},
            "Rococo (French)": {"emoji":"🌸","period":"18th Century","background":"Rococo emerged as a lighter, playful reaction to Baroque grandeur. Pastel palettes, delicate ornamentation, and themes of pastoral romance flourished in French aristocratic interiors and portrait painting.","importance":"Rococo captured the refinement of 18th-century aristocratic culture and influenced interior design, fashion, and the decorative arts across Europe.","restoration":"Rococo works feature delicate pastel pigments and gold leaf that fade and flake. Restoration requires preserving the airiness of the style while stabilising fragile decorative surfaces.","techniques":["Pastel colour palette","Asymmetric decorative curves","Gold leaf highlights","Delicate feathery brushwork","Pastoral and romantic themes"],"famous_works":["The Swing","Pilgrimage to Cythera","Diana Leaving Her Bath","Versailles interior schemes"]},
            "Indian Mughal Art": {"emoji":"🕌","period":"16th–19th Century","background":"Mughal miniature paintings synthesise Persian, Indian, and Islamic traditions. Created for royal courts, these intricate works document historical events, flora, and court life with meticulous single-hair brushwork and vibrant natural pigments.","importance":"Mughal art represents a unique cultural synthesis and provides an invaluable visual record of one of history's most sophisticated imperial courts.","restoration":"Mughal miniatures are painted on paper with mineral pigments and gold. Restoration must address insect damage, pigment fading, and paper deterioration while preserving delicate gilded work.","techniques":["Fine single-hair brushwork","Natural mineral pigments","Gold leaf (sona)","Elaborate architectural borders","Layered compositional structure"],"famous_works":["Hamzanama manuscripts","Akbarnama","Padshahnama","Baburnama illustrations"]},
            "Indian Rajput Painting": {"emoji":"🎭","period":"16th–19th Century","background":"Rajput paintings from various court schools depicted Hindu mythology, devotional poetry, and court culture. Known for bold flat colour, expressive faces, and spiritual themes — particularly the love of Krishna and Radha.","importance":"Rajput art preserved Hindu religious narrative and regional cultural identity. Each school developed a distinctive visual language contributing to India's extraordinarily diverse artistic heritage.","restoration":"Similar materials to Mughal art but with bolder pigment application and regional technique variations. Conservation must respect religious and iconographic symbolism.","techniques":["Bold, flat colour fields","Expressive gesture and pose","Symbolic colour language","Poetry-inspired composition","Distinctive regional styles"],"famous_works":["Bani Thani (Kishangarh)","Ragamala series","Krishna Lila paintings","Mewar Ramayana"]},
            "Islamic Art & Calligraphy": {"emoji":"🕌","period":"7th Century–Present","background":"Islamic art emphasises geometric pattern, arabesque, and calligraphy in response to religious restrictions on figural imagery. Quranic scripture elevated to visual art through scripts including Kufic, Naskh, and Thuluth.","importance":"Islamic art demonstrates how religious principles inspire mathematical precision and aesthetic mastery. Calligraphy treats the written word as an act of devotion made visible.","restoration":"Islamic manuscripts and architectural decoration require specialist knowledge of Arabic scripts and geometric principles. Symmetry and repeating pattern integrity must be perfectly maintained.","techniques":["Sacred geometry","Arabesque scroll pattern","Illuminated manuscript borders","Geometric tilework","Multiple calligraphic scripts"],"famous_works":["Blue Quran (Fatimid)","Alhambra palace decoration","Topkapi Saray manuscripts","Isfahan mosque tilework"]},
            "Japanese Ukiyo-e": {"emoji":"🎌","period":"17th–19th Century","background":"Ukiyo-e woodblock prints depicted kabuki actors, beautiful women, and landscapes in Edo-period Japan. Hokusai and Hiroshige profoundly influenced European Post-Impressionism and the aesthetics of modernity.","importance":"Ukiyo-e democratised art in Japan and catalysed a revolution in European painting, demonstrating the power of asymmetric composition, flat colour, and the radical cropping of the image field.","restoration":"Woodblock prints are extremely vulnerable to light-induced fading, foxing, and acid degradation of Japanese paper. Conservation requires understanding traditional washi papermaking and mica powder printing.","techniques":["Woodblock printing (mokuhanga)","Bokashi (gradated colour)","Strong ink outlines","Flat colour fields","Asymmetric composition"],"famous_works":["The Great Wave off Kanagawa","Thirty-Six Views of Fuji","Fifty-Three Stations of Tokaido","Beauties of Yoshiwara"]},
            "Chinese Ming Dynasty": {"emoji":"🐉","period":"14th–17th Century","background":"Ming Dynasty art revived classical Chinese tradition. Celebrated for blue-and-white porcelain, ink landscape painting, and calligraphy, Ming artists articulated a philosophy of harmony between humanity and the natural world.","importance":"Ming art represents the apex of Chinese ceramic production and literati painting. Its porcelain output shaped global trade patterns and aesthetic sensibility worldwide.","restoration":"Ming ceramics require specialist knowledge of high-temperature reduction firing and cobalt pigment behaviour. Ink paintings on silk demand extreme care due to the fragility of the support.","techniques":["Blue-and-white porcelain","Monochrome ink landscape","Calligraphic brushwork","Scholar's rock aesthetics","Imperial court painting"],"famous_works":["Ming blue-and-white vases","Shen Zhou landscapes","Tang Yin figure paintings","Imperial porcelain collections"]},
            "Byzantine Art": {"emoji":"☦️","period":"4th–15th Century","background":"Byzantine art served the Eastern Orthodox Church, developing a visual language of gold-ground icons, monumental mosaics, and frontal hieratic figures designed to manifest spiritual presence.","importance":"Byzantine art preserved classical techniques through the medieval period and established the visual vocabulary of Orthodox Christianity still active in religious practice today.","restoration":"Byzantine panels and mosaics require specialist conservation of egg tempera, gold leaf, and glass tesserae. Orthodox tradition governs acceptable intervention on liturgical works.","techniques":["Gold leaf backgrounds","Egg tempera on gesso","Mosaic glass tesserae","Hierarchical figure scaling","Symbolic colour theology"],"famous_works":["Hagia Sophia mosaics","Vladimir Mother of God","Ravenna apse mosaics","Christ Pantocrator (Daphni)"]},
            "Egyptian Art": {"emoji":"🏛️","period":"3000–30 BCE","background":"Ancient Egyptian art served religious and political functions — depicting gods, pharaohs, and the afterlife across a formal visual system so stable it endured with minimal change for over three millennia.","importance":"Egyptian art provides the most sustained visual record in human history, preserving cosmological knowledge, funerary belief, and royal propaganda across thirty dynasties.","restoration":"Egyptian objects require strict climate control. Millennia-old mineral pigments need careful stabilisation. Works on stone, papyrus, linen, and plaster each demand distinct conservation approaches.","techniques":["Hierarchical figure scale","Composite frontal/profile view","Register-based composition","Symbolic colour coding","Incised relief carving"],"famous_works":["Tutankhamun funerary mask","Nefertiti bust (Berlin)","Tomb of Nefertari frescoes","Book of the Dead papyri"]},
            "Greek Classical Art": {"emoji":"🏛️","period":"5th–4th Century BCE","background":"Classical Greek art enshrined ideals of beauty, proportion, and naturalism in stone and bronze. Phidias and Praxiteles created a canon of the idealised human form that shaped Western aesthetics for two millennia.","importance":"Greek classical art established foundational principles of proportion, harmony, and naturalistic representation that defined Western artistic tradition from the Renaissance to the present.","restoration":"Ancient sculptures often survive as Roman marble copies of lost bronzes. Conservation involves careful stone cleaning, structural consolidation, and ethically contested decisions about reconstruction of missing limbs.","techniques":["Contrapposto naturalistic stance","Golden ratio proportions","Idealised anatomical accuracy","Bronze hollow lost-wax casting","Original polychromy (now largely lost)"],"famous_works":["Parthenon Elgin Marbles","Discobolus","Aphrodite of Melos","Winged Victory of Samothrace"]},
            "Aboriginal Australian Art": {"emoji":"🪃","period":"40,000+ years–Present","background":"Aboriginal art is humanity's oldest continuous artistic tradition — encoding Dreamtime cosmology, ancestral narrative, and country connection in rock paintings, body decoration, and dot paintings. Each mark carries living cultural knowledge.","importance":"Aboriginal art preserves tens of thousands of years of cultural memory. It is inseparable from land rights, spiritual law, and community identity — not merely aesthetic production.","restoration":"Conservation requires prior consultation with traditional custodians and respect for secret-sacred restrictions on certain imagery. Rock art in outdoor environments presents extreme long-term preservation challenges.","techniques":["Ochre pigment earth colours","X-ray internal anatomy style","Dot painting (acrylic revival)","Symbolic mapping of country","Layered narrative encoding"],"famous_works":["Bradshaw/Gwion rock paintings","X-ray art of Kakadu","Papunya Tula Western Desert movement","Wandjina spirit figures (Kimberley)"]}
        }

        if insight_type in cultural_insights:
            insight = cultural_insights[insight_type]

            st.markdown(f"""
            <div class="period-hero">
                <div class="period-emoji">{insight['emoji']}</div>
                <div>
                    <div class="period-name">{insight_type}</div>
                    <div class="period-era">📅 {insight['period']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_ins1, col_ins2 = st.columns([3, 2], gap="large")
            with col_ins1:
                for icon, title, content in [
                    ("📖", "Historical Background", insight['background']),
                    ("⭐", "Cultural Significance", insight['importance']),
                    ("🛠️", "Conservation Considerations", insight['restoration']),
                ]:
                    st.markdown(f"""
                    <div class="insight-card">
                        <div class="insight-card-title">{icon} {title}</div>
                        <div class="insight-card-body">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with col_ins2:
                st.markdown("""
                <div class="insight-card">
                    <div class="insight-card-title">🎨 Key Techniques</div>
                """, unsafe_allow_html=True)
                for t in insight['techniques']:
                    st.markdown(f'<span class="technique-tag">{t}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("""
                <div class="insight-card" style="margin-top:16px;">
                    <div class="insight-card-title">🖼️ Major Works</div>
                """, unsafe_allow_html=True)
                for w in insight['famous_works']:
                    st.markdown(f'<div class="work-item">{w}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 4: TIMELINE PLANNER ====================
    with tab4:
        st.markdown("""
        <div class="page-title-block">
            <div class="page-eyebrow">Project Planning Tool</div>
            <div class="page-title">Restoration <em>Timeline</em></div>
            <div class="page-desc">Configure your project parameters and receive a phased restoration schedule with risk assessments and expert scheduling recommendations.</div>
        </div>
        """, unsafe_allow_html=True)

        tl_col1, tl_col2 = st.columns(2)
        with tl_col1:
            st.markdown('<div class="section-label">Artwork Type</div>', unsafe_allow_html=True)
            tl_artwork_type = st.selectbox("", ["Oil Painting","Watercolor on Paper","Stone Sculpture","Bronze Sculpture","Textile / Tapestry","Illuminated Manuscript","Mural / Fresco","Ceramic / Pottery","Mixed Media"], key="tl_art_type", label_visibility="collapsed")
            st.markdown('<div class="section-label" style="margin-top:16px;">Damage Severity</div>', unsafe_allow_html=True)
            tl_damage_severity = st.select_slider("", options=["Minimal (surface dust/light scratches)","Moderate (fading, minor losses)","Significant (structural cracks, major losses)","Severe (major structural damage, 50%+ loss)","Critical (near-total deterioration)"], value="Moderate (fading, minor losses)", key="tl_damage", label_visibility="collapsed")
            st.markdown('<div class="section-label" style="margin-top:16px;">Artwork Scale</div>', unsafe_allow_html=True)
            tl_size = st.selectbox("", ["Small (< 30cm)","Medium (30–100cm)","Large (100–200cm)","Very Large (> 200cm)","Monumental (architectural scale)"], key="tl_size", label_visibility="collapsed")

        with tl_col2:
            st.markdown('<div class="section-label">Project Urgency</div>', unsafe_allow_html=True)
            tl_urgency = st.selectbox("", ["Flexible (timeline open)","Standard (6–12 months)","Priority (3–6 months)","Urgent (< 3 months)"], key="tl_urgency", label_visibility="collapsed")
            st.markdown('<div class="section-label" style="margin-top:16px;">Conservation Team</div>', unsafe_allow_html=True)
            tl_team_size = st.select_slider("", options=["Solo conservator","2–3 specialists","4–6 person team","Large institutional team (7+)"], value="2–3 specialists", key="tl_team", label_visibility="collapsed")
            st.markdown('<div class="section-label" style="margin-top:16px;">Project Goals</div>', unsafe_allow_html=True)
            tl_goals = st.multiselect("", ["Stabilisation only","Full visual restoration","Scientific documentation","Public exhibition prep","Digital archiving","Loan/transport preparation","Educational reproduction","Insurance documentation"], default=["Stabilisation only","Full visual restoration"], key="tl_goals", label_visibility="collapsed")

        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

        if st.button("Generate Timeline Plan", key="gen_timeline"):
            damage_map = {"Minimal (surface dust/light scratches)":(1,"LOW"),"Moderate (fading, minor losses)":(2,"MEDIUM"),"Significant (structural cracks, major losses)":(3,"HIGH"),"Severe (major structural damage, 50%+ loss)":(4,"HIGH"),"Critical (near-total deterioration)":(5,"HIGH")}
            size_map = {"Small (< 30cm)":0.7,"Medium (30–100cm)":1.0,"Large (100–200cm)":1.4,"Very Large (> 200cm)":1.8,"Monumental (architectural scale)":2.5}
            urgency_map = {"Flexible (timeline open)":1.0,"Standard (6–12 months)":0.85,"Priority (3–6 months)":0.65,"Urgent (< 3 months)":0.45}
            team_map = {"Solo conservator":1.3,"2–3 specialists":1.0,"4–6 person team":0.75,"Large institutional team (7+)":0.55}

            dmg_level, risk_base = damage_map[tl_damage_severity]
            size_f = size_map[tl_size]
            urg_f = urgency_map[tl_urgency]
            team_f = team_map[tl_team_size]

            def calc_weeks(base_w):
                return max(1, round(base_w * (dmg_level / 2) * size_f * urg_f * team_f))

            phases = [
                {"phase":"01","icon":"🔬","title":"Assessment & Documentation","weeks":calc_weeks(3),"tasks":[("Comprehensive visual inspection and condition mapping","HIGH"),("UV fluorescence, X-radiography, infrared reflectography","HIGH"),("Material sampling — pigment, substrate, binding media analysis","MEDIUM"),("Historical research and archival provenance study","MEDIUM"),("Photographic documentation (raking light, multispectral)","LOW")],"milestone":"Condition Report approved by stakeholders","deliverable":"Detailed Condition Report"},
                {"phase":"02","icon":"🛡️","title":"Emergency Stabilisation","weeks":calc_weeks(2),"tasks":[("Consolidation of flaking or delaminating paint layers","HIGH"),("Structural support for cracked or fragile substrate","HIGH"),("Facing of vulnerable areas prior to treatment","MEDIUM"),("Climate and environmental stabilisation measures","LOW")],"milestone":"Artwork structurally stable — safe to proceed","deliverable":"Stabilisation Report"},
                {"phase":"03","icon":"🧹","title":"Surface Cleaning & Preparation","weeks":calc_weeks(4),"tasks":[("Dry mechanical cleaning — removal of surface deposits","LOW"),("Solvent-based removal of discoloured varnish layers","HIGH"),("Aqueous cleaning where appropriate (pH controlled)","MEDIUM"),("Removal of previous incompatible restorations","HIGH"),("Final surface assessment of revealed original material","MEDIUM")],"milestone":"Original surface fully accessible and documented","deliverable":"Cleaning Records & Solubility Maps"},
                {"phase":"04","icon":"🔧","title":"Structural Conservation","weeks":calc_weeks(3) if dmg_level >= 3 else 0,"tasks":[("Substrate consolidation — relining, cradling, or backing","HIGH"),("Loss filling with conservation-grade fills","MEDIUM"),("Surface texture inpainting to match surrounding original","MEDIUM"),("Adhesive consolidation of all previously loose elements","LOW")],"milestone":"Structural integrity fully restored","deliverable":"Structural Treatment Report"},
                {"phase":"05","icon":"🎨","title":"Aesthetic Restoration & Inpainting","weeks":calc_weeks(5),"tasks":[("Colour matching and reference sample creation","HIGH"),("Inpainting of losses using reversible conservation media","HIGH"),("Texture recreation — integrating losses with original","HIGH"),("Intermediate varnish for optical unification","MEDIUM"),("Chromatic reintegration review with client/curator","MEDIUM")],"milestone":"Visual reintegration approved — aesthetic integrity restored","deliverable":"Inpainting Log & Photographic Record"},
                {"phase":"06","icon":"✅","title":"Final Varnish, Review & Handover","weeks":calc_weeks(2),"tasks":[("Application of final reversible UV-stable varnish","MEDIUM"),("Full post-treatment documentation photography","LOW"),("Preparation of comprehensive conservation treatment report","HIGH"),("Client review, sign-off, and formal handover","LOW"),("Long-term preventive conservation guidance issued","LOW")],"milestone":"Project complete — artwork delivered with full documentation","deliverable":"Final Conservation Report & Certificate"}
            ]

            active_phases = [p for p in phases if p['weeks'] > 0]
            total_weeks = sum(p['weeks'] for p in active_phases)
            total_months = round(total_weeks / 4.3, 1)

            # Stat strip
            st.markdown(f"""
            <div class="stat-strip">
                <div class="stat-cell"><div class="stat-val">{total_weeks}w</div><div class="stat-lbl">Total Duration</div></div>
                <div class="stat-cell"><div class="stat-val">{total_months}mo</div><div class="stat-lbl">Approx. Months</div></div>
                <div class="stat-cell"><div class="stat-val">{len(active_phases)}</div><div class="stat-lbl">Project Phases</div></div>
                <div class="stat-cell"><div class="stat-val">{risk_base}</div><div class="stat-lbl">Risk Level</div></div>
            </div>
            """, unsafe_allow_html=True)

            if tl_urgency == "Urgent (< 3 months)" and total_weeks > 12:
                st.warning(f"⚠ Urgent timeline selected but estimated duration is {total_weeks} weeks. Consider expanding the team or reducing scope.")

            st.markdown("""<div class="page-eyebrow" style="margin-bottom:20px;">Phase-by-Phase Schedule</div>""", unsafe_allow_html=True)

            dot_class = {"HIGH":"dot-high","MEDIUM":"dot-medium","LOW":"dot-low"}
            running_week = 0
            for i, phase in enumerate(active_phases):
                start_w = running_week + 1
                end_w = running_week + phase['weeks']
                running_week = end_w

                tasks_html = ""
                for task, priority in phase['tasks']:
                    tasks_html += f"""
                    <div class="phase-task">
                        <div class="priority-dot {dot_class[priority]}"></div>
                        <span>{task}</span>
                    </div>"""

                st.markdown(f"""
                <div class="phase-block">
                    <div class="phase-left">
                        <div>
                            <div class="phase-num">Phase {phase['phase']}</div>
                            <div class="phase-icon-big">{phase['icon']}</div>
                            <div class="phase-name">{phase['title']}</div>
                        </div>
                        <div class="phase-weeks">Wks {start_w}–{end_w} &nbsp;·&nbsp; {phase['weeks']}w</div>
                    </div>
                    <div class="phase-right">
                        {tasks_html}
                        <div class="phase-milestone">
                            <div class="milestone-label">Milestone</div>
                            {phase['milestone']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Recommendations
            st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
            st.markdown("""<div class="page-eyebrow" style="margin-bottom:16px;">Planning Recommendations</div>""", unsafe_allow_html=True)

            rec_items = []
            if dmg_level >= 4:
                rec_items.append(("🚨","HIGH","#8b3a2a","Immediate structural stabilisation is critical. Do not proceed to cleaning before all fragile elements are secured."))
            if "Scientific documentation" in tl_goals:
                rec_items.append(("🔬","MEDIUM","#b8963e","Allow 2–3 additional weeks for laboratory analysis turnaround. Partner with a university conservation science department."))
            if "Public exhibition prep" in tl_goals:
                rec_items.append(("🖼️","MEDIUM","#b8963e","Build a 4-week buffer before the exhibition date. Final varnish requires two weeks to cure under stable conditions."))
            if tl_urgency in ["Priority (3–6 months)","Urgent (< 3 months)"]:
                rec_items.append(("⚡","HIGH","#8b3a2a","Compressed timeline increases risk. Consider enlarging the team or reducing scope to essential stabilisation only."))
            rec_items.append(("📋","LOW","#2a6b6e","Document every intervention in a running treatment log. Photographs before, during, and after each phase are mandatory."))
            rec_items.append(("🌡️","LOW","#2a6b6e","Maintain stable environment throughout: 18–22°C, 45–55% RH. Fluctuations undo treatment gains rapidly."))
            if "Digital archiving" in tl_goals:
                rec_items.append(("💾","LOW","#2a6b6e","Schedule multispectral imaging at end of Phase 3 (cleaned, pre-inpainting) for the highest-quality archival record."))

            for icon, priority, color, text in rec_items:
                st.markdown(f"""
                <div class="rec-item" style="border-left-color:{color};">
                    <div class="rec-icon">{icon}</div>
                    <div class="rec-body">
                        <div class="rec-priority" style="color:{color};">{priority}</div>
                        {text}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Download
            timeline_export = f"""CONSERVE — RESTORATION TIMELINE PLAN
{"="*56}
Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}

PROJECT PARAMETERS
Artwork Type:  {tl_artwork_type}
Damage:        {tl_damage_severity}
Scale:         {tl_size}
Team:          {tl_team_size}
Urgency:       {tl_urgency}
Goals:         {', '.join(tl_goals)}

SUMMARY
Total Duration:  {total_weeks} weeks (~{total_months} months)
Phases:          {len(active_phases)}
Risk Level:      {risk_base}

PHASES
"""
            rw = 0
            for ph in active_phases:
                sw = rw + 1; ew = rw + ph['weeks']; rw = ew
                timeline_export += f"\nPhase {ph['phase']}: {ph['title']}\nWeeks {sw}–{ew} ({ph['weeks']} weeks)\n"
                for t, p in ph['tasks']:
                    timeline_export += f"  [{p}] {t}\n"
                timeline_export += f"Milestone: {ph['milestone']}\nDeliverable: {ph['deliverable']}\n"

            st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
            st.download_button(
                label="Download Timeline Plan",
                data=timeline_export,
                file_name=f"CONSERVE_Timeline_{tl_artwork_type.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                key="dl_timeline"
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== RESULTS PAGE ====================
elif st.session_state.page == 'results':
    render_header()

    st.markdown("""
    <div class="result-header">
        <div class="result-tag">Analysis Complete</div>
        <div class="result-title">Restoration<br><em>Report</em></div>
        <div class="result-body">Expert conservation guidance generated for your submitted artwork</div>
    </div>
    """, unsafe_allow_html=True)

    col_dl, col_back = st.columns([1, 5])
    with col_dl:
        st.download_button(
            label="Export Report",
            data=f"""CONSERVE — RESTORATION ANALYSIS REPORT\n{"="*56}\nDATE: {datetime.now().strftime('%B %d, %Y')}\n\n{st.session_state.result_text}\n{"="*56}\nGenerated by CONSERVE · Cultural Heritage Preservation\nThis analysis is advisory only. Always consult certified conservators.\n""",
            file_name=f"CONSERVE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_report"
        )

    # Format and render result
    result = st.session_state.result_text
    sections = result.split('─────────────────────────────────────────────────────────')
    
    st.markdown('<div class="result-content-wrap">', unsafe_allow_html=True)
    for i, section in enumerate(sections):
        s = section.strip()
        if not s:
            continue
        lines = s.split('\n')
        head = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        if i == 0:
            st.markdown(f'<div class="result-text" style="font-size:15px;color:var(--text-muted);margin-bottom:24px;">{s}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-section-head">{head}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-text">{body}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("← Analyse Another Artwork", key="back_btn"):
            st.session_state.page = 'main'
            st.rerun()

    # Feedback
    st.markdown("""
    <div class="feedback-wrap">
        <div class="page-eyebrow">Share Your Experience</div>
        <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:600;color:var(--text-primary);margin-bottom:4px;">Help Improve CONSERVE</div>
        <div style="font-family:'Crimson Pro',serif;font-size:16px;color:var(--text-muted);font-style:italic;margin-bottom:24px;">Your feedback shapes the future of this platform</div>
    """, unsafe_allow_html=True)

    col_fb1, col_fb2, col_fb3 = st.columns([1,1,1])
    with col_fb2:
        if st.button("Open Feedback Form", key="open_feedback_results"):
            st.session_state.show_feedback_results = True

    if 'show_feedback_results' not in st.session_state:
        st.session_state.show_feedback_results = False

    if st.session_state.show_feedback_results:
        fb_col1, fb_col2 = st.columns(2)
        with fb_col1:
            st.markdown('<div class="section-label">Your Name</div>', unsafe_allow_html=True)
            feedback_name = st.text_input("", key="feedback_name_results", placeholder="Enter your name", label_visibility="collapsed")
            st.markdown('<div class="section-label" style="margin-top:12px;">Email (Optional)</div>', unsafe_allow_html=True)
            feedback_email = st.text_input("", key="feedback_email_results", placeholder="your@email.com", label_visibility="collapsed")
            st.markdown('<div class="section-label" style="margin-top:12px;">Rating</div>', unsafe_allow_html=True)
            feedback_rating = st.select_slider("", options=["⭐ Poor","⭐⭐ Fair","⭐⭐⭐ Good","⭐⭐⭐⭐ Very Good","⭐⭐⭐⭐⭐ Excellent"], value="⭐⭐⭐ Good", key="feedback_rating_results", label_visibility="collapsed")
        with fb_col2:
            st.markdown('<div class="section-label">Category</div>', unsafe_allow_html=True)
            feedback_category = st.selectbox("", ["General Feedback","Feature Request","Bug Report","Accuracy of Analysis","User Experience","Other"], key="feedback_category_results", label_visibility="collapsed")
            st.markdown('<div class="section-label" style="margin-top:12px;">Recommend?</div>', unsafe_allow_html=True)
            feedback_recommend = st.radio("", ["👍 Yes","🤔 Maybe","👎 No"], horizontal=True, key="feedback_recommend_results", label_visibility="collapsed")
        st.markdown('<div class="section-label" style="margin-top:12px;">Comments & Suggestions</div>', unsafe_allow_html=True)
        feedback_comments = st.text_area("", placeholder="Share your thoughts...", height=120, key="feedback_comments_results", label_visibility="collapsed")

        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("Cancel", key="cancel_feedback_results"):
                st.session_state.show_feedback_results = False
                st.rerun()
        with btn_c2:
            if st.button("Submit Feedback", key="submit_feedback_results"):
                if feedback_name and feedback_comments:
                    st.success("✓ Thank you. Your feedback has been recorded.")
                    import time; time.sleep(2)
                    st.session_state.show_feedback_results = False
                    st.rerun()
                else:
                    st.error("Please provide your name and comments.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:32px;margin-top:0;">
        <span style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:0.25em;color:var(--text-muted);text-transform:uppercase;">
            CONSERVE Studio &nbsp;·&nbsp; Powered by OpenAI &nbsp;·&nbsp; Cultural Heritage Preservation
        </span>
    </div>
    """, unsafe_allow_html=True)
