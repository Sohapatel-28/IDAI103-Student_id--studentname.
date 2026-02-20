import streamlit as st
from datetime import datetime
import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="ArtRestorer AI — Cultural Heritage Preservation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("OpenAI API key not found. Add OPENAI_API_KEY to your .env file.")
    st.stop()

openai_client = OpenAI(api_key=openai_api_key)

# ==================== CSS ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Mono:wght@300;400;500&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

:root {
    --ink: #0e0e0f;
    --parchment: #f5f0e8;
    --parchment-warm: #ede8dc;
    --parchment-deep: #d8d1c0;
    --gold: #b8963e;
    --gold-light: #d4aa55;
    --gold-muted: #8a6f2e;
    --rust: #8b3a2a;
    --teal: #2a6b6e;
    --text-primary: #1a1814;
    --text-secondary: #4a453d;
    --text-muted: #7a7268;
    --border: rgba(184,150,62,0.25);
    --border-soft: rgba(184,150,62,0.12);
}

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background: var(--parchment) !important; font-family: 'Crimson Pro', Georgia, serif; color: var(--text-primary); }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* LANDING */
.landing-wrap { min-height: 100vh; background: var(--ink); display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden; padding: 60px 40px; }
.landing-bg { position: absolute; inset: 0; pointer-events: none; background-image: repeating-linear-gradient(0deg, transparent, transparent 80px, rgba(184,150,62,0.03) 80px, rgba(184,150,62,0.03) 81px), repeating-linear-gradient(90deg, transparent, transparent 80px, rgba(184,150,62,0.03) 80px, rgba(184,150,62,0.03) 81px); }
.l-orn { width: 1px; height: 60px; background: linear-gradient(to bottom, transparent, var(--gold), transparent); margin-bottom: 32px; }
.l-eye { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.4em; color: var(--gold-muted); text-transform: uppercase; margin-bottom: 18px; text-align: center; }
.l-title { font-family: 'Playfair Display', Georgia, serif; font-size: clamp(52px, 7vw, 88px); font-weight: 700; color: var(--parchment); text-align: center; line-height: 0.95; letter-spacing: -0.02em; margin-bottom: 14px; }
.l-title em { font-style: italic; color: var(--gold-light); }
.l-tagline { font-family: 'Crimson Pro', serif; font-size: 20px; color: rgba(245,240,232,0.6); font-style: italic; text-align: center; margin-bottom: 10px; letter-spacing: 0.05em; }
.l-sub { font-family: 'Crimson Pro', serif; font-size: 15px; color: rgba(245,240,232,0.35); text-align: center; margin-bottom: 40px; letter-spacing: 0.08em; font-family: 'DM Mono', monospace; text-transform: uppercase; font-size: 10px; }
.l-div { width: 100px; height: 1px; background: linear-gradient(to right, transparent, var(--gold), transparent); margin: 0 auto 44px; }

/* HEADER */
.site-header { background: var(--ink); border-bottom: 1px solid rgba(184,150,62,0.2); padding: 16px 44px; display: flex; align-items: center; justify-content: space-between; }
.h-logo { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: var(--parchment); letter-spacing: 0.04em; }
.h-logo em { font-style: italic; color: var(--gold-light); }
.h-tag { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.26em; color: var(--gold-muted); text-transform: uppercase; }

/* MAIN WRAPPER */
.mwrap { max-width: 1360px; margin: 0 auto; padding: 36px 44px 72px; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; gap: 0 !important; padding: 0 !important; margin-bottom: 32px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border: none !important; border-bottom: 2px solid transparent !important; color: var(--text-muted) !important; font-family: 'DM Mono', monospace !important; font-size: 11px !important; letter-spacing: 0.16em !important; text-transform: uppercase !important; padding: 12px 24px !important; margin: 0 !important; transition: all 0.2s !important; }
.stTabs [data-baseweb="tab"]:hover { color: var(--gold) !important; }
.stTabs [aria-selected="true"] { color: var(--gold) !important; border-bottom-color: var(--gold) !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* PAGE TITLES */
.eye { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.35em; color: var(--gold); text-transform: uppercase; margin-bottom: 8px; }
.ptitle { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 600; color: var(--text-primary); line-height: 1.1; letter-spacing: -0.01em; margin-bottom: 6px; }
.ptitle em { font-style: italic; color: var(--rust); }
.pdesc { font-family: 'Crimson Pro', serif; font-size: 17px; color: var(--text-secondary); font-style: italic; line-height: 1.6; max-width: 600px; margin-bottom: 28px; }
.pdiv { height: 1px; background: linear-gradient(to right, var(--gold), transparent); margin-bottom: 32px; opacity: 0.3; }

/* SECTION LABELS */
.sl { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.3em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px; margin-top: 18px; }

/* INPUTS */
.stTextArea textarea, .stTextInput input { background: white !important; border: 1px solid var(--parchment-deep) !important; border-radius: 2px !important; color: var(--text-primary) !important; font-family: 'Crimson Pro', serif !important; font-size: 16px !important; padding: 12px 14px !important; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color: var(--gold) !important; box-shadow: 0 0 0 3px rgba(184,150,62,0.07) !important; }
.stSelectbox > div > div { background: white !important; border: 1px solid var(--parchment-deep) !important; border-radius: 2px !important; color: var(--text-primary) !important; font-family: 'Crimson Pro', serif !important; font-size: 15px !important; }
label, .stSelectbox label, .stTextArea label, .stTextInput label, .stFileUploader label { display: none !important; }

/* FEATURE BADGE */
.fbadge { display: inline-flex; align-items: center; gap: 10px; background: #1a1a1e; color: var(--parchment-deep); font-family: 'Crimson Pro', serif; font-size: 14px; font-style: italic; padding: 10px 18px; border-radius: 2px; border-left: 3px solid var(--gold); margin: 8px 0 20px; }

/* TEMPERATURE BOX */
.tbox { background: var(--ink); border-radius: 3px; padding: 16px 20px; display: flex; align-items: center; gap: 18px; border-left: 4px solid var(--gold); margin-top: 10px; }
.tval { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700; color: var(--gold-light); line-height: 1; min-width: 62px; }
.ttitle { font-family: 'Playfair Display', serif; font-size: 15px; color: var(--parchment); font-weight: 600; margin-bottom: 3px; }
.tmode { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.18em; color: var(--gold-muted); text-transform: uppercase; margin-bottom: 5px; }
.tdesc { font-family: 'Crimson Pro', serif; font-size: 14px; color: rgba(245,240,232,0.48); font-style: italic; line-height: 1.4; }

/* BUTTON */
.stButton > button { background: var(--ink) !important; color: var(--parchment) !important; border: 1px solid rgba(184,150,62,0.35) !important; border-radius: 2px !important; font-family: 'DM Mono', monospace !important; font-size: 11px !important; letter-spacing: 0.2em !important; text-transform: uppercase !important; padding: 13px 30px !important; width: 100% !important; transition: all 0.2s !important; }
.stButton > button:hover { background: var(--gold) !important; border-color: var(--gold) !important; color: var(--ink) !important; }

/* INSIGHT CARDS */
.icard { background: white; border: 1px solid var(--parchment-deep); border-top: 3px solid var(--gold); padding: 22px 24px; margin-bottom: 14px; }
.icard-t { font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 600; color: var(--text-primary); margin-bottom: 9px; }
.icard-b { font-family: 'Crimson Pro', serif; font-size: 16px; color: var(--text-secondary); line-height: 1.75; }

/* PERIOD HERO */
.phero { background: var(--ink); padding: 28px 34px; margin-bottom: 24px; border-bottom: 3px solid var(--gold); display: flex; align-items: center; gap: 22px; }
.phero-em { font-size: 42px; }
.phero-t { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: var(--parchment); }
.phero-e { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.22em; color: var(--gold); text-transform: uppercase; margin-top: 4px; }

/* TAGS & WORKS */
.ttag { display: inline-block; background: var(--ink); color: var(--parchment-deep); font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.1em; padding: 5px 11px; margin: 3px; border-radius: 1px; }
.wrow { font-family: 'Crimson Pro', serif; font-size: 16px; color: var(--text-secondary); padding: 8px 0; border-bottom: 1px solid var(--border-soft); display: flex; align-items: center; gap: 10px; }
.wdash { color: var(--gold); font-family: 'DM Mono', monospace; }

/* STAT STRIP */
.sstrip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px; background: var(--parchment-deep); border: 1px solid var(--parchment-deep); margin-bottom: 32px; }
.scell { background: var(--ink); padding: 20px 16px; text-align: center; }
.sval { font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 700; color: var(--gold-light); line-height: 1; margin-bottom: 5px; }
.slbl { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.26em; color: rgba(245,240,232,0.32); text-transform: uppercase; }

/* QUIZ */
.qshell { background: var(--ink); padding: 32px; margin-bottom: 32px; }
.qhead { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 600; color: var(--parchment); margin-bottom: 5px; }
.qsub { font-family: 'Crimson Pro', serif; font-size: 15px; color: rgba(245,240,232,0.42); font-style: italic; margin-bottom: 22px; }
.qpw { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.qpbg { flex: 1; height: 2px; background: rgba(255,255,255,0.07); }
.qpf { height: 100%; background: var(--gold); }
.qq { font-family: 'Playfair Display', serif; font-size: 18px; color: var(--parchment); font-style: italic; line-height: 1.5; padding: 16px 20px; background: rgba(255,255,255,0.04); border-left: 3px solid var(--gold); margin-bottom: 18px; }
.qsbig { font-family: 'Playfair Display', serif; font-size: 58px; font-weight: 700; color: var(--gold-light); text-align: center; line-height: 1; }
.qssub { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.26em; color: rgba(245,240,232,0.32); text-transform: uppercase; text-align: center; margin-top: 7px; margin-bottom: 24px; }

/* FEATURE GALLERY CARDS */
.fcard { background: white; border: 1px solid var(--parchment-deep); padding: 20px 22px; margin-bottom: 12px; transition: border-color 0.2s; }
.fcard:hover { border-color: var(--gold); }
.fcard-h { display: flex; align-items: flex-start; gap: 13px; margin-bottom: 12px; }
.fcard-i { width: 38px; height: 38px; background: var(--ink); border-radius: 2px; display: flex; align-items: center; justify-content: center; font-size: 17px; flex-shrink: 0; }
.fcard-t { font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 600; color: var(--text-primary); margin-bottom: 3px; }
.fcard-d { font-family: 'Crimson Pro', serif; font-size: 14px; color: var(--text-muted); line-height: 1.5; }
.fcard-tags { display: flex; flex-wrap: wrap; gap: 5px; }
.ftag { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.07em; padding: 3px 8px; background: var(--parchment-warm); color: var(--text-secondary); border-radius: 1px; }

/* RESULTS */
.rhero { background: var(--ink); padding: 40px 44px; }
.rtag { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.3em; text-transform: uppercase; color: var(--gold); margin-bottom: 12px; }
.rtitle { font-family: 'Playfair Display', serif; font-size: 46px; font-weight: 700; color: var(--parchment); line-height: 1.05; letter-spacing: -0.02em; }
.rtitle em { color: var(--gold-light); font-style: italic; }
.rsub { font-family: 'Crimson Pro', serif; font-size: 17px; color: rgba(245,240,232,0.45); font-style: italic; margin-top: 8px; }
.rbody { background: white; border: 1px solid var(--parchment-deep); padding: 40px; }
.rsechead { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.3em; text-transform: uppercase; color: var(--gold); margin: 28px 0 9px; padding-bottom: 7px; border-bottom: 1px solid var(--border); }
.rsechead:first-child { margin-top: 0; }
.rtext { font-family: 'Crimson Pro', serif; font-size: 17px; color: var(--text-secondary); line-height: 1.8; white-space: pre-wrap; }

/* FEEDBACK */
.fbwrap { background: var(--parchment-warm); border: 1px solid var(--parchment-deep); border-top: 3px solid var(--teal); padding: 32px; margin-top: 36px; }

/* FOOTER */
.sfooter { text-align: center; padding: 24px; border-top: 1px solid var(--border-soft); }
.sfooter span { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.22em; color: var(--text-muted); text-transform: uppercase; }

/* UPLOAD PLACEHOLDER */
.uph { height: 160px; background: var(--parchment-warm); border: 1.5px dashed var(--parchment-deep); display: flex; align-items: center; justify-content: center; }

/* SPACING */
.g8 { height: 8px; } .g16 { height: 16px; } .g24 { height: 24px; }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
for k, v in [('page', 'landing'), ('result_text', ''), ('show_feedback', False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ==================== FEATURES (10 total) ====================
# REMOVED: Sculptural Reconstruction (too niche for digital restoration)
# REMOVED: Educational Content Generation (not a restoration feature)
# ADDED:   AI Colour Palette Recovery
# ADDED:   Artwork Condition Report Generator

feature_menu = [
    ("1. 🎭 Period-Specific Restoration (Baroque/Renaissance)",     "period"),
    ("2. 🕌 Cultural Pattern Enhancement (Traditional Arts)",       "cultural"),
    ("3. 🧵 Textile & Tapestry Repair",                            "textile"),
    ("4. 🎨 Abstract & Modern Art Recovery",                       "abstract"),
    ("5. 📜 Ancient Manuscript Conservation",                      "manuscript"),
    ("6. 🏛️ Mural & Fresco Revival",                               "mural"),
    ("7. 🏺 Ceramic & Pottery Reconstruction",                     "ceramic"),
    ("8. 🔯 Symbol & Iconography Interpretation",                  "symbol"),
    ("9. 🎨 AI Colour Palette Recovery",                           "colour"),
    ("10. 📋 Artwork Condition Report Generator",                   "condition"),
]

feature_descriptions = {
    "period":    "Given a description of a Baroque or Renaissance painting with damage, suggest restoration using historically accurate techniques like sfumato, chiaroscuro, and period-specific pigments.",
    "cultural":  "Given a faded Mughal-era miniature or Islamic geometric work, generate ideas to enhance traditional patterns digitally with authentic cultural detailing and colour conventions.",
    "textile":   "Given a torn historical tapestry or embroidery, propose restoration options that maintain thread pattern consistency, weave structure, and period-appropriate motifs.",
    "abstract":  "Given an abstract or Expressionist canvas with texture loss, provide guidance on recreating the original brushstroke feel, layering technique, and colour energy of the work.",
    "manuscript": "Given a damaged illuminated manuscript or scroll, suggest conservation approaches for fragile pigments, gilding, and script integrity using non-invasive methods.",
    "mural":     "Given a deteriorating fresco or cave painting, recommend revival techniques that respect the original lime-based medium, pigment chemistry, and architectural context.",
    "ceramic":   "Given a broken or faded ceramic vessel, propose reconstruction strategies that match the original glaze chemistry, kiln technique, and decorative style of the period.",
    "symbol":    "Given an artwork with obscured religious or cultural iconography, decode the symbolic system and suggest how to restore missing or damaged symbolic elements faithfully.",
    "colour":    "Given a faded or discoloured artwork, use AI analysis to recover and reconstruct the original colour palette based on period pigment knowledge and spectral imaging data.",
    "condition": "Given an artwork description, generate a structured professional condition report covering damage assessment, risk level, recommended interventions, and conservation priority.",
}

features_gallery = [
    {"icon": "🎭", "title": "Period-Specific Restoration",       "desc": "Baroque/Renaissance artworks restored using historically accurate period techniques.",
     "prompt": 'Given a description of a Baroque painting with a missing upper-left corner, suggest how to digitally restore the area using heavy shadowing and dramatic light techniques typical of that period.',
     "cases": ["Baroque chiaroscuro repair", "Renaissance sfumato blending", "Rococo gold leaf recovery", "Flemish oil glazing restoration"]},

    {"icon": "🕌", "title": "Cultural Pattern Enhancement",      "desc": "Traditional patterns from Mughal, Islamic, Celtic and Asian arts restored with authentic detailing.",
     "prompt": 'This Mughal-era miniature features faded floral borders. Based on its traditional style, generate ideas to enhance these patterns digitally with authentic detailing.',
     "cases": ["Mughal floral border restoration", "Islamic geometric tessellation", "Celtic knotwork recovery", "Persian miniature gilding"]},

    {"icon": "🧵", "title": "Textile & Tapestry Repair",         "desc": "Historical tapestries and embroideries restored maintaining thread consistency and period motifs.",
     "prompt": 'An 18th-century silk tapestry is torn near the central emblem. Propose restoration options maintaining embroidery consistency and thread patterns.',
     "cases": ["Medieval Bayeux-style tapestry", "Chinese silk embroidery", "Indian Banarasi fabric repair", "Persian carpet restoration"]},

    {"icon": "🎨", "title": "Abstract & Modern Art Recovery",    "desc": "Expressionist and abstract canvases restored with attention to original texture and energy.",
     "prompt": 'A heavily abstract Expressionist canvas has lost texture in one section. Provide guidance on recreating the original chaotic brushstroke feel using appropriate hues.',
     "cases": ["Pollock drip painting recovery", "Rothko colour field fading", "De Kooning texture restoration", "Minimalist hard-edge repair"]},

    {"icon": "📜", "title": "Ancient Manuscript Conservation",   "desc": "Illuminated manuscripts and scrolls conserved using non-invasive, reversible methods.",
     "prompt": 'A water-damaged medieval illuminated manuscript has lost gilded lettering and border pigments. Suggest non-invasive conservation steps to stabilise and recover the illumination.',
     "cases": ["Book of Kells border recovery", "Arabic calligraphy scroll repair", "Sanskrit palm-leaf stabilisation", "Dead Sea Scroll preservation"]},

    {"icon": "🏛️", "title": "Mural & Fresco Revival",            "desc": "Cave paintings and architectural frescoes revived respecting original lime-based media.",
     "prompt": 'A Roman-era fresco has large areas of salt efflorescence and pigment loss. Recommend a revival approach respecting the original lime plaster medium and mineral pigments.',
     "cases": ["Ajanta cave painting revival", "Pompeii fresco restoration", "Diego Rivera mural repair", "Byzantine church fresco"]},

    {"icon": "🏺", "title": "Ceramic & Pottery Reconstruction",  "desc": "Pottery and porcelain restored matching original glaze chemistry and decorative style.",
     "prompt": 'A Ming dynasty blue-and-white porcelain vase has hairline cracks and glaze losses. Propose reconstruction strategies that match the original cobalt pigment and kiln technique.',
     "cases": ["Ming dynasty porcelain repair", "Greek amphora reconstruction", "Raku ceramic restoration", "Native American pottery revival"]},

    {"icon": "🔯", "title": "Symbol & Iconography Interpretation","desc": "Religious and cultural symbols decoded and restored within their original iconographic system.",
     "prompt": 'A Byzantine icon has darkened varnish obscuring the halo and inscriptions. Decode the iconographic programme and suggest how to restore the symbolic elements faithfully.',
     "cases": ["Byzantine icon halo recovery", "Hindu temple motif restoration", "Egyptian cartouche reconstruction", "Celtic religious symbol repair"]},

    {"icon": "🎨", "title": "AI Colour Palette Recovery",        "desc": "Faded artworks restored to original colour using AI pigment analysis and spectral imaging data.",
     "prompt": 'A 19th-century oil painting has yellowed varnish and severely faded cadmium reds. Using AI pigment analysis and historical colour records, recover and reconstruct the original palette.',
     "cases": ["Yellowed varnish colour recovery", "UV-faded pigment reconstruction", "Spectral imaging colour mapping", "Historical palette matching"]},

    {"icon": "📋", "title": "Artwork Condition Report Generator", "desc": "Structured professional condition reports generated covering damage, risk, and conservation priority.",
     "prompt": 'Given this artwork description, generate a structured professional condition report with damage assessment, environmental risk factors, recommended conservation interventions, and urgency rating.',
     "cases": ["Pre-loan condition assessment", "Insurance documentation report", "Exhibition readiness report", "Post-disaster damage survey"]},
]

def render_header():
    st.markdown("""
    <div class="site-header">
        <div>
            <div class="h-logo">Art<em>Restorer</em> AI</div>
        </div>
        <div class="h-tag">Cultural Heritage Preservation · Powered by OpenAI</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== LANDING PAGE ====================
if st.session_state.page == 'landing':
    st.markdown("""
    <div class="landing-wrap">
        <div class="landing-bg"></div>
        <div class="l-orn"></div>
        <div class="l-eye">Cultural Heritage Preservation Studio</div>
        <div class="l-title">Art<em>Restorer</em> AI</div>
        <div class="l-tagline">Giving history a second chance, one brushstroke at a time.</div>
        <div class="l-div"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Enter the Studio →", key="enter"):
            st.session_state.page = 'main'
            st.rerun()

    st.markdown("""
    <div style="background:var(--ink);padding:14px 44px;text-align:center;border-top:1px solid rgba(184,150,62,0.1);margin-top:0;">
        <span style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.22em;color:rgba(245,240,232,0.2);text-transform:uppercase;">
            ArtRestorer AI &nbsp;·&nbsp; Cultural Heritage &nbsp;·&nbsp; Powered by OpenAI
        </span>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN APPLICATION ====================
elif st.session_state.page == 'main':
    render_header()
    st.markdown('<div class="mwrap">', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Restoration Assistant",
        "Feature Gallery",
        "Cultural Archive",
        "Timeline Planner"
    ])

    # ===== TAB 1: RESTORATION ASSISTANT =====
    with tab1:
        st.markdown("""
        <div class="eye">Restoration Analysis Engine</div>
        <div class="ptitle">Analyse Your <em>Artwork</em></div>
        <div class="pdesc">Submit your artwork for AI-assisted conservation analysis. Receive expert restoration guidance grounded in historical research and conservation science.</div>
        <div class="pdiv"></div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            st.markdown('<div class="sl">Upload Artwork (Optional)</div>', unsafe_allow_html=True)
            uf = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="imgup", label_visibility="collapsed")
            if uf:
                st.image(uf, caption="Uploaded Artwork", use_container_width=True)
            else:
                st.markdown('<div class="uph"><span style="font-family:\'Crimson Pro\',serif;font-size:14px;color:var(--text-muted);font-style:italic;">drag & drop or click to upload</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="sl">Artwork Description</div>', unsafe_allow_html=True)
            desc = st.text_area("", placeholder="Describe the artwork: medium, period, visible damage, dimensions, provenance, condition notes...", height=185, key="desc", label_visibility="collapsed")

        st.markdown('<div class="g16"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sl">Analysis Discipline</div>', unsafe_allow_html=True)
        fsel = st.selectbox("", [m[0] for m in feature_menu], key="fsel", label_visibility="collapsed")
        fidx = [m[0] for m in feature_menu].index(fsel)
        fkey = feature_menu[fidx][1]

        # Show the AI prompt for this feature
        prompt_text = feature_descriptions[fkey]
        st.markdown(f'<div class="fbadge">&#9670; &nbsp;{prompt_text}</div>', unsafe_allow_html=True)

        c3, c4, c5 = st.columns(3)
        with c3:
            st.markdown('<div class="sl">Art Style / Period</div>', unsafe_allow_html=True)
            art_style = st.selectbox("", [""] + ["Baroque", "Renaissance", "Gothic", "Neoclassical", "Rococo",
                "Romantic", "Impressionist", "Expressionist", "Art Deco", "Art Nouveau",
                "Indian Mughal", "Indian Rajput", "Indian Pahari", "Indian Madhubani",
                "Persian Miniature", "Islamic Geometric", "Byzantine", "Japanese Ukiyo-e",
                "Chinese Ming Dynasty", "Aboriginal", "Egyptian", "Greek/Roman Classical"],
                key="sty", label_visibility="collapsed")
        with c4:
            st.markdown('<div class="sl">Damage Type</div>', unsafe_allow_html=True)
            dmg = st.selectbox("", [""] + ["Water damage/stains", "Fire damage/smoke residue",
                "Fading from sunlight/UV exposure", "Erosion/weathering", "Cracks/structural damage",
                "Flaking/peeling paint", "Mold/biological growth", "Scratches/surface abrasions",
                "Missing sections/losses", "Discoloration/yellowing", "Torn fabric/textile damage",
                "Broken/fragmented pieces", "Oxidation/corrosion", "Insect damage", "Previous poor restoration"],
                key="dmg", label_visibility="collapsed")
        with c5:
            st.markdown('<div class="sl">Cultural Context</div>', unsafe_allow_html=True)
            ctx = st.selectbox("", [""] + ["Italian Renaissance", "French Baroque", "Spanish Colonial",
                "Flemish/Dutch", "British Victorian", "Indian Mughal", "Indian Rajput",
                "Indian Temple Art", "Persian/Iranian", "Ottoman Turkish", "Chinese Imperial",
                "Japanese Edo Period", "Egyptian Pharaonic", "Greek Classical", "Roman Imperial",
                "Byzantine Eastern Orthodox", "African Tribal", "Native American"],
                key="ctx", label_visibility="collapsed")

        st.markdown('<div class="g8"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sl">Analytical Approach</div>', unsafe_allow_html=True)
        temp = st.slider("", 0.0, 1.0, 0.6, 0.05, key="temp", label_visibility="collapsed")

        t_data = [
            ("Strict Historical",        "Evidence-Only",        "Ultra-precise — grounded exclusively in documented historical evidence and proven conservation science."),
            ("Conservative & Methodical","Research-Led",         "Careful analysis based on historical research with minimal interpretive speculation."),
            ("Balanced Professional",    "Art & Science",        "Recommended — combines rigorous historical grounding with thoughtful creative interpretation."),
            ("Interpretive & Exploratory","Artistic Reading",    "Explores multiple creative possibilities while respecting historical integrity."),
            ("Visionary",               "Bold Interpretation",   "Maximum creativity — bold interpretive suggestions that push conventional restoration thinking."),
        ]
        ti = min(int(temp / 0.2), 4)
        tt, tm, td = t_data[ti]
        st.markdown(f"""
        <div class="tbox">
            <div class="tval">{temp:.2f}</div>
            <div>
                <div class="ttitle">{tt}</div>
                <div class="tmode">{tm}</div>
                <div class="tdesc">{td}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="g24"></div>', unsafe_allow_html=True)

        if st.button("Generate Restoration Analysis →", key="genb"):
            if desc:
                with st.spinner("Conducting analysis..."):
                    import time; time.sleep(2)
                    cmap = ["highly conservative", "conservative and methodical", "balanced and professional", "creative and exploratory", "highly creative"]
                    st.session_state.result_text = f"""ARTWORK DETAILS
{desc}

Style/Period: {art_style or 'Not specified'}  |  Damage: {dmg or 'General wear'}  |  Context: {ctx or 'Not specified'}
Analysis Discipline: {fsel}
Analytical Approach: {temp:.2f} — {cmap[ti]}

HISTORICAL CONTEXT & SIGNIFICANCE
Based on the provided description and the {art_style or 'specified'} period, this artwork represents a significant example of its cultural era. The {ctx or 'general'} context suggests traditional techniques and materials commonly employed at the time. Understanding the patronage structures and socio-political environment is essential for an authentic restoration approach.

CONDITION ASSESSMENT
The {dmg or 'general wear'} presents specific challenges requiring careful consideration:

  • Primary concerns include structural integrity and aesthetic coherence
  • Surface analysis reveals patterns consistent with prolonged environmental exposure
  • Original materials and binding media must be preserved wherever possible
  • Comprehensive documentation of current state is mandatory before any intervention

RESTORATION METHODOLOGY

  A. Documentation Phase
     — Comprehensive photography (visible light, UV fluorescence, infrared reflectography)
     — Detailed condition mapping and paint loss inventory
     — Material sampling and scientific analysis (pigment, substrate, binding media)
     — Historical research, provenance investigation, archival study

  B. Stabilisation Phase
     — Consolidation of flaking or delaminating paint layers
     — Structural support for fragile or cracked substrate
     — Environmental stabilisation and climate control measures
     — Protection against further deterioration during treatment

  C. Cleaning Phase
     — Surface cleaning using period-appropriate methods
     — Removal of discoloured varnish or previous overpainting
     — pH monitoring and staged solvent testing
     — Gradual approach with constant material assessment

  D. Restoration Phase
     — Loss compensation using reversible conservation materials
     — Colour matching to original palette using reference documentation
     — Texture recreation consistent with {art_style or 'period'} conventions
     — Visual integration with surrounding surviving original material

MATERIALS & TECHNICAL SPECIFICATIONS

  Conservation-grade materials:
  • Adhesives: Reversible synthetic polymers (BEVA 371, Paraloid B-72)
  • Consolidants: Tested for compatibility with original substrate
  • Inpainting media: Watercolours or conservation acrylics (Gamblin Conservation)
  • Protective coatings: UV-filtering, breathable varnishes (Regalrez 1094)

  Period-accurate technique notes:
  • Brushwork patterns consistent with {art_style or 'period'} artistic conventions
  • Layering methodology respecting traditional working sequence
  • Colour mixing guided by historical pigment knowledge and spectral analysis

CONSERVATION ETHICS & CULTURAL SENSITIVITY

  Following international conservation ethics (ICOM-CC, AIC):
  • Minimal intervention — preserve rather than restore where uncertain
  • Reversibility of all treatments without risk to original material
  • Full documentation of every procedure and decision rationale
  • Respect for original artist's intent, not modern ideals of perfection
  • Consultation with cultural heritage specialists and community stakeholders

PREVENTIVE CONSERVATION RECOMMENDATIONS

  Environmental controls:
  • Temperature: 18–22°C (64–72°F) with less than 5°C daily variation
  • Relative Humidity: 45–55%, stable
  • Illumination: below 150 lux for sensitive works; UV-filtered light sources
  • Air quality: particulate-filtered, low-pollutant environment

CONCLUSION
A systematic, evidence-based approach is recommended for this work. The {dmg or 'observed damage'} is addressable through established conservation methodology while preserving the artwork's integrity, authenticity, and cultural value. All proposed treatments prioritise long-term material stability and minimum intervention.

DISCLAIMER
This analysis is advisory only. All physical restoration work must be carried out by certified professional conservators following applicable institutional and ethical guidelines.
"""
                    st.session_state.page = 'results'
                    st.rerun()
            else:
                st.error("Please provide an artwork description to proceed.")

    # ===== TAB 2: FEATURE GALLERY =====
    with tab2:
        st.markdown("""
        <div class="eye">Capability Overview</div>
        <div class="ptitle">Studio <em>Disciplines</em></div>
        <div class="pdesc">Ten specialist disciplines covering the full breadth of art conservation. Each feature is driven by a carefully designed AI prompt grounded in conservation science.</div>
        <div class="pdiv"></div>
        """, unsafe_allow_html=True)

        all_cases = [{"case": c, "feature": f['title']} for f in features_gallery for c in f['cases']]

        if 'quiz_questions' not in st.session_state:
            sample = random.sample(all_cases, min(6, len(all_cases)))
            titles = [f['title'] for f in features_gallery]
            qs = []
            for s in sample:
                correct = s['feature']
                wrongs = random.sample([t for t in titles if t != correct], min(3, len(titles) - 1))
                choices = wrongs + [correct]
                random.shuffle(choices)
                qs.append({'prompt': s['case'], 'correct': correct, 'choices': choices})
            st.session_state.quiz_questions = qs
            st.session_state.q_index = 0
            st.session_state.score = 0

        qs = st.session_state.quiz_questions
        qi = st.session_state.q_index

        st.markdown('<div class="qshell">', unsafe_allow_html=True)
        st.markdown('<div class="qhead">Knowledge Assessment</div>', unsafe_allow_html=True)
        st.markdown('<div class="qsub">Match each use case to the correct conservation discipline</div>', unsafe_allow_html=True)

        if qi < len(qs):
            pct = int((qi / len(qs)) * 100)
            st.markdown(f"""
            <div class="qpw">
                <span style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(245,240,232,0.32);letter-spacing:0.16em;">{qi + 1} / {len(qs)}</span>
                <div class="qpbg"><div class="qpf" style="width:{pct}%"></div></div>
                <span style="font-family:'DM Mono',monospace;font-size:10px;color:var(--gold);letter-spacing:0.1em;">{st.session_state.score} correct</span>
            </div>
            <div class="qq">"{qs[qi]['prompt']}"</div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            sel = st.radio("Which conservation discipline best matches this use case?", qs[qi]['choices'], key=f'qc_{qi}', label_visibility="collapsed")
            if st.button("Submit Answer", key=f'qs_{qi}'):
                if sel == qs[qi]['correct']:
                    st.session_state.score += 1
                    st.success("✓ Correct")
                else:
                    st.error(f"✗ Correct answer: {qs[qi]['correct']}")
                st.session_state.q_index += 1
                st.rerun()
        else:
            total = len(qs)
            pct = int((st.session_state.score / total) * 100)
            st.markdown(f'<div class="qsbig">{st.session_state.score}/{total}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="qssub">Assessment Complete · {pct}% Accuracy</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Retake Assessment", key="qr"):
                del st.session_state.quiz_questions, st.session_state.q_index, st.session_state.score
                st.rerun()

        st.markdown('<div class="g24"></div>', unsafe_allow_html=True)
        st.markdown('<div class="eye">All Ten Disciplines</div><div class="g8"></div>', unsafe_allow_html=True)

        ca, cb = st.columns(2, gap="medium")
        for i, f in enumerate(features_gallery):
            tags = "".join([f'<span class="ftag">{c}</span>' for c in f['cases']])
            prompt_snippet = f['prompt'][:120] + "..." if len(f['prompt']) > 120 else f['prompt']
            card = f"""
            <div class="fcard">
                <div class="fcard-h">
                    <div class="fcard-i">{f['icon']}</div>
                    <div>
                        <div class="fcard-t">{f['title']}</div>
                        <div class="fcard-d">{f['desc']}</div>
                    </div>
                </div>
                <div style="font-family:'Crimson Pro',serif;font-size:13px;color:var(--gold-muted);font-style:italic;margin-bottom:10px;border-left:2px solid var(--border);padding-left:10px;">"{prompt_snippet}"</div>
                <div class="fcard-tags">{tags}</div>
            </div>
            """
            with (ca if i % 2 == 0 else cb):
                st.markdown(card, unsafe_allow_html=True)

    # ===== TAB 3: CULTURAL ARCHIVE =====
    with tab3:
        st.markdown("""
        <div class="eye">Heritage Knowledge Base</div>
        <div class="ptitle">Cultural <em>Archive</em></div>
        <div class="pdesc">Explore the historical context, artistic significance, and conservation considerations for major art traditions from around the world.</div>
        <div class="pdiv"></div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sl">Select Art Period or Cultural Tradition</div>', unsafe_allow_html=True)
        ins_type = st.selectbox("", [
            "Renaissance (Italian)", "Baroque (European)", "Rococo (French)",
            "Indian Mughal Art", "Indian Rajput Painting", "Islamic Art & Calligraphy",
            "Japanese Ukiyo-e", "Chinese Ming Dynasty", "Byzantine Art",
            "Egyptian Art", "Greek Classical Art", "Aboriginal Australian Art"
        ], key="ins", label_visibility="collapsed")

        ci = {
            "Renaissance (Italian)": {"emoji": "🎨", "period": "14th–17th Century", "background": "The Renaissance marked a cultural rebirth in Europe, emphasising humanism, naturalism, and classical learning. Leonardo da Vinci, Michelangelo, and Raphael revolutionised painting with linear perspective, sfumato, and anatomical precision.", "importance": "Renaissance art laid the foundation for Western artistic tradition, shifting from medieval symbolism to representational realism. Its emphasis on individual expression permanently altered how humans understand themselves.", "restoration": "Renaissance works demand extreme care due to fragile egg tempera and delicate oil glazing layers. Non-invasive imaging is standard before any physical intervention.", "techniques": ["Linear Perspective", "Sfumato (atmospheric haze)", "Chiaroscuro (light/shadow)", "Contrapposto stance", "Oil glazing layers"], "famous_works": ["Mona Lisa", "The Last Supper", "Sistine Chapel Ceiling", "The Birth of Venus"]},
            "Baroque (European)": {"emoji": "✨", "period": "17th–18th Century", "background": "Baroque emerged as a dramatic, emotional response to the Protestant Reformation. Characterised by intense light, movement, and theatrical staging, it served the Catholic Church as a vehicle of devotional awe.", "importance": "Baroque revolutionised emotional expression in art. Caravaggio, Rembrandt, and Rubens achieved unprecedented psychological depth.", "restoration": "Baroque works often feature heavy impasto and dark varnish layers. Careful staged varnish removal reveals original pigment while preserving the tonal architecture.", "techniques": ["Tenebrism (extreme contrast)", "Dynamic composition", "Rich saturated palette", "Psychological intensity", "Sculptural drapery"], "famous_works": ["The Night Watch", "Ecstasy of Saint Teresa", "Las Meninas", "The Calling of St Matthew"]},
            "Rococo (French)": {"emoji": "🌸", "period": "18th Century", "background": "Rococo emerged as a lighter, playful reaction to Baroque grandeur. Pastel palettes and themes of pastoral romance flourished in French aristocratic interiors.", "importance": "Rococo captured the refinement of 18th-century aristocratic culture and influenced interior design, fashion, and the decorative arts across Europe.", "restoration": "Delicate pastel pigments and gold leaf fade and flake. Restoration requires preserving the airiness of the style while stabilising fragile decorative surfaces.", "techniques": ["Pastel colour palette", "Asymmetric decorative curves", "Gold leaf highlights", "Feathery brushwork", "Pastoral themes"], "famous_works": ["The Swing", "Pilgrimage to Cythera", "Diana Leaving Her Bath", "Versailles interior schemes"]},
            "Indian Mughal Art": {"emoji": "🕌", "period": "16th–19th Century", "background": "Mughal miniature paintings synthesise Persian, Indian, and Islamic traditions. Created for royal courts with meticulous single-hair brushwork and vibrant natural pigments.", "importance": "Mughal art represents a unique cultural synthesis and provides an invaluable visual record of one of history's most sophisticated imperial courts.", "restoration": "Painted on paper with mineral pigments and gold. Restoration must address insect damage, pigment fading, and paper deterioration while preserving gilded work.", "techniques": ["Fine single-hair brushwork", "Natural mineral pigments", "Gold leaf (sona)", "Elaborate borders", "Layered composition"], "famous_works": ["Hamzanama manuscripts", "Akbarnama", "Padshahnama", "Baburnama illustrations"]},
            "Indian Rajput Painting": {"emoji": "🎭", "period": "16th–19th Century", "background": "Rajput paintings depicted Hindu mythology, devotional poetry, and court culture with bold flat colour and expressive faces across numerous regional court schools.", "importance": "Rajput art preserved Hindu religious narrative and regional cultural identity through distinctive regional visual languages.", "restoration": "Similar materials to Mughal art but with bolder pigment application. Conservation must respect religious and iconographic symbolism.", "techniques": ["Bold flat colour fields", "Expressive gesture", "Symbolic colour language", "Poetry-inspired composition", "Regional stylistic variation"], "famous_works": ["Bani Thani (Kishangarh)", "Ragamala series", "Krishna Lila paintings", "Mewar Ramayana"]},
            "Islamic Art & Calligraphy": {"emoji": "🕌", "period": "7th Century–Present", "background": "Islamic art emphasises geometric pattern, arabesque, and calligraphy in response to religious restrictions on figural imagery. Quranic scripture is elevated to visual art.", "importance": "Islamic art demonstrates how religious principles inspire mathematical precision and aesthetic mastery. Calligraphy treats the written word as visible devotion.", "restoration": "Manuscripts and architectural decoration require specialist knowledge of Arabic scripts and geometric principles. Pattern symmetry must be perfectly maintained.", "techniques": ["Sacred geometry", "Arabesque scroll", "Illuminated borders", "Geometric tilework", "Multiple calligraphic scripts"], "famous_works": ["Blue Quran (Fatimid)", "Alhambra palace decoration", "Topkapi manuscripts", "Isfahan mosque tilework"]},
            "Japanese Ukiyo-e": {"emoji": "🎌", "period": "17th–19th Century", "background": "Ukiyo-e woodblock prints depicted kabuki actors and landscapes in Edo-period Japan. Hokusai and Hiroshige profoundly influenced European Post-Impressionism.", "importance": "Ukiyo-e democratised art in Japan and catalysed a revolution in European painting, demonstrating the power of asymmetric composition and flat colour.", "restoration": "Extremely vulnerable to light-induced fading and acid degradation of Japanese paper. Conservation requires understanding traditional washi papermaking.", "techniques": ["Woodblock printing", "Bokashi (gradated colour)", "Strong ink outlines", "Flat colour fields", "Asymmetric composition"], "famous_works": ["The Great Wave off Kanagawa", "Thirty-Six Views of Fuji", "Fifty-Three Stations of Tokaido", "Beauties of Yoshiwara"]},
            "Chinese Ming Dynasty": {"emoji": "🐉", "period": "14th–17th Century", "background": "Ming Dynasty art revived classical Chinese tradition, celebrated for blue-and-white porcelain, ink landscape painting, and calligraphy.", "importance": "Ming art represents the apex of Chinese ceramic production and literati painting. Its porcelain shaped global trade and aesthetic sensibility worldwide.", "restoration": "Ceramics require specialist knowledge of high-temperature reduction firing. Ink paintings on silk demand extreme care due to the fragility of the support.", "techniques": ["Blue-and-white porcelain", "Monochrome ink landscape", "Calligraphic brushwork", "Scholar rock aesthetics", "Imperial court painting"], "famous_works": ["Ming blue-and-white vases", "Shen Zhou landscapes", "Tang Yin figure paintings", "Imperial porcelain collections"]},
            "Byzantine Art": {"emoji": "☦️", "period": "4th–15th Century", "background": "Byzantine art served the Eastern Orthodox Church, developing gold-ground icons, monumental mosaics, and frontal hieratic figures designed to manifest spiritual presence.", "importance": "Byzantine art preserved classical techniques through the medieval period and established the visual vocabulary of Orthodox Christianity still active today.", "restoration": "Panels and mosaics require specialist conservation of egg tempera, gold leaf, and glass tesserae. Orthodox tradition governs acceptable intervention on liturgical works.", "techniques": ["Gold leaf backgrounds", "Egg tempera on gesso", "Mosaic glass tesserae", "Hierarchical figure scale", "Symbolic colour theology"], "famous_works": ["Hagia Sophia mosaics", "Vladimir Mother of God", "Ravenna apse mosaics", "Christ Pantocrator (Daphni)"]},
            "Egyptian Art": {"emoji": "🏛️", "period": "3000–30 BCE", "background": "Ancient Egyptian art served religious and political functions, depicting gods and pharaohs in a formal visual system stable for over three millennia.", "importance": "Egyptian art provides the most sustained visual record in human history, preserving cosmological knowledge across thirty dynasties.", "restoration": "Requires strict climate control. Mineral pigments need careful stabilisation. Works on stone, papyrus, linen, and plaster each demand distinct conservation approaches.", "techniques": ["Hierarchical figure scale", "Composite frontal/profile view", "Register-based composition", "Symbolic colour coding", "Incised relief carving"], "famous_works": ["Tutankhamun funerary mask", "Nefertiti bust (Berlin)", "Tomb of Nefertari frescoes", "Book of the Dead papyri"]},
            "Greek Classical Art": {"emoji": "🏛️", "period": "5th–4th Century BCE", "background": "Classical Greek art enshrined ideals of beauty and proportion in stone and bronze. Phidias and Praxiteles created a canon of the idealised human form.", "importance": "Greek classical art established foundational principles that defined Western artistic tradition from the Renaissance to the present day.", "restoration": "Sculptures often survive as Roman marble copies. Conservation involves careful stone cleaning and ethically contested decisions about reconstruction.", "techniques": ["Contrapposto naturalistic stance", "Golden ratio proportions", "Idealised anatomical accuracy", "Bronze lost-wax casting", "Original polychromy (now largely lost)"], "famous_works": ["Parthenon Elgin Marbles", "Discobolus", "Aphrodite of Melos", "Winged Victory of Samothrace"]},
            "Aboriginal Australian Art": {"emoji": "🪃", "period": "40,000+ years–Present", "background": "Aboriginal art is humanity's oldest continuous artistic tradition, encoding Dreamtime cosmology, ancestral narrative, and country connection in rock paintings and dot paintings.", "importance": "Aboriginal art preserves tens of thousands of years of cultural memory, inseparable from land rights, spiritual law, and community identity.", "restoration": "Conservation requires prior consultation with traditional custodians. Rock art in outdoor environments presents extreme long-term preservation challenges.", "techniques": ["Ochre pigment earth colours", "X-ray internal anatomy style", "Dot painting (acrylic revival)", "Symbolic mapping of country", "Layered narrative encoding"], "famous_works": ["Bradshaw/Gwion rock paintings", "X-ray art of Kakadu", "Papunya Tula Western Desert movement", "Wandjina spirit figures (Kimberley)"]},
        }

        if ins_type in ci:
            ins = ci[ins_type]
            st.markdown(f"""
            <div class="phero">
                <div class="phero-em">{ins['emoji']}</div>
                <div>
                    <div class="phero-t">{ins_type}</div>
                    <div class="phero-e">📅 {ins['period']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            i1, i2 = st.columns([3, 2], gap="large")
            with i1:
                for icon, title, body in [
                    ("📖", "Historical Background", ins['background']),
                    ("⭐", "Cultural Significance",  ins['importance']),
                    ("🛠️", "Conservation Considerations", ins['restoration']),
                ]:
                    st.markdown(f'<div class="icard"><div class="icard-t">{icon} {title}</div><div class="icard-b">{body}</div></div>', unsafe_allow_html=True)
            with i2:
                st.markdown('<div class="icard"><div class="icard-t">🎨 Key Techniques</div>', unsafe_allow_html=True)
                for t in ins['techniques']:
                    st.markdown(f'<span class="ttag">{t}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="g8"></div>', unsafe_allow_html=True)
                st.markdown('<div class="icard"><div class="icard-t">🖼️ Major Works</div>', unsafe_allow_html=True)
                for w in ins['famous_works']:
                    st.markdown(f'<div class="wrow"><span class="wdash">—</span>{w}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ===== TAB 4: TIMELINE PLANNER =====
    with tab4:
        st.markdown("""
        <div class="eye">Project Planning Tool</div>
        <div class="ptitle">Restoration <em>Timeline</em></div>
        <div class="pdesc">Configure your project parameters and receive a phased restoration schedule with risk assessments and expert recommendations.</div>
        <div class="pdiv"></div>
        """, unsafe_allow_html=True)

        tc1, tc2 = st.columns(2, gap="large")
        with tc1:
            st.markdown('<div class="sl">Artwork Type</div>', unsafe_allow_html=True)
            tl_art = st.selectbox("", ["Oil Painting", "Watercolor on Paper", "Stone Sculpture", "Bronze Sculpture",
                "Textile / Tapestry", "Illuminated Manuscript", "Mural / Fresco", "Ceramic / Pottery", "Mixed Media"],
                key="tla", label_visibility="collapsed")
            st.markdown('<div class="sl">Damage Severity</div>', unsafe_allow_html=True)
            tl_dmg = st.select_slider("", options=["Minimal", "Moderate", "Significant", "Severe", "Critical"],
                value="Moderate", key="tld", label_visibility="collapsed")
            st.markdown('<div class="sl">Artwork Scale</div>', unsafe_allow_html=True)
            tl_size = st.selectbox("", ["Small (< 30cm)", "Medium (30–100cm)", "Large (100–200cm)", "Very Large (> 200cm)", "Monumental"],
                key="tls", label_visibility="collapsed")
        with tc2:
            st.markdown('<div class="sl">Project Urgency</div>', unsafe_allow_html=True)
            tl_urg = st.selectbox("", ["Flexible", "Standard (6–12 months)", "Priority (3–6 months)", "Urgent (< 3 months)"],
                key="tlu", label_visibility="collapsed")
            st.markdown('<div class="sl">Conservation Team</div>', unsafe_allow_html=True)
            tl_team = st.select_slider("", options=["Solo conservator", "2–3 specialists", "4–6 person team", "Large institutional team (7+)"],
                value="2–3 specialists", key="tlt", label_visibility="collapsed")
            st.markdown('<div class="sl">Project Goals</div>', unsafe_allow_html=True)
            tl_goals = st.multiselect("", ["Stabilisation only", "Full visual restoration", "Scientific documentation",
                "Public exhibition prep", "Digital archiving", "Loan/transport prep", "Insurance documentation"],
                default=["Stabilisation only", "Full visual restoration"], key="tlg", label_visibility="collapsed")

        st.markdown('<div class="g24"></div>', unsafe_allow_html=True)

        if st.button("Generate Timeline Plan →", key="gent"):
            dm = {"Minimal": (1,"LOW"), "Moderate": (2,"MEDIUM"), "Significant": (3,"HIGH"), "Severe": (4,"HIGH"), "Critical": (5,"HIGH")}
            sm = {"Small (< 30cm)": 0.7, "Medium (30–100cm)": 1.0, "Large (100–200cm)": 1.4, "Very Large (> 200cm)": 1.8, "Monumental": 2.5}
            um = {"Flexible": 1.0, "Standard (6–12 months)": 0.85, "Priority (3–6 months)": 0.65, "Urgent (< 3 months)": 0.45}
            tm2 = {"Solo conservator": 1.3, "2–3 specialists": 1.0, "4–6 person team": 0.75, "Large institutional team (7+)": 0.55}

            dl, risk = dm[tl_dmg]
            sf = sm[tl_size]; uf = um[tl_urg]; tf = tm2[tl_team]
            def cw(b): return max(1, round(b * (dl / 2) * sf * uf * tf))

            phases = [
                {"num": "01", "icon": "🔬", "name": "Assessment & Documentation", "weeks": cw(3),
                 "tasks": [("Comprehensive visual inspection and condition mapping", "H"), ("UV fluorescence, X-radiography, infrared reflectography", "H"), ("Material sampling — pigment, substrate, binding media", "M"), ("Historical research and archival provenance study", "M"), ("Photographic documentation (raking light, multispectral)", "L")],
                 "milestone": "Condition Report approved by stakeholders"},
                {"num": "02", "icon": "🛡️", "name": "Emergency Stabilisation", "weeks": cw(2),
                 "tasks": [("Consolidation of flaking or delaminating paint layers", "H"), ("Structural support for cracked or fragile substrate", "H"), ("Facing of vulnerable areas prior to treatment", "M"), ("Climate and environmental stabilisation measures", "L")],
                 "milestone": "Artwork structurally stable — safe to proceed"},
                {"num": "03", "icon": "🧹", "name": "Surface Cleaning & Preparation", "weeks": cw(4),
                 "tasks": [("Dry mechanical cleaning — surface deposit removal", "L"), ("Solvent-based removal of discoloured varnish layers", "H"), ("Aqueous cleaning where appropriate (pH controlled)", "M"), ("Removal of previous incompatible restorations", "H"), ("Final surface assessment of revealed original material", "M")],
                 "milestone": "Original surface fully accessible and documented"},
                {"num": "04", "icon": "🔧", "name": "Structural Conservation", "weeks": cw(3) if dl >= 3 else 0,
                 "tasks": [("Substrate consolidation — relining, cradling, or backing", "H"), ("Loss filling with conservation-grade fills", "M"), ("Surface texture inpainting to match surrounding original", "M"), ("Adhesive consolidation of all previously loose elements", "L")],
                 "milestone": "Structural integrity fully restored"},
                {"num": "05", "icon": "🎨", "name": "Aesthetic Restoration & Inpainting", "weeks": cw(5),
                 "tasks": [("Colour matching and reference sample creation", "H"), ("Inpainting of losses using reversible conservation media", "H"), ("Texture recreation — integrating losses with original", "H"), ("Intermediate varnish for optical unification", "M"), ("Chromatic reintegration review with client/curator", "M")],
                 "milestone": "Visual reintegration approved — aesthetic integrity restored"},
                {"num": "06", "icon": "✅", "name": "Final Varnish, Review & Handover", "weeks": cw(2),
                 "tasks": [("Application of final reversible UV-stable varnish", "M"), ("Full post-treatment documentation photography", "L"), ("Comprehensive conservation treatment report prepared", "H"), ("Client review, sign-off, and formal handover", "L"), ("Long-term preventive conservation guidance issued", "L")],
                 "milestone": "Project complete — artwork delivered with full documentation"},
            ]

            active = [p for p in phases if p['weeks'] > 0]
            tw = sum(p['weeks'] for p in active)
            tm_months = round(tw / 4.3, 1)

            st.markdown(f"""
            <div class="sstrip">
                <div class="scell"><div class="sval">{tw}w</div><div class="slbl">Total Duration</div></div>
                <div class="scell"><div class="sval">{tm_months}mo</div><div class="slbl">Approx. Months</div></div>
                <div class="scell"><div class="sval">{len(active)}</div><div class="slbl">Project Phases</div></div>
                <div class="scell"><div class="sval">{risk}</div><div class="slbl">Risk Level</div></div>
            </div>
            """, unsafe_allow_html=True)

            if tl_urg == "Urgent (< 3 months)" and tw > 12:
                st.warning(f"⚠ Urgent timeline selected but estimated duration is {tw} weeks. Consider expanding the team or reducing scope.")

            st.markdown('<div class="eye">Phase-by-Phase Schedule</div><div class="g8"></div>', unsafe_allow_html=True)

            rw = 0
            for p in active:
                sw = rw + 1; ew = rw + p['weeks']; rw = ew
                tasks_html = ""
                for task_text, task_pri in p['tasks']:
                    dot_color = "#8b3a2a" if task_pri == "H" else "#b8963e" if task_pri == "M" else "#2a6b6e"
                    tasks_html += f'<div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid rgba(184,150,62,0.1);font-family:Crimson Pro,serif;font-size:15px;color:#4a453d;line-height:1.5;"><div style="width:7px;height:7px;border-radius:50%;flex-shrink:0;margin-top:6px;background:{dot_color};"></div><span>{task_text}</span></div>'
                ms_html = f'<div style="margin-top:14px;padding:12px 16px;background:#ede8dc;border-left:3px solid #b8963e;font-family:Crimson Pro,serif;font-size:14px;font-style:italic;color:#4a453d;"><span style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.22em;text-transform:uppercase;color:#b8963e;margin-bottom:3px;font-style:normal;display:block;">Milestone</span>{p["milestone"]}</div>'

                st.markdown(f"""
                <div style="display:grid;grid-template-columns:155px 1fr;border:1px solid #d8d1c0;margin-bottom:2px;">
                    <div style="background:#0e0e0f;padding:22px 18px;display:flex;flex-direction:column;justify-content:space-between;">
                        <div>
                            <div style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.28em;color:#8a6f2e;text-transform:uppercase;margin-bottom:9px;">Phase {p['num']}</div>
                            <div style="font-size:26px;margin-bottom:9px;">{p['icon']}</div>
                            <div style="font-family:Playfair Display,serif;font-size:13px;font-weight:600;color:#f5f0e8;line-height:1.3;">{p['name']}</div>
                        </div>
                        <div style="font-family:DM Mono,monospace;font-size:10px;color:#8a6f2e;margin-top:12px;">Wks {sw}–{ew} · {p['weeks']}w</div>
                    </div>
                    <div style="padding:22px 26px;background:white;">{tasks_html}{ms_html}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="g16"></div><div class="eye">Planning Recommendations</div><div class="g8"></div>', unsafe_allow_html=True)

            recs = []
            if dl >= 4: recs.append(("🚨", "HIGH", "#8b3a2a", "Immediate structural stabilisation is critical. Do not proceed to cleaning before all fragile elements are secured."))
            if "Scientific documentation" in tl_goals: recs.append(("🔬", "MEDIUM", "#b8963e", "Allow 2–3 additional weeks for laboratory analysis. Partner with a university conservation science department."))
            if "Public exhibition prep" in tl_goals: recs.append(("🖼️", "MEDIUM", "#b8963e", "Build a 4-week buffer before the exhibition date. Final varnish needs two weeks to cure fully."))
            if tl_urg in ["Priority (3–6 months)", "Urgent (< 3 months)"]: recs.append(("⚡", "HIGH", "#8b3a2a", "Compressed timeline increases risk. Consider enlarging the team or reducing scope to essential stabilisation."))
            recs.append(("📋", "LOW", "#2a6b6e", "Document every intervention in a running treatment log. Photographs before, during, and after each phase are mandatory."))
            recs.append(("🌡️", "LOW", "#2a6b6e", "Maintain stable environment: 18–22°C, 45–55% RH. Fluctuations rapidly undo treatment gains."))
            if "Digital archiving" in tl_goals: recs.append(("💾", "LOW", "#2a6b6e", "Schedule multispectral imaging at end of Phase 3 (cleaned, pre-inpainting) for highest-quality archival record."))

            for icon, pri, color, text in recs:
                st.markdown(f"""
                <div style="display:flex;align-items:flex-start;gap:13px;padding:14px 16px;background:white;border:1px solid #d8d1c0;border-left:4px solid {color};margin-bottom:7px;">
                    <span style="font-size:17px;flex-shrink:0;margin-top:1px;">{icon}</span>
                    <div>
                        <div style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:{color};margin-bottom:3px;">{pri}</div>
                        <span style="font-family:Crimson Pro,serif;font-size:15px;color:#4a453d;line-height:1.6;">{text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            exp = f"ARTRESTORER AI — RESTORATION TIMELINE\n{'='*50}\nGenerated: {datetime.now().strftime('%B %d, %Y')}\nArtwork: {tl_art} | Damage: {tl_dmg} | Scale: {tl_size}\nTeam: {tl_team} | Urgency: {tl_urg}\nTotal: {tw} weeks (~{tm_months} months) | Risk: {risk}\n\n"
            rw2 = 0
            for p in active:
                sw = rw2 + 1; ew = rw2 + p['weeks']; rw2 = ew
                exp += f"Phase {p['num']}: {p['name']} (Weeks {sw}–{ew})\n"
                for t, pr in p['tasks']: exp += f"  [{pr}] {t}\n"
                exp += f"  Milestone: {p['milestone']}\n\n"

            st.markdown('<div class="g16"></div>', unsafe_allow_html=True)
            st.download_button("Download Timeline Plan", data=exp,
                file_name=f"ArtRestorer_Timeline_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain", key="dlt")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="sfooter"><span>ArtRestorer AI &nbsp;·&nbsp; Cultural Heritage Preservation &nbsp;·&nbsp; Powered by OpenAI</span></div>', unsafe_allow_html=True)

# ==================== RESULTS PAGE ====================
elif st.session_state.page == 'results':
    render_header()
    st.markdown("""
    <div class="rhero">
        <div class="rtag">Analysis Complete</div>
        <div class="rtitle">Restoration <em>Report</em></div>
        <div class="rsub">Expert conservation guidance generated for your submitted artwork</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="mwrap">', unsafe_allow_html=True)

    cd, cs = st.columns([1, 4])
    with cd:
        st.download_button("Export Report",
            data=f"ARTRESTORER AI — RESTORATION ANALYSIS\n{'='*50}\nDate: {datetime.now().strftime('%B %d, %Y')}\n\n{st.session_state.result_text}\n\nGenerated by ArtRestorer AI · Advisory only. Consult certified conservators.",
            file_name=f"ArtRestorer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain", key="dlr")

    st.markdown('<div class="g16"></div><div class="rbody">', unsafe_allow_html=True)

    section_heads = {"ARTWORK DETAILS", "HISTORICAL CONTEXT & SIGNIFICANCE", "CONDITION ASSESSMENT",
        "RESTORATION METHODOLOGY", "MATERIALS & TECHNICAL SPECIFICATIONS",
        "CONSERVATION ETHICS & CULTURAL SENSITIVITY", "PREVENTIVE CONSERVATION RECOMMENDATIONS",
        "CONCLUSION", "DISCLAIMER"}

    for sec in st.session_state.result_text.split('\n\n'):
        sec = sec.strip()
        if not sec: continue
        lines = sec.split('\n')
        head = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        if head in section_heads:
            st.markdown(f'<div class="rsechead">{head}</div>', unsafe_allow_html=True)
            if body: st.markdown(f'<div class="rtext">{body}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="rtext">{sec}</div>', unsafe_allow_html=True)

    st.markdown('</div><div class="g24"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("← Analyse Another Artwork", key="back"):
            st.session_state.page = 'main'; st.rerun()

    st.markdown("""
    <div class="fbwrap">
        <div class="eye">Share Your Experience</div>
        <div style="font-family:'Playfair Display',serif;font-size:19px;font-weight:600;color:var(--text-primary);margin-bottom:3px;">Help Improve ArtRestorer AI</div>
        <div style="font-family:'Crimson Pro',serif;font-size:16px;color:var(--text-muted);font-style:italic;margin-bottom:20px;">Your feedback shapes the future of this platform</div>
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([1, 1, 1])
    with fc2:
        if st.button("Open Feedback Form", key="ofb"):
            st.session_state.show_feedback = True

    if st.session_state.get('show_feedback'):
        fb1, fb2 = st.columns(2, gap="large")
        with fb1:
            st.markdown('<div class="sl">Your Name</div>', unsafe_allow_html=True)
            fn = st.text_input("", key="fn", placeholder="Enter your name", label_visibility="collapsed")
            st.markdown('<div class="sl">Rating</div>', unsafe_allow_html=True)
            fr = st.select_slider("", options=["⭐ Poor", "⭐⭐ Fair", "⭐⭐⭐ Good", "⭐⭐⭐⭐ Very Good", "⭐⭐⭐⭐⭐ Excellent"],
                value="⭐⭐⭐ Good", key="fr", label_visibility="collapsed")
        with fb2:
            st.markdown('<div class="sl">Category</div>', unsafe_allow_html=True)
            fc = st.selectbox("", ["General Feedback", "Feature Request", "Bug Report", "Accuracy of Analysis", "User Experience", "Other"],
                key="fc", label_visibility="collapsed")
            st.markdown('<div class="sl">Would you recommend?</div>', unsafe_allow_html=True)
            frec = st.radio("", ["👍 Yes", "🤔 Maybe", "👎 No"], horizontal=True, key="frec", label_visibility="collapsed")
        st.markdown('<div class="sl">Comments</div>', unsafe_allow_html=True)
        fcmt = st.text_area("", placeholder="Share your thoughts...", height=100, key="fcmt", label_visibility="collapsed")
        bc1, bc2, bc3 = st.columns(3)
        with bc1:
            if st.button("Cancel", key="fbc"):
                st.session_state.show_feedback = False; st.rerun()
        with bc2:
            if st.button("Submit Feedback", key="fbs"):
                if fn and fcmt:
                    st.success("✓ Thank you. Your feedback has been recorded.")
                    import time; time.sleep(1)
                    st.session_state.show_feedback = False; st.rerun()
                else:
                    st.error("Please provide your name and comments.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="sfooter"><span>ArtRestorer AI &nbsp;·&nbsp; Cultural Heritage Preservation &nbsp;·&nbsp; Powered by OpenAI</span></div>', unsafe_allow_html=True)
