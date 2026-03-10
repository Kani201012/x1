import streamlit as st
import zipfile
import io
import json
import datetime
import re
import requests

# --- 0. STATE MANAGEMENT & EMBEDDED THEME REGISTRY ---
def init_state(key, default_val):
    if key not in st.session_state:
        st.session_state[key] = default_val

init_state('hero_h', "Stop Paying Rent for Your Website.")
init_state('hero_sub', "The Titan Engine is the world’s first 0.1s website architecture that runs on $0 monthly fees. Pay once. Own it forever.")
init_state('about_h', "Control Your Empire")
init_state('about_short', "No WordPress dashboard. No plugins to update. Just open your private Google Sheet, change a text, and watch your site update globally in seconds.")
init_state('feat_data', "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. Titan loads instantly.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions.\ntable | The Functional Pillar | **Google Sheets CMS**. Update prices/photos from a spreadsheet.\nshield | The Authority Pillar | **Unhackable Security**. Zero-DB Architecture.\nlayers | The Reliability Pillar | **Global Edge Deployment**. Distributed across 100+ servers.\nstar | The Conversion Pillar | **One-Tap WhatsApp**. Direct-to-Chat technology.")

# HARDCODED 2050 TITAN THEME REGISTRY (Replaces titan_themes.py completely)
THEME_REGISTRY = {
    "1. Stripe Cloud (Modern SaaS)": {"bg": "#f8fafc", "txt": "#0f172a", "card": "#ffffff", "p": "#6366f1", "s": "#10b981", "nav": "rgba(255,255,255,0.8)", "shadow": "0 10px 40px -10px rgba(99,102,241,0.15)", "radius": "16px", "border": "1px solid #e2e8f0"},
    "2. Vercel Dark (Developer Core)": {"bg": "#000000", "txt": "#ededed", "card": "#111111", "p": "#ffffff", "s": "#0070f3", "nav": "rgba(0,0,0,0.8)", "shadow": "0 0 0 1px #333", "radius": "8px", "border": "1px solid #333"},
    "3. Apple Minimalist (Pure Clean)": {"bg": "#fbfbfd", "txt": "#1d1d1f", "card": "#ffffff", "p": "#000000", "s": "#0066cc", "nav": "rgba(251,251,253,0.8)", "shadow": "0 4px 24px rgba(0,0,0,0.04)", "radius": "24px", "border": "none"},
    "4. Neo-Brutalist (Gumroad Style)": {"bg": "#f4f4f0", "txt": "#000000", "card": "#ffffff", "p": "#000000", "s": "#ff90e8", "nav": "#f4f4f0", "shadow": "6px 6px 0px #000000", "radius": "0px", "border": "3px solid #000000"},
    "5. Glassmorphism (Translucent)": {"bg": "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)", "txt": "#1e1e24", "card": "rgba(255, 255, 255, 0.25)", "p": "#3a0ca3", "s": "#ff006e", "nav": "rgba(255,255,255,0.1)", "shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.37)", "radius": "20px", "border": "1px solid rgba(255, 255, 255, 0.4)"},
    "6. Luxury Boutique (High-End)": {"bg": "#faf9f6", "txt": "#2c2a29", "card": "#ffffff", "p": "#d4af37", "s": "#1a1a1a", "nav": "rgba(250,249,246,0.9)", "shadow": "0 15px 35px rgba(0,0,0,0.05)", "radius": "0px", "border": "1px solid #eaeaea"},
    "7. Streetwear Edge (Hypebeast)": {"bg": "#121212", "txt": "#f4f4f4", "card": "#1e1e1e", "p": "#ff4500", "s": "#ffffff", "nav": "rgba(18,18,18,0.9)", "shadow": "0 20px 40px rgba(255,69,0,0.15)", "radius": "4px", "border": "1px solid #333"},
    "8. Organic Eco (Sustainable)": {"bg": "#f0f4f0", "txt": "#2c3e2e", "card": "#ffffff", "p": "#4a7c59", "s": "#f39c12", "nav": "rgba(240,244,240,0.9)", "shadow": "0 10px 30px rgba(74,124,89,0.08)", "radius": "30px", "border": "none"},
    "9. Cosmetic Pastel (Beauty)": {"bg": "#fff5f5", "txt": "#5c4a4a", "card": "#ffffff", "p": "#e8b4b8", "s": "#a36b7e", "nav": "rgba(255,245,245,0.9)", "shadow": "0 12px 24px rgba(232,180,184,0.15)", "radius": "20px", "border": "1px solid #ffe3e3"},
    "10. Tech Hardware (Neon Dark)": {"bg": "#0d1117", "txt": "#c9d1d9", "card": "#161b22", "p": "#58a6ff", "s": "#238636", "nav": "rgba(13,17,23,0.9)", "shadow": "0 0 20px rgba(88,166,255,0.1)", "radius": "12px", "border": "1px solid #30363d"},
    "11. Medical Platinum (Trust)": {"bg": "#ffffff", "txt": "#1e293b", "card": "#f8fafc", "p": "#0284c7", "s": "#059669", "nav": "rgba(255,255,255,0.95)", "shadow": "0 4px 6px -1px rgba(0,0,0,0.05)", "radius": "12px", "border": "1px solid #e2e8f0"},
    "12. Dental Aqua (Clean)": {"bg": "#f0fdfa", "txt": "#0f172a", "card": "#ffffff", "p": "#0d9488", "s": "#0284c7", "nav": "rgba(240,253,250,0.9)", "shadow": "0 10px 25px rgba(13,148,136,0.1)", "radius": "16px", "border": "1px solid #ccfbf1"},
    "13. Fitness Aggressive (Gym)": {"bg": "#0a0a0a", "txt": "#ffffff", "card": "#171717", "p": "#e11d48", "s": "#facc15", "nav": "rgba(10,10,10,0.9)", "shadow": "0 10px 30px rgba(225,29,72,0.2)", "radius": "8px", "border": "1px solid #262626"},
    "14. Spa Therapy (Calm)": {"bg": "#faf5f0", "txt": "#4a443c", "card": "#ffffff", "p": "#bfa58a", "s": "#8c735a", "nav": "rgba(250,245,240,0.9)", "shadow": "0 8px 20px rgba(191,165,138,0.1)", "radius": "24px", "border": "1px solid #f0e6da"},
    "15. Yoga Mindfulness": {"bg": "#fdf8f5", "txt": "#333333", "card": "#ffffff", "p": "#d4a373", "s": "#a1c181", "nav": "rgba(253,248,245,0.9)", "shadow": "0 5px 15px rgba(0,0,0,0.03)", "radius": "50px", "border": "none"},
    "16. Law Firm Heritage": {"bg": "#ffffff", "txt": "#1f2937", "card": "#f9fafb", "p": "#1e3a8a", "s": "#b45309", "nav": "rgba(255,255,255,0.95)", "shadow": "0 4px 6px rgba(0,0,0,0.05)", "radius": "4px", "border": "1px solid #e5e7eb"},
    "17. Real Estate Prime": {"bg": "#111827", "txt": "#f3f4f6", "card": "#1f2937", "p": "#fbbf24", "s": "#f9fafb", "nav": "rgba(17,24,39,0.9)", "shadow": "0 10px 30px rgba(251,191,36,0.1)", "radius": "8px", "border": "1px solid #374151"},
    "18. Construction Industrial": {"bg": "#f5f5f5", "txt": "#1a1a1a", "card": "#ffffff", "p": "#f59e0b", "s": "#000000", "nav": "rgba(245,245,245,0.95)", "shadow": "0 8px 0px #e5e5e5", "radius": "0px", "border": "2px solid #000000"},
    "19. Architecture Grid": {"bg": "#ffffff", "txt": "#000000", "card": "#f4f4f5", "p": "#000000", "s": "#3b82f6", "nav": "#ffffff", "shadow": "none", "radius": "0px", "border": "1px solid #000000"},
    "20. Agency Bold (Creative)": {"bg": "#4f46e5", "txt": "#ffffff", "card": "#4338ca", "p": "#f9a8d4", "s": "#fde047", "nav": "rgba(79,70,229,0.9)", "shadow": "0 20px 40px rgba(0,0,0,0.2)", "radius": "20px", "border": "none"},
    "21. Cyberpunk 2077": {"bg": "#fcee0a", "txt": "#000000", "card": "#000000", "p": "#00ffff", "s": "#ff003c", "nav": "#fcee0a", "shadow": "8px 8px 0px #00ffff", "radius": "0px", "border": "2px solid #000000"},
    "22. Monochromatic Black/White": {"bg": "#ffffff", "txt": "#000000", "card": "#ffffff", "p": "#000000", "s": "#000000", "nav": "#ffffff", "shadow": "4px 4px 0px #000000", "radius": "0px", "border": "2px solid #000000"},
    "23. Retro Synthwave": {"bg": "#2b213a", "txt": "#e0d6eb", "card": "#181425", "p": "#ff007f", "s": "#00f0ff", "nav": "rgba(43,33,58,0.9)", "shadow": "0 0 15px rgba(255,0,127,0.5)", "radius": "10px", "border": "1px solid #ff007f"},
    "24. Gradient Mesh": {"bg": "linear-gradient(45deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)", "txt": "#333333", "card": "rgba(255,255,255,0.6)", "p": "#f77062", "s": "#3f51b5", "nav": "rgba(255,255,255,0.4)", "shadow": "0 8px 32px rgba(0,0,0,0.1)", "radius": "30px", "border": "1px solid rgba(255,255,255,0.5)"},
    "25. Midnight Ocean": {"bg": "#0f2027", "txt": "#d1d5db", "card": "#203a43", "p": "#2c5364", "s": "#38ef7d", "nav": "rgba(15,32,39,0.9)", "shadow": "0 15px 25px rgba(0,0,0,0.3)", "radius": "16px", "border": "1px solid #2c5364"}
}

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan Architect | Apex Emulator", 
    layout="wide", 
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED UI SYSTEM ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { 
        background: linear-gradient(90deg, #0f172a, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important; font-size: 1.8rem !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; color: #0f172a !important;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        color: white; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); text-transform: uppercase; letter-spacing: 1px; transition: transform 0.2s;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v100.5 | Standalone Engine")
    st.divider()
    
    # AI GENERATOR
    with st.expander("🤖 Titan AI Generator", expanded=False):
        raw_key = st.text_input("Groq API Key", type="password")
        groq_key = raw_key.strip() if raw_key else ""
        biz_desc = st.text_input("Business Description")
        
        if st.button("✨ Generate Copy"):
            if not groq_key or not biz_desc:
                st.error("Key & Description required.")
            else:
                try:
                    with st.spinner("Writing Context..."):
                        url = "https://api.groq.com/openai/v1/chat/completions"
                        headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                        prompt = f"Act as a copywriter. Return JSON for '{biz_desc}': hero_h, hero_sub, about_h, about_short, feat_data (icon|Title|Desc format)."
                        data = {"messages": [{"role": "user", "content": prompt}], "model": "llama-3.1-8b-instant", "response_format": {"type": "json_object"}}
                        resp = requests.post(url, headers=headers, json=data)
                        if resp.status_code == 200:
                            res = resp.json()['choices'][0]['message']['content']
                            parsed = json.loads(res)
                            for k, v in parsed.items():
                                if k == 'feat_data' and isinstance(v, list): v = "\n".join(map(str, v))
                                st.session_state[k] = str(v)
                            st.success("Generated Successfully!")
                            st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # VISUAL DNA & THEMES
    with st.expander("🎨 Design Studio", expanded=True):
        st.markdown("**1-Click Global Themes**")
        theme_names = list(THEME_REGISTRY.keys())
        theme_mode = st.selectbox("Select Architecture Theme", theme_names)
        st.divider()
        
        st.markdown("**Layout & Typography**")
        c1, c2 = st.columns(2)
        with c1: hero_layout = st.selectbox("Hero Alignment", ["Center", "Left"])
        with c2: anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])
            
        c3, c4 = st.columns(2)
        with c3: h_font = st.selectbox("Headings Font", ["Space Grotesk", "Montserrat", "Playfair Display", "Outfit", "Clash Display"])
        with c4: b_font = st.selectbox("Body Font", ["Inter", "Plus Jakarta Sans", "Satoshi", "Roboto"])

    # TYPOGRAPHY & COLOR MASTERY
    with st.expander("👁️ Typography & Color Mastery", expanded=False):
        col_h = st.color_picker("Headings Color", "#0f172a")
        col_b = st.color_picker("Body Text Color", "#475569")
        size_h1 = st.slider("H1 Main Heading Size", 1.0, 8.0, 4.5)
        size_p = st.slider("Body Text Size", 0.8, 2.0, 1.1)
        cta_bg_color = st.color_picker("Final CTA Background", "#10b981")
        cta_txt_color = st.color_picker("Final CTA Text Color", "#ffffff")

    # FEATURE FLAGS (2050 TECH)
    with st.expander("🚀 2050 Feature Flags", expanded=True):
        enable_ar = st.checkbox("Spatial Web (AR 3D Models)", value=True)
        enable_voice = st.checkbox("Voice Command Search", value=True)
        enable_context = st.checkbox("Context-Aware UI (Time Based)", value=True)
        enable_ab = st.checkbox("Edge A/B Testing", value=True)

    # MODULE MANAGER
    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Section", value=True)
        show_stats = st.checkbox("Trust Stats", value=True)
        show_features = st.checkbox("Feature Grid", value=True)
        show_pricing = st.checkbox("Pricing Table", value=True)
        show_inventory = st.checkbox("Tour Packages", value=True) # Renamed!
        show_blog = st.checkbox("Blog Engine", value=True)
        show_gallery = st.checkbox("About Section", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)
        show_cta = st.checkbox("Final CTA", value=True)
        show_booking = st.checkbox("Booking Engine", value=True)

    # TECHNICAL
    with st.expander("⚙️ SEO & Analytics", expanded=False):
        seo_area = st.text_input("Service Area", "Global / Online")
        seo_kw = st.text_area("SEO Keywords", "web design, no monthly fees")
        gsc_tag = st.text_input("Google Verification ID")
        ga_tag = st.text_input("Google Analytics ID")
        og_image = st.text_input("Social Share Image URL")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent Builder")

tabs = st.tabs(["1. Identity & PWA", "2. Content Blocks", "3. Marketing Tools", "4. Pricing", "5. Tour Packages", "6. Booking", "7. Blog", "8. Legal", "9. Web3 / IPFS"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "Dexigi Vibez Tours")
        hero_badge_txt = st.text_input("Hero Mini-Badge", "✈️ Premium Tours & Events in Nakuru")
        biz_tagline = st.text_input("Tagline", "Explore. Vibe. Repeat.")
        biz_phone = st.text_input("Phone", "254712799837")
        biz_email = st.text_input("Email", "dexigivibeztoursandevents@gmail.com")
    with c2:
        prod_url = st.text_input("Website URL", "https://www.dexigiexcursions.co.ke")
        biz_addr = st.text_area("Address", "Sansora Building, Nakuru, Kenya", height=100)
        map_iframe = st.text_area("Google Map Embed", placeholder='<iframe src="..."></iframe>', height=100)
        seo_d = st.text_area("Meta Description", "Premium tours, safaris, and coastal getaways in Kenya & beyond.", height=100)
        logo_url = st.text_input("Logo URL (PNG/SVG)")

    st.subheader("📱 Progressive Web App (PWA)")
    pwa_short = st.text_input("App Short Name", biz_name[:12])
    pwa_desc = st.text_input("App Description", "Official App")
    pwa_icon = st.text_input("App Icon (512x512 PNG)", logo_url)
    
    st.subheader("🌍 Multi-Language")
    lang_sheet = st.text_input("Translation Sheet CSV URL")
        
    st.subheader("Social Links")
    sc1, sc2, sc3 = st.columns(3)
    fb_link = sc1.text_input("Facebook URL", "https://facebook.com/dexigivibeztours")
    ig_link = sc2.text_input("Instagram URL", "https://instagram.com/dexigivibeztours")
    x_link = sc3.text_input("X (Twitter) URL")
    sc4, sc5, sc6 = st.columns(3)
    li_link = sc4.text_input("LinkedIn URL")
    yt_link = sc5.text_input("YouTube URL")
    wa_num = sc6.text_input("WhatsApp Number (No +)", "254712799837")

with tabs[1]:
    st.subheader("Hero Carousel")
    hero_h = st.text_input("Hero Headline", st.session_state.hero_h)
    hero_sub = st.text_input("Hero Subtext", st.session_state.hero_sub)
    hero_video_id = st.text_input("YouTube Video ID (Background Override)", placeholder="e.g. dQw4w9WgXcQ")
    
    hc1, hc2, hc3 = st.columns(3)
    hero_img_1 = hc1.text_input("Slide 1", "https://images.unsplash.com/photo-1516426122078-c23e76319801?q=80&w=1600")
    hero_img_2 = hc2.text_input("Slide 2", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600")
    hero_img_3 = hc3.text_input("Slide 3", "https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?q=80&w=1600")
    
    st.divider()
    st.subheader("Stats & Features")
    col_s1, col_s2, col_s3 = st.columns(3)
    stat_1 = col_s1.text_input("Stat 1", "500+")
    label_1 = col_s1.text_input("Label 1", "Happy Travelers")
    stat_2 = col_s2.text_input("Stat 2", "50+")
    label_2 = col_s2.text_input("Label 2", "Destinations")
    stat_3 = col_s3.text_input("Stat 3", "100%")
    label_3 = col_s3.text_input("Label 3", "Good Vibez")

    f_title = st.text_input("Features Title", "Our Experiences")
    feat_data_input = st.text_area("Features List", st.session_state.feat_data, height=150)
    
    st.subheader("About")
    about_h_in = st.text_input("About Title", st.session_state.about_h)
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1489392191049-fc10c97e64b6?q=80&w=800")
    about_short_in = st.text_area("Short Summary", st.session_state.about_short, height=100)
    about_long = st.text_area("Full Content", "**The Trap**\nMost business owners...", height=200)

with tabs[2]:
    st.subheader("📣 Marketing Suite")
    top_bar_enabled = st.checkbox("Enable Top Bar", True)
    top_bar_text = st.text_input("Promo Text", "🔥 Booking Now Open for WRC Safari Rally! Secure your spot.")
    top_bar_link = st.text_input("Promo Link", "#store")
    
    st.divider()
    popup_enabled = st.checkbox("Enable Popup", True)
    popup_delay = st.slider("Delay (seconds)", 1, 30, 5)
    popup_title = st.text_input("Popup Headline", "Need a Weekend Plan?")
    popup_text = st.text_input("Popup Body", "Message us on WhatsApp to get our latest group rates.")
    popup_cta = st.text_input("Popup Button", "Chat with Us")

with tabs[3]:
    st.subheader("💰 Pricing")
    col_p1, col_p2, col_p3 = st.columns(3)
    titan_price = col_p1.text_input("Setup Price", "KES 3,500")
    titan_mo = col_p1.text_input("Monthly Fee", "KES 15,000")
    wix_name = col_p2.text_input("Competitor", "Standard Agencies")
    wix_mo = col_p2.text_input("Comp. Monthly", "Boring Itineraries")
    save_val = col_p3.text_input("Savings", "Unmatched Vibez")

with tabs[4]:
    st.subheader("🛒 Tour Packages")
    st.info("💡 **Pro Tip:** In your CSV, separate multiple images with a `|` symbol for automatic galleries.")
    sheet_url = st.text_input("Store CSV", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Default Product Img", "https://images.unsplash.com/photo-1436450412740-6b988f486c6b?q=80&w=800")
    col_pay1, col_pay2 = st.columns(2)
    paypal_link = col_pay1.text_input("PayPal Link")
    upi_id = col_pay2.text_input("UPI ID")

with tabs[5]:
    st.subheader("📅 Booking Engine")
    booking_embed = st.text_area("Embed Code", height=150)
    booking_title = st.text_input("Booking Title", "Plan Your Next Adventure")
    booking_desc = st.text_input("Booking Subtext", "Choose a time to consult with our travel planners.")

with tabs[6]:
    st.subheader("📰 Blog")
    blog_sheet_url = st.text_input("Blog CSV")
    blog_hero_title = st.text_input("Blog Title", "The Travel Diary")
    blog_hero_sub = st.text_input("Blog Subtext", "Tips and destination guides.")

with tabs[7]:
    st.subheader("Legal")
    testi_data = st.text_area("Testimonials", "Sarah K.|Ultimate vibez!")
    faq_data = st.text_area("FAQ", "Do you offer customized packages? ? Yes we do.")
    priv_txt = st.text_area("Privacy", "We collect minimum data.")
    term_txt = st.text_area("Terms", "You own the code.")

with tabs[8]:
    st.subheader("🪐 Web3 Deployment")
    pinata_jwt = st.text_input("Pinata API JWT", type="password")


# --- 5. COMPILER ENGINE HELPER FUNCTIONS ---

def format_text(text):
    if not text: return ""
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    lines = processed_text.split('\n')
    html_out = ""
    in_list = False
    for line in lines:
        clean_line = line.strip()
        if not clean_line: continue
        if clean_line.startswith("* "):
            if not in_list: 
                html_out += '<ul style="margin-bottom:1rem; padding-left:1.5rem;">'
                in_list = True
            html_out += f'<li style="margin-bottom:0.5rem; opacity:0.9; color:inherit;">{clean_line[2:]}</li>'
        else:
            if in_list: 
                html_out += "</ul>"
                in_list = False
            html_out += f"<p style='margin-bottom:1rem; opacity:0.9; color:inherit;'>{clean_line}</p>"
    if in_list: html_out += "</ul>"
    return html_out

def get_simple_icon(name):
    icon_map = {
        "bolt": "M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66.19-.34.05-.08.07-.12C8.48 10.94 10.42 7.54 13 3h1l-1 7h3.5c.49 0 .56.33.47.51l-.07.15C12.96 17.55 11 21 11 21z", 
        "wallet": "M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z", 
        "table": "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM5 19V5h14v14H5zm2-2h10v-2H7v2zm0-4h10v-2H7v2zm0-4h10V7H7v2z", 
        "shield": "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"
    }
    path = icon_map.get(name.lower().strip(), "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z")
    return f'<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="{path}"/></svg>'

# --- 6. CORE GENERATORS ---

def generate_modern_css():
    t = THEME_REGISTRY.get(theme_mode, THEME_REGISTRY["1. Stripe Cloud (Modern SaaS)"])
    align = "center" if hero_layout == "Center" else "left"
    justify = "center" if hero_layout == "Center" else "flex-start"
    h_f = h_font.replace(' ', '+')
    b_f = b_font.replace(' ', '+')

    return f"""
    :root {{
        --p: {t['p']}; --s: {cta_bg_color}; --bg: {t['bg']}; --txt: {col_b}; --txt-h: {col_h}; --card: {t['card']};
        --glass: {t['glass']}; --border: {t['border']}; --radius: {border_rad}px;
        --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif;
        --btn-txt: {cta_txt_color}; --shadow: {t['shadow']};
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-size: 16px; }}
    body {{ background: var(--bg); color: var(--txt); font-family: var(--b-font); line-height: 1.8; overflow-x: hidden; transition: 0.3s; font-size: {size_p}rem; }}
    body.dark-mode {{ --bg: #0f172a; --txt: #f8fafc; --txt-h: #ffffff; --card: #1e293b; --glass: rgba(30, 41, 59, 0.9); --border: rgba(255, 255, 255, 0.1); }}
    
    h1, h2, h3, h4 {{ font-family: var(--h-font); color: var(--txt-h); line-height: 1.2; font-weight: 800; margin-bottom: 1.5rem; }}
    h1 {{ font-size: {size_h1}rem; }}
    p {{ margin-bottom: 2rem; opacity: 0.9; text-align: justify; hyphens: auto; -webkit-hyphens: auto; }}
    a {{ text-decoration: none; color: inherit; transition: 0.3s; }}
    
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 2rem; box-sizing: border-box; }}
    section {{ padding: clamp(4rem, 8vw, 8rem) 0; position: relative; }}
    .section-head {{ text-align: center; margin-bottom: clamp(3rem, 5vw, 5rem); display:flex; flex-direction:column; align-items:center; }}
    
    /* UI COMPONENTS */
    .glass {{ background: var(--glass); backdrop-filter: blur(16px); border: 1px solid var(--border); box-shadow: var(--shadow); }}
    .card {{ background: var(--card); border-radius: var(--radius); border: var(--border); box-shadow: var(--shadow); transition: 0.4s; display: flex; flex-direction: column; overflow: hidden; }}
    .card:hover {{ transform: translateY(-10px); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.2); }}
    .card-body {{ padding: 2rem; display: flex; flex-direction: column; flex-grow: 1; text-align:left; }}
    .card-desc {{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
    
    .btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 1.2rem 2.5rem; border-radius: var(--radius); font-weight: 800; transition: 0.3s; text-transform: uppercase; letter-spacing: 1.5px; cursor:pointer; text-decoration:none; border:none; }}
    .btn-primary {{ background: var(--p); color: #fff !important; }}
    .btn-accent {{ background: var(--s); color: var(--btn-txt) !important; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn-outline-light {{ background: transparent; border: 2px solid #fff; color: #fff !important; }}
    .btn:hover {{ transform: translateY(-3px) scale(1.02); filter: brightness(1.15); }}
    
    /* NAVIGATION */
    #top-bar {{ position: fixed; top: 0; left: 0; width: 100%; background: var(--s); color: var(--btn-txt); text-align: center; padding: 8px; z-index: 2005; font-weight: 800; font-size: 0.85rem; height: 40px; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(0,0,0,0.1); }}
    #top-bar a {{ color: var(--btn-txt) !important; text-decoration: underline; margin-left:10px; }}
    
    nav#main-navbar {{ position: fixed; top: 0; width: 100%; z-index: 2000; background: var(--nav); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(128,128,128,0.1); padding: 1.2rem 0; transition: top 0.3s; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; align-items: center; gap: 2rem; }}
    .nav-links a {{ text-decoration: none; font-weight: 600; color: var(--txt-h); font-size: 0.95rem; position: relative; }}
    .nav-links a::after {{ content: ''; position: absolute; width: 0; height: 2px; bottom: -4px; left: 0; background-color: var(--p); transition: 0.3s; }}
    .nav-links a:hover::after {{ width: 100%; }}
    .nav-links a:hover {{ color: var(--p); }}
    .mobile-menu {{ display: none; font-size: 1.8rem; cursor: pointer; color:var(--txt-h); }}
    
    /* HERO */
    .modern-hero {{ position: relative; min-height: 100vh; display: flex; align-items: center; text-align: {align}; padding-top: 140px; overflow: hidden; background: var(--p); }}
    .modern-hero-bg {{ position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle at 50% 50%, rgba(128,128,128,0.05) 0%, transparent 50%); z-index: -1; animation: rotate 60s linear infinite; }}
    .modern-hero-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; width: 100%; z-index: 2; position: relative; }}
    .modern-hero-text {{ display: flex; flex-direction: column; align-items: {align}; justify-content: {justify}; width: 100%; }}
    .hero-btn-group {{ display: flex; gap: 1rem; flex-wrap: wrap; justify-content: {justify}; margin-top: 1rem; width:100%; }}
    .hero-badge {{ display: inline-block; padding: 0.5rem 1rem; margin-bottom: 1.5rem; background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.3); border-radius: 50px; font-size: 0.85rem; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 1px; }}
    .modern-hero h1 {{ color: #ffffff !important; margin-bottom: 1.5rem; text-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
    .modern-hero p {{ color: rgba(255,255,255,0.9) !important; font-size: clamp(1.2rem, 2vw, 1.4rem); margin-bottom: 2.5rem; max-width: 800px; }}
    .modern-hero-visual {{ position: relative; width: 100%; height: 500px; display: flex; align-items: center; justify-content: center; }}
    .visual-frame {{ width: 100%; height: 100%; border-radius: 32px; overflow: hidden; position: relative; z-index: 2; box-shadow: 0 30px 60px rgba(0,0,0,0.15); border: 8px solid var(--card); }}
    
    /* GRIDS & LAYOUTS */
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem; }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items: center; }}
    .contact-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: stretch; }}
    
    .detail-view {{ display: grid; grid-template-columns: 0.8fr 1.2fr; gap: 6rem; align-items: start; background: var(--card); padding: 5rem; border-radius: 32px; box-shadow: var(--shadow); border: var(--border); }}
    .gallery-main {{ width: 100%; height: 500px; object-fit: cover; border-radius: var(--radius); margin-bottom: 1rem; box-shadow: var(--shadow); }}
    
    /* WIDGETS */
    .reveal {{ opacity: 0; transform: translateY(40px); transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94); z-index: 10; position:relative; }}
    .reveal.active {{ opacity: 1; transform: translateY(0); }}
    
    #toast-box {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 9999; display: flex; flex-direction: column; gap: 10px; }}
    .toast {{ background: var(--txt); color: var(--bg); padding: 12px 24px; border-radius: 50px; font-weight: 600; box-shadow: 0 10px 30px rgba(0,0,0,0.2); opacity: 0; transform: translateY(20px); transition: 0.4s; }}
    .toast.show {{ opacity: 1; transform: translateY(0); }}
    
    .float-btn {{ position: fixed; width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2); z-index: 990; cursor: pointer; transition: 0.3s; }}
    .float-btn:hover {{ transform: scale(1.1); }}
    #wa-float {{ bottom: 100px; right: 30px; background: #25D366; color: white; border: none; }}
    #cart-float {{ bottom: 30px; right: 30px; background: var(--p); color: white; border: none; }}
    #mode-toggle {{ bottom: 30px; left: 30px; background: var(--card); color: var(--txt); border: 1px solid var(--border); }}
    
    @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    
    /* MOBILE OPTIMIZATION */
    @media (max-width: 992px) {{
        nav#main-navbar .nav-links {{ position: absolute; top: 100%; left: -100%; width: 100vw; height: 100dvh; background: var(--bg); flex-direction: column; padding: 3rem; transition: left 0.4s ease; align-items: center; justify-content: flex-start; gap: 2.5rem; z-index: 1999; overflow-y: auto; }}
        nav#main-navbar .nav-links.active {{ left: 0; }}
        .nav-links a {{ font-size: 1.5rem; }}
        .mobile-menu {{ display: block; }}
        .about-grid, .detail-view, .grid-3, .contact-grid {{ grid-template-columns: 1fr !important; gap: 3rem; }}
        .modern-hero-grid {{ grid-template-columns: 1fr; text-align: center; }}
        .modern-hero-text {{ text-align: center; align-items: center; justify-content: center; }}
        .hero-btn-group {{ justify-content: center; }}
        .modern-hero-visual {{ height: 400px; }}
        .detail-view {{ padding: 2rem; gap: 2rem; }}
    }}
    
    @media (max-width: 480px) {{
        p {{ text-align: left; hyphens: auto; }}
        html, body, .container {{ width: 100% !important; overflow-x: hidden !important; }}
        .container {{ padding: 0 24px !important; box-sizing: border-box !important; }}
        h1, #hero-title, .modern-hero-text h1 {{ font-size: 2.4rem !important; line-height: 1.1 !important; margin-bottom: 1.5rem !important; }}
        .hero-btn-group {{ flex-direction: column !important; width: 100%; }}
        .hero-btn-group .btn {{ width: 100% !important; }}
        #wa-float {{ bottom: 15px !important; right: 10px !important; scale: 0.8; }}
        #theme-toggle {{ bottom: 15px !important; left: 10px !important; scale: 0.8; }}
        #cart-float {{ bottom: 80px !important; right: 10px !important; scale: 0.8; }}
        .modern-hero-visual {{ height: 300px !important; margin-top: 2rem !important; }}
    }}
    """

def gen_html_components():
    logo_display = f'<img src="{logo_url}" style="height:40px; margin-right:10px; object-fit:contain;" alt="{biz_name} Logo">' if logo_url else ''
    nav_links = f'<a href="index.html">Home</a>'
    if show_features: nav_links += '<a href="index.html#features">Features</a>'
    if show_pricing: nav_links += '<a href="index.html#pricing">Pricing</a>'
    if show_inventory: nav_links += '<a href="index.html#store">Tour Packages</a>'
    if show_blog: nav_links += '<a href="blog.html">Blog</a>'
    if show_booking: nav_links += '<a href="booking.html">Book</a>'
    nav_links += '<a href="contact.html">Contact</a>'
    
    top_bar = f'<div id="top-bar"><a href="{top_bar_link}">{top_bar_text}</a></div>' if top_bar_enabled else ''
    nav_top_offset = "40px" if top_bar_enabled else "0px"
    
    nav_html = f"""
        {top_bar}
        <nav id="main-navbar" class="glass" style="top:{nav_top_offset}">
            <div class="container nav-flex">
                <a href="index.html" style="font-weight:800; font-size:1.3rem; display:flex; align-items:center; text-decoration:none; color:var(--txt-h);">
                    {logo_display}{biz_name}
                </a>
                <div class="nav-links">
                    {nav_links}
                    {'<a href="#" onclick="openLangModal()">🌐</a>' if lang_sheet else ''}
                </div>
                <div class="mobile-menu" onclick="toggleMenu()">☰</div>
            </div>
        </nav>
    """
    return nav_html

def gen_footer():
    icons = ""
    if fb_link: icons += f'<a href="{fb_link}" target="_blank" style="margin-right:15px; color:#94a3b8;"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>'
    if ig_link: icons += f'<a href="{ig_link}" target="_blank" style="margin-right:15px; color:#94a3b8;"><svg class="social-icon" viewBox="0 0 24 24"><path d="M16.98 0a6.9 6.9 0 0 1 5.08 1.98A6.94 6.94 0 0 1 24 7.02v9.96c0 2.08-.68 3.87-1.98 5.13A7.14 7.14 0 0 1 16.94 24H7.06a7.06 7.06 0 0 1-5.03-1.89A6.96 6.96 0 0 1 0 16.94V7.02C0 2.8 2.8 0 7.02 0h9.96zM7.17 2.1c-1.4 0-2.6.48-3.46 1.33c-.85.85-1.33 2.06-1.33 3.46v10.3c0 1.3.47 2.5 1.33 3.36c.86.85 2.06 1.33 3.46 1.33h9.66c1.4 0 2.6-.48 3.46-1.33c.85-.85 1.33-2.06 1.33-3.46V6.89c0-1.4-.47-2.6-1.33-3.46c-.86-.85-2.06-1.33-3.46-1.33H7.17zm11.97 3.33c.77 0 1.4.63 1.4 1.4c0 .77-.63 1.4-1.4 1.4c-.77 0-1.4-.63-1.4-1.4c0-.77.63-1.4 1.4-1.4zM12 5.76c3.39 0 6.14 2.75 6.14 6.14c0 3.39-2.75 6.14-6.14 6.14c-3.39 0-6.14-2.75-6.14-6.14c0-3.39 2.75-6.14 6.14-6.14zm0 2.1c-2.2 0-3.99 1.79-3.99 4.04c0 2.25 1.79 4.04 3.99 4.04c2.2 0 3.99-1.79 3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04z"/></svg></a>'
    if x_link: icons += f'<a href="{x_link}" target="_blank" style="margin-right:15px; color:#94a3b8;"><svg class="social-icon" viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>'

    return f"""
    <footer><div class="container">
        <div class="footer-grid">
            <div>
                <h3 style="color:#fff; margin-bottom:1rem;">{biz_name}</h3>
                <p style="opacity:0.8; margin-bottom:1rem;">{biz_addr}</p>
                <p style="font-weight:bold; color:var(--s);">{biz_phone}</p>
                <div style="margin-top:1.5rem; display:flex;">{icons}</div>
            </div>
            <div>
                <h4 style="color:#fff;">Quick Links</h4>
                <a href="index.html">Home</a>
                <a href="about.html">About Us</a>
                {'<a href="blog.html">Blog</a>' if show_blog else ''}
                {'<a href="booking.html">Book Appointment</a>' if show_booking else ''}
            </div>
            <div>
                <h4 style="color:#fff;">Legal</h4>
                <a href="privacy.html">Privacy Policy</a>
                <a href="terms.html">Terms of Service</a>
            </div>
        </div>
        <div style="border-top:1px solid rgba(255,255,255,0.1); margin-top:3rem; padding-top:2rem; text-align:center; opacity:0.6;">
            &copy; {datetime.datetime.now().year} {biz_name}. Powered by Titan Architecture.
        </div>
    </div></footer>
    """

def build_page(title, content):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {biz_name}</title>
    <meta name="description" content="{seo_d}">
    <link rel="manifest" href="manifest.json">
    <style>{generate_modern_css()}</style>
    {gen_2050_scripts()}
</head>
<body>
    <main>
        {gen_html_components()}
        {content}
        {gen_footer()}
        
        <div id="cart-overlay" onclick="toggleCart()" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1999;"></div>
        <div id="cart-modal" class="glass" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); padding:2rem; z-index:2000; width:90%; max-width:400px; border-radius:24px;">
            <h3 style="color:var(--p); margin-bottom:1rem;">Your Cart</h3><hr style="margin:10px 0; opacity:0.2;">
            <div id="cart-items" style="max-height:200px; overflow-y:auto; margin:1rem 0;"></div>
            <div style="font-weight:bold; font-size:1.2rem; margin-bottom:1rem; text-align:right;">Total: <span id="cart-total">0.00</span></div>
            <button onclick="checkoutWhatsApp()" class="btn btn-accent" style="width:100%;">Checkout via WhatsApp</button>
        </div>

        {gen_wa_widget()}
        <div class="float-btn" id="cart-float" onclick="toggleCart()" style="display:none;">🛒 <span id="cart-count" style="position:absolute; top:-5px; right:-5px; background:var(--s); color:white; border-radius:50%; width:20px; height:20px; font-size:12px; display:flex; align-items:center; justify-content:center;">0</span></div>
        {f'<div class="float-btn" id="mode-toggle" onclick="toggleTheme()">🌓</div>' if show_dark_toggle else ''}
        
        {f'<div id="cookie-banner" class="glass" style="position:fixed; bottom:0; left:0; width:100%; padding:1.5rem; transform:translateY(100%); transition:0.5s; z-index:9000; display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border);"><div>{cookie_txt}</div><button class="btn btn-primary" onclick="acceptCookies()">Accept</button></div>' if show_cookie else ''}
        {f'<div id="lead-popup" class="glass" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); padding:3rem; text-align:center; border-radius:24px; z-index:3000; box-shadow:0 30px 60px rgba(0,0,0,0.5); width:90%; max-width:450px;"><div style="position:absolute; top:15px; right:20px; cursor:pointer; font-size:1.5rem; opacity:0.5;" onclick="document.getElementById(\\'lead-popup\\').style.display=\\'none\\'">✕</div><h3 style="margin-bottom:1rem;">{popup_title}</h3><p style="margin-bottom:2rem;">{popup_text}</p><a href="https://wa.me/{wa_num}?text=I want the offer" class="btn btn-accent" target="_blank" style="width:100%;">{popup_cta}</a></div>' if popup_enabled else ''}
    </main>
    {gen_csv_parser()}
    {gen_js_engine()}
    <script>window.addEventListener('scroll', () => {{ document.querySelectorAll('.reveal').forEach(r => {{ if(r.getBoundingClientRect().top < window.innerHeight - 80) r.classList.add('active'); }}); }});</script>
</body>
</html>"""
    return html

# --- 7. CONTENT GENERATORS ---

def gen_inner_header(title):
    return f"""<section class="modern-hero" style="min-height: 40vh; display:flex; align-items:center; justify-content:center; text-align:center; padding-top:140px;"><div class="container modern-hero-text"><h1>{title}</h1></div></section>"""

def gen_booking_content():
    return f"""
    <section class="modern-hero" style="min-height:40vh; display:flex; align-items:center; justify-content:center; text-align:center; padding-top:140px;">
        <div class="container modern-hero-text reveal"><h1>{booking_title}</h1><p>{booking_desc}</p></div>
    </section>
    <section style="background:var(--bg);">
        <div class="container" style="text-align:center;">
            <div style="background:var(--card); border:1px solid var(--border); border-radius:24px; overflow:hidden; box-shadow:var(--shadow); width:100%;">{booking_embed}</div>
        </div>
    </section>
    """

def gen_inventory_js_client():
    return f"""
    <script defer>
    async function loadStore() {{
        try {{
            const res = await fetch('{sheet_url}'); const text = await res.text(); const data = parseCSV(text);
            const grid = document.getElementById('store-grid');
            for(let i=1; i<data.length; i++) {{
                let row = data[i]; if(!row || row.length < 2) continue;
                let images = row[3] ? row[3].split('|') : ['{custom_feat}'];
                let mainImg = images[0].trim(); let title = row[0]; let price = row[1];
                if(grid) {{
                    grid.innerHTML += `
                    <div class="card reveal">
                        <div class="prod-img-box"><img src="${{mainImg}}" class="prod-img"></div>
                        <div class="card-body">
                            <h3 style="font-size:1.35rem; margin-bottom:0.5rem; color:var(--txt-h);">${{title}}</h3>
                            <p style="color:var(--s); font-weight:800; font-size:1.2rem; margin-bottom:1rem;">${{price}}</p>
                            <div style="display:flex; gap:0.5rem; margin-top:auto;">
                                <a href="product.html?item=${{encodeURIComponent(title)}}" class="btn btn-primary" style="flex:1; padding:0.8rem; font-size:0.85rem;">View</a>
                                <button onclick="addToCart('${{title}}', '${{price}}')" class="btn btn-accent" style="flex:1; padding:0.8rem; font-size:0.85rem;">Add</button>
                            </div>
                        </div>
                    </div>`;
                }}
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    if(document.getElementById('store-grid')) loadStore();
    </script>
    """

def gen_product_page_content(is_demo=False):
    demo_flag = "true" if is_demo else "false"
    return f"""
    <div class="container detail-view" id="detail-app" style="margin-top:140px; margin-bottom:6rem;">Loading Product...</div>
    <script defer>
    async function initProduct() {{
        const params = new URLSearchParams(window.location.search); let target = params.get('item');
        if({demo_flag} && !target) target = "Demo Product";
        const res = await fetch('{sheet_url}'); const text = await res.text(); const data = parseCSV(text);
        for(let i=1; i<data.length; i++) {{
            let row = data[i];
            if(row[0] === target || ({demo_flag} && i===1)) {{
                let images = row[3] ? row[3].split('|') : ['{custom_feat}'];
                let thumbsHtml = '';
                images.forEach((img, idx) => {{ thumbsHtml += `<img src="${{img.trim()}}" class="thumb ${{idx===0?'active':''}}" onclick="switchImg('${{img.trim()}}', this)">`; }});
                document.getElementById('detail-app').innerHTML = `
                    <div class="product-media-column"><img src="${{images[0].trim()}}" class="gallery-main" id="main-img"><div class="gallery-thumbs">${{thumbsHtml}}</div></div>
                    <div class="product-info-column"><h1 style="font-size:3.5rem; margin-bottom:1rem; color:var(--txt-h);">${{row[0]}}</h1><div class="product-price-tag">${{row[1]}}</div><div class="product-specs-container" style="margin-bottom:3rem;">${{parseMarkdown(row[2])}}</div><button onclick="addToCart('${{row[0]}}', '${{row[1]}}')" class="btn btn-accent" style="width:100%; padding:1.2rem; font-size:1.1rem;">Add to Cart</button></div>
                `;
                break;
            }}
        }}
    }}
    initProduct();
    </script>
    """

def gen_blog_index_html():
    return f"""
    <section class="modern-hero" style="min-height:40vh; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img_1}'); background-size: cover; background-position:center; text-align:center; justify-content:center;">
        <div class="container modern-hero-text"><h1>{blog_hero_title}</h1><p>{blog_hero_sub}</p></div>
    </section>
    <section style="background:var(--bg);"><div class="container"><div id="blog-grid" class="grid-3">Loading Posts...</div></div></section>
    <script defer>
    async function loadBlog() {{ 
        const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/); 
        const box = document.getElementById('blog-grid'); box.innerHTML = ''; 
        for(let i=1; i<lines.length; i++) {{ 
            const r = parseCSVLine(lines[i]); 
            if(r.length > 4) {{ 
                box.innerHTML += `<article class="card reveal"><div style="width:100%; height:220px; overflow:hidden;"><img src="${{r[5]}}" style="width:100%; height:100%; object-fit:cover;"></div><div class="card-body"><span style="display:inline-block; padding:0.4rem 1rem; background:var(--border); color:var(--txt-h); border-radius:50px; font-size:0.75rem; font-weight:800; text-transform:uppercase; margin-bottom:1rem; width:fit-content;">${{r[3]}}</span><h3 style="margin-bottom:1rem; font-size:1.4rem;">${{r[1]}}</h3><p style="margin-bottom: 2rem; opacity:0.8;">${{r[4]}}</p><a href="post.html?id=${{r[0]}}" class="btn btn-primary" style="width:100%; margin-top:auto;">Read Article</a></div></article>`; 
            }} 
        }} 
    }} 
    window.addEventListener('load', loadBlog);
    </script>
    """

def gen_blog_post_html():
    return f"""
    <article id="post-container" style="padding-top:0px;">Loading Content...</article>
    <script defer>
    async function loadPost() {{
        const params = new URLSearchParams(window.location.search); const slug = params.get('id');
        const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
        const container = document.getElementById('post-container');
        for(let i=1; i<lines.length; i++) {{
            const r = parseCSVLine(lines[i]);
            if(r[0] === slug) {{
                container.innerHTML = `<header class="modern-hero" style="min-height:40vh; display:flex; align-items:center; justify-content:center; text-align:center;"><div class="container modern-hero-text"><span style="display:inline-block; padding:0.4rem 1.5rem; background:rgba(255,255,255,0.2); color:white; border-radius:50px; font-weight:800; text-transform:uppercase; margin-bottom:1rem;">${{r[3]}}</span><h1>${{r[1]}}</h1></div></header><div class="container" style="max-width:800px; padding: 4rem 1rem; background:var(--bg); color:var(--txt);"><img src="${{r[5]}}" style="width:100%; border-radius:16px; margin-bottom:3rem; box-shadow:var(--shadow);"><div style="line-height:1.9; font-size:1.15rem; opacity:0.9;">${{parseMarkdown(r[6])}}</div><hr style="margin:3rem 0; border:0; border-top:1px solid var(--border);"><a href="blog.html" class="btn btn-primary">&larr; Back to Blog</a></div>`;
                break;
            }}
        }}
    }}
    window.addEventListener('load', loadPost);
    </script>
    """

# --- 8. PREVIEW & EXPORT ASSEMBLY ---
st.divider()
st.subheader("🚀 2050 Launchpad")

col_nav1, col_nav2 = st.columns([3, 1])

# DECLARE PREVIEW_MODE AT ROOT LEVEL TO PREVENT NAME ERROR
with col_nav1:
    preview_mode = st.radio("Preview Page:", ["Home", "About", "Contact", "Blog Index", "Blog Post (Demo)", "Privacy", "Terms", "Product Detail (Demo)", "Booking Page"], horizontal=True)
with col_nav2:
    device_mode = st.radio("Device View:", ["💻 Desktop", "📱 Mobile Phone"], horizontal=True)

# ASSEMBLE HOME BODY
home_body = ""
if show_hero: home_body += gen_hero()
if show_stats: 
    home_body += f'<div class="stats-ribbon-container container reveal"><div class="stats-ribbon"><div class="stat-block"><h3>{stat_1}</h3><p>{label_1}</p></div><div class="stat-divider"></div><div class="stat-block"><h3>{stat_2}</h3><p>{label_2}</p></div><div class="stat-divider"></div><div class="stat-block"><h3>{stat_3}</h3><p>{label_3}</p></div></div></div>'
if show_features: 
    cards = "".join([f'<div class="card reveal" style="padding:0;"><div class="card-body"><div style="color:var(--s); margin-bottom:1.5rem; background:rgba(128,128,128,0.05); width:50px; height:50px; display:flex; align-items:center; justify-content:center; border-radius:12px;">{get_simple_icon(p[0])}</div><h3 style="font-size:1.35rem;">{p[1]}</h3><div style="opacity:0.8; line-height:1.7;">{format_text(p[2])}</div></div></div>' for line in feat_data_input.split('\n') if "|" in line for p in [line.split('|')] if len(p)>=3])
    home_body += f'<section id="features"><div class="container"><div class="section-head reveal"><h2 style="font-size:2.5rem; margin-bottom:0.5rem;">{f_title}</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem auto; border-radius:2px;"></div></div><div class="grid-3">{cards}</div></div></section>'
if show_pricing: 
    home_body += f'<section id="pricing"><div class="container"><div class="section-head reveal"><h2 style="font-size:2.5rem; margin-bottom:0.5rem;">Pricing</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem auto; border-radius:2px;"></div></div><div class="pricing-wrapper reveal"><table class="pricing-table"><thead><tr><th>Expense Item</th><th style="background:var(--s);">Titan Engine</th><th>{wix_name}</th></tr></thead><tbody><tr><td>Setup Fee</td><td><strong>{titan_price}</strong></td><td>$0</td></tr><tr><td>Monthly Hosting</td><td><strong>{titan_mo}</strong></td><td>{wix_mo}</td></tr><tr style="background:rgba(128,128,128,0.03);"><td><strong>Total Savings</strong></td><td style="color:var(--s); font-size:1.4rem; font-weight:800;">{save_val}</td><td>$0</td></tr></tbody></table></div></div></section>'
if show_inventory: 
    home_body += f'<section id="store" style="background:rgba(128,128,128,0.02)"><div class="container"><div class="section-head reveal"><h2 style="font-size:2.5rem; margin-bottom:0.5rem;">Tour Packages</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem auto; border-radius:2px;"></div></div><div id="store-grid" class="grid-3"></div></div></section>{gen_inventory_js_client()}'
if show_gallery: 
    home_body += f'<section id="about"><div class="container about-grid"><div class="reveal"><img src="{about_img}" style="width:100%; border-radius:32px; box-shadow:var(--shadow);"></div><div class="reveal"><h2 style="font-size:2.5rem; margin-bottom:1.5rem;">{about_h_in}</h2><div style="margin-bottom:2rem; font-size:1.1rem; opacity:0.9; line-height:1.8;">{format_text(about_short_in)}</div><a href="about.html" class="btn btn-primary">Read Our Story</a></div></div></section>'
if show_testimonials: 
    t_cards = "".join([f'<div class="card reveal"><div class="card-body"><p style="font-size:1.1rem; font-style:italic; line-height:1.7; opacity:0.9; margin-bottom:2rem; flex-grow:1;">"{x.split("|")[1].strip()}"</p><div style="display:flex; align-items:center; gap:15px; border-top:1px solid var(--border); padding-top:1.5rem;"><div style="width:45px; height:45px; border-radius:50%; background:var(--p); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:1.2rem;">{x.split("|")[0].strip()[0]}</div><div><b style="color:var(--txt-h); font-size:1.1rem; display:block;">{x.split("|")[0].strip()}</b><span style="font-size:0.8rem; opacity:0.6;">Verified Client</span></div></div></div></div>' for x in testi_data.split('\n') if "|" in x])
    home_body += f'<section id="testimonials" style="background:rgba(128,128,128,0.02)"><div class="container"><div class="section-head reveal"><h2 style="font-size:2.5rem; margin-bottom:0.5rem;">Client Stories</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem auto; border-radius:2px;"></div></div><div class="grid-3">{t_cards}</div></div></section>'
if show_faq: 
    items = "".join([f"<details class='reveal'><summary>{l.split('?')[0]}?</summary><p style='margin-top:1rem; opacity:0.9; line-height:1.6;'>{l.split('?')[1]}</p></details>" for l in faq_data.split('\n') if "?" in l and len(l.split('?'))>1])
    home_body += f'<section id="faq"><div class="container" style="max-width:800px;"><div class="section-head reveal"><h2 style="font-size:2.5rem; margin-bottom:0.5rem;">FAQ</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem auto; border-radius:2px;"></div></div>{items}</div></section>'
if show_cta: 
    home_body += f'<section style="background:var(--s); color:white; text-align:center;"><div class="container reveal"><h2 style="color:var(--btn-txt) !important; font-size:clamp(2.5rem, 5vw, 3.5rem); margin-bottom:1rem;">Ready to Launch?</h2><p style="margin-bottom:2rem; font-size:1.3rem; opacity:0.9; color:var(--btn-txt) !important;">Join the future of web architecture.</p><a href="contact.html" class="btn" style="background:var(--bg); color:var(--txt-h) !important;">Get Started</a></div></section>'

# ASSEMBLE CONTACT
contact_content = f"""{gen_inner_header("Contact Us")}<section style="background:var(--bg);"><div class="container"><div class="contact-grid"><div class="card"><div class="card-body"><h3 style="font-size:2rem; margin-bottom:1.5rem;">Get In Touch</h3><div style="margin-bottom:1.5rem;"><strong style="font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; color:var(--txt-h);">Headquarters</strong><p style="font-size:1.1rem; opacity:0.9; margin-top:0.5rem;">{biz_addr}</p></div><div style="margin-bottom:1.5rem;"><strong style="font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; color:var(--txt-h);">Direct Line</strong><p style="font-size:1.1rem; margin-top:0.5rem;"><a href="tel:{biz_phone}" style="color:var(--s); font-weight:bold;">{biz_phone}</a></p></div><div style="margin-bottom:2.5rem;"><strong style="font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; color:var(--txt-h);">Email</strong><p style="font-size:1.1rem; margin-top:0.5rem;">{biz_email}</p></div><a href="https://wa.me/{wa_num}" target="_blank" class="btn btn-accent" style="width:100%;">WhatsApp Us Instantly</a></div></div><div class="card"><div class="card-body"><h3 style="font-size:2rem; margin-bottom:1.5rem;">Send a Message</h3><form action="https://formsubmit.co/{biz_email}" method="POST" style="display:flex; flex-direction:column; gap:1.5rem;"><div><label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem; display:block;">Full Name</label><input type="text" name="name" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; outline:none;"></div><div><label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem; display:block;">Email</label><input type="email" name="email" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; outline:none;"></div><div><label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem; display:block;">Message</label><textarea name="msg" rows="5" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; outline:none; resize:vertical;"></textarea></div><button class="btn btn-primary" type="submit" style="height:4rem; font-size:1.1rem; margin-top:1rem;">Send Secure Message</button></form></div></div></div><div style="border-radius:24px; overflow:hidden; border:var(--border); margin-top:4rem; box-shadow:var(--shadow); height: 450px; position: relative;">{map_iframe.replace('<iframe ', '<iframe style="width:100% !important; height:100% !important; position:absolute; top:0; left:0; border:none;" ')}</div></div></section>"""

# HTML STRING ROUTING
html_to_render = ""
if preview_mode == "Home": html_to_render = build_page("Home", home_content)
elif preview_mode == "About": html_to_render = build_page("About", f"{gen_inner_header('About')}<section><div class='container'>{format_text(about_long)}</div></section>")
elif preview_mode == "Contact": html_to_render = build_page("Contact", contact_content)
elif preview_mode == "Privacy": html_to_render = build_page("Privacy", f"{gen_inner_header('Privacy')}<section><div class='container'>{format_text(priv_txt)}</div></section>")
elif preview_mode == "Terms": html_to_render = build_page("Terms", f"{gen_inner_header('Terms')}<section><div class='container'>{format_text(term_txt)}</div></section>")
elif preview_mode == "Blog Index": html_to_render = build_page("Blog", gen_blog_index_html())
elif preview_mode == "Blog Post (Demo)": html_to_render = build_page("Article", gen_blog_post_html())
elif preview_mode == "Product Detail (Demo)": html_to_render = build_page("Product", gen_product_page_content(is_demo=True))
elif preview_mode == "Booking Page": html_to_render = build_page("Book Now", gen_booking_content())

# DISPLAY TO SCREEN
c1, c2 = st.columns([3, 1])
with c1:
    if device_mode == "📱 Mobile Phone":
        st.markdown("<div style='text-align: center; color: #888; margin-bottom:10px;'><i>📱 Mobile Emulation Active</i></div>", unsafe_allow_html=True)
        left_sp, phone_screen, right_sp = st.columns([1.2, 1.5, 1.2])
        with phone_screen:
            st.markdown("<style>.phone-bezel { border: 14px solid #1a1a1a; border-radius: 40px; padding: 0; background: #000; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); overflow: hidden; margin: 0 auto; }</style><div class='phone-bezel'>", unsafe_allow_html=True)
            st.components.v1.html(html_to_render, height=750, scrolling=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.components.v1.html(html_to_render, height=750, scrolling=True)

# EXPORT SYSTEM
with c2:
    st.success("System Operational.")
    
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", build_page("Home", home_content))
        zf.writestr("about.html", build_page("About", f"{gen_inner_header('About')}<section><div class='container'>{format_text(about_long)}</div></section>"))
        zf.writestr("contact.html", build_page("Contact", contact_content))
        zf.writestr("privacy.html", build_page("Privacy", f"{gen_inner_header('Privacy')}<section><div class='container'>{format_text(priv_txt)}</div></section>"))
        zf.writestr("terms.html", build_page("Terms", f"{gen_inner_header('Terms')}<section><div class='container'>{format_text(term_txt)}</div></section>"))
        if show_booking: zf.writestr("booking.html", build_page("Book Now", gen_booking_content()))
        if show_inventory: zf.writestr("product.html", build_page("Product Details", gen_product_page_content(is_demo=False)))
        if show_blog: zf.writestr("blog.html", build_page("Blog", gen_blog_index_html())); zf.writestr("post.html", build_page("Article", gen_blog_post_html()))
        
        zf.writestr("manifest.json", gen_pwa_manifest())
        zf.writestr("service-worker.js", gen_sw())
        zf.writestr("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {prod_url}/sitemap.xml")
        zf.writestr("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{prod_url}/</loc></url></urlset>""")
    
    if pinata_jwt:
        if st.button("🌌 PUSH TO Web3 (IPFS)", type="primary"):
            with st.spinner("Encrypting and uploading to IPFS Blockchain..."):
                try:
                    res = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS", headers={"Authorization": f"Bearer {pinata_jwt}"}, files={"file": ("titan_site.zip", z_b.getvalue())})
                    if res.status_code == 200:
                        cid = res.json()['IpfsHash']
                        st.success(f"Deployed! Live forever on IPFS.")
                        st.markdown(f"**Gateway Link:** [ipfs.io/ipfs/{cid}](https://ipfs.io/ipfs/{cid})")
                    else: st.error(f"IPFS Error: {res.text}")
                except Exception as e: st.error(f"Upload failed: {e}")
    else:
        st.download_button("📥 DOWNLOAD APEX PACKAGE", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_apex.zip", "application/zip", type="primary")
