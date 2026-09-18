import random

import streamlit as st

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide",
)

INSIGHTS_PAGE = "insights"
ABOUT_PAGE = "about"
PROPERTY_PHOTOS = [
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1400&q=85",
    "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1400&q=85",
    "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1400&q=85",
]

# ---------------------------------------------------------
# Custom CSS to match the reference design
# (colors are hardcoded + !important so the app looks the
#  same regardless of the visitor's OS/browser dark-mode setting)
# ---------------------------------------------------------
st.markdown("""
<style>
    html, body {
        background-color: #f4f7fb !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 100% !important;
        overflow: hidden !important;
    }
    #root,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"] {
        background-color: #f4f7fb !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    body, .stApp * {
        color: #1a1a2e !important;
        
    }

    /* Hide default streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Remove Streamlit's default space above the navbar */
    .block-container {
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .main,
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stAppViewContainer"] > .main > div {
        margin: 0 !important;
        padding: 0 !important;
        max-width: none !important;
    }

    [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
    }

    [data-testid="stMain"] {
        height: 100vh !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        scrollbar-width: thin;
        scrollbar-color: #9bb9e8 transparent;
    }

    [data-testid="stMain"]::-webkit-scrollbar {
        width: 8px;
    }

    [data-testid="stMain"]::-webkit-scrollbar-track {
        background: transparent;
    }

    [data-testid="stMain"]::-webkit-scrollbar-thumb {
        background: #9bb9e8;
        border-radius: 8px;
    }

    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    [data-testid="stMainBlockContainer"]
        > [data-testid="stVerticalBlock"]
        > [data-testid="stElementContainer"]:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* Top navbar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-sizing: border-box;
    
      
        background: linear-gradient(
    90deg,
    #0B1F3A 0%,
    #123B6D 40%,
    #1769AA 75%,
    #3155D9 100%);
        padding: 14px 32px;
  
        color: white !important;
        font-weight: 600;
        font-size: 20px;
        width: 100vw;
        top: 0;
        position:fixed !important;
        z-index:2;
    }
    .navbar * { color: white !important; }
    .navbar a {
        color: white !important;
        text-decoration: none !important;
        margin-left: 18px;
        transition: opacity 0.2s ease;
    }
    .navbar a:hover {
        opacity: 0.78;
    }
    .navbar .disabled-link {
        color: rgba(255, 255, 255, 0.48) !important;
        margin-left: 18px;
        cursor: not-allowed;
    }
    .navbar {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 20px;
        padding: 14px 40px;
    }
    .navbar-brand {
        justify-self: start;
        white-space: nowrap;
    }
    .navbar-links {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-size: 14px;
    }
    .navbar .navbar-links a {
        margin-left: 0;
        padding: 10px 16px;
        border-radius: 22px;
    }
    .navbar .navbar-links a.active {
        background: #e8f0ff;
        color: #315be9 !important;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(49, 91, 233, 0.16);
    }
    .navbar .navbar-links a:focus {
        background: #e8f0ff;
        color: #315be9 !important;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(49, 91, 233, 0.16);
        outline: none;
    }
    body:has(#about:target) .navbar .navbar-links a[href="#about"],
    body:has(#insights:target) .navbar .navbar-links a[href="#insights"] {
        background: #e8f0ff;
        color: #315be9 !important;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(49, 91, 233, 0.16);
    }
    body:has(#about:target) .navbar .navbar-links a[href="#predictor"],
    body:has(#insights:target) .navbar .navbar-links a[href="#predictor"] {
        background: transparent;
        color: white !important;
        box-shadow: none;
    }
    .client-page {
        display: none;
    }
    .client-page.is-visible {
        position: fixed;
        inset: 60px 0 0;
        display: block;
        overflow-y: auto;
        z-index: 3;
        background: #f4f7fb;
    }
    body.app-dark-mode .client-page.is-visible {
        background: #101b33 !important;
    }
    .client-page:target {
        position: fixed;
        inset: 60px 0 0;
        display: block;
        overflow-y: auto;
        z-index: 3;
        background: #f4f7fb;
    }
    body.app-dark-mode .client-page:target {
        background: #101b33 !important;
    }
    .navbar-actions {
        display: flex;
        align-items: center;
        justify-self: end;
        gap: 10px;
        font-size: 16px;
    }
    .mode-toggle {
        position: relative;
        display: inline-block;
        width: 42px;
        height: 24px;
    }
    .mode-toggle input {
        width: 0;
        height: 0;
        opacity: 0;
    }
    .mode-slider {
        position: absolute;
        inset: 0;
        cursor: pointer;
        background: #d8e3f7;
        border-radius: 20px;
        transition: 0.2s ease;
    }
    .mode-slider::before {
        content: "";
        position: absolute;
        width: 18px;
        height: 18px;
        left: 3px;
        top: 3px;
        background: white;
        border-radius: 50%;
        transition: 0.2s ease;
        box-shadow: 0 2px 5px rgba(24, 55, 90, 0.2);
    }
    .mode-toggle input:checked + .mode-slider {
        background: #4771ed;
    }
    .mode-toggle input:checked + .mode-slider::before {
        transform: translateX(18px);
    }
    body.app-dark-mode,
    body.app-dark-mode .stApp,
    body.app-dark-mode [data-testid="stAppViewContainer"] {
        background: #101b33 !important;
    }
    body.app-dark-mode .about-reference-panel,
    body.app-dark-mode .about-reference-lower-panel,
    body.app-dark-mode .about-reference-hero {
        background: #172746 !important;
        border-color: #2b4672 !important;
    }
    body.app-dark-mode .about-reference-page h1,
    body.app-dark-mode .about-reference-page h2,
    body.app-dark-mode .about-reference-page strong {
        color: #e3edff !important;
    }
    body.app-dark-mode .about-reference-page p {
        color: #a9bddc !important;
    }
    body.app-dark-mode .stApp,
    body.app-dark-mode [data-testid="stMainBlockContainer"],
    body.app-dark-mode [data-testid="stVerticalBlockBorderWrapper"],
    body.app-dark-mode div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        background: #172746 !important;
        border-color: #2b4672 !important;
    }
    body.app-dark-mode .stApp * {
        color: #e3edff !important;
    }
    body.app-dark-mode .navbar,
    body.app-dark-mode .navbar * {
        color: white !important;
    }
    body.app-dark-mode div[data-baseweb="input"] > div,
    body.app-dark-mode div[data-baseweb="select"] > div,
    body.app-dark-mode div[data-testid="stTextInputRootElement"],
    body.app-dark-mode div[data-testid="stSelectbox"] div[role="group"] {
        background: #20365c !important;
        border-color: #41669d !important;
    }
    body.app-dark-mode input,
    body.app-dark-mode textarea,
    body.app-dark-mode [role="combobox"] {
        color: #e3edff !important;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(rgba(20,20,40,0.45), rgba(20,20,40,0.45)),
                    url("https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-position: center;
        overflow: hidden;
        padding: 60px 40px;
        text-align: center;
        height: 32rem;
        width: 100vw;
        margin-left: calc((100% - 100vw) / 2);
        margin-bottom: -18rem;
        position: relative;
        z-index: 1;
        margin-top: 60px;
    }
.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin: -55px 0 10px 0;
    line-height: 1.12;
    letter-spacing: -0.8px;
    text-align: center;

    background: linear-gradient(
        90deg,
        #FFFFFF 10%,
        #DDEBFF 20%,
        #AFC8FF 50%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow: 0 3px 10px rgba(0, 0, 0, 0.20);
} 
.hero p {
    font-size: 16px;
    font-weight: 500;
 
color: #E2E8F0 !important;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.6;
    letter-spacing: 0.2px;
    text-shadow: 0 2px 7px rgba(0, 0, 0, 0.4);
}



    .section-title {
        font-weight: 700;
        font-size: 17px;
        margin-bottom: 14px;
        color: inherit !important;
    }
    .basics-title { color: #2953b8 !important; }
    .structure-title { color: #1f9d6b !important; }
    .features-title { color: #7c4fd6 !important; }

    /* Card look + colors for each of the three input sections */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        background: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        height: 100%;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(1)
        div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #d7e3fb !important;
        margin: 0 8px 20px !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2)
        div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #d1f0de !important;
        margin: 0 8px 20px !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(3)
        div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #e3d9fb !important;
        margin: 0 8px 20px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 20px 20px 12px 20px;
    }

    /* Keep the three input cards visually consistent */
  /* =========================================================
   MODERN INPUT CARDS
   ========================================================= */

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box !important;
    margin: 12px 8px 24px !important;

    padding: 22px !important;
    border-radius: 18px !important;

    /* Soft premium background */
    background: linear-gradient(
        145deg,
        rgba(255, 255, 255, 0.98),
        rgba(248, 251, 255, 0.96)
    ) !important;

    /* Elegant border */
    border: 1px solid rgba(218, 228, 240, 0.95) !important;

    /* Soft shadow */
    box-shadow:
        0 8px 25px rgba(24, 55, 90, 0.08),
        0 2px 6px rgba(24, 55, 90, 0.04) !important;

    position: relative !important;
    z-index: 1 !important;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease !important;
}


/* =========================================================
   HOVER EFFECT
   ========================================================= */

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:hover {
    transform: translateY(-4px) !important;

    box-shadow:
        0 16px 35px rgba(24, 55, 90, 0.12),
        0 4px 10px rgba(24, 55, 90, 0.05) !important;

    border-color: rgba(76, 126, 205, 0.35) !important;
}


/* =========================================================
   TOP GLOW LINE
   ========================================================= */

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]::before {
    content: "" !important;

    position: absolute !important;
    top: 0 !important;
    left: 18px !important;
    right: 18px !important;

    height: 3px !important;

    border-radius: 0 0 10px 10px !important;

    background: linear-gradient(
        90deg,
        #2474ed,
        #6952e8
    ) !important;

    opacity: 0.85 !important;
}


/* =========================================================
   FIRST CARD - BASICS
   ========================================================= */

div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:nth-child(1) {

    background: linear-gradient(
        145deg,
        #f3faff 0%,
        #edf7ff 100%
    ) !important;

    border-color: #d4e9fb !important;
}

div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:nth-child(1)::before {

    background: linear-gradient(
        90deg,
        #1976e8,
        #4c8ff2
    ) !important;
}


/* =========================================================
   SECOND CARD - STRUCTURE
   ========================================================= */

div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:nth-child(2) {

    background: linear-gradient(
        145deg,
        #f2fcf9 0%,
        #ebfaf6 100%
    ) !important;

    border-color: #d0eee5 !important;
}

div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:nth-child(2)::before {

    background: linear-gradient(
        90deg,
        #08a17e,
        #24b99a
    ) !important;
}


/* =========================================================
   THIRD CARD - FEATURES
   ========================================================= */

div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:nth-child(3) {

    background: linear-gradient(
        145deg,
        #faf7ff 0%,
        #f5f1ff 100%
    ) !important;

    border-color: #e4dafa !important;
}

div[data-testid="stHorizontalBlock"]
> div[data-testid="stColumn"]:nth-child(3)::before {

    background: linear-gradient(
        90deg,
        #6945dc,
        #875eea
    ) !important;
}


/* =========================================================
   INPUT LABELS
   ========================================================= */

div[data-testid="stWidgetLabel"] p {

    color: #243e5e !important;

    font-size: 11px !important;

    font-weight: 700 !important;

    letter-spacing: 0.1px !important;

    margin-bottom: 4px !important;
}


/* =========================================================
   INPUT AND SELECT CONTROLS
   ========================================================= */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    min-height: 50px !important;
    height: 50px !important;
    background: transparent !important;
    border: 1px solid #D6E5FF !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-baseweb="select"] > div > div {
    min-height: 48px !important;
    background: transparent !important;
    border: 0 !important;
    border-radius: 9px !important;
    box-shadow: none !important;
}

/* Streamlit's current widget surfaces */
div[data-testid="stTextInputRootElement"],
div[data-testid="stSelectbox"] div[role="group"] {
    min-height: 50px !important;
    height: 50px !important;
    background: transparent !important;
    border: 1px solid #D6E5FF !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1)
div[data-testid="stTextInputRootElement"],
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1)
div[data-testid="stSelectbox"] div[role="group"] {
    background: linear-gradient(145deg, #f3faff 0%, #edf7ff 100%) !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2)
div[data-testid="stTextInputRootElement"],
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2)
div[data-testid="stSelectbox"] div[role="group"] {
    background: linear-gradient(145deg, #f2fcf9 0%, #ebfaf6 100%) !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3)
div[data-testid="stTextInputRootElement"],
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3)
div[data-testid="stSelectbox"] div[role="group"] {
    background: linear-gradient(145deg, #faf7ff 0%, #f5f1ff 100%) !important;
}

div[data-testid="stTextInputRootElement"] input,
div[data-testid="stSelectbox"] input[role="combobox"] {
    background: transparent !important;
    color: #172554 !important;
    font-size: 15px !important;
}

/* Selectbox dropdown menu */
div[data-baseweb="menu"],
div[role="listbox"] {
    background: #f3faff !important;
    border: 1px solid #D6E5FF !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 20px rgba(24, 55, 90, 0.12) !important;
}

div[data-baseweb="menu"] [role="option"],
div[role="listbox"] [role="option"] {
    background: transparent !important;
    color: #172554 !important;
    font-size: 15px !important;
}

div[data-baseweb="menu"] [role="option"]:hover,
div[role="listbox"] [role="option"]:hover,
div[data-baseweb="menu"] [role="option"][aria-selected="true"],
div[role="listbox"] [role="option"][aria-selected="true"] {
    background: #D6E5FF !important;
    color: #172554 !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1)
div[data-baseweb="input"] > div,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1)
div[data-baseweb="select"] > div {
    background: linear-gradient(145deg, #f3faff 0%, #edf7ff 100%) !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2)
div[data-baseweb="input"] > div,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2)
div[data-baseweb="select"] > div {
    background: linear-gradient(145deg, #f2fcf9 0%, #ebfaf6 100%) !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3)
div[data-baseweb="input"] > div,
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3)
div[data-baseweb="select"] > div {
    background: linear-gradient(145deg, #faf7ff 0%, #f5f1ff 100%) !important;
}


/* =========================================================
   INPUT FOCUS
   ========================================================= */

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within,
div[data-testid="stTextInputRootElement"]:focus-within,
div[data-testid="stSelectbox"] div[role="group"]:focus-within {
    border-color: #60A5FA !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,0.15) !important;
}


/* =========================================================
   INPUT TEXT
   ========================================================= */

div[data-baseweb="input"] input {
    height: 48px !important;
    background: transparent !important;
    color: #172554 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}


/* =========================================================
   SELECTBOX TEXT
   ========================================================= */

div[data-baseweb="select"] * {
    font-size: 15px !important;
    color: #172554 !important;
}

div[data-baseweb="select"] svg {
    color: #172554 !important;
    fill: #172554 !important;
}


/* =========================================================
   SPACE BETWEEN INPUTS
   ========================================================= */

div[data-testid="stSelectbox"],
div[data-testid="stNumberInput"] {

    margin-bottom: 9px !important;
}

    /* Predict button */
    div.stButton,
    div[data-testid="stButton"] {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto !important;
        margin-bottom: 32px !important;
    }

    div[data-testid="stElementContainer"]:has(> div[data-testid="stButton"]) {
        width: calc(100% + 10px) !important;
        display: flex !important;
        justify-content: center !important;
        
    }
    div.stButton > button,
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #3b5bfd, #7c4fd6) !important;
        color: white !important;
        font-weight: 700;
        font-size: 16px;
        padding: 12px 40px;
        border-radius: 20px;
        border: none;
        width: fit-content !important;
        margin: 10px auto 0 !important;
    }
    div.stButton > button:hover {
        opacity: 0.68;
        color: gray !important;
        scale: 1.08;
    }
    div.stButton > button p { color: white !important; }
    .view-insights-link {
        display: block;
        width: fit-content;
        margin: 10px auto 32px;
        padding: 12px 40px;
        border-radius: 20px;
        background: linear-gradient(90deg, #3b5bfd, #7c4fd6) !important;
        color: white !important;
        font-size: 16px;
        font-weight: 700;
        text-decoration: none !important;
        transition: opacity 0.2s ease, transform 0.2s ease;
    }
    .view-insights-link:hover {
        opacity: 0.68;
        color: white !important;
        transform: scale(1.08);
    }

    /* ================================
   RESULT BOX
================================ */
.result-box {
    width: min(90%, 720px);
    min-height: 260px;
    margin: 28px auto 40px;
    padding: 38px 28px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(145deg, #ffffff 0%, #effbf6 100%);
    border: 1px solid #b8ead8;
    border-radius: 24px;
    box-shadow: 0 16px 38px rgba(20, 130, 100, 0.12);
    position: relative;
    overflow: hidden;
}


/* Decorative glow */
.result-box::after {
    content: "";
    position: absolute;

    width: 300px;
    height: 300px;

    right: -100px;
    bottom: -160px;

    background: rgba(55, 190, 145, 0.08);

    border-radius: 50%;
}


/* ================================
   HOUSE ICON AREA
================================ */
.result-icon {
    width: 76px;
    height: 76px;
    min-width: 76px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(145deg, #ecfff6, #d8f8e9);
    border-radius: 22px;
    font-size: 42px;
    box-shadow: 0 10px 24px rgba(35, 170, 120, 0.12);
}


/* Divider */
.result-divider {
    display: none;
}


/* ================================
   RESULT CONTENT
================================ */
.result-content {
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.result-label {
    font-size: 18px;
    font-weight: 700;
    color: #172b4d;
    margin: 18px 0 8px;
}


.result-price {
    font-size: clamp(42px, 6vw, 64px);
    font-weight: 800;
    line-height: 1.1;
    color: #16a673;
    letter-spacing: 0;
    margin: 0;
}

.result-scroll-spacer {
    height: 220px;
}

.insights-page {
    width: min(92%, 1100px);
    margin: 110px auto 50px;
}

.insights-heading {
    color: #172554 !important;
    font-size: clamp(30px, 5vw, 48px);
    margin: 0 0 8px;
    text-align: center;
}

.insights-subtitle {
    color: #64748B !important;
    font-size: 16px;
    margin: 0 auto 28px;
    text-align: center;
}

.insight-photo {
    display: block;
    width: 100%;
    height: 300px;
    object-fit: cover;
    margin: 0 0 28px calc((100% - 100vw) / 2);
    box-sizing: border-box;
    border-radius: 18px;
    border: 1px solid #D6E5FF;
    box-shadow: 0 12px 28px rgba(24, 55, 90, 0.12);
}

.insight-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
}

.insight-card {
    min-height: 132px;
    padding: 22px;
    background: #ffffff;
    border: 1px solid #D6E5FF;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(24, 55, 90, 0.08);
}

.insight-card-label {
    color: #64748B !important;
    font-size: 14px;
    margin-bottom: 10px;
}

.insight-card-value {
    color: #172554 !important;
    font-size: 24px;
    font-weight: 800;
}

.insight-note {
    margin: 22px 0 28px;
    padding: 20px 22px;
    background: #effbf6;
    border-left: 4px solid #16a673;
    border-radius: 12px;
    color: #172554 !important;
    line-height: 1.6;
}

/* Reference-style insights dashboard */
.insights-dashboard {
    --insight-ink: #12356f;
    --insight-muted: #6682ad;
    width: min(96%, 1640px);
    margin: 78px auto 36px;
    color: var(--insight-ink);
}

.insights-empty-state {
    max-width: 680px;
    margin: 120px auto;
    padding: 56px 32px;
    text-align: center;
    background: #ffffff;
    border: 1px solid #dceafa;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(36, 81, 139, 0.07);
}

.insights-empty-state h1 {
    margin: 0 0 12px;
    color: #12356f !important;
    font-size: 32px;
}

.insights-empty-state p {
    margin: 0;
    color: #6682ad !important;
}

body.app-dark-mode .insights-empty-state {
    background: #172746 !important;
    border-color: #2b4672 !important;
}

body.app-dark-mode .insights-empty-state h1 {
    color: #e3edff !important;
}

body.app-dark-mode .insights-empty-state p {
    color: #a9bddc !important;
}

.insights-dashboard .insights-page-title {
    display: none;
}

.insights-hero-panel {
    display: grid;
    grid-template-columns: minmax(300px, 34%) 1fr;
    min-height: 205px;
    overflow: hidden;
    margin-bottom: 24px;
    background: linear-gradient(110deg, #f0f8ff 0%, #ffffff 64%, #eaf5ff 100%);
    border: 1px solid #dceafa;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(36, 81, 139, 0.07);
}

.insights-hero-photo {
    width: 100%;
    height: 205px;
    object-fit: cover;
}

.insights-hero-copy {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 28px 34px;
    background: linear-gradient(105deg, rgba(255,255,255,0.62), rgba(237,247,255,0.82));
}

.insights-eyebrow {
    margin-bottom: 10px;
    color: #387cf0 !important;
    font-size: 15px;
    font-weight: 700;
}

.insights-hero-copy h1 {
    margin: 0 0 10px;
    color: var(--insight-ink) !important;
    font-size: clamp(28px, 3vw, 42px);
    line-height: 1.1;
}

.insights-hero-copy p {
    max-width: 620px;
    margin: 0;
    color: var(--insight-muted) !important;
    font-size: 16px;
    line-height: 1.55;
}

.insights-location {
    align-self: flex-start;
    margin-top: 18px;
    padding: 8px 14px;
    color: var(--insight-ink) !important;
    background: #edf3ff;
    border-radius: 18px;
    font-size: 13px;
    font-weight: 700;
}

.insights-metric-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 22px;
    margin-bottom: 24px;
}

.insights-metric-card {
    position: relative;
    min-height: 128px;
    padding: 20px 24px 18px 88px;
    overflow: hidden;
    border: 1px solid #e1eafa;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(44, 82, 131, 0.07);
}

.insights-metric-card:nth-child(1) { background: linear-gradient(135deg, #f3faff, #ffffff); }
.insights-metric-card:nth-child(2) { background: linear-gradient(135deg, #faf6ff, #ffffff); }
.insights-metric-card:nth-child(3) { background: linear-gradient(135deg, #effcf9, #ffffff); }
.insights-metric-card:nth-child(4) { background: linear-gradient(135deg, #fff5fb, #ffffff); }
.insights-metric-card:nth-child(5) { background: linear-gradient(135deg, #effdff, #ffffff); }
.insights-metric-card:nth-child(6) { background: linear-gradient(135deg, #fffaf0, #ffffff); }

.insight-metric-icon {
    position: absolute;
    top: 20px;
    left: 24px;
    display: grid;
    width: 44px;
    height: 44px;
    place-items: center;
    color: white !important;
    border-radius: 50%;
    font-size: 22px;
}

.insights-metric-card:nth-child(1) .insight-metric-icon { background: #315be9; }
.insights-metric-card:nth-child(2) .insight-metric-icon { background: #7652df; }
.insights-metric-card:nth-child(3) .insight-metric-icon { background: #0eaf9a; }
.insights-metric-card:nth-child(4) .insight-metric-icon { background: #cc3ca8; }
.insights-metric-card:nth-child(5) .insight-metric-icon { background: #10abb6; }
.insights-metric-card:nth-child(6) .insight-metric-icon { background: #f39a0b; }

.insights-market-trend {
    position: absolute;
    top: 22px;
    right: 24px;
    padding: 8px 12px;
    color: #0eaf9a !important;
    background: rgba(223, 250, 244, 0.72);
    border-radius: 18px;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
}

.insights-market-trend strong {
    display: block;
    margin-top: 2px;
    color: #0eaf9a !important;
    font-size: 15px;
}

.insights-metric-label {
    margin-bottom: 8px;
    color: var(--insight-muted) !important;
    font-size: 14px;
}

.insights-metric-value {
    margin-bottom: 10px;
    color: var(--insight-ink) !important;
    font-size: clamp(22px, 2vw, 30px);
    font-weight: 800;
}

.insights-metric-detail {
    color: var(--insight-muted) !important;
    font-size: 12px;
}

.insights-key-strip {
    display: grid;
    grid-template-columns: 1.3fr repeat(4, 1fr);
    gap: 0;
    padding: 22px 24px;
    background: linear-gradient(105deg, #f2f9ff, #ffffff);
    border: 1px solid #dceafa;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(44, 82, 131, 0.06);
}

.key-strip-intro,
.key-strip-item {
    padding: 4px 22px;
}

.key-strip-item {
    border-left: 1px solid #dce7f5;
}

.key-strip-intro h2 {
    margin: 0 0 10px;
    color: var(--insight-ink) !important;
    font-size: 22px;
}

.key-strip-intro p,
.key-strip-item p {
    margin: 0;
    color: var(--insight-muted) !important;
    font-size: 12px;
    line-height: 1.55;
}

.key-strip-item strong {
    display: block;
    margin-bottom: 7px;
    color: var(--insight-ink) !important;
    font-size: 13px;
}

.key-strip-icon {
    display: inline-grid;
    width: 34px;
    height: 34px;
    margin-bottom: 10px;
    place-items: center;
    border-radius: 50%;
    background: #dff2e8;
    color: #1aaf73 !important;
}

.insights-back-button {
    margin: 22px auto 0;
    text-align: center;
}

.about-dashboard {
    width: min(92%, 1120px);
    margin: 108px auto 50px;
    color: #12356f;
}

.about-hero {
    padding: 48px 42px;
    text-align: center;
    background: linear-gradient(135deg, #edf7ff 0%, #ffffff 55%, #eefbf8 100%);
    border: 1px solid #dceafa;
    border-radius: 22px;
    box-shadow: 0 12px 28px rgba(36, 81, 139, 0.08);
}

.about-hero-icon {
    display: grid;
    width: 68px;
    height: 68px;
    margin: 0 auto 18px;
    place-items: center;
    color: white !important;
    background: linear-gradient(135deg, #315be9, #16a673);
    border-radius: 20px;
    font-size: 34px;
}

.about-hero h1 {
    margin: 0 0 12px;
    color: #12356f !important;
    font-size: clamp(30px, 5vw, 48px);
}

.about-hero p {
    max-width: 720px;
    margin: 0 auto;
    color: #6682ad !important;
    font-size: 17px;
    line-height: 1.65;
}

.about-card-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 20px;
    margin-top: 24px;
}

.about-card {
    min-height: 190px;
    padding: 26px;
    background: white;
    border: 1px solid #dceafa;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(36, 81, 139, 0.07);
}

.about-card-icon {
    margin-bottom: 14px;
    color: #315be9 !important;
    font-size: 28px;
}

.about-card h2 {
    margin: 0 0 10px;
    color: #12356f !important;
    font-size: 20px;
}

.about-card p {
    margin: 0;
    color: #6682ad !important;
    font-size: 14px;
    line-height: 1.6;
}

.about-flow {
    margin-top: 24px;
    padding: 26px 30px;
    background: #ffffff;
    border: 1px solid #dceafa;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(36, 81, 139, 0.06);
}

.about-flow h2 {
    margin: 0 0 18px;
    color: #12356f !important;
    font-size: 22px;
}

.about-flow-steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.about-flow-step strong {
    display: block;
    margin-bottom: 6px;
    color: #12356f !important;
}

.about-flow-step p {
    margin: 0;
    color: #6682ad !important;
    font-size: 13px;
    line-height: 1.5;
}

.about-reference-page {
    width: min(96%, 1640px);
    margin: 78px auto 36px;
    color: #12356f;
}

.about-reference-hero {
    display: grid;
    grid-template-columns: 1.08fr 0.92fr;
    min-height: 184px;
    overflow: hidden;
    background: linear-gradient(105deg, #e5f7ff 0%, #ffffff 55%, #eef0ff 100%);
    border: 1px solid #dceafa;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(36, 81, 139, 0.07);
}

.about-reference-copy {
    padding: 28px 32px;
}

.about-reference-badge {
    display: inline-block;
    margin-bottom: 10px;
    padding: 7px 13px;
    color: #2563c7 !important;
    background: #d8efff;
    border-radius: 18px;
    font-size: 13px;
    font-weight: 700;
}

.about-reference-copy h1 {
    margin: 0 0 10px;
    color: #12356f !important;
    font-size: clamp(30px, 3.2vw, 43px);
}

.about-reference-copy p {
    max-width: 610px;
    margin: 0;
    color: #2e67a4 !important;
    font-size: 16px;
    line-height: 1.55;
}

.about-reference-house {
    width: 100%;
    height: 184px;
    object-fit: cover;
    object-position: center;
}

.about-reference-row {
    display: grid;
    grid-template-columns: 0.82fr 1.18fr;
    gap: 18px;
    margin-top: 18px;
}

.about-reference-panel,
.about-reference-lower-panel {
    padding: 24px;
    background: rgba(255, 255, 255, 0.86);
    border: 1px solid #dceafa;
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(36, 81, 139, 0.06);
}

.about-reference-panel h2,
.about-reference-lower-panel h2 {
    margin: 0 0 18px;
    color: #12356f !important;
    font-size: 21px;
}

.about-reference-panel p,
.about-reference-lower-panel p {
    margin: 0;
    color: #6682ad !important;
    font-size: 13px;
    line-height: 1.6;
}

.about-application-content {
    display: grid;
    grid-template-columns: 112px 1fr;
    gap: 20px;
    align-items: center;
}

.about-application-icon {
    display: grid;
    width: 98px;
    height: 98px;
    place-items: center;
    color: #2f74e8 !important;
    background: linear-gradient(145deg, #e6f3ff, #d4eaff);
    border-radius: 22px;
    font-size: 54px;
}

.about-workflow {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.about-workflow-step {
    position: relative;
    padding: 8px 12px;
    text-align: center;
}

.about-workflow-step:not(:last-child)::after {
    content: "→";
    position: absolute;
    top: 28px;
    right: -14px;
    color: #b4d5ff !important;
    font-size: 26px;
}

.about-workflow-icon {
    display: grid;
    width: 58px;
    height: 58px;
    margin: 0 auto 12px;
    place-items: center;
    border-radius: 50%;
    background: #e8e4ff;
    color: #7955e8 !important;
    font-size: 27px;
}

.about-workflow-step strong {
    display: block;
    margin-bottom: 6px;
    color: #12356f !important;
    font-size: 13px;
}

.about-workflow-step p {
    font-size: 12px;
}

.about-reference-lower {
    display: grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr) minmax(0, 0.9fr);
    gap: 18px;
    margin-top: 18px;
}

.about-benefit-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
}

.about-benefit strong {
    display: block;
    margin-bottom: 5px;
    color: #12356f !important;
    font-size: 13px;
}

.about-benefit p {
    font-size: 12px;
}

.about-tech-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
}

.about-tech {
    padding: 14px 8px;
    text-align: center;
    background: #f8fbff;
    border: 1px solid #e1ebfa;
    border-radius: 10px;
}

.about-tech strong {
    display: block;
    margin-top: 5px;
    color: #12356f !important;
    font-size: 12px;
}

.about-feature-list {
    display: grid;
    gap: 10px;
}

.about-feature-list p::before {
    content: "✓";
    display: inline-grid;
    width: 18px;
    height: 18px;
    margin-right: 8px;
    place-items: center;
    color: white !important;
    background: #4771ed;
    border-radius: 50%;
    font-size: 11px;
}

@media (max-width: 900px) {
    .about-reference-hero,
    .about-reference-row,
    .about-reference-lower {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 640px) {
    .navbar {
        grid-template-columns: 1fr auto;
        padding: 12px 18px;
    }
    .navbar-links {

/* Keep every page readable when dark mode is enabled. */
body.app-dark-mode .hero,
body.app-dark-mode .result-box,
body.app-dark-mode div[data-testid="stVerticalBlockBorderWrapper"],
body.app-dark-mode div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
body.app-dark-mode .insights-hero-panel,
body.app-dark-mode .insights-metric-card,
body.app-dark-mode .insights-key-strip,
body.app-dark-mode .about-reference-panel,
body.app-dark-mode .about-reference-lower-panel {
    background: #172746 !important;
    border-color: #2b4672 !important;
    color: #e3edff !important;
}

body.app-dark-mode .insights-hero-copy,
body.app-dark-mode .about-reference-hero,
body.app-dark-mode div[data-baseweb="input"] > div,
body.app-dark-mode div[data-baseweb="select"] > div,
body.app-dark-mode div[data-testid="stTextInputRootElement"],
body.app-dark-mode div[data-testid="stSelectbox"] div[role="group"] {
    background: #20365c !important;
    border-color: #41669d !important;
}

body.app-dark-mode .about-reference-lower,
body.app-dark-mode .about-tech,
body.app-dark-mode .about-workflow-step,
body.app-dark-mode .insights-location,
body.app-dark-mode .insights-market-trend {
    background: #20365c !important;
    border-color: #41669d !important;
}

body.app-dark-mode .hero h1,
body.app-dark-mode .hero p,
body.app-dark-mode .section-title,
body.app-dark-mode .insights-dashboard h1,
body.app-dark-mode .insights-dashboard h2,
body.app-dark-mode .insights-dashboard strong,
body.app-dark-mode .insights-metric-value,
body.app-dark-mode .insights-metric-label,
body.app-dark-mode .insights-metric-detail,
body.app-dark-mode .key-strip-intro p,
body.app-dark-mode .key-strip-item p,
body.app-dark-mode .about-reference-page h1,
body.app-dark-mode .about-reference-page h2,
body.app-dark-mode .about-reference-page p,
body.app-dark-mode .about-reference-page strong,
body.app-dark-mode .about-tech strong,
body.app-dark-mode input,
body.app-dark-mode textarea,
body.app-dark-mode [role="combobox"] {
    color: #e3edff !important;
}

body.app-dark-mode .key-strip-item {
    border-color: #41669d !important;
}

body.app-dark-mode .stApp,
body.app-dark-mode [data-testid="stAppViewContainer"],
body.app-dark-mode [data-testid="stMain"],
body.app-dark-mode [data-testid="stMainBlockContainer"],
body.app-dark-mode [data-testid="stVerticalBlock"],
body.app-dark-mode [data-testid="stVerticalBlockBorderWrapper"],
body.app-dark-mode [data-testid="stHorizontalBlock"],
body.app-dark-mode [data-testid="stColumn"],
body.app-dark-mode .client-page.is-visible,
body.app-dark-mode .client-page:target,
body.app-dark-mode .result-box,
body.app-dark-mode .insights-metric-card,
body.app-dark-mode .about-reference-panel,
body.app-dark-mode .about-reference-lower-panel {
    opacity: 1 !important;
    filter: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
}

body.app-dark-mode [data-testid="stVerticalBlockBorderWrapper"] > div,
body.app-dark-mode [data-testid="stColumn"] > div,
body.app-dark-mode .insights-hero-panel,
body.app-dark-mode .insights-hero-copy,
body.app-dark-mode .insights-key-strip,
body.app-dark-mode .about-reference-hero,
body.app-dark-mode .about-reference-lower,
body.app-dark-mode .about-tech,
body.app-dark-mode .about-workflow-step {
    background-image: none !important;
    background-color: #172746 !important;
}

body.app-dark-mode .stApp * {
    text-shadow: none !important;
}
body.app-dark-mode .navbar {
    background: #071a36 !important;
    border-bottom: 1px solid #183d76 !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.28) !important;
}
body.app-dark-mode .insights-dashboard {
    --insight-ink: #f4f8ff;
    --insight-muted: #9bbbe8;
}
body.app-dark-mode .insights-hero-panel,
body.app-dark-mode .insights-hero-copy,
body.app-dark-mode .insights-key-strip,
body.app-dark-mode .insights-metric-card,
body.app-dark-mode .insights-metric-card:nth-child(1),
body.app-dark-mode .insights-metric-card:nth-child(2),
body.app-dark-mode .insights-metric-card:nth-child(3),
body.app-dark-mode .insights-metric-card:nth-child(4),
body.app-dark-mode .insights-metric-card:nth-child(5),
body.app-dark-mode .insights-metric-card:nth-child(6) {
    background: #0b2144 !important;
    border-color: #1d4b8e !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.28) !important;
}
body.app-dark-mode .insights-hero-copy {
    background: linear-gradient(105deg, #0b2144, #0a1c3a) !important;
}
body.app-dark-mode .insights-location {
    color: #dceaff !important;
    background: #173b76 !important;
}
body.app-dark-mode .insights-market-trend {
    color: #43e0bb !important;
    background: #073b4a !important;
}
body.app-dark-mode .insights-market-trend strong {
    color: #43e0bb !important;
}
body.app-dark-mode .key-strip-item {
    border-color: #1d4b8e !important;
}
body.app-dark-mode .about-reference-lower-panel,
body.app-dark-mode .about-tech {
    background: #0b2144 !important;
    border-color: #1d4b8e !important;
    color: #e3edff !important;
}
body.app-dark-mode .about-tech strong,
body.app-dark-mode .about-tech p {
    color: #b8d0f4 !important;
}
body.app-dark-mode .about-reference-lower-panel h2 {
    color: #f4f8ff !important;
}
        grid-column: 1 / -1;
        grid-row: 2;
        order: 3;
    }
    .navbar-actions { grid-column: 2; grid-row: 1; }
    .navbar-brand { font-size: 16px; }
    .about-reference-page { margin-top: 116px; }
    .about-reference-copy { padding: 24px 20px; }
    .about-reference-house { height: 180px; }
    .about-workflow { grid-template-columns: 1fr; }
    .about-workflow-step:not(:last-child)::after { content: "↓"; top: auto; right: 50%; bottom: -22px; }
    .about-benefit-grid { grid-template-columns: 1fr; }
}

@media (max-width: 760px) {
    .about-card-grid,
    .about-flow-steps {
        grid-template-columns: 1fr;
    }

    .about-hero {
        padding: 34px 22px;
    }
}

@media (max-width: 900px) {
    .insights-metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .insights-key-strip { grid-template-columns: repeat(2, 1fr); }
    .key-strip-intro { grid-column: 1 / -1; padding-bottom: 18px; }
    .key-strip-item:nth-child(3) { border-left: 0; }
}

@media (max-width: 640px) {
    .insights-dashboard { width: 94%; margin-top: 72px; }
    .insights-hero-panel { grid-template-columns: 1fr; }
    .insights-hero-photo { height: 220px; }
    .insights-metric-grid,
    .insights-key-strip { grid-template-columns: 1fr; }
    .key-strip-item,
    .key-strip-item:nth-child(3) { border-left: 0; border-top: 1px solid #dce7f5; }
    .key-strip-item { padding: 18px 0 4px; }
}

@media (max-width: 768px) {
    .insight-grid {
        grid-template-columns: 1fr;
    }

    .insight-photo {
        height: 220px;
    }
}


/* ================================
   INFO BADGE
================================ */
.result-badge {
    display: inline-flex;
    align-items: center;

    padding: 10px 20px;

    background: #ddf8ec;

    border-radius: 30px;

    color: #36967a;

    font-size: 16px;
    font-weight: 500;
}


/* ================================
   RESPONSIVE
================================ */
@media (max-width: 768px) {

    .result-box {
        width: 94%;
        min-height: 230px;
        padding: 30px 20px;
    }

    .result-divider {
        display: none;
    }

    .result-price {
        font-size: 42px;
    }

    .result-icon {
        width: 110px;
        height: 110px;
        min-width: 110px;
        font-size: 55px;
    }

    .result-badge {
        font-size: 14px;
    }
}
    }
body.app-dark-mode .navbar { background: #071a36 !important; border-bottom: 1px solid #183d76 !important; }
body.app-dark-mode .insights-dashboard { --insight-ink: #f4f8ff; --insight-muted: #9bbbe8; }
body.app-dark-mode .insights-hero-panel,
body.app-dark-mode .insights-hero-copy,
body.app-dark-mode .insights-key-strip,
body.app-dark-mode .insights-metric-card,
body.app-dark-mode .insights-metric-card:nth-child(1),
body.app-dark-mode .insights-metric-card:nth-child(2),
body.app-dark-mode .insights-metric-card:nth-child(3),
body.app-dark-mode .insights-metric-card:nth-child(4),
body.app-dark-mode .insights-metric-card:nth-child(5),
body.app-dark-mode .insights-metric-card:nth-child(6) {
    background: #0b2144 !important;
    border-color: #1d4b8e !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.28) !important;
}
body.app-dark-mode .insights-hero-copy { background: linear-gradient(105deg, #0b2144, #0a1c3a) !important; }
body.app-dark-mode .insights-location { color: #dceaff !important; background: #173b76 !important; }
body.app-dark-mode .insights-market-trend,
body.app-dark-mode .insights-market-trend strong { color: #43e0bb !important; }
body.app-dark-mode .insights-market-trend { background: #073b4a !important; }
body.app-dark-mode .key-strip-item { border-color: #1d4b8e !important; }
body.app-dark-mode .result-box {
    background: #0b2144 !important;
    border-color: #1d4b8e !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3) !important;
}
body.app-dark-mode .result-box::after {
    background: rgba(49, 91, 233, 0.14) !important;
}
body.app-dark-mode .result-icon {
    background: #173b76 !important;
    box-shadow: 0 10px 24px rgba(49, 91, 233, 0.24) !important;
}
body.app-dark-mode .result-label {
    color: #9bbbe8 !important;
}
body.app-dark-mode .result-price {
    color: #43e0bb !important;
}
body.app-dark-mode .about-reference-lower-panel,
body.app-dark-mode .about-tech {
    background: #0b2144 !important;
    border-color: #1d4b8e !important;
    color: #e3edff !important;
}
body.app-dark-mode .about-tech strong,
body.app-dark-mode .about-tech p {
    color: #b8d0f4 !important;
}
body.app-dark-mode .about-reference-lower-panel h2 {
    color: #f4f8ff !important;
}
div[data-testid="stTextInputRootElement"] input,
div[data-testid="stSelectbox"] input[role="combobox"],
div[data-baseweb="input"] input,
div[data-baseweb="select"] input[role="combobox"] {
    font-weight: 700 !important;
}
div[data-baseweb="menu"] [role="option"],
div[role="listbox"] [role="option"] {
    font-weight: 700 !important;
}
body.app-dark-mode div[data-testid="stTextInputRootElement"] input,
body.app-dark-mode div[data-testid="stSelectbox"] input[role="combobox"],
body.app-dark-mode div[data-baseweb="input"] input,
body.app-dark-mode div[data-baseweb="select"] input[role="combobox"] {
    color: #172554 !important;
    caret-color: #172554 !important;
}
body.app-dark-mode div[data-testid="stTextInputRootElement"] input::placeholder {
    color: #52698f !important;
    opacity: 1 !important;
}
body.app-dark-mode div[data-baseweb="select"] svg {
    color: #315be9 !important;
    fill: #315be9 !important;
}
div[data-testid="stCheckbox"] [role="switch"] {
    background: #a9bdd8 !important;
    border: 1px solid #7895bb !important;
}
div[data-testid="stCheckbox"] [role="switch"][aria-checked="true"] {
    background: #4771ed !important;
    border-color: #4771ed !important;
}
div[data-testid="stCheckbox"] [role="switch"]::after {
    background: #ffffff !important;
    box-shadow: 0 1px 4px rgba(24, 55, 90, 0.28) !important;
}
body.app-dark-mode div[data-testid="stCheckbox"] [role="switch"] {
    background: #41669d !important;
    border-color: #5e86c2 !important;
}
body.app-dark-mode div[data-testid="stCheckbox"] [role="switch"][aria-checked="true"] {
    background: #4771ed !important;
    border-color: #4771ed !important;
}
div[data-testid="stCheckbox"] > label > div:first-of-type {
    width: 42px !important;
    height: 24px !important;
    flex: 0 0 42px !important;
    background: #a9bdd8 !important;
    border: 1px solid #7895bb !important;
    border-radius: 999px !important;
}
div[data-testid="stCheckbox"] > label > div:first-of-type > div {
    width: 18px !important;
    height: 18px !important;
    margin: 2px !important;
    background: #ffffff !important;
    border-radius: 50% !important;
    box-shadow: 0 1px 4px rgba(24, 55, 90, 0.28) !important;
}
div[data-testid="stCheckbox"] > label[data-selected="true"] > div:first-of-type {
    background: #4771ed !important;
    border-color: #4771ed !important;
}
div[data-testid="stCheckbox"] > label[data-selected="true"] > div:first-of-type > div {
    transform: translateX(18px) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Navbar
# ---------------------------------------------------------
current_page = st.query_params.get("page", "predictor")
has_prediction = st.session_state.get("prediction") is not None
insights_nav_item = (
    f'<a href="#insights" data-page="insights" class="{"active" if current_page == INSIGHTS_PAGE else ""}">Insights</a>'
    if has_prediction
    else '<span class="disabled-link" aria-disabled="true">Insights</span>'
)

st.markdown(f"""
<div class="navbar">
    <div class="navbar-brand">🏠 House Price Predictor</div>
    <div class="navbar-links">
        <a href="#predictor" data-page="predictor" class="{"active" if current_page == "predictor" else ""}">🏡 Home</a>
        {insights_nav_item}
        <a href="#about" data-page="about" class="{"active" if current_page == ABOUT_PAGE else ""}">ⓘ About</a>
    </div>
    <div class="navbar-actions">
        <span aria-hidden="true">☀</span>
        <label class="mode-toggle" title="Toggle theme">
            <input id="mode-toggle" type="checkbox">
            <span class="mode-slider"></span>
        </label>
        <span aria-hidden="true">☾</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.html(
    """
    <script>
        const appDocument = window.parent && window.parent.document
            ? window.parent.document
            : document;
        const appStorage = window.parent && window.parent.localStorage
            ? window.parent.localStorage
            : window.localStorage;
        const modeToggle = appDocument.getElementById('mode-toggle');
        if (modeToggle) {
            const savedDarkMode = appStorage.getItem('house-price-dark-mode') === 'true';
            appDocument.body.classList.toggle('app-dark-mode', savedDarkMode);
            modeToggle.checked = savedDarkMode;
            modeToggle.addEventListener('change', (event) => {
                appDocument.body.classList.toggle('app-dark-mode', event.target.checked);
                appStorage.setItem(
                    'house-price-dark-mode',
                    String(event.target.checked),
                );
            });
        }
    </script>
    """,
    unsafe_allow_javascript=True,
)

st.html(
    f"""
    <div id="about" class="client-page" data-client-page="about">
        <main class="about-reference-page">
            <section class="about-reference-hero">
                <div class="about-reference-copy">
                    <span class="about-reference-badge">ⓘ &nbsp; About Our Project</span>
                    <h1>House Price Predictor</h1>
                    <p>A smart and data-driven web application that helps you estimate house prices based on key property features using machine learning.</p>
                </div>
                <img class="about-reference-house" src="{PROPERTY_PHOTOS[0]}" alt="Modern house preview">
            </section>

            <section class="about-reference-row">
                <article class="about-reference-panel">
                    <h2>▣ &nbsp; What is This Application?</h2>
                    <div class="about-application-content">
                        <div class="about-application-icon">⌂</div>
                        <div>
                            <p>The House Price Predictor is a machine learning powered web application that predicts the estimated price of a house based on various property features such as location, area, number of bedrooms, bathrooms, and more.</p>
                            <p style="margin-top:12px;">It also provides useful insights about the property, helping you make informed decisions in the real estate market.</p>
                        </div>
                    </div>
                </article>
                <article class="about-reference-panel">
                    <h2>⚙ &nbsp; How It Works</h2>
                    <div class="about-workflow">
                        <div class="about-workflow-step">
                            <div class="about-workflow-icon">⌂</div>
                            <strong>1 &nbsp; Enter Property Details</strong>
                            <p>Fill in the required details about the property.</p>
                        </div>
                        <div class="about-workflow-step">
                            <div class="about-workflow-icon" style="background:#d9faf5;color:#10a98d !important;">✣</div>
                            <strong>2 &nbsp; ML Model Predicts Price</strong>
                            <p>Our machine learning model analyzes the data and estimates the house price.</p>
                        </div>
                        <div class="about-workflow-step">
                            <div class="about-workflow-icon" style="background:#dcecff;color:#2f74e8 !important;">▥</div>
                            <strong>3 &nbsp; View Insights</strong>
                            <p>Get the predicted price along with useful property insights and trends.</p>
                        </div>
                    </div>
                </article>
            </section>

            <section class="about-reference-lower">
                <article class="about-reference-lower-panel">
                    <h2>★ &nbsp; Why Use This Tool?</h2>
                    <div class="about-benefit-grid">
                        <div class="about-benefit"><strong>⚡ Fast Predictions</strong><p>Get instant and accurate price estimates.</p></div>
                        <div class="about-benefit"><strong>◎ Data-Driven Estimates</strong><p>Based on real market data and machine learning.</p></div>
                        <div class="about-benefit"><strong>♧ Easy to Understand Insights</strong><p>Simple and clear breakdowns of key factors.</p></div>
                        <div class="about-benefit"><strong>▣ User-Friendly Interface</strong><p>Clean, modern and responsive design for a better experience.</p></div>
                    </div>
                </article>
                <article class="about-reference-lower-panel">
                    <h2>⌘ &nbsp; Technology Stack</h2>
                    <div class="about-tech-grid">
                        <div class="about-tech">🐍<strong>Python</strong><p>Programming Language</p></div>
                        <div class="about-tech">👑<strong>Streamlit</strong><p>Web Framework</p></div>
                        <div class="about-tech">▦<strong>Pandas</strong><p>Data Analysis</p></div>
                        <div class="about-tech">●<strong>Scikit-learn</strong><p>Machine Learning</p></div>
                        <div class="about-tech">✣<strong>Machine Learning</strong><p>Model Building & Prediction</p></div>
                    </div>
                </article>
                <article class="about-reference-lower-panel">
                    <h2>♙ &nbsp; Project Features</h2>
                    <div class="about-feature-list">
                        <p>Accurate price prediction using machine learning</p>
                        <p>Detailed property insights and analysis</p>
                        <p>Interactive and easy-to-use UI</p>
                        <p>Responsive design for all devices</p>
                    </div>
                </article>
            </section>
        </main>
    </div>
    """
)

prediction = st.session_state.get("prediction")

if prediction is None:
    st.html(
        """
        <div id="insights" class="client-page" data-client-page="insights">
            <main class="insights-dashboard">
                <section class="insights-empty-state">
                    <h1>Property Insights</h1>
                    <p>Make a prediction first to view property insights.</p>
                </section>
            </main>
        </div>
        """
    )
else:
    st.html(
        f"""
        <div id="insights" class="client-page" data-client-page="insights">
        <main class="insights-dashboard">
            <section class="insights-hero-panel">
                <img class="insights-hero-photo" src="{prediction.get('photo_url', PROPERTY_PHOTOS[0])}" alt="Property preview">
                <div class="insights-hero-copy">
                    <div class="insights-eyebrow">📈 Property Insights</div>
                    <h1>Beautiful Home in {prediction['city']}</h1>
                    <p>Here's a quick look at the key details and insights about the property based on your input.</p>
                    <span class="insights-location">📍 {prediction['city']}</span>
                </div>
            </section>

            <section class="insights-metric-grid">
                <article class="insights-metric-card">
                    <span class="insight-metric-icon">⌂</span>
                    <div class="insights-metric-label">Estimated value</div>
                    <div class="insights-metric-value">${prediction['price']:,.0f}</div>
                    <div class="insights-metric-detail">Predicted property value based on current market trends.</div>
                    <div class="insights-market-trend">↑ Market Trend<strong>+5.2%</strong></div>
                </article>
                <article class="insights-metric-card">
                    <span class="insight-metric-icon">⌖</span>
                    <div class="insights-metric-label">Location</div>
                    <div class="insights-metric-value">{prediction['city']}</div>
                    <div class="insights-metric-detail">Prime location with strong demand and growth.</div>
                </article>
                <article class="insights-metric-card">
                    <span class="insight-metric-icon">□</span>
                    <div class="insights-metric-label">Living area</div>
                    <div class="insights-metric-value">{prediction['living_val']:,.0f} sq ft</div>
                    <div class="insights-metric-detail">Spacious living area for a comfortable lifestyle.</div>
                </article>
                <article class="insights-metric-card">
                    <span class="insight-metric-icon">▣</span>
                    <div class="insights-metric-label">Bedrooms / bathrooms</div>
                    <div class="insights-metric-value">{prediction['bedrooms']} / {prediction['bathrooms']}</div>
                    <div class="insights-metric-detail">{prediction['bedrooms']} bedrooms &nbsp;|&nbsp; {prediction['bathrooms']} bathrooms</div>
                </article>
                <article class="insights-metric-card">
                    <span class="insight-metric-icon">⌗</span>
                    <div class="insights-metric-label">Lot area</div>
                    <div class="insights-metric-value">{prediction['lot_val']:,.0f} sq ft</div>
                    <div class="insights-metric-detail">Generous lot size with outdoor possibilities.</div>
                </article>
                <article class="insights-metric-card">
                    <span class="insight-metric-icon">◷</span>
                    <div class="insights-metric-label">House age</div>
                    <div class="insights-metric-value">{prediction['house_age']} years</div>
                    <div class="insights-metric-detail">Well-maintained home with modern features.</div>
                </article>
            </section>

            <section class="insights-key-strip">
                <div class="key-strip-intro">
                    <span class="key-strip-icon">✧</span>
                    <h2>Key Insights</h2>
                    <p>Based on the property details, here are some quick takeaways:</p>
                </div>
                <div class="key-strip-item">
                    <strong>Strong Value</strong>
                    <p>The estimated value of ${prediction['price']:,.0f} is competitive for the {prediction['city']} market.</p>
                </div>
                <div class="key-strip-item">
                    <strong>Great Location</strong>
                    <p>{prediction['city']} offers high demand, excellent amenities and long-term growth potential.</p>
                </div>
                <div class="key-strip-item">
                    <strong>Ideal Size</strong>
                    <p>{prediction['living_val']:,.0f} sq ft with {prediction['bedrooms']} beds and {prediction['bathrooms']} baths provides good space utilization.</p>
                </div>
                <div class="key-strip-item">
                    <strong>Good Investment</strong>
                    <p>With {prediction['house_age']} years of age, the home is relatively new and likely requires less immediate maintenance.</p>
                </div>
            </section>
        </main>
        </div>
        """,
    )

    st.html(
        """
        <script>
            const showInsightsHero = () => {
                const scrollArea = document.querySelector('[data-testid="stMain"]');
                if (scrollArea) {
                    scrollArea.scrollTo({ top: 0, behavior: 'instant' });
                    scrollArea.scrollTop = 0;
                }
            };

            setTimeout(showInsightsHero, 100);
            setTimeout(showInsightsHero, 500);
        </script>
        """,
        unsafe_allow_javascript=True,
    )


# ---------------------------------------------------------
# Hero section
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🏠 House Price Predictor</h1>
    <p>Get accurate <b>house price predictions</b> using advanced machine learning.
    Enter the property details below to find out the estimated price.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Form: three cards side by side
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container(key="basics-card"):
        st.markdown('<div class="section-title basics-title">🏠 Basics</div>', unsafe_allow_html=True)
        city = st.selectbox("City", ["Select City", "Seattle", "Portland", "San Francisco", "Los Angeles", "Austin"], index=1)
        zip_code = st.text_input("ZIP Code", value="98101", placeholder="e.g. 98101")
        living_area = st.text_input("Living Area (sq ft)", value="1500", placeholder="e.g. 1500")
        lot_area = st.text_input("Lot Area (sq ft)", value="5000", placeholder="e.g. 5000")

with col2:
    with st.container(key="structure-card"):
        st.markdown('<div class="section-title structure-title">🏢 Structure</div>', unsafe_allow_html=True)
        bedrooms = st.selectbox("Bedrooms", [1, 2, 3, 4, 5, 6], index=2)
        bathrooms = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)
        year_built = st.text_input("Year Built", value="2010", placeholder="e.g. 2010")
        house_age = st.text_input("House Age (years)", value="15", placeholder="e.g. 15")

with col3:
    with st.container(key="features-card"):
        st.markdown('<div class="section-title features-title">✨ Features</div>', unsafe_allow_html=True)
        renovated = st.toggle("Renovated", value=True)
        has_view = st.toggle("Has View", value=True)
        good_condition = st.toggle("Good Condition", value=True)
        floors = st.selectbox("Floors", [1, 1.5, 2, 2.5, 3], index=2)

st.write("")
predict_clicked = st.button("✨  Predict House Price")

# ---------------------------------------------------------
# Prediction logic (placeholder formula — swap in your real model)
# ---------------------------------------------------------
if predict_clicked:
    try:
        base_price = 150000
        living_val = float(living_area) if living_area else 1500
        lot_val = float(lot_area) if lot_area else 5000

        price = base_price
        price += living_val * 180
        price += lot_val * 5
        price += bedrooms * 8000
        price += bathrooms * 6000
        price += (2 - abs(floors - 2)) * 5000
        if renovated:
            price += 20000
        if has_view:
            price += 35000
        if good_condition:
            price += 15000
        if house_age:
            price -= float(house_age) * 500

        st.session_state["prediction"] = {
            "price": price,
            "city": city,
            "zip_code": zip_code,
            "living_val": living_val,
            "lot_val": lot_val,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "year_built": year_built,
            "house_age": float(house_age) if house_age else 0,
            "renovated": renovated,
            "has_view": has_view,
            "good_condition": good_condition,
            "floors": floors,
            "photo_url": random.choice(PROPERTY_PHOTOS),
        }
        st.session_state["just_predicted"] = True
        st.rerun()
    except ValueError:
        st.error("Please enter valid numeric values for area and house age.")

prediction = st.session_state.get("prediction")
just_predicted = st.session_state.pop("just_predicted", False)

if prediction is not None:
    price = prediction["price"]

    st.markdown(f"""
        <div class="result-box">
            <div class="result-icon">🏠</div>
            <div class="result-content">
                <div class="result-label">Estimated House Price</div>
                <div class="result-price">${price:,.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.html(
        """
        <script>
            setTimeout(() => {
                const predictButton = Array.from(document.querySelectorAll('button'))
                    .find((button) => button.textContent.includes('Predict House Price'));
                if (predictButton) {
                    predictButton.style.opacity = '0.58';
                    predictButton.style.transition = 'opacity 0.2s ease';
                }
            }, 150);
        </script>
        """,
        unsafe_allow_javascript=True,
    )

    st.markdown(
        '<a href="#insights" data-page="insights" class="view-insights-link">📊 View Insights</a>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="result-scroll-spacer" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    if predict_clicked or just_predicted:
        st.html(
            """
            <script>
                const centerResultBox = () => {
                    const resultBox = document.querySelector('.result-box');
                    const scrollArea = document.querySelector('[data-testid="stMain"]');
                    const navbar = document.querySelector('.navbar');
                    if (!resultBox || !scrollArea) return;

                    const resultTop = resultBox.getBoundingClientRect().top;
                    const resultHeight = resultBox.getBoundingClientRect().height;
                    const navbarHeight = navbar ? navbar.getBoundingClientRect().height : 0;
                    const target = scrollArea.scrollTop + resultTop
                        - (scrollArea.clientHeight + navbarHeight - resultHeight) / 2;
                    const boundedTarget = Math.max(
                        0,
                        Math.min(target, scrollArea.scrollHeight - scrollArea.clientHeight),
                    );
                    scrollArea.scrollTo({ top: boundedTarget, behavior: 'smooth' });
                    setTimeout(() => {
                        scrollArea.scrollTop = boundedTarget;
                    }, 500);
                };

                setTimeout(centerResultBox, 400);
                setTimeout(centerResultBox, 1000);
                setTimeout(centerResultBox, 1600);
            </script>
            """,
            unsafe_allow_javascript=True,
        )

st.html(
    """
    <script>
        (() => {
            const showPage = (page, updateHistory = true) => {
                const validPages = ['predictor', 'insights', 'about'];
                const activePage = validPages.includes(page) ? page : 'predictor';

                document.querySelectorAll('[data-client-page]').forEach((panel) => {
                    panel.classList.toggle(
                        'is-visible',
                        panel.dataset.clientPage === activePage,
                    );
                });
                document.querySelectorAll('.navbar-links [data-page]').forEach((link) => {
                    link.classList.toggle('active', link.dataset.page === activePage);
                    if (link.dataset.page === activePage) {
                        link.setAttribute('aria-current', 'page');
                    } else {
                        link.removeAttribute('aria-current');
                    }
                });

                if (updateHistory) {
                    const nextUrl = activePage === 'predictor'
                        ? window.location.pathname
                        : `${window.location.pathname}#${activePage}`;
                    window.history.replaceState({}, '', nextUrl);
                }
            };

            const insightsNav = document.querySelector('.navbar-links .disabled-link');
            if (insightsNav && document.querySelector('.result-box')) {
                insightsNav.outerHTML = '<a href="#insights" data-page="insights">Insights</a>';
            }

            document.addEventListener('click', (event) => {
                const link = event.target.closest('[data-page]');
                if (!link) return;
                event.preventDefault();
                showPage(link.dataset.page);
            });

            const queryPage = new URLSearchParams(window.location.search).get('page');
            const requestedPage = window.location.hash.slice(1) || queryPage || 'predictor';
            const insightsEnabled = Boolean(document.querySelector('[data-page="insights"]'));
            const initialPage = requestedPage === 'insights' && !insightsEnabled
                ? 'predictor'
                : requestedPage;
            showPage(initialPage, false);
            window.addEventListener('hashchange', () => {
                showPage(window.location.hash.slice(1) || 'predictor', false);
            });
            setTimeout(() => showPage(window.location.hash.slice(1) || initialPage, false), 250);
        })();
    </script>
    """,
    unsafe_allow_javascript=True,
)
