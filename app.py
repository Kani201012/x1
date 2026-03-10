import streamlit as st
import zipfile
import io
import json
import datetime
import re
import requests

# --- 0. STATE MANAGEMENT ---
def init_state(key, default_val):
    if key not in st.session_state:
        st.session_state[key] = default_val

init_state('hero_h', "Stop Paying Rent for Your Website.")
init_state('hero_sub', "The Titan Engine is the world’s first 0.1s website architecture that runs on $0 monthly fees. Pay once. Own it forever.")
init_state('about_h', "Control Your Empire from a Spreadsheet")
init_state('about_short', "No WordPress dashboard. No plugins to update. Just open your private Google Sheet, change a text, and watch your site update globally in seconds.")
init_state('feat_data', "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. While traditional sites take 3–5s, Titan loads instantly.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions.\ntable | The Functional Pillar | **Google Sheets CMS**. Update prices and photos directly from a simple spreadsheet.\nshield | The Authority Pillar | **Unhackable Security**. Zero-DB Architecture removes the hacker's primary entry point.\nlayers | The Reliability Pillar | **Global Edge Deployment**. Distributed across 100+ servers worldwide.\nstar | The Conversion Pillar | **One-Tap WhatsApp**. Direct-to-Chat technology.")

# --- 2050 TITAN THEME REGISTRY ---
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
    "24. Gradient Mesh": {"bg": "linear-gradient(45deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)", "txt": "#333", "card": "rgba(255,255,255,0.6)", "p": "#f77062", "s": "#3f51b5", "nav": "rgba(255,255,255,0.4)", "shadow": "0 8px 32px rgba(0,0,0,0.1)", "radius": "30px", "border": "1px solid rgba(255,255,255,0.5)"},
    "25. Midnight Ocean": {"bg": "#0f2027", "txt": "#d1d5db", "card": "#203a43", "p": "#2c5364", "s": "#38ef7d", "nav": "rgba(15,32,39,0.9)", "shadow": "0 15px 25px rgba(0,0,0,0.3)", "radius": "16px", "border": "1px solid #2c5364"}
}

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="Titan Architect | 2050 Apex Edition", layout="wide", page_icon="⚡", initial_sidebar_state="expanded")

# --- 2. ADVANCED UI SYSTEM ---
st.markdown("""
    <style>
    :root { --primary: #0f172a; --accent: #ef4444; }
    .stApp { background-color: #f8fafc; color: #1e293b; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] h1 { background: linear-gradient(90deg, #0f172a, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; font-size: 1.8rem !important; }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] { background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; color: #0f172a !important; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5rem; background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3); text-transform: uppercase; letter-spacing: 1px; transition: transform 0.2s; }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Titan Architect")
    st.caption("v100.8 | Syntax Error Fixed")
    st.divider()
    
    # --- AI GENERATOR ---
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
                            if 'hero_h' in parsed: st.session_state.hero_h = str(parsed['hero_h'])
                            if 'hero_sub' in parsed: st.session_state.hero_sub = str(parsed['hero_sub'])
                            if 'about_h' in parsed: st.session_state.about_h = str(parsed['about_h'])
                            if 'about_short' in parsed: st.session_state.about_short = str(parsed['about_short'])
                            if 'feat_data' in parsed:
                                if isinstance(parsed['feat_data'], list): st.session_state.feat_data = "\n".join(map(str, parsed['feat_data']))
                                else: st.session_state.feat_data = str(parsed['feat_data'])
                            st.success("Generated Successfully!")
                            st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    # 3.1 VISUAL DNA & UI VARIATIONS (2026 ENGINE)
    with st.expander("🎨 Design Studio", expanded=True):
        st.markdown("**1-Click Global Themes**")
        theme_names = list(THEME_REGISTRY.keys())
        theme_mode = st.selectbox("Select 2026 Architecture Theme", theme_names)
        st.divider()
        st.markdown("**Layout & Typography**")
        c1, c2 = st.columns(2)
        with c1: hero_layout = st.selectbox("Hero Alignment", ["Center", "Left"])
        with c2: anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])
        c3, c4 = st.columns(2)
        with c3: h_font = st.selectbox("Headings Font", ["Space Grotesk", "Montserrat", "Playfair Display", "Outfit", "Clash Display"])
        with c4: b_font = st.selectbox("Body Font", ["Inter", "Plus Jakarta Sans", "Satoshi", "Roboto"])
        
        btn_style = st.selectbox("Button Shape", ["Rounded", "Sharp", "Pill"])
        border_rad = st.slider("Global Corner Radius", 0, 40, 12)

    # 3.1.2 TYPOGRAPHY & COLOR MASTERY
    with st.expander("👁️ Typography & Color Mastery", expanded=False):
        st.markdown("**Global Text Colors**")
        col_h = st.color_picker("Headings Color", "#0f172a")
        col_b = st.color_picker("Body Text Color", "#475569")
        st.divider()
        st.markdown("**Global Font Sizes (Rem)**")
        size_h1 = st.slider("H1 Main Heading Size", 1.0, 8.0, 4.5)
        size_p = st.slider("Body Text Size", 0.8, 2.0, 1.1)
        st.divider()
        st.markdown("**CTA Section Adjustment**")
        cta_bg_color = st.color_picker("Final CTA Background", "#10b981")
        cta_txt_color = st.color_picker("Final CTA Text Color", "#ffffff")

    # 3.2 2050 FEATURE FLAGS
    with st.expander("🚀 2050 Feature Flags", expanded=True):
        st.write("Enable Next-Gen Capabilities:")
        enable_ar = st.checkbox("Spatial Web (AR 3D Models)", value=True, help="Injects <model-viewer> for .glb links in your CSV.")
        enable_voice = st.checkbox("Voice Command Search", value=True, help="Native browser NLP for store filtering.")
        enable_context = st.checkbox("Context-Aware UI", value=True, help="Auto dark-mode based on user's local time.")
        enable_ab = st.checkbox("Edge A/B Testing", value=True, help="Client-side variant testing without tracking cookies.")

    # 3.3 MODULE MANAGER
    with st.expander("🧩 Section Manager", expanded=False):
        show_hero = st.checkbox("Hero Section", value=True)
        show_stats = st.checkbox("Trust Stats", value=True)
        show_features = st.checkbox("Feature Grid", value=True)
        show_pricing = st.checkbox("Pricing Table", value=True)
        show_inventory = st.checkbox("Tour Packages", value=True)
        show_blog = st.checkbox("Blog Engine", value=True)
        show_gallery = st.checkbox("About Section", value=True)
        show_testimonials = st.checkbox("Testimonials", value=True)
        show_faq = st.checkbox("F.A.Q.", value=True)
        show_cta = st.checkbox("Final CTA", value=True)
        show_booking = st.checkbox("Booking Engine", value=True)

    # 3.4 TECHNICAL
    with st.expander("⚙️ SEO & Analytics", expanded=False):
        seo_area = st.text_input("Service Area", "Global / Online")
        seo_kw = st.text_area("SEO Keywords", "web design, no monthly fees")
        gsc_tag = st.text_input("Google Verification ID")
        ga_tag = st.text_input("Google Analytics ID")
        og_image = st.text_input("Social Share Image URL")

# --- 4. MAIN WORKSPACE ---
st.title("🏗️ StopWebRent 2050 Compiler")

tabs = st.tabs(["1. Identity & PWA", "2. Content Blocks", "3. Marketing Tools", "4. Pricing", "5. Packages", "6. Booking", "7. Blog", "8. Legal", "9. Web3 / IPFS"])

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
    stat_1 = col_s1.text_input("Stat 1", "0.1s")
    label_1 = col_s1.text_input("Label 1", "Speed")
    stat_2 = col_s2.text_input("Stat 2", "$0")
    label_2 = col_s2.text_input("Label 2", "Fees")
    stat_3 = col_s3.text_input("Stat 3", "100%")
    label_3 = col_s3.text_input("Label 3", "Ownership")

    f_title = st.text_input("Features Title", "Value Pillars")
    feat_data_input = st.text_area("Features List", st.session_state.feat_data, height=150)
    
    st.subheader("About")
    about_h_in = st.text_input("About Title", key="about_h")
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    about_short_in = st.text_area("Short Summary", key="about_short", height=100)
    about_long = st.text_area("Full Content", "The Digital Landlord Trap...", height=200)

with tabs[2]:
    st.subheader("📣 Marketing Suite")
    top_bar_enabled = st.checkbox("Enable Top Bar")
    top_bar_text = st.text_input("Promo Text", "🔥 50% OFF Launch Sale - Ends Soon!")
    top_bar_link = st.text_input("Promo Link", "#pricing")
    
    st.divider()
    popup_enabled = st.checkbox("Enable Popup")
    popup_delay = st.slider("Delay (seconds)", 1, 30, 5)
    popup_title = st.text_input("Popup Headline", "Wait! Don't leave empty handed.")
    popup_text = st.text_input("Popup Body", "Get our free pricing guide on WhatsApp.")
    popup_cta = st.text_input("Popup Button", "Get it Now")

with tabs[3]:
    st.subheader("💰 Pricing")
    col_p1, col_p2, col_p3 = st.columns(3)
    titan_price = col_p1.text_input("Setup Price", "$199")
    titan_mo = col_p1.text_input("Monthly Fee", "$0")
    wix_name = col_p2.text_input("Competitor", "Wix")
    wix_mo = col_p2.text_input("Comp. Monthly", "$29/mo")
    save_val = col_p3.text_input("Savings", "$1,466")

with tabs[4]:
    st.subheader("🛒 Store & Payments")
    st.info("💡 **2050 AR Protocol:** In your Store CSV, make Column F (the 6th column) a link to a `.glb` 3D model to enable native Augmented Reality.")
    sheet_url = st.text_input("Store CSV", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    custom_feat = st.text_input("Default Product Img", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800")
    col_pay1, col_pay2 = st.columns(2)
    paypal_link = col_pay1.text_input("PayPal Link", "https://paypal.me/yourid")
    upi_id = col_pay2.text_input("UPI ID", "name@upi")

with tabs[5]:
    st.subheader("📅 Booking Engine")
    booking_embed = st.text_area("Embed Code", height=150, value='<!-- Calendly inline widget begin -->\n<div class="calendly-inline-widget" data-url="https://calendly.com/titan-demo/30min" style="min-width:320px;height:630px;"></div>\n<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>\n<!-- Calendly inline widget end -->')
    booking_title = st.text_input("Booking Title", "Book an Appointment")
    booking_desc = st.text_input("Booking Subtext", "Select a time slot.")

with tabs[6]:
    st.subheader("📰 Blog")
    blog_sheet_url = st.text_input("Blog CSV", placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv")
    blog_hero_title = st.text_input("Blog Title", "Latest Insights")
    blog_hero_sub = st.text_input("Blog Subtext", "Thoughts on tech.")

with tabs[7]:
    st.subheader("Legal")
    testi_data = st.text_area("Testimonials", "Rajesh Gupta | Titan stopped the bleeding.\nSarah Jenkins | Easy updates.", height=100)
    faq_data = st.text_area("FAQ", "Do I pay $0? ? Yes.\nIs it secure? ? Yes.", height=100)
    priv_txt = st.text_area("Privacy", "We collect minimum data.", height=100)
    term_txt = st.text_area("Terms", "You own the code.", height=100)

with tabs[8]:
    st.subheader("🪐 InterPlanetary File System (IPFS) Deployment")
    st.markdown("Host your site on the decentralized Web3 network. It can never be taken down, and costs $0/month.")
    pinata_jwt = st.text_input("Pinata API JWT (Leave blank for standard ZIP download)", type="password")


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

def gen_schema():
    schema = {
        "@context": "https://schema.org", 
        "@type": "LocalBusiness", 
        "name": biz_name, 
        "image": logo_url or hero_img_1, 
        "telephone": biz_phone, 
        "email": biz_email, 
        "url": prod_url, 
        "description": seo_d
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def gen_pwa_manifest():
    current_theme = THEME_REGISTRY.get(theme_mode, THEME_REGISTRY.get("1. Stripe Cloud (Modern SaaS)", {}))
    bg_color = current_theme.get('bg', '#ffffff')
    if bg_color.startswith('linear'): bg_color = '#ffffff'

    return json.dumps({
        "name": biz_name, 
        "short_name": pwa_short, 
        "start_url": "./index.html",
        "display": "standalone", 
        "background_color": bg_color, 
        "theme_color": current_theme.get('p', p_color),
        "description": pwa_desc, 
        "icons": [{"src": pwa_icon, "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]
    })

def gen_sw():
    return """
    const CACHE_NAME = 'titan-v50-cache';
    const urlsToCache = ['./index.html', './about.html', './contact.html', './product.html', './blog.html', './post.html'];
    
    self.addEventListener('install', (e) => { 
        e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))); 
        self.skipWaiting(); 
    });
    
    self.addEventListener('fetch', (e) => { 
        if (e.request.url.includes('google.com/spreadsheets')) {
            e.respondWith(fetch(e.request).then(res => {
                const resClone = res.clone(); 
                caches.open('titan-data').then(cache => cache.put(e.request, resClone)); 
                return res;
            }).catch(() => caches.match(e.request)));
        } else {
            e.respondWith(caches.match(e.request).then((response) => response || fetch(e.request)));
        }
    });
    """

def gen_2050_scripts():
    context_js = "if(new Date().getHours() >= 19 || new Date().getHours() <= 6) document.body.classList.add('dark-mode');" if enable_context else ""
    ab_js = "let variant = localStorage.getItem('titan_ab') || (Math.random() > 0.5 ? 'A' : 'B'); localStorage.setItem('titan_ab', variant); if(variant === 'B') document.documentElement.style.setProperty('--s', '#10b981');" if enable_ab else ""
    voice_js = "function startVoiceSearch() { if (!('webkitSpeechRecognition' in window)) return alert('Voice search not supported in this browser.'); const rec = new webkitSpeechRecognition(); rec.lang = 'en-US'; const btn = document.getElementById('voice-btn'); btn.classList.add('listening'); rec.onresult = (e) => { const transcript = e.results[0][0].transcript.toLowerCase(); alert('Searching for: ' + transcript); document.querySelectorAll('.card').forEach(c => { c.style.display = c.innerText.toLowerCase().includes(transcript) ? 'flex' : 'none'; }); }; rec.onend = () => btn.classList.remove('listening'); rec.start(); }" if enable_voice else ""
    return f"<script defer>{context_js} {ab_js} {voice_js}</script>"


def generate_modern_css():
    t = THEME_REGISTRY.get(theme_mode, THEME_REGISTRY.get("1. Stripe Cloud (Modern SaaS)", {}))
    
    glass_val = t.get('glass', t.get('nav', 'rgba(255,255,255,0.8)'))
    border_val = t.get('border', '1px solid rgba(128,128,128,0.1)')
    shadow_val = t.get('shadow', '0 4px 6px rgba(0,0,0,0.05)')
    
    gradient_text = ""
    if any(x in theme_mode for x in ["SaaS", "Dark", "Creative"]):
        gradient_text = f"background: linear-gradient(90deg, {t.get('p', p_color)}, {t.get('s', s_color)}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"

    btn_hover = "transform: translateY(-3px) scale(1.02); filter: brightness(1.15); box-shadow: 0 10px 25px -5px var(--p);"
    if any(x in theme_mode for x in ["Brutalist", "Cyberpunk", "Monochromatic"]):
        btn_hover = "transform: translate(-4px, -4px); box-shadow: 8px 8px 0px #000;"

    backdrop = "backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);" if any(x in theme_mode for x in ["Glass", "Mesh"]) else ""

    h_align = "text-align: center; justify-content: center;"
    if hero_layout == "Left":
        h_align = "text-align: left; justify-content: flex-start; align-items: center;"

    radius_val = f"{border_rad}px"
    if btn_style == "Sharp": radius_val = "0px"
    elif btn_style == "Pill": radius_val = "50px"

    return f"""
    :root {{
        --p: {t.get('p', p_color)}; --s: {cta_bg_color}; --bg: {t.get('bg', '#ffffff')}; 
        --txt: {col_b}; --txt-h: {col_h}; --card: {t.get('card', '#ffffff')};
        --glass: {glass_val}; --border: {border_val}; --radius: {radius_val};
        --shadow: {shadow_val}; --btn-txt: {cta_txt_color};
        --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif;
        --h1-size: {size_h1}rem; --p-size: {size_p}rem;
    }}
    
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-size: 16px; }}
    
    body {{ 
        background: var(--bg); 
        color: var(--txt); 
        font-family: var(--b-font); 
        font-size: var(--p-size); 
        line-height: 1.8;
        letter-spacing: 0.01em; 
        overflow-x: hidden; 
        width: 100vw; max-width: 100%;
        transition: background 0.3s, color 0.3s;
    }}

    body.dark-mode {{
        --bg: #0f172a; --txt: #f8fafc; --txt-h: #ffffff;
        --card: #1e293b; --glass: rgba(30, 41, 59, 0.8); --border: rgba(255, 255, 255, 0.05);
    }}
    
    iframe, model-viewer {{ max-width: 100%; }}
    
    h1, h2, h3, h4 {{ 
        font-family: var(--h-font); 
        color: var(--txt-h); 
        line-height: 1.1; 
        font-weight: 800;
        margin-bottom: 1.5rem;
    }}

    h1 {{ font-size: var(--h1-size); {gradient_text} }}
    h2 {{ font-size: calc(var(--h1-size) * 0.7); }}
    h3 {{ font-size: 1.6rem; color: var(--txt-h); }}

    p {{ margin-bottom: 2rem; opacity: 0.9; font-weight: 400; text-align: justify; hyphens: auto; -webkit-hyphens: auto; }}
    
    /* HERO ENGINE */
    .hero {{ position: relative; min-height: 95vh; overflow: hidden; display: flex; {h_align} padding-top: 140px; }}
    .carousel-slide {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s cubic-bezier(0.4, 0, 0.2, 1); z-index: 0; transform: scale(1.05); }}
    .carousel-slide.active {{ opacity: 1; transform: scale(1); }}
    .hero-overlay {{ background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.8) 100%); position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
    .hero-content {{ z-index: 2; position: relative; width: 100%; padding: 0 5%; max-width: 1400px; }}
    .hero h1 {{ color: #ffffff !important; text-shadow: 0 10px 30px rgba(0,0,0,0.5); -webkit-text-fill-color: #fff; background: none; }}
    .hero p {{ color: rgba(255,255,255,0.9) !important; font-size: clamp(1.2rem, 2vw, 1.4rem); max-width: 800px; margin: 0 {'auto' if hero_layout == 'Center' else '0'} 2.5rem {'auto' if hero_layout == 'Center' else '0'}; font-weight: 400; }}
    
    /* GRIDS */
    .container {{ max-width: 1300px; margin: 0 auto; padding: 0 2rem; box-sizing: border-box; }}
    main section {{ padding: clamp(2rem, 8vw, 8rem) 0; position: relative; }}
    .section-head {{ text-align: center; margin-bottom: clamp(3rem, 5vw, 5rem); display:flex; flex-direction:column; align-items:center; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem; }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items: center; }}
    .contact-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: stretch; }}
    
    /* CARDS */
    .card {{ background: var(--card); border-radius: var(--radius); border: var(--border); box-shadow: var(--shadow); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); display: flex; flex-direction: column; overflow: hidden; position: relative; color: var(--txt) !important; {backdrop} }}
    .card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--p), var(--s)); opacity: 0; transition: 0.3s; z-index: 5; }}
    .card:hover {{ transform: translateY(-10px); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.2); }}
    .card:hover::before {{ opacity: 1; }}
    
    .card h3 {{ font-size: 1.35rem !important; font-weight: 800; line-height: 1.2; margin-bottom: 0.4rem; color: var(--txt-h) !important; letter-spacing: -0.02em; }}
    .card-body {{ padding: 2rem; display: flex; flex-direction: column; flex-grow: 1; text-align:left; }}
    .card-desc {{ font-size: 0.95rem; line-height: 1.6; opacity: 0.7; margin-bottom: 1.5rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; color: var(--txt); }}
    .prod-img {{ width: 100%; height: 260px; object-fit: cover; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }}
    .card:hover .prod-img {{ transform: scale(1.08); }}
    
    /* BUTTONS */
    .btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 1.2rem 2.5rem; border-radius: var(--radius); font-weight: 800; text-decoration: none; transition: all 0.3s ease; text-transform: uppercase; cursor: pointer; border: none; text-align: center; font-size: 0.95rem; letter-spacing: 1.5px; position: relative; overflow: hidden; }}
    .btn-primary {{ background: var(--p); color: #fff !important; }}
    .btn-accent {{ background: var(--s); color: var(--btn-txt) !important; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn-outline-light {{ background: transparent; border: 2px solid #fff; color: #fff !important; }}
    .btn:hover {{ {btn_hover} }}
    
    /* NAV */
    nav#main-navbar {{ position: fixed; top: 0; width: 100%; z-index: 2000; background: var(--glass); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); padding: 1.2rem 0; transition: top 0.3s, background 0.3s; }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; align-items: center; gap: 2rem; }}
    .nav-links a {{ text-decoration: none; font-weight: 600; color: var(--txt-h); font-size: 0.95rem; transition: 0.2s; position: relative; }}
    .nav-links a::after {{ content: ''; position: absolute; width: 0; height: 2px; bottom: -4px; left: 0; background-color: var(--p); transition: 0.3s; }}
    .nav-links a:hover::after {{ width: 100%; }}
    .nav-links a:hover {{ color: var(--p); }}
    .mobile-menu {{ display: none; font-size: 1.8rem; cursor: pointer; background:none; border:none; color:var(--txt-h); z-index: 2001; }} 
    
    /* PRODUCT VIEW */
    .detail-view {{ display: grid; grid-template-columns: 0.8fr 1.2fr; gap: 6rem; align-items: start; background: var(--card); padding: 5rem; border-radius: 32px; box-shadow: var(--shadow); border: var(--border); }}
    .product-price-tag {{ display: inline-block; padding: 0.5rem 1.5rem; background: rgba(5, 150, 105, 0.1); color: #059669; font-size: 2rem; font-weight: 900; border-radius: 50px; margin-bottom: 2rem; }}
    .product-info-column h1 {{ font-size: clamp(1.8rem, 3vw, 2.5rem) !important; margin-bottom: 1.5rem; line-height: 1; }}
    .gallery-main {{ width: 100%; height: 500px; object-fit: cover; border-radius: var(--radius); margin-bottom: 1rem; box-shadow: var(--shadow); }}
    .gallery-thumbs {{ display: flex; gap: 15px; margin-top: 20px; overflow-x: auto; padding-bottom:10px; }}
    .thumb {{ width: 80px; height: 80px; border-radius: var(--radius); object-fit: cover; cursor: pointer; border: 2px solid transparent; opacity: 0.6; transition: 0.3s; }}
    .thumb:hover, .thumb.active {{ border-color: var(--p); opacity: 1; transform: translateY(-5px); }}
    
    /* TABLES & FOOTER */
    .pricing-table {{ width: 100%; border-collapse: collapse; min-width: 800px; }}
    .pricing-table th {{ background: var(--p); color: white; padding: 2rem; text-align: left; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }}
    .pricing-table td {{ padding: 2rem; border-bottom: 1px solid var(--border); color: var(--txt); font-size: 1.1rem; }}
    .pricing-table tr:hover td {{ background: rgba(128,128,128,0.03); }}

    footer {{ background: #0f172a; color: #f8fafc; padding: 6rem 0 3rem 0; margin-top: auto; border-top: 4px solid var(--p); }}
    .footer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 4rem; }}
    footer a {{ color: #94a3b8 !important; text-decoration: none; display: block; margin-bottom: 1rem; transition: 0.3s; font-size: 1.05rem; }}
    footer a:hover {{ color: #ffffff !important; transform: translateX(5px); }}
    .social-icon {{ width: 28px; height: 28px; fill: #94a3b8; transition: 0.3s; }}
    .social-icon:hover {{ fill: var(--p); transform: scale(1.2) translateY(-3px); }}

    /* UTILS & TOASTS */
    .reveal {{ opacity: 0; transform: translateY(40px); transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94); z-index: 10; position:relative; }}
    .reveal.active {{ opacity: 1; transform: translateY(0); }}
    details {{ background: var(--card); border: var(--border); border-radius: var(--radius); margin-bottom: 1.5rem; padding: 1.5rem; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition:0.3s; color:var(--txt); }}
    details:hover {{ box-shadow: var(--shadow); transform: translateX(5px); border-left: 4px solid var(--p); }}
    details summary {{ font-weight: 800; font-size: 1.2rem; outline: none; color:var(--txt-h); }}

    #toast-box {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 9999; display: flex; flex-direction: column; gap: 10px; }}
    .toast {{ background: var(--txt); color: var(--bg); padding: 12px 24px; border-radius: 50px; font-weight: 600; box-shadow: 0 10px 30px rgba(0,0,0,0.2); opacity: 0; transform: translateY(20px); transition: 0.4s; }}
    .toast.show {{ opacity: 1; transform: translateY(0); }}
    
    .float-btn {{ position: fixed; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 20px rgba(0,0,0,0.1); z-index: 990; cursor: pointer; transition: 0.3s; }}
    #wa-float {{ bottom: 100px; right: 30px; background: #25D366; color: white; }}
    #cart-float {{ bottom: 30px; right: 30px; background: var(--p); color: white; }}
    #mode-toggle {{ bottom: 30px; left: 30px; background: var(--card); color: var(--txt); border:1px solid var(--border); }}

    /* MODERN HERO 2.0 */
    .modern-hero {{ position: relative; min-height: 100vh; display: flex; {h_align} padding-top: 120px; }}
    .modern-hero-bg {{ position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle at 50% 50%, rgba(128,128,128,0.05) 0%, transparent 50%); z-index: -1; animation: rotate 60s linear infinite; }}
    .modern-hero-grid {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 4rem; align-items: center; width: 100%; }}
    .hero-badge {{ display: inline-block; padding: 0.5rem 1rem; background: rgba(128,128,128,0.1); border: 1px solid rgba(128,128,128,0.2); border-radius: 50px; font-size: 0.9rem; font-weight: 700; margin-bottom: 1.5rem; color: var(--txt-h); text-transform: uppercase; letter-spacing: 1px; }}
    .modern-hero-visual {{ position: relative; width: 100%; height: 600px; display: flex; align-items: center; justify-content: center; }}
    .visual-frame {{ width: 100%; height: 100%; border-radius: 32px; overflow: hidden; position: relative; z-index: 2; box-shadow: 0 30px 60px rgba(0,0,0,0.15); border: 8px solid var(--card); }}
    .floating-element {{ position: absolute; border-radius: 50%; filter: blur(60px); z-index: 1; opacity: 0.6; }}
    .glow-1 {{ width: 300px; height: 300px; background: var(--p); top: -50px; right: -50px; }}
    .glow-2 {{ width: 250px; height: 250px; background: var(--s); bottom: -50px; left: -50px; }}

    /* MOBILE RESPONSIVE FIXES */
    @media (max-width: 992px) {{
        nav#main-navbar .nav-links {{ position: absolute; top: 100%; left: -100%; width: 100vw; height: 100dvh; background: var(--bg); flex-direction: column; padding: 3rem; transition: left 0.4s ease; align-items: center; justify-content: flex-start; gap: 2.5rem; z-index: 1999; overflow-y: auto; }}
        nav#main-navbar .nav-links.active {{ left: 0; }}
        .nav-links a {{ font-size: 1.5rem; }}
        .mobile-menu {{ display: block; }}
        .about-grid, .detail-view, .grid-3, .contact-grid {{ grid-template-columns: 1fr !important; gap: 3rem; }}
        .modern-hero-grid {{ grid-template-columns: 1fr; text-align: center; }}
        .modern-hero-text {{ text-align: center; align-items: center; justify-content: center; margin:0 auto; }}
        .hero-btn-group {{ justify-content: center; }}
        .modern-hero-visual {{ height: 400px; }}
        .detail-view {{ padding: 2rem; gap: 2rem; }}
        .pricing-table th, .pricing-table td {{ padding: 1.2rem 1rem; font-size: 0.95rem; }}
    }}
    
    @media (max-width: 480px) {{
        p {{ text-align: left; hyphens: auto; }}
        html, body {{ width: 100% !important; margin: 0 !important; padding: 0 !important; overflow-x: hidden !important; }}
        .container {{ width: 100% !important; max-width: 100% !important; padding: 0 24px !important; box-sizing: border-box !important; }}
        footer {{ padding: 4rem 0 10rem 0 !important; }}
        h1, #hero-title, .modern-hero-text h1 {{ font-size: 2.4rem !important; line-height: 1.1 !important; margin-bottom: 1.5rem !important; }}
        .hero-btn-group {{ display: flex; flex-direction: column !important; gap: 12px; width: 100%; }}
        .hero-btn-group .btn {{ width: 100% !important; }}
        #wa-float {{ bottom: 15px !important; right: 10px !important; scale: 0.8; }}
        #theme-toggle {{ bottom: 15px !important; left: 10px !important; scale: 0.8; }}
        #cart-float {{ bottom: 80px !important; right: 10px !important; scale: 0.8; }}
        .modern-hero-visual {{ height: 300px !important; margin-top: 2rem !important; }}
        .pricing-table {{ min-width: 100% !important; }}
    }}
    
    /* TOP BAR AND POPUP */
    #top-bar {{ position: fixed; top: 0; left: 0; width: 100%; background: var(--s); color: var(--btn-txt); text-align: center; padding: 8px; z-index: 2005; font-weight: 800; font-size: 0.85rem; height: 40px; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 10px rgba(0,0,0,0.1); }}
    #top-bar a {{ color: var(--btn-txt) !important; text-decoration: underline; margin-left:10px; }}
    """

def gen_nav():
    logo_display = f'<img src="{logo_url}" height="40" width="auto" alt="{biz_name} Logo" loading="eager" style="margin-right:10px; object-fit:contain;">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    
    nav_links = f'<a href="index.html" onclick="toggleMenu()">Home</a>'
    if show_features: nav_links += '<a href="index.html#features" onclick="toggleMenu()">Features</a>'
    if show_pricing: nav_links += '<a href="index.html#pricing" onclick="toggleMenu()">Savings</a>'
    if show_inventory: nav_links += '<a href="index.html#store" onclick="toggleMenu()">Tour Packages</a>'
    if show_blog: nav_links += '<a href="blog.html" onclick="toggleMenu()">Blog</a>'
    if show_booking: nav_links += '<a href="booking.html" onclick="toggleMenu()">Book Now</a>'
    nav_links += '<a href="contact.html" onclick="toggleMenu()">Contact</a>'
    
    lang_btn = f'<a href="#" onclick="openLangModal()" aria-label="Switch Language">🌐 ES</a>' if lang_sheet else ''
    top_bar = f'<div id="top-bar"><a href="{top_bar_link}">{top_bar_text}</a></div>' if top_bar_enabled else ''
    
    return f"""
    {top_bar}
    <nav id="main-navbar">
        <div class="container nav-flex">
            <a href="index.html" aria-label="Home" style="text-decoration:none; display:flex; align-items:center; color:var(--txt-h);">{logo_display}</a>
            <div class="mobile-menu" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div>
            <div class="nav-links">
                {nav_links}
                {lang_btn}
                <a href="tel:{biz_phone}" class="btn btn-accent" style="padding:0.6rem 1.5rem; border-radius:50px;">Call Now</a>
            </div>
        </div>
    </nav>
    <div id="theme-toggle" onclick="document.body.classList.toggle('dark-mode')" aria-label="Toggle Dark Mode">🌓</div>
    <script>
        function toggleMenu() {{ document.querySelector('.nav-links').classList.remove('active'); }}
        if({str(top_bar_enabled).lower()}) {{ document.querySelector('#main-navbar').style.top = '40px'; }}
    </script>
    """

def build_page(title, content, extra_js=""):
    gsc_meta = f'<meta name="google-site-verification" content="{gsc_tag}">' if gsc_tag else ""
    og_meta = f'<meta property="og:title" content="{title} | {biz_name}"><meta property="og:description" content="{seo_d}"><meta property="og:image" content="{og_image or logo_url}"><meta name="twitter:card" content="summary_large_image">'
    pwa_tags = f'<link rel="manifest" href="manifest.json"><meta name="theme-color" content="#000000"><link rel="apple-touch-icon" href="{pwa_icon}">'
    sw_script = "<script>if ('serviceWorker' in navigator) { navigator.serviceWorker.register('service-worker.js'); }</script>"
    ga_script_opt = f"<script async src='https://www.googletagmanager.com/gtag/js?id={ga_tag}'></script><script>window.dataLayer = window.dataLayer ||[]; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{ga_tag}');</script>" if ga_tag else ""

    h_f = h_font.replace(' ', '+')
    b_f = b_font.replace(' ', '+')

    # EXPLICITLY EXTRACT COOKIE AND POPUP LOGIC TO AVOID F-STRING SLASH ERRORS
    cookie_html = f"""<div id="cookie-banner" class="glass" style="position:fixed; bottom:0; left:0; width:100%; padding:1.5rem; transform:translateY(100%); transition:0.5s; z-index:9000; display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border);"><div>{cookie_txt}</div><button class="btn btn-primary" onclick="acceptCookies()">Accept</button></div>""" if show_cookie else ""
    
    popup_html = f"""<div id="lead-popup" class="glass" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); padding:3rem; text-align:center; border-radius:24px; z-index:3000; box-shadow:0 30px 60px rgba(0,0,0,0.5); width:90%; max-width:450px;"><div style="position:absolute; top:15px; right:20px; cursor:pointer; font-size:1.5rem; opacity:0.5;" onclick="document.getElementById('lead-popup').style.display='none'">✕</div><h3 style="margin-bottom:1rem; color:var(--txt-h);">{popup_title}</h3><p style="margin-bottom:2rem; color:var(--txt);">{popup_text}</p><a href="https://wa.me/{wa_num}?text=I want the offer" class="btn btn-accent" target="_blank" style="width:100%;">{popup_cta}</a></div>""" if popup_enabled else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {biz_name}</title>
    <meta name="description" content="{seo_d}">
    {gsc_meta}{og_meta}{pwa_tags}{gen_schema()}
    
    <link rel="preload" as="image" href="{hero_img_1}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family={h_f}:wght@400;600;800;900&family={b_f}:wght@300;400;500;700&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={h_f}:wght@400;600;800;900&family={b_f}:wght@300;400;500;700&display=swap" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={h_f}:wght@400;600;800;900&family={b_f}:wght@300;400;500;700&display=swap"></noscript>
    
    <style>{generate_modern_css()}</style>
    
    {ga_script_opt}
    {gen_2050_scripts()}
</head>
<body>
    <main>
        {gen_nav()}
        {content}
        {gen_footer()}
        
        <!-- WIDGETS -->
        <div id="cart-overlay" onclick="toggleCart()" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1999;"></div>
        <div id="cart-modal" class="glass" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); padding:2rem; z-index:2000; width:90%; max-width:400px; border-radius:24px;">
            <h3 style="color:var(--p); margin-bottom:1rem;">Your Cart</h3><hr style="margin:10px 0; opacity:0.2;">
            <div id="cart-items" style="max-height:200px; overflow-y:auto; margin:1rem 0;"></div>
            <div style="font-weight:bold; font-size:1.2rem; margin-bottom:1rem; text-align:right; color:var(--txt);">Total: <span id="cart-total">0.00</span></div>
            <div class="local-vault" style="background:rgba(128,128,128,0.05); padding:1rem; border-radius:12px; margin-bottom:1rem;">
                <h4 style="font-size:0.9rem; color:var(--txt-h);">🔒 Fast Checkout Vault</h4>
                <input type="text" id="vault-name" placeholder="Full Name" style="width:100%; padding:10px; margin-top:5px; border-radius:8px; border:1px solid var(--border); background:var(--bg); color:var(--txt);">
                <input type="text" id="vault-address" placeholder="Delivery Address" style="width:100%; padding:10px; margin-top:5px; border-radius:8px; border:1px solid var(--border); background:var(--bg); color:var(--txt);">
            </div>
            <button onclick="checkoutWhatsApp()" class="btn btn-accent" style="width:100%;">Checkout via WhatsApp</button>
        </div>

        {gen_wa_widget()}
        <div class="float-btn" id="cart-float" onclick="toggleCart()" style="display:none;">🛒 <span id="cart-count" style="position:absolute; top:-5px; right:-5px; background:var(--s); color:white; border-radius:50%; width:20px; height:20px; font-size:12px; display:flex; align-items:center; justify-content:center;">0</span></div>
        
        {gen_lang_script()}
        {cookie_html}
        {popup_html}
        {extra_js}
    </main>
    {gen_csv_parser()}
    {gen_js_engine()}
    <script defer>window.addEventListener('scroll', () => {{ document.querySelectorAll('.reveal').forEach(r => {{ if(r.getBoundingClientRect().top < window.innerHeight - 80) r.classList.add('active'); }}); }}); window.dispatchEvent(new Event('scroll'));</script>
    {sw_script}
</body>
</html>"""

# --- 9. SUB-PAGE GENERATORS ---
def gen_booking_content():
    if not show_booking: return ""
    return f'<section class="modern-hero" style="min-height:30vh; display:flex; align-items:center; justify-content:center; text-align:center;"><div class="container modern-hero-text"><h1>{booking_title}</h1><p>{booking_desc}</p></div></section><section style="background:var(--bg);"><div class="container" style="text-align:center;"><div style="background:var(--card); border:1px solid var(--border); border-radius:24px; overflow:hidden; box-shadow:var(--shadow); width:100%;">{booking_embed}</div></div></section>'

def gen_blog_index_html():
    if not show_blog: return ""
    return f"""
    <section class="modern-hero" style="min-height:40vh; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img_1}'); background-size: cover; background-position:center; text-align:center; justify-content:center;">
        <div class="container modern-hero-text"><h1>{blog_hero_title}</h1><p>{blog_hero_sub}</p></div>
    </section>
    <section style="background:var(--bg);"><div class="container"><div id="blog-grid" class="grid-3">Loading Posts...</div></div></section>
    <script defer>
    async function loadBlog() {{ 
        if (!'{blog_sheet_url}') return; 
        try {{ 
            const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/); 
            const box = document.getElementById('blog-grid'); box.innerHTML = ''; 
            for(let i=1; i<lines.length; i++) {{ 
                const r = parseCSVLine(lines[i]); 
                if(r.length > 4) {{ 
                    box.innerHTML += `<article class="card reveal" style="padding:0;"><div style="width:100%; height:220px; overflow:hidden;"><img src="${{r[5]}}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.5s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" alt="${{r[1]}}"></div><div class="card-body"><span style="display:inline-block; padding:0.4rem 1rem; background:var(--border); color:var(--txt-h); border-radius:50px; font-size:0.75rem; font-weight:800; text-transform:uppercase; margin-bottom:1rem; width:fit-content;">${{r[3]}}</span><h3 style="margin-bottom:1rem; font-size:1.4rem;">${{r[1]}}</h3><p style="flex-grow:1; margin-bottom: 2rem; opacity:0.8; line-height:1.6; font-size:0.95rem;">${{r[4]}}</p><a href="post.html?id=${{r[0]}}" class="btn btn-primary" style="width:100%; margin-top:auto;">Read Article</a></div></article>`; 
                }} 
            }} 
        }} catch(e) {{ console.log(e); }} 
    }} 
    window.addEventListener('load', loadBlog);
    </script>
    """

def gen_product_page_content(is_demo=False):
    demo_flag = "true" if is_demo else "false"
    ar_script = '<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>' if enable_ar else ''
    return f"""
    {ar_script}
    <section style="padding-top:140px; background: var(--bg); min-height: 100vh;">
        <div class="container">
            <a href="index.html#inventory" class="btn glass" style="color:var(--txt-h); padding:0.5rem 1rem; margin-bottom:2rem; font-size:0.8rem;">← BACK TO STORE</a>
            <div id="product-detail-target">Loading Specifications...</div>
        </div>
    </section>
    <script defer>
    {demo_flag}
    function changeImg(src) {{ document.getElementById('main-img').src = src; }}
    async function loadProduct() {{
        const params = new URLSearchParams(window.location.search); 
        let targetName = params.get('item'); 
        if(isDemo && !targetName) targetName = "Demo Product";
        try {{
            const res = await fetch('{sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            for(let i=1; i<lines.length; i++) {{
                const clean = parseCSVLine(lines[i]);
                if(clean[0] === targetName || (isDemo && i===1)) {{
                    let allImgs = clean[3] ? clean[3].split('|') : ['{custom_feat}'];
                    let thumbHtml = '';
                    allImgs.forEach(img => {{ thumbHtml += `<img src="${{img.trim()}}" class="thumb" onclick="changeImg('${{img.trim()}}')">`; }});
                    
                    let mainMedia = `<img src="${{allImgs[0]}}" id="main-img" class="gallery-main" alt="${{clean[0]}}">`;
                    if({str(enable_ar).lower()} && clean.length > 5 && clean[5].includes('.glb')) {{
                        mainMedia = `<model-viewer src="${{clean[5]}}" ar ar-modes="webxr scene-viewer quick-look" camera-controls tone-mapping="neutral" shadow-intensity="1" auto-rotate style="width:100%; height:500px; border-radius:24px;"></model-viewer>`;
                    }}

                    const u = encodeURIComponent(window.location.href); const t = encodeURIComponent(clean[0]);
                    
                    document.getElementById('product-detail-target').innerHTML = `
                        <div class="detail-view">
                            <div class="product-media-column">
                                ${{mainMedia}}
                                <div class="gallery-thumbs">${{thumbHtml}}</div>
                            </div>
                            <div class="product-info-column">
                                <h1>${{clean[0]}}</h1>
                                <div class="product-price-tag">${{clean[1]}}</div>
                                <div class="product-specs-container">${{parseMarkdown(clean[2])}}</div>
                                <div style="margin-top:3rem; position: sticky; bottom: 20px; z-index: 10;">
                                    <button onclick="addToCart('${{clean[0]}}', '${{clean[1]}}')" class="btn btn-accent" style="width: 100%; padding: 1.2rem; font-size:1.1rem;">ADD TO CART</button>
                                </div>
                            </div>
                        </div>`;
                    document.title = clean[0] + " | {biz_name}";
                    break;
                }}
            }}
        }} catch(e) {{ console.error("Product Load Error:", e); }}
    }}
    window.addEventListener('load', loadProduct);
    </script>
    """

def gen_inner_header(title):
    return f"""<div class="modern-hero" style="min-height: 40vh; display:flex; align-items:center; justify-content:center; text-align:center; padding-top: 150px; padding-bottom: 50px;"><div class="container"><h1 style="color:#ffffff !important; margin:0; text-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: clamp(3rem, 6vw, 4.5rem);">{title}</h1></div></div>"""

# --- 10. PRE-GENERATE HTML & PREVIEW ASSEMBLY ---
home_content = ""
if show_hero: home_content += gen_hero()
if show_stats: home_content += f'<div class="stats-ribbon-container container reveal"><div class="stats-ribbon"><div class="stat-block"><h3>{stat_1}</h3><p>{label_1}</p></div><div class="stat-divider"></div><div class="stat-block"><h3>{stat_2}</h3><p>{label_2}</p></div><div class="stat-divider"></div><div class="stat-block"><h3>{stat_3}</h3><p>{label_3}</p></div></div></div>'
if show_features: home_content += gen_features()
if show_pricing: home_content += gen_pricing_table()
if show_inventory: home_content += gen_inventory()
if show_gallery: home_content += f'<section id="about" style="background:var(--bg); border-top:1px solid var(--border);"><div class="container about-grid"><div class="reveal"><img src="{about_img}" style="width:100%; border-radius:32px; box-shadow:var(--shadow);" alt="About Us"></div><div class="reveal"><h2 style="font-size:2.5rem; margin-bottom:1.5rem; color:var(--txt-h);">{about_h_in}</h2><div style="margin-bottom:2rem; font-size:1.1rem; opacity:0.9; line-height:1.8; color:var(--txt);">{format_text(about_short_in)}</div><a href="about.html" class="btn btn-primary">Read Our Story</a></div></div></section>'
if show_testimonials: 
    t_cards = "".join([f'<div class="card reveal" style="padding: 2rem;"><p style="font-size: 1.1rem; font-style: italic; line-height: 1.7; opacity: 0.9; flex-grow: 1; margin-bottom: 2rem; color:var(--txt); text-align:left;">"{x.split("|")[1].strip()}"</p><div style="display: flex; align-items: center; gap: 15px; border-top: 1px solid var(--border); padding-top: 1.5rem;"><div style="width: 45px; height: 45px; min-width: 45px; border-radius: 50%; background: var(--p); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; text-transform: uppercase;">{x.split("|")[0].strip()[0]}</div><div style="text-align:left;"><b style="color: var(--txt-h); font-size: 1.1rem; display: block;">{x.split("|")[0].strip()}</b><span style="display: block; font-size: 0.8rem; opacity: 0.6; margin-top: 2px; color:var(--txt);">Verified Client</span></div></div></div>' for x in testi_data.split('\n') if "|" in x and len(x.split("|")[0].strip()) > 0])
    home_content += f'<section id="testimonials" style="background:var(--bg); border-top:1px solid var(--border);"><div class="container"><div class="section-head reveal" style="display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom:4rem;"><h2 style="margin-bottom:0.5rem; font-size:2.5rem;">Client Stories</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem 0; border-radius:2px;"></div></div><div class="grid-3">{t_cards}</div></div></section>'
if show_faq: 
    items = "".join([f"<details class='reveal' style='background:var(--card); border:1px solid var(--border); padding:1.5rem; border-radius:12px; margin-bottom:1rem; color:var(--txt);'><summary style='font-weight:800; font-size:1.1rem; cursor:pointer; color:var(--txt-h);'>{l.split('?')[0]}?</summary><p style='margin-top:1rem; opacity:0.9; line-height:1.6;'>{l.split('?')[1]}</p></details>" for l in faq_data.split('\n') if "?" in l and len(l.split('?'))>1])
    home_content += f'<section id="faq" style="background:var(--bg);"><div class="container" style="max-width:800px;"><div class="section-head reveal" style="display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom:4rem;"><h2 style="margin-bottom:0.5rem; font-size:2.5rem;">FAQ</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem 0; border-radius:2px;"></div></div>{items}</div></section>'
if show_cta: 
    home_content += f'<section style="background:var(--s); color:white; text-align:center;"><div class="container reveal"><h2 style="color:var(--btn-txt) !important; font-size:clamp(2.5rem, 5vw, 3.5rem); margin-bottom:1rem;">Ready to Launch?</h2><p style="margin-bottom:2rem; font-size:1.3rem; opacity:0.9; color:var(--btn-txt) !important;">Join the future of web architecture.</p><a href="contact.html" class="btn" style="background:var(--bg); color:var(--txt-h) !important;">Get Started</a></div></section>'

contact_content = f"""
{gen_inner_header("Contact Us")}
<section style="background:var(--bg);">
    <div class="container">
        <div class="contact-grid">
            <div class="card" style="padding: clamp(1.5rem, 5vw, 3rem);">
                <h3 style="margin-bottom:1.5rem; font-size:2rem;">Get In Touch</h3>
                <div style="margin-bottom:1.5rem;"><strong style="font-size:0.9rem; text-transform:uppercase;">Headquarters</strong><p style="font-size:1.1rem; opacity:0.9; margin-top:0.5rem;">{biz_addr}</p></div>
                <div style="margin-bottom:1.5rem;"><strong style="font-size:0.9rem; text-transform:uppercase;">Direct Line</strong><p style="font-size:1.1rem; margin-top:0.5rem;"><a href="tel:{biz_phone}" style="color:var(--s); font-weight:bold;">{biz_phone}</a></p></div>
                <div style="margin-bottom:2.5rem;"><strong style="font-size:0.9rem; text-transform:uppercase;">Email</strong><p style="font-size:1.1rem; margin-top:0.5rem;">{biz_email}</p></div>
                <a href="https://wa.me/{wa_num}" target="_blank" class="btn btn-accent" style="width:100%;">WhatsApp Us Instantly</a>
            </div>
            <div class="card" style="padding: clamp(1.5rem, 5vw, 3rem);">
                <h3 style="margin-bottom:1.5rem; font-size:2rem;">Send a Message</h3>
                <form action="https://formsubmit.co/{biz_email}" method="POST" style="display:flex; flex-direction:column; gap:1.5rem;">
                    <div><label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; margin-bottom:0.5rem; display:block;">Full Name</label><input type="text" name="name" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; outline:none;"></div>
                    <div><label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; margin-bottom:0.5rem; display:block;">Email Address</label><input type="email" name="email" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; outline:none;"></div>
                    <div><label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; margin-bottom:0.5rem; display:block;">Your Message</label><textarea name="msg" rows="5" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; outline:none; resize:vertical;"></textarea></div>
                    <button class="btn btn-primary" type="submit" style="height:4rem; font-size:1.1rem; margin-top:1rem; border:none; cursor:pointer;">Send Secure Message</button>
                </form>
            </div>
        </div>
        <div style="border-radius:var(--radius); overflow:hidden; border:var(--border); margin-top:4rem; box-shadow:var(--shadow); height: 450px; position: relative;">
            {map_iframe.replace('<iframe ', '<iframe style="width:100% !important; height:100% !important; position:absolute; top:0; left:0; border:none;" ')}
        </div>
    </div>
</section>
"""

# HTML STRING ROUTING
html_to_render = ""
st.divider()
st.subheader("🚀 2050 Launchpad")

col_nav1, col_nav2 = st.columns([3, 1])
with col_nav1:
    preview_mode = st.radio("Preview Page:", ["Home", "About", "Contact", "Blog Index", "Blog Post (Demo)", "Privacy", "Terms", "Product Detail (Demo)", "Booking Page"], horizontal=True)
with col_nav2:
    device_mode = st.radio("Device View:", ["💻 Desktop", "📱 Mobile Phone"], horizontal=True)


if preview_mode == "Home": html_to_render = build_page("Home", home_content)
elif preview_mode == "About": html_to_render = build_page("About", f"{gen_inner_header('About')}<section style='background:var(--bg)'><div class='container'>{format_text(about_long)}</div></section>")
elif preview_mode == "Contact": html_to_render = build_page("Contact", contact_content)
elif preview_mode == "Privacy": html_to_render = build_page("Privacy", f"{gen_inner_header('Privacy Policy')}<section style='background:var(--bg)'><div class='container'>{format_text(priv_txt)}</div></section>")
elif preview_mode == "Terms": html_to_render = build_page("Terms", f"{gen_inner_header('Terms of Service')}<section style='background:var(--bg)'><div class='container'>{format_text(term_txt)}</div></section>")
elif preview_mode == "Blog Index": html_to_render = build_page("Blog", gen_blog_index_html())
elif preview_mode == "Blog Post (Demo)": html_to_render = build_page("Article", gen_blog_post_html())
elif preview_mode == "Product Detail (Demo)":
    st.info("ℹ️ Demo Mode Active: Showing the first available product from your CSV.")
    html_to_render = build_page("Product", gen_product_page_content(is_demo=True))
elif preview_mode == "Booking Page":
    html_to_render = build_page("Book Now", gen_booking_content())

# --- 11. DISPLAY TO SCREEN ---
c1, c2 = st.columns([3, 1])
with c1:
    if device_mode == "📱 Mobile Phone":
        st.markdown("<div style='text-align: center; color: #888; margin-bottom:10px;'><i>📱 iPhone 14 Pro Simulation</i></div>", unsafe_allow_html=True)
        left_spacer, phone_screen, right_spacer = st.columns([1.2, 1.5, 1.2])
        with phone_screen:
            st.markdown("<style>.phone-bezel { border: 14px solid #1a1a1a; border-radius: 40px; padding: 0; background: #000; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); overflow: hidden; margin: 0 auto; }</style><div class='phone-bezel'>", unsafe_allow_html=True)
            st.components.v1.html(html_to_render, height=750, scrolling=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.components.v1.html(html_to_render, height=750, scrolling=True)

with c2:
    st.success("System Operational.")
    
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", build_page("Home", home_content))
        zf.writestr("about.html", build_page("About", f"{gen_inner_header('About')}<section style='background:var(--bg)'><div class='container'>{format_text(about_long)}</div></section>"))
        zf.writestr("contact.html", build_page("Contact", contact_content))
        zf.writestr("privacy.html", build_page("Privacy", f"{gen_inner_header('Privacy Policy')}<section style='background:var(--bg)'><div class='container'>{format_text(priv_txt)}</div></section>"))
        zf.writestr("terms.html", build_page("Terms", f"{gen_inner_header('Terms of Service')}<section style='background:var(--bg)'><div class='container'>{format_text(term_txt)}</div></section>"))
        if show_booking: zf.writestr("booking.html", build_page("Book Now", gen_booking_content()))
        if show_inventory: zf.writestr("product.html", build_page("Product Details", gen_product_page_content(is_demo=False)))
        if show_blog: 
            zf.writestr("blog.html", build_page("Blog", gen_blog_index_html()))
            zf.writestr("post.html", build_page("Article", gen_blog_post_html()))
        
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
