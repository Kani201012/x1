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
init_state('about_h', "Control Your Empire from a Spreadsheet")
init_state('about_short', "No WordPress dashboard. No plugins to update. Just open your private Google Sheet, change a text, and watch your site update globally in seconds.")
init_state('feat_data', "bolt | The Performance Pillar | **0.1s High-Velocity Loading**. While traditional sites take 3–5s, Titan loads instantly.\nwallet | The Economic Pillar | **$0 Monthly Fees**. We eliminated hosting subscriptions.\ntable | The Functional Pillar | **Google Sheets CMS**. Update prices and photos directly from a simple spreadsheet.\nshield | The Authority Pillar | **Unhackable Security**. Zero-DB Architecture removes the hacker's primary entry point.\nlayers | The Reliability Pillar | **Global Edge Deployment**. Distributed across 100+ servers worldwide.\nstar | The Conversion Pillar | **One-Tap WhatsApp**. Direct-to-Chat technology.")

# HARDCODED THEME REGISTRY (Replaces the missing titan_themes.py module)
THEME_REGISTRY = {
    "1. Stripe Cloud (Modern SaaS)": {"bg": "#ffffff", "card": "#ffffff", "glass": "rgba(255, 255, 255, 0.9)", "border": "rgba(0,0,0,0.05)", "p": "#6366f1"},
    "2. Midnight Cyberpunk": {"bg": "#050505", "card": "#111111", "glass": "rgba(0, 0, 0, 0.8)", "border": "rgba(0, 255, 157, 0.2)", "p": "#00ff9d"},
    "3. Luxury Gold": {"bg": "#1c1c1c", "card": "#2a2a2a", "glass": "rgba(30, 30, 30, 0.9)", "border": "rgba(212, 175, 55, 0.3)", "p": "#d4af37"},
    "4. Glassmorphism (Blur)": {"bg": "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)", "card": "rgba(255, 255, 255, 0.6)", "glass": "rgba(255, 255, 255, 0.5)", "border": "rgba(255, 255, 255, 0.4)", "p": "#3b82f6"},
    "5. Forest Eco": {"bg": "#f0fdf4", "card": "#ffffff", "glass": "rgba(255, 255, 255, 0.9)", "border": "rgba(16, 185, 129, 0.2)", "p": "#10b981"},
    "6. Ocean Breeze": {"bg": "#f0f9ff", "card": "#ffffff", "glass": "rgba(255, 255, 255, 0.9)", "border": "rgba(2, 132, 199, 0.2)", "p": "#0284c7"}
}

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Titan Architect | 2050 Apex Edition", 
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
    st.caption("v50.0 | Edge-Dynamic Architecture")
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
        with c1:
            hero_layout = st.selectbox("Hero Alignment", ["Center", "Left"])
        with c2:
            anim_type = st.selectbox("Animation Style", ["Fade Up", "Zoom In", "Slide Right", "None"])
            
        c3, c4 = st.columns(2)
        with c3:
            h_font = st.selectbox("Headings Font", ["Space Grotesk", "Montserrat", "Playfair Display", "Outfit", "Clash Display"])
        with c4:
            b_font = st.selectbox("Body Font", ["Inter", "Plus Jakarta Sans", "Satoshi", "Roboto"])
            
        overlay_opacity = st.slider("Hero Image Darkness", 0.1, 0.9, 0.5, help="Increases text readability over busy background images.")

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
        show_inventory = st.checkbox("Store/Inventory", value=True)
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

tabs = st.tabs(["1. Identity & PWA", "2. Content Blocks", "3. Marketing Tools", "4. Pricing", "5. Store", "6. Booking", "7. Blog", "8. Legal", "9. Web3 / IPFS"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Business Name", "StopWebRent.com")
        hero_badge_txt = st.text_input("Hero Mini-Badge", "🚀 Next-Generation Architecture")
        biz_tagline = st.text_input("Tagline", "Stop Renting. Start Owning.")
        biz_phone = st.text_input("Phone", "966572562151")
        biz_email = st.text_input("Email", "hello@kaydiemscriptlab.com")
    with c2:
        prod_url = st.text_input("Website URL", "https://www.stopwebrent.com")
        biz_addr = st.text_area("Address", "Kaydiem Script Lab\nKolkata, India", height=100)
        map_iframe = st.text_area("Google Map Embed", placeholder='<iframe src="..."></iframe>', height=100)
        seo_d = st.text_area("Meta Description", "Stop paying monthly fees for web hosting.", height=100)
        logo_url = st.text_input("Logo URL (PNG/SVG)")

    st.subheader("📱 Progressive Web App (PWA)")
    pwa_short = st.text_input("App Short Name", biz_name[:12])
    pwa_desc = st.text_input("App Description", "Official App")
    pwa_icon = st.text_input("App Icon (512x512 PNG)", logo_url)
    
    st.subheader("🌍 Multi-Language")
    lang_sheet = st.text_input("Translation Sheet CSV URL")
        
    st.subheader("Social Links")
    sc1, sc2, sc3 = st.columns(3)
    fb_link = sc1.text_input("Facebook URL")
    ig_link = sc2.text_input("Instagram URL")
    x_link = sc3.text_input("X (Twitter) URL")
    sc4, sc5, sc6 = st.columns(3)
    li_link = sc4.text_input("LinkedIn URL")
    yt_link = sc5.text_input("YouTube URL")
    wa_num = sc6.text_input("WhatsApp Number (No +)", "966572562151")

with tabs[1]:
    st.subheader("Hero Carousel")
    hero_h = st.text_input("Hero Headline", st.session_state.hero_h)
    hero_sub = st.text_input("Hero Subtext", st.session_state.hero_sub)
    hero_video_id = st.text_input("YouTube Video ID (Background Override)", placeholder="e.g. dQw4w9WgXcQ")
    
    hc1, hc2, hc3 = st.columns(3)
    hero_img_1 = hc1.text_input("Slide 1", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600")
    hero_img_2 = hc2.text_input("Slide 2", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1600")
    hero_img_3 = hc3.text_input("Slide 3", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1600")
    
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
    about_h_in = st.text_input("About Title", st.session_state.about_h)
    about_img = st.text_input("About Image", "https://images.unsplash.com/photo-1543286386-713df548e9cc?q=80&w=1600")
    about_short_in = st.text_area("Short Summary", st.session_state.about_short, height=100)
    about_long = st.text_area("Full Content", "**The Trap**\nMost business owners...", height=200)

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
    current_theme = THEME_REGISTRY.get(theme_mode, THEME_REGISTRY["1. Stripe Cloud (Modern SaaS)"])
    return json.dumps({
        "name": biz_name, 
        "short_name": pwa_short, 
        "start_url": "./index.html",
        "display": "standalone", 
        "background_color": current_theme['bg'] if not current_theme['bg'].startswith('linear') else '#ffffff', 
        "theme_color": current_theme['p'],
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

def gen_nav():
    logo_display = f'<img src="{logo_url}" height="40" width="auto" alt="{biz_name} Logo" loading="eager">' if logo_url else f'<span style="font-weight:900; font-size:1.5rem; color:var(--p)">{biz_name}</span>'
    blog_link = '<a href="blog.html" onclick="toggleMenu()">Blog</a>' if show_blog else ''
    book_link = '<a href="booking.html" onclick="toggleMenu()">Book Now</a>' if show_booking else ''
    lang_btn = f'<a href="#" onclick="openLangModal()" aria-label="Switch Language">🌐 ES</a>' if lang_sheet else ''
    
    return f"""
    {f'<div id="top-bar"><a href="{top_bar_link}">{top_bar_text}</a></div>' if top_bar_enabled else ''}
    <nav id="main-navbar">
        <div class="container nav-flex">
            <a href="index.html" aria-label="Home" style="text-decoration:none;">{logo_display}</a>
            <div class="mobile-menu" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div>
            <div class="nav-links">
                <a href="index.html" onclick="toggleMenu()">Home</a>
                {'<a href="index.html#features" onclick="toggleMenu()">Features</a>' if show_features else ''}
                {'<a href="index.html#pricing" onclick="toggleMenu()">Savings</a>' if show_pricing else ''}
                {'<a href="index.html#inventory" onclick="toggleMenu()">Store</a>' if show_inventory else ''}
                {blog_link}
                {book_link}
                {lang_btn}
                <a href="contact.html" onclick="toggleMenu()">Contact</a>
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

def gen_hero():
    bg_media = f"""
    <div class="carousel-slide active" style="background-image: url('{hero_img_1}')" fetchpriority="high"></div>
    <div class="carousel-slide" style="background-image: url('{hero_img_2}')" loading="lazy"></div>
    <div class="carousel-slide" style="background-image: url('{hero_img_3}')" loading="lazy"></div>
    <script defer>
        let slides = document.querySelectorAll('.carousel-slide'); let currentSlide = 0; 
        setInterval(() => {{ slides[currentSlide].classList.remove('active'); currentSlide = (currentSlide + 1) % slides.length; slides[currentSlide].classList.add('active'); }}, 4000);
    </script>
    """
    
    if hero_video_id: 
        match = re.search(r'(?:v=|/v/|youtu\.be/|/embed/|/shorts/|^)([a-zA-Z0-9_-]{11})', hero_video_id.strip())
        clean_id = match.group(1) if match else hero_video_id.strip()
        bg_media = f'<iframe src="https://www.youtube.com/embed/{clean_id}?autoplay=1&mute=1&loop=1&playlist={clean_id}&controls=0&showinfo=0&rel=0" class="hero-video" style="width:100%; height:100%; object-fit:cover; pointer-events:none;" frameborder="0" allow="autoplay; encrypted-media"></iframe>'
    
    badge_html = f'<div class="hero-badge">{hero_badge_txt}</div>' if hero_badge_txt.strip() else ''

    return f"""
    <section class="modern-hero">
        <div class="modern-hero-bg"></div>
        <div class="container modern-hero-grid">
            <div class="modern-hero-text reveal active">
                {badge_html}
                <h1 id="hero-title">{hero_h}</h1>
                <p id="hero-sub">{hero_sub}</p>
                <div class="hero-btn-group">
                    <a href="#inventory" class="btn btn-accent">Explore Now</a>
                    <a href="contact.html" class="btn btn-outline-light">Contact Us</a>
                </div>
            </div>
            <div class="modern-hero-visual reveal active" style="transition-delay: 0.2s;">
                <div class="visual-frame">
                    {bg_media}
                </div>
            </div>
        </div>
    </section>
    """

def gen_features():
    cards = ""
    for line in feat_data_input.split('\n'):
        if "|" in line:
            p = line.split('|')
            if len(p) >= 3:
                raw_text = p[2].strip()
                styled_text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:var(--txt); font-weight:800; font-size:1.05rem;">\1</strong>', raw_text)
                
                cards += f"""
                <div class="card reveal" style="padding:0;">
                    <div class="card-content" style="text-align:left; padding: 2rem;">
                        <div style="color:var(--s); margin-bottom:1.5rem; background:rgba(0,0,0,0.04); width:50px; height:50px; display:flex; align-items:center; justify-content:center; border-radius:12px;">
                            {get_simple_icon(p[0])}
                        </div>
                        <h3 style="font-size:1.3rem; margin-bottom:1rem; color:var(--txt-h);">{p[1].strip()}</h3>
                        <p style="opacity:0.8; line-height:1.7; font-size:1rem; color:var(--txt); margin:0; hyphens:none; -webkit-hyphens:none; text-align:left;">{styled_text}</p>
                    </div>
                </div>"""
                
    return f"""
    <section id="features" style="background:var(--bg)">
        <div class="container">
            <div class="section-head reveal" style="display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom:4rem;">
                <h2 style="margin-bottom:0.5rem; font-size:2.5rem;">{f_title}</h2>
                <div style="width:60px; height:4px; background:var(--s); margin:1rem 0; border-radius:2px;"></div>
            </div>
            <div class="grid-3">{cards}</div>
        </div>
    </section>
    """

def gen_stats():
    return f"""
    <div class="stats-ribbon-container container reveal" style="margin-top: 2rem;">
        <div class="stats-ribbon" style="display:flex; justify-content:space-around; background:var(--p); color:white; padding:2rem; border-radius:12px;">
            <div class="stat-block" style="text-align:center;">
                <h3 style="color:white; font-size:2rem; margin:0;">{stat_1}</h3><p style="margin:0; opacity:0.8;">{label_1}</p>
            </div>
            <div class="stat-block" style="text-align:center;">
                <h3 style="color:white; font-size:2rem; margin:0;">{stat_2}</h3><p style="margin:0; opacity:0.8;">{label_2}</p>
            </div>
            <div class="stat-block" style="text-align:center;">
                <h3 style="color:white; font-size:2rem; margin:0;">{stat_3}</h3><p style="margin:0; opacity:0.8;">{label_3}</p>
            </div>
        </div>
    </div>
    """

def gen_pricing_table():
    if not show_pricing: return ""
    return f"""
    <section id="pricing">
        <div class="container">
            <div class="section-head reveal" style="text-align:center; margin-bottom:2rem;"><h2 style="color:var(--txt-h);">Pricing</h2></div>
            <div class="pricing-wrapper reveal" style="overflow-x:auto;">
                <table class="pricing-table" style="width:100%; border-collapse:collapse; min-width:600px; border-radius:12px; overflow:hidden;">
                    <thead><tr><th style="padding:1.5rem; background:var(--p); color:white;">Expense Category</th><th style="padding:1.5rem; background:var(--s); color:white;">Titan</th><th style="padding:1.5rem; background:var(--p); color:white;">{wix_name}</th></tr></thead>
                    <tbody>
                        <tr><td style="padding:1.5rem; border-bottom:1px solid var(--border); background:var(--card);">Initial Setup Fee</td><td style="padding:1.5rem; border-bottom:1px solid var(--border); background:var(--card);"><strong>{titan_price}</strong></td><td style="padding:1.5rem; border-bottom:1px solid var(--border); background:var(--card);">$0</td></tr>
                        <tr><td style="padding:1.5rem; border-bottom:1px solid var(--border); background:var(--card);">Annual Costs</td><td style="padding:1.5rem; border-bottom:1px solid var(--border); background:var(--card);"><strong>{titan_mo}</strong></td><td style="padding:1.5rem; border-bottom:1px solid var(--border); background:var(--card);">{wix_mo}</td></tr>
                        <tr><td style="padding:1.5rem; background:var(--card);"><strong>5-Year Savings</strong></td><td style="padding:1.5rem; background:var(--card); color:var(--s); font-size:1.3rem;">You Save {save_val}</td><td style="padding:1.5rem; background:var(--card);">$0</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
    """

def gen_csv_parser():
    return """
    <script defer>
    function parseCSVLine(str) { 
        const res = []; let cur = ''; let inQuote = false; 
        for (let i = 0; i < str.length; i++) { 
            const c = str[i]; 
            if (c === '"') { if (inQuote && str[i+1] === '"') { cur += '"'; i++; } else { inQuote = !inQuote; } } 
            else if (c === ',' && !inQuote) { res.push(cur.trim()); cur = ''; } 
            else { cur += c; } 
        } 
        res.push(cur.trim()); return res; 
    } 
    
    function parseMarkdown(text) { 
        if (!text) return '';
        let clean = text.split('\\\\n').join('<br>').split('\\n').join('<br>');
        let parts = clean.split('**');
        for (let i = 1; i < parts.length; i += 2) {
            parts[i] = '<strong>' + parts[i] + '</strong>';
        }
        let bolded = parts.join('');
        return bolded.split('<br>').map(line => {
            let t = line.trim();
            if (t.startsWith('* ')) { return '<li style="margin-left:20px; list-style-type:disc; margin-bottom:8px;">' + t.substring(2) + '</li>'; }
            return t ? '<p style="margin-bottom:15px;">' + t + '</p>' : '';
        }).join('');
    }
    </script>
    """

def gen_cart_system():
    if not wa_num: return ""
    clean_wa = wa_num.replace("+", "").replace(" ", "").replace("-", "")
    return f"""
    <div id="cart-float" onclick="toggleCart()" style="display:none; position:fixed; bottom:30px; right:90px; background:var(--p); color:white; width:50px; height:50px; border-radius:50%; align-items:center; justify-content:center; box-shadow:0 4px 15px rgba(0,0,0,0.2); z-index:990; cursor:pointer;" aria-label="Cart">🛒 <span id="cart-count" style="position:absolute; top:-5px; right:-5px; background:var(--s); color:white; border-radius:50%; width:20px; height:20px; font-size:12px; display:flex; align-items:center; justify-content:center;">0</span></div>
    <div id="cart-overlay" onclick="toggleCart()" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1999;"></div>
    <div id="cart-modal" class="glass" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); padding:2rem; z-index:2000; width:90%; max-width:400px; border-radius:12px;">
        <h3 style="color:var(--txt-h);">Your Cart</h3><hr style="margin:10px 0; opacity:0.2; border:1px solid var(--border);">
        <div id="cart-items" style="max-height:200px; overflow-y:auto; margin:1rem 0;"></div>
        <div style="font-weight:bold; font-size:1.2rem; margin-bottom:1rem; text-align:right; color:var(--txt);">Total: <span id="cart-total">0.00</span></div>
        <div class="local-vault">
            <h4 style="font-size:0.9rem; color:var(--txt-h);">🔒 Fast Checkout Vault</h4>
            <input type="text" id="vault-name" placeholder="Full Name" style="width:100%; padding:10px; margin-bottom:10px; border-radius:8px; border:1px solid var(--border); background:var(--bg); color:var(--txt);">
            <input type="text" id="vault-address" placeholder="Delivery Address" style="width:100%; padding:10px; margin-bottom:10px; border-radius:8px; border:1px solid var(--border); background:var(--bg); color:var(--txt);">
        </div>
        <button onclick="checkoutWhatsApp()" class="btn btn-accent" style="width:100%; margin-top:1rem; border:none; padding:15px; border-radius:8px; font-weight:bold; cursor:pointer;">1-Click Checkout via WhatsApp</button>
    </div>
    <script defer>
    let cart = JSON.parse(localStorage.getItem('titanCart')) || [];
    window.addEventListener('load', () => {{
        document.getElementById('vault-name').value = localStorage.getItem('t_name') || ''; 
        document.getElementById('vault-address').value = localStorage.getItem('t_addr') || '';
        renderCart();
    }});
    
    function renderCart() {{
        const box = document.getElementById('cart-items'); if(!box) return; box.innerHTML = ''; let total = 0;
        cart.forEach((item, i) => {{ 
            total += parseFloat(item.price.replace(/[^0-9.]/g, '')) || 0; 
            box.innerHTML += `<div class="cart-item" style="display:flex; justify-content:space-between; margin-bottom:10px; color:var(--txt);"><span>${{item.name}}</span><span>${{item.price}} <b onclick="remItem(${{i}})" style="color:red;cursor:pointer;margin-left:10px;">×</b></span></div>`; 
        }});
        const cc = document.getElementById('cart-count');
        const cf = document.getElementById('cart-float');
        if(cc) cc.innerText = cart.length; 
        const ct = document.getElementById('cart-total');
        if(ct) ct.innerText = total.toFixed(2);
        if(cf) cf.style.display = cart.length > 0 ? 'flex' : 'none';
        localStorage.setItem('titanCart', JSON.stringify(cart));
    }}
    
    function addToCart(name, price) {{ cart.push({{name, price}}); renderCart(); alert(name + " added!"); }}
    function remItem(i) {{ cart.splice(i,1); renderCart(); }}
    function toggleCart() {{ const m = document.getElementById('cart-modal'); m.style.display = m.style.display === 'block' ? 'none' : 'block'; document.getElementById('cart-overlay').style.display = m.style.display; }}
    
    function checkoutWhatsApp() {{
        const n = document.getElementById('vault-name').value; const a = document.getElementById('vault-address').value;
        localStorage.setItem('t_name', n); localStorage.setItem('t_addr', a);
        let msg = "New Order:%0A"; let total = 0;
        cart.forEach(i => {{ msg += `- ${{i.name}} (${{i.price}})%0A`; total += parseFloat(i.price.replace(/[^0-9.]/g,'')) || 0; }});
        msg += `%0ATotal: ${{total.toFixed(2)}}%0A`; 
        if(n) msg += `%0ADeliver to: ${{n}}, ${{a}}`;
        msg += `%0A%0AUPI: {upi_id} | PayPal: {paypal_link}`;
        
        window.open(`https://wa.me/{clean_wa}?text=${{encodeURIComponent(msg)}}`, '_blank', 'noopener,noreferrer');
        cart = []; renderCart(); toggleCart();
    }}
    </script>
    """

def gen_wa_widget():
    if not wa_num: return ""
    clean_wa = wa_num.replace("+", "").replace(" ", "").replace("-", "")
    return f"""
    <a href="https://wa.me/{clean_wa}" target="_blank" rel="noopener noreferrer" id="wa-widget" aria-label="Chat on WhatsApp" style="position: fixed; bottom: 30px; right: 30px; background: #25D366; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 990; transition: transform 0.3s;">
        <svg viewBox="0 0 24 24" fill="white" width="24" height="24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91c0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23c-1.48 0-2.93-.39-4.19-1.15l-.3-.17l-3.12.82l.83-3.04l-.2-.32a8.188 8.188 0 0 1-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24m-3.53 3.16c-.13 0-.35.05-.54.26c-.19.2-.72.7-.72 1.72s.73 2.01.83 2.14c.1.13 1.44 2.19 3.48 3.07c.49.21.87.33 1.16.43c.49.16.94.13 1.29.08c.4-.06 1.21-.5 1.38-.98c.17-.48.17-.89.12-.98c-.05-.09-.18-.13-.37-.23c-.19-.1-.1.13-.1.13s-1.13-.56-1.32-.66c-.19-.1-.32-.15-.45.05c-.13.2-.51.65-.62.78c-.11.13-.23.15-.42.05c-.19-.1-.8-.3-1.53-.94c-.57-.5-1.02-1.12-1.21-1.45c-.11-.19-.01-.29.09-.38c.09-.08.19-.23.29-.34c.1-.11.13-.19.19-.32c.06-.13.03-.24-.01-.34c-.05-.1-.45-1.08-.62-1.48c-.16-.4-.36-.34-.51-.35c-.11-.01-.25-.01-.4-.01Z"/></path></svg>
    </a>
    """

def gen_lang_script():
    if not lang_sheet: return ""
    return f"""
    <div id="lang-overlay" onclick="closeLangModal()" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1999;"></div>
    <div id="lang-modal" class="glass" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); padding:2rem; z-index:2000; width:90%; max-width:400px; border-radius:12px;">
        <h3 style="margin-bottom:1.5rem; border-bottom:1px solid var(--border); padding-bottom:10px; color:var(--txt-h);">Select Language</h3>
        <div class="lang-grid" style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div onclick="switchLang('en', 0)" class="lang-opt" style="padding:10px; border:1px solid var(--border); border-radius:8px; cursor:pointer; text-align:center; color:var(--txt);">🇺🇸 English</div>
            <div onclick="switchLang('es', 1)" class="lang-opt" style="padding:10px; border:1px solid var(--border); border-radius:8px; cursor:pointer; text-align:center; color:var(--txt);">🇪🇸 Español</div>
        </div>
    </div>
    <script defer>
    function openLangModal() {{ document.getElementById('lang-modal').style.display='block'; document.getElementById('lang-overlay').style.display='block'; }} 
    function closeLangModal() {{ document.getElementById('lang-modal').style.display='none'; document.getElementById('lang-overlay').style.display='none'; }} 
    
    async function switchLang(langCode, colIndex) {{ 
        closeLangModal(); 
        localStorage.setItem('titan_lang', langCode);
        localStorage.setItem('titan_col', colIndex);
        if(langCode === 'en') {{ location.reload(); return; }} 
        if(!'{lang_sheet}') return;
        try {{ 
            const res = await fetch('{lang_sheet}'); 
            const txt = await res.text(); 
            const lines = txt.split(/\\r\\n|\\n/); 
            for(let i=1; i<lines.length; i++) {{ 
                const row = parseCSVLine(lines[i]); 
                if(row.length > colIndex) {{ 
                    const el = document.getElementById(row[0]); 
                    if(el && row[colIndex]) el.innerText = row[colIndex]; 
                }} 
            }} 
            document.documentElement.lang = langCode;
        }} catch(e) {{ console.log("Lang Error", e); }} 
    }}
    </script>
    """

def gen_popup():
    if not popup_enabled: return ""
    return f"""
    <div id="lead-popup" class="glass" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); padding:2rem; text-align:center; border-radius:12px; z-index:2000; box-shadow:0 25px 100px rgba(0,0,0,0.5); width:90%; max-width:450px;">
        <div class="close-popup" onclick="document.getElementById('lead-popup').style.display='none'" style="position:absolute; top:10px; right:15px; cursor:pointer; font-size:1.2rem; color:var(--txt);">✕</div>
        <h3 style="color:var(--txt-h); margin-bottom:1rem;">{popup_title}</h3><p style="color:var(--txt); margin-bottom:1.5rem;">{popup_text}</p>
        <a href="https://wa.me/{wa_num}?text=I want the offer" class="btn btn-accent" target="_blank" rel="noopener noreferrer" style="display:block; width:100%;">{popup_cta}</a>
    </div>
    <script defer>
    setTimeout(() => {{ 
        if(!localStorage.getItem('popupShown')) {{ document.getElementById('lead-popup').style.display = 'block'; localStorage.setItem('popupShown', 'true'); }} 
    }}, {popup_delay * 1000});
    </script>
    """

def gen_inventory_js(is_demo=False):
    demo_flag = "const isDemo = true;" if is_demo else "const isDemo = false;"
    return f"""
    {gen_csv_parser()}
    <script defer>
    {demo_flag}
    async function loadInv() {{
        if (!'{sheet_url}') return;
        try {{
            const res = await fetch('{sheet_url}'); 
            const txt = await res.text(); 
            const lines = txt.split(/\\r\\n|\\n/);
            const box = document.getElementById('inv-grid'); 
            if(!box) return; 
            box.innerHTML = '';
            for(let i=1; i<lines.length; i++) {{
                if(!lines[i].trim()) continue;
                const c = parseCSVLine(lines[i]);
                let allImgs = c[3] ? c[3].split('|') : []; 
                let mainImg = allImgs.length > 0 ? allImgs[0].trim() : '{custom_feat}';
                if(c.length > 1) {{
                    const pName = encodeURIComponent(c[0]);
                    box.innerHTML += `
                        <div class="card reveal" style="padding:0;">
                            <img src="${{mainImg}}" class="prod-img" style="width:100%; height:250px; object-fit:cover;" loading="lazy" alt="${{c[0]}}">
                            <div class="card-content" style="padding:1.5rem; flex-grow:1; display:flex; flex-direction:column;">
                                <h3 style="font-size:1.2rem; margin-bottom:0.5rem; color:var(--txt-h);">${{c[0]}}</h3>
                                <p style="font-weight:bold; color:var(--s); margin-bottom:10px; font-size:1.1rem;">${{c[1]}}</p>
                                <p class="card-desc" style="color:var(--txt); opacity:0.8; font-size:0.9rem; margin-bottom:1rem; flex-grow:1;">${{c[2]}}</p>
                                <div style="display:flex; gap:10px;">
                                    <a href="product.html?item=${{pName}}" class="btn btn-primary" style="flex:1; padding:0.6rem; text-align:center; font-size:0.8rem;">VIEW</a>
                                    <button onclick="addToCart('${{c[0]}}', '${{c[1]}}')" class="btn btn-accent" style="flex:1; padding:0.6rem; font-size:0.8rem;">ADD</button>
                                </div>
                            </div>
                        </div>`;
                }}
            }}
        }} catch(e) {{ console.log(e); }}
    }}
    if(document.getElementById('inv-grid')) window.addEventListener('load', loadInv);
    </script>
    """

def gen_inventory():
    if not show_inventory: return ""
    voice_btn = '<button id="voice-btn" onclick="startVoiceSearch()" aria-label="Voice Search" style="position:fixed; bottom:30px; right:150px; background:var(--card); border:1px solid var(--border); border-radius:50%; width:50px; height:50px; cursor:pointer; z-index:990;">🎤</button>' if enable_voice else ''
    return f'<section id="inventory" style="background:var(--bg);"><div class="container"><div class="section-head reveal" style="text-align:center; margin-bottom:3rem;"><h2 id="store-title" style="color:var(--txt-h);">Latest Collection</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem auto; border-radius:2px;"></div></div><div id="inv-grid" class="grid-3"><div>Loading...</div></div></div>{voice_btn}</section>{gen_inventory_js(is_demo=False)}'

def gen_about_section():
    if not show_gallery: return ""
    return f"""
    <section id="about" style="background:var(--card); border-top:1px solid var(--border); border-bottom:1px solid var(--border);">
        <div class="container">
            <div class="about-grid">
                <div class="about-visual reveal">
                    <img src="{about_img}" style="width:100%; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.1);" loading="lazy" alt="About Us">
                </div>
                <div class="about-text reveal">
                    <h2 id="about-title" style="color:var(--txt-h); margin-bottom:1.5rem;">{about_h_in}</h2>
                    <div class="about-lead" style="color:var(--txt); opacity:0.9; line-height:1.7;">{format_text(about_short_in)}</div>
                    <div style="margin-top:2rem;"><a href="about.html" class="btn btn-primary">Read Our Story</a></div>
                </div>
            </div>
        </div>
    </section>
    """
def gen_faq_section():
    if not show_faq: return ""
    items = "".join([f"<details class='reveal' style='background:var(--card); border:1px solid var(--border); padding:1rem; border-radius:8px; margin-bottom:1rem; color:var(--txt);'><summary style='font-weight:bold; cursor:pointer;'>{l.split('?')[0]}?</summary><p style='margin-top:1rem; opacity:0.9;'>{l.split('?')[1]}</p></details>" for l in faq_data.split('\n') if "?" in l])
    return f'<section id="faq"><div class="container" style="max-width:800px;"><div class="section-head reveal" style="text-align:center; margin-bottom:3rem;"><h2 id="faq-title" style="color:var(--txt-h);">Frequently Asked Questions</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem auto; border-radius:2px;"></div></div>{items}</div></section>'

def gen_footer():
    icons = ""
    if fb_link: icons += f'<a href="{fb_link}" target="_blank" rel="noopener noreferrer" style="display:inline-block; margin-right:15px; color:white;"><svg viewBox="0 0 24 24" width="24" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>'
    if ig_link: icons += f'<a href="{ig_link}" target="_blank" rel="noopener noreferrer" style="display:inline-block; margin-right:15px; color:white;"><svg viewBox="0 0 24 24" width="24" fill="currentColor"><path d="M16.98 0a6.9 6.9 0 0 1 5.08 1.98A6.94 6.94 0 0 1 24 7.02v9.96c0 2.08-.68 3.87-1.98 5.13A7.14 7.14 0 0 1 16.94 24H7.06a7.06 7.06 0 0 1-5.03-1.89A6.96 6.96 0 0 1 0 16.94V7.02C0 2.8 2.8 0 7.02 0h9.96zM7.17 2.1c-1.4 0-2.6.48-3.46 1.33c-.85.85-1.33 2.06-1.33 3.46v10.3c0 1.3.47 2.5 1.33 3.36c.86.85 2.06 1.33 3.46 1.33h9.66c1.4 0 2.6-.48 3.46-1.33c.85-.85 1.33-2.06 1.33-3.46V6.89c0-1.4-.47-2.6-1.33-3.46c-.86-.85-2.06-1.33-3.46-1.33H7.17zm11.97 3.33c.77 0 1.4.63 1.4 1.4c0 .77-.63 1.4-1.4 1.4c-.77 0-1.4-.63-1.4-1.4c0-.77.63-1.4 1.4-1.4zM12 5.76c3.39 0 6.14 2.75 6.14 6.14c0 3.39-2.75 6.14-6.14 6.14c-3.39 0-6.14-2.75-6.14-6.14c0-3.39 2.75-6.14 6.14-6.14zm0 2.1c-2.2 0-3.99 1.79-3.99 4.04c0 2.25 1.79 4.04 3.99 4.04c2.2 0 3.99-1.79 3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04c0-2.25-1.79-4.04-3.99-4.04z"/></svg></a>'
    if x_link: icons += f'<a href="{x_link}" target="_blank" rel="noopener noreferrer" style="display:inline-block; margin-right:15px; color:white;"><svg viewBox="0 0 24 24" width="24" fill="currentColor"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584l-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"></path></svg></a>'

    return f"""
    <footer style="background:var(--p); color:white; padding:4rem 0 2rem 0; margin-top:auto;">
        <div class="container">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:3rem; margin-bottom:3rem;">
                <div>
                    <h3 style="color:white; margin-bottom:1rem;">{biz_name}</h3>
                    <p style="opacity:0.8; margin-bottom:1rem;">{biz_addr}</p>
                    <p style="opacity:0.8; font-weight:bold;">{biz_phone}</p>
                    <div style="margin-top:1.5rem;">{icons}</div>
                </div>
                <div>
                    <h4 style="color:white; text-transform:uppercase; letter-spacing:1px; margin-bottom:1rem;">Quick Links</h4>
                    <a href="index.html" style="color:white; text-decoration:none; display:block; margin-bottom:0.5rem; opacity:0.8;">Home</a>
                    <a href="about.html" style="color:white; text-decoration:none; display:block; margin-bottom:0.5rem; opacity:0.8;">About Us</a>
                    {'<a href="blog.html" style="color:white; text-decoration:none; display:block; margin-bottom:0.5rem; opacity:0.8;">Blog</a>' if show_blog else ''}
                    {'<a href="booking.html" style="color:white; text-decoration:none; display:block; margin-bottom:0.5rem; opacity:0.8;">Book Appointment</a>' if show_booking else ''}
                </div>
                <div>
                    <h4 style="color:white; text-transform:uppercase; letter-spacing:1px; margin-bottom:1rem;">Legal</h4>
                    <a href="privacy.html" style="color:white; text-decoration:none; display:block; margin-bottom:0.5rem; opacity:0.8;">Privacy Policy</a>
                    <a href="terms.html" style="color:white; text-decoration:none; display:block; margin-bottom:0.5rem; opacity:0.8;">Terms of Service</a>
                </div>
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:2rem; text-align:center; font-size:0.9rem; opacity:0.6;">
                &copy; {datetime.datetime.now().year} {biz_name}. Powered by Titan Architecture.
            </div>
        </div>
    </footer>
    """

def gen_scripts():
    return "<script defer>window.addEventListener('scroll', () => { var r = document.querySelectorAll('.reveal'); for (var i = 0; i < r.length; i++) { if (r[i].getBoundingClientRect().top < window.innerHeight - 100) r[i].classList.add('active'); } }); window.dispatchEvent(new Event('scroll'));</script>"

# --- 8. THE MASTER CSS INJECTOR & PAGE BUILDER ---

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
        --btn-txt: {cta_txt_color};
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-size: 16px; }}
    body {{ background: var(--bg); color: var(--txt); font-family: var(--b-font); line-height: 1.6; overflow-x: hidden; transition: 0.3s; font-size: {size_p}rem; }}
    body.dark-mode {{ --bg: #0f172a; --txt: #f8fafc; --txt-h: #ffffff; --card: #1e293b; --glass: rgba(30, 41, 59, 0.9); --border: rgba(255, 255, 255, 0.1); }}
    h1, h2, h3, h4 {{ font-family: var(--h-font); font-weight: 800; line-height: 1.2; margin-bottom: 1rem; color: var(--txt-h); }}
    h1 {{ font-size: {size_h1}rem; }}
    a {{ text-decoration: none; color: inherit; transition: 0.3s; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    section {{ padding: clamp(4rem, 5vw, 6rem) 0; }}
    
    .glass {{ background: var(--glass); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid var(--border); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05); }}
    .card {{ background: var(--card); border-radius: var(--radius); border: 1px solid var(--border); overflow: hidden; transition: 0.4s; display: flex; flex-direction: column; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
    .card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: var(--p); }}
    
    .btn {{ padding: 0.8rem 2rem; border-radius: var(--radius); font-weight: 700; cursor: pointer; border: none; display: inline-flex; align-items: center; justify-content: center; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem; text-decoration: none; }}
    .btn-primary {{ background: var(--p); color: #ffffff !important; }}
    .btn-accent {{ background: var(--s); color: var(--btn-txt) !important; box-shadow: 0 10px 25px -5px var(--s); }}
    .btn-outline-light {{ background: transparent; border: 2px solid #ffffff; color: #ffffff !important; }}
    .btn:hover {{ transform: translateY(-2px); filter: brightness(1.1); }}
    
    nav {{ position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; padding: 1rem 0; transition: top 0.3s; border-bottom: 1px solid var(--border); }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; gap: 2rem; align-items: center; }}
    .nav-links a {{ font-weight: 600; opacity: 0.9; font-size: 0.95rem; color: var(--txt-h); }}
    .nav-links a:hover {{ color: var(--p); opacity: 1; }}
    .mobile-menu {{ display: none; font-size: 1.5rem; cursor: pointer; color: var(--txt-h); }}
    
    /* PADDING FIX FOR HERO */
    .modern-hero {{ position: relative; min-height: 90vh; display: flex; text-align: {align}; align-items: center; color: white; padding-top: 140px; overflow: hidden; background: var(--p); }}
    .modern-hero-grid {{ display: grid; grid-template-columns: 1fr; gap: 2rem; align-items: center; width: 100%; z-index: 2; position: relative; }}
    .modern-hero-text {{ display: flex; flex-direction: column; align-items: {align}; justify-content: {justify}; width: 100%; max-width: 800px; margin: 0 auto; }}
    .hero-btn-group {{ display: flex; gap: 1rem; flex-wrap: wrap; justify-content: {justify}; margin-top: 1rem; }}
    .hero-badge {{ display: inline-block; padding: 0.5rem 1.5rem; margin-bottom: 1.5rem; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 50px; font-size: 0.85rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #ffffff; }}
    .modern-hero h1 {{ color: #ffffff !important; text-shadow: 0 4px 30px rgba(0,0,0,0.5); margin-bottom: 1.5rem; line-height: 1.1; }}
    .modern-hero p {{ color: #ffffff !important; opacity: 0.95; font-size: 1.25rem; margin-bottom: 2rem; max-width: 700px; }}
    .modern-hero-visual {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; }}
    .visual-frame {{ width: 100%; height: 100%; position: relative; }}
    .visual-frame::after {{ content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1; }}
    
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2.5rem; }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }}
    .pricing-table {{ width: 100%; border-collapse: collapse; min-width: 600px; }}
    .pricing-table th {{ background: var(--p); color: white; padding: 1.5rem; text-align: left; }}
    .pricing-table td {{ padding: 1.5rem; border-bottom: 1px solid var(--border); background: var(--card); color: var(--txt); }}
    
    .reveal {{ opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; }}
    .reveal.active {{ opacity: 1; transform: translateY(0); }}
    
    #top-bar {{ position: fixed; top: 0; width: 100%; background: var(--s); color: var(--btn-txt); text-align: center; padding: 8px; z-index: 1002; font-weight: bold; font-size: 0.85rem; height: 40px; display:flex; align-items:center; justify-content:center; }}
    #top-bar a {{ color: var(--btn-txt); text-decoration: underline; margin-left:5px; }}
    
    @media (max-width: 768px) {{
        .nav-links {{ display: none; position: absolute; top: 100%; left: 0; width: 100%; background: var(--bg); flex-direction: column; padding: 2rem; border-bottom: 1px solid var(--border); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .nav-links.active {{ display: flex; }}
        .mobile-menu {{ display: block; }}
        .about-grid, .detail-view {{ grid-template-columns: 1fr; gap: 2rem; }}
        .modern-hero h1 {{ font-size: 2.5rem !important; }}
        .modern-hero {{ text-align: center; }}
        .modern-hero-text {{ align-items: center; }}
        .hero-btn-group {{ justify-content: center; }}
    }}
    """

def build_page(title, content, extra_js=""):
    gsc_meta = f'<meta name="google-site-verification" content="{gsc_tag}">' if gsc_tag else ""
    og_meta = f'<meta property="og:title" content="{title} | {biz_name}"><meta property="og:description" content="{seo_d}"><meta property="og:image" content="{og_image or logo_url}"><meta name="twitter:card" content="summary_large_image">'
    pwa_tags = f'<link rel="manifest" href="manifest.json"><meta name="theme-color" content="#000000"><link rel="apple-touch-icon" href="{pwa_icon}">'
    sw_script = "<script>if ('serviceWorker' in navigator) { navigator.serviceWorker.register('service-worker.js'); }</script>"
    ga_script_opt = f"<script async src='https://www.googletagmanager.com/gtag/js?id={ga_tag}'></script><script>window.dataLayer = window.dataLayer ||[]; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{ga_tag}');</script>" if ga_tag else ""

    h_f = h_font.replace(' ', '+')
    b_f = b_font.replace(' ', '+')
    modern_css = generate_modern_css()

    logo_display = f'<img src="{logo_url}" style="height: 40px; margin-right: 10px; object-fit: contain;" alt="{biz_name} Logo">' if logo_url else ''
    nav_links = f'<a href="index.html">Home</a>'
    if show_features: nav_links += '<a href="index.html#features">Features</a>'
    if show_pricing: nav_links += '<a href="index.html#pricing">Pricing</a>'
    if show_inventory: nav_links += '<a href="index.html#store">Store</a>'
    if show_blog: nav_links += '<a href="blog.html">Blog</a>'
    if show_booking: nav_links += '<a href="booking.html">Book</a>'
    nav_links += '<a href="contact.html">Contact</a>'
    
    top_bar = f'<div id="top-bar"><a href="{top_bar_link}">{top_bar_text}</a></div>' if top_bar_enabled else ''
    nav_top_offset = "40px" if top_bar_enabled else "0px"

    nav_html = f"""
        {top_bar}
        <nav class="glass" style="top:{nav_top_offset}">
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

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {biz_name}</title>
    <meta name="description" content="{seo_d}">
    {gsc_meta}{og_meta}{pwa_tags}{gen_schema()}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={h_f}:wght@400;600;800;900&family={b_f}:wght@300;400;500;700&display=swap">
    <style>{modern_css}</style>
    {ga_script_opt}
    {gen_2050_scripts()}
</head>
<body>
    <main>
        {nav_html}
        {content}
        {gen_footer()}
        {gen_wa_widget()}
        {gen_cart_system()}
        {gen_lang_script()}
        {gen_popup()}
        {extra_js}
    </main>
    {gen_scripts()}
    {sw_script}
</body>
</html>"""

# --- 9. SUB-PAGE GENERATORS ---

def gen_booking_content():
    if not show_booking: return ""
    return f'<section class="modern-hero" style="min-height:30vh; display:flex; align-items:center; justify-content:center;"><div class="container modern-hero-text" style="text-align:center;"><h1>{booking_title}</h1><p>{booking_desc}</p></div></section><section style="background:var(--bg);"><div class="container" style="text-align:center;"><div style="background:var(--card); border:1px solid var(--border); border-radius:12px; overflow:hidden; box-shadow:0 10px 40px rgba(0,0,0,0.1); width:100%;">{booking_embed}</div></div></section>'

def gen_blog_index_html():
    if not show_blog: return ""
    return f"""
    <section class="modern-hero" style="min-height:40vh; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{hero_img_1}'); background-size: cover; background-position:center;">
        <div class="container modern-hero-text"><h1>{blog_hero_title}</h1><p>{blog_hero_sub}</p></div>
    </section>
    <section style="background:var(--bg);"><div class="container"><div id="blog-grid" class="grid-3">Loading Posts...</div></div></section>
    {gen_csv_parser()}
    <script defer>
    async function loadBlog() {{ 
        if (!'{blog_sheet_url}') return; 
        try {{ 
            const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/); 
            const box = document.getElementById('blog-grid'); box.innerHTML = ''; 
            for(let i=1; i<lines.length; i++) {{ 
                const r = parseCSVLine(lines[i]); 
                if(r.length > 4) {{ 
                    box.innerHTML += `
                    <article class="card reveal" style="padding:0;">
                        <div style="width:100%; height:220px; overflow:hidden;">
                            <img src="${{r[5]}}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.5s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" alt="${{r[1]}}">
                        </div>
                        <div style="padding: 2rem; display:flex; flex-direction:column; flex-grow:1;">
                            <span style="display:inline-block; padding:0.4rem 1rem; background:var(--border); color:var(--txt-h); border-radius:50px; font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; width:fit-content; margin-bottom:1rem;">${{r[3]}}</span>
                            <h3 style="margin-bottom:1rem; line-height:1.3; font-size:1.4rem;">
                                <a href="post.html?id=${{r[0]}}" style="color:var(--txt-h); text-decoration:none;">${{r[1]}}</a>
                            </h3>
                            <p style="flex-grow:1; margin-bottom: 2rem; opacity:0.8; line-height:1.6; font-size:0.95rem; color:var(--txt);">${{r[4]}}</p>
                            <a href="post.html?id=${{r[0]}}" class="btn btn-primary" style="width:100%; margin-top:auto;">Read Article</a>
                        </div>
                    </article>`; 
                }} 
            }} 
        }} catch(e) {{ console.log(e); }} 
    }} 
    window.addEventListener('load', loadBlog);
    </script>
    """

def gen_product_page_content(is_demo=False):
    demo_flag = "const isDemo = true;" if is_demo else "const isDemo = false;"
    ar_script = '<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>' if enable_ar else ''
    return f"""
    {ar_script}
    <section style="padding-top:140px; background: var(--bg); min-height: 100vh;">
        <div class="container">
            <a href="index.html#inventory" class="btn glass" style="color:var(--txt-h); padding:0.5rem 1rem; margin-bottom:2rem; font-size:0.8rem;">← BACK TO STORE</a>
            <div id="product-detail-target">Loading Specifications...</div>
        </div>
    </section>
    {gen_csv_parser()}
    <script defer>
    {demo_flag}
    function changeImg(src) {{ document.getElementById('main-img').src = src; }}
    async function loadProduct() {{
        const params = new URLSearchParams(window.location.search); 
        let targetName = params.get('item'); 
        if(isDemo && !targetName) targetName = "Demo Product";
        
        try {{
            const res = await fetch('{sheet_url}'); 
            const txt = await res.text(); 
            const lines = txt.split(/\\r\\n|\\n/);
            for(let i=1; i<lines.length; i++) {{
                const clean = parseCSVLine(lines[i]);
                if(clean[0] === targetName || (isDemo && i===1)) {{
                    let allImgs = clean[3] ? clean[3].split('|') : ['{custom_feat}'];
                    let thumbHtml = '';
                    allImgs.forEach(img => {{ thumbHtml += `<img src="${{img.trim()}}" class="thumb" onclick="changeImg('${{img.trim()}}')" style="width:80px; height:80px; object-fit:cover; margin-right:10px; cursor:pointer; border-radius:8px; border:2px solid transparent; transition:0.3s;" onmouseover="this.style.borderColor='var(--p)'">`; }});
                    
                    let mainMedia = `<img src="${{allImgs[0]}}" id="main-img" style="width:100%; border-radius:16px; height:500px; object-fit:cover; box-shadow: 0 10px 30px rgba(0,0,0,0.1);" alt="${{clean[0]}}">`;
                    if({str(enable_ar).lower()} && clean.length > 5 && clean[5].includes('.glb')) {{
                        mainMedia = `<model-viewer src="${{clean[5]}}" ar ar-modes="webxr scene-viewer quick-look" camera-controls tone-mapping="neutral" shadow-intensity="1" auto-rotate style="width:100%; height:500px; border-radius:16px;"></model-viewer>`;
                    }}

                    let btnAction = `<button onclick="addToCart('${{clean[0]}}', '${{clean[1]}}')" class="btn btn-accent" style="width:100%; padding: 1.2rem; font-size:1.1rem;">ADD TO CART</button>`;
                    
                    document.getElementById('product-detail-target').innerHTML = `
                        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 4rem; align-items: start;">
                            <div>
                                ${{mainMedia}}
                                <div style="display:flex; margin-top:15px; overflow-x:auto;">${{thumbHtml}}</div>
                            </div>
                            <div>
                                <h1 style="font-size:clamp(2.5rem, 4vw, 3.5rem); margin-bottom:0.5rem; color:var(--txt-h);">${{clean[0]}}</h1>
                                <h2 style="color:var(--s); font-size:2rem; margin-bottom:1.5rem;">${{clean[1]}}</h2>
                                <div style="font-size:1.1rem; line-height:1.8; opacity:0.9; margin-bottom:3rem; color:var(--txt);">${{parseMarkdown(clean[2])}}</div>
                                ${{btnAction}}
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

def gen_blog_post_html():
    if not show_blog: return ""
    return f"""
    <article id="post-container" style="padding-top:0px;">Loading Content...</article>
    {gen_csv_parser()}
    <script defer>
    async function loadPost() {{
        if (!'{blog_sheet_url}') return;
        const params = new URLSearchParams(window.location.search); const slug = params.get('id');
        try {{
            const res = await fetch('{blog_sheet_url}'); const txt = await res.text(); const lines = txt.split(/\\r\\n|\\n/);
            const container = document.getElementById('post-container');
            for(let i=1; i<lines.length; i++) {{
                const r = parseCSVLine(lines[i]);
                if(r[0] === slug) {{
                    const contentHtml = parseMarkdown(r[6]);
                    document.title = r[1] + " | {biz_name}";
                    
                    container.innerHTML = `
                        <header class="modern-hero" style="min-height:40vh; display:flex; align-items:center; justify-content:center; text-align:center;">
                            <div class="container modern-hero-text">
                                <span style="display:inline-block; padding:0.4rem 1.5rem; background:rgba(255,255,255,0.2); color:white; border-radius:50px; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:1rem;">${{r[3]}}</span>
                                <h1>${{r[1]}}</h1>
                            </div>
                        </header>
                        <div class="container" style="max-width:800px; padding: 4rem 1rem; background:var(--bg); color:var(--txt);">
                            <img src="${{r[5]}}" style="width:100%; border-radius:16px; margin-bottom:3rem; box-shadow:0 10px 30px rgba(0,0,0,0.1);" alt="${{r[1]}}">
                            <div style="line-height:1.9; font-size:1.15rem; opacity:0.9;">${{contentHtml}}</div>
                            <hr style="margin:3rem 0; border:0; border-top:1px solid var(--border);">
                            <a href="blog.html" class="btn btn-primary">&larr; Back to Blog</a>
                        </div>`;
                    break;
                }}
            }}
        }} catch(e) {{}}
    }}
    window.addEventListener('load', loadPost);
    </script>
    """

def gen_inner_header(title):
    return f"""
    <div class="modern-hero" style="min-height: 40vh; display:flex; align-items:center; justify-content:center; text-align:center;">
        <div class="container modern-hero-text">
            <h1 style="color:#ffffff !important; margin:0; text-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: clamp(3rem, 6vw, 4.5rem);">{title}</h1>
        </div>
    </div>
    """

# --- 10. PAGE ASSEMBLY & RENDER ---

home_content = ""
if show_hero: home_content += gen_hero()
if show_stats: home_content += gen_stats()
if show_features: home_content += gen_features()
if show_pricing: home_content += gen_pricing_table()
if show_inventory: home_content += gen_inventory()
if show_gallery: 
    home_content += f"""
    <section id="about" style="background:var(--bg); border-top:1px solid var(--border);">
        <div class="container about-grid">
            <div class="reveal"><img src="{about_img}" style="width:100%; border-radius:var(--radius); box-shadow:0 10px 30px rgba(0,0,0,0.1);" alt="About Us"></div>
            <div class="reveal">
                <h2 style="font-size:2.5rem; margin-bottom:1.5rem; color:var(--txt-h);">{about_h_in}</h2>
                <div style="margin-bottom:2rem; font-size:1.1rem; opacity:0.9; line-height:1.8; color:var(--txt);">{format_text(about_short_in)}</div>
                <a href="about.html" class="btn btn-primary">Read Our Story</a>
            </div>
        </div>
    </section>"""
if show_testimonials: 
    # Bulletproof Grid Testimonials
    t_cards = "".join([
        f'''<div class="card reveal" style="padding: 2rem;">
                <div style="margin-bottom: 1.5rem;"><svg viewBox="0 0 24 24" width="28" height="28" fill="var(--p)" style="opacity: 0.4;"><path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/></svg></div>
                <p style="font-size: 1.1rem; font-style: italic; line-height: 1.7; opacity: 0.9; flex-grow: 1; margin-bottom: 2rem; color:var(--txt); text-align:left;">"{x.split("|")[1].strip()}"</p>
                <div style="display: flex; align-items: center; gap: 15px; border-top: 1px solid var(--border); padding-top: 1.5rem;">
                    <div style="width: 45px; height: 45px; min-width: 45px; border-radius: 50%; background: var(--p); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; text-transform: uppercase;">{x.split("|")[0].strip()[0]}</div>
                    <div style="text-align:left;">
                        <b style="color: var(--txt-h); font-size: 1.1rem; display: block;">{x.split("|")[0].strip()}</b>
                        <span style="display: block; font-size: 0.8rem; opacity: 0.6; margin-top: 2px; color:var(--txt);">Verified Client</span>
                    </div>
                </div>
            </div>''' 
        for x in testi_data.split('\n') if "|" in x and len(x.split("|")[0].strip()) > 0
    ])
    home_content += f'<section id="testimonials" style="background:var(--bg); border-top:1px solid var(--border);"><div class="container"><div class="section-head reveal" style="display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom:4rem;"><h2 style="margin-bottom:0.5rem; font-size:2.5rem;">Client Stories</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem 0; border-radius:2px;"></div></div><div class="grid-3">{t_cards}</div></div></section>'
if show_faq: 
    items = "".join([f"<details class='reveal' style='background:var(--card); border:1px solid var(--border); padding:1.5rem; border-radius:12px; margin-bottom:1rem; color:var(--txt);'><summary style='font-weight:800; font-size:1.1rem; cursor:pointer; color:var(--txt-h);'>{l.split('?')[0]}?</summary><p style='margin-top:1rem; opacity:0.9; line-height:1.6;'>{l.split('?')[1]}</p></details>" for l in faq_data.split('\n') if "?" in l and len(l.split('?'))>1])
    home_content += f'<section id="faq" style="background:var(--bg);"><div class="container" style="max-width:800px;"><div class="section-head reveal" style="display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom:4rem;"><h2 style="margin-bottom:0.5rem; font-size:2.5rem;">FAQ</h2><div style="width:60px; height:4px; background:var(--s); margin:1rem 0; border-radius:2px;"></div></div>{items}</div></section>'
if show_cta: 
    home_content += f'<section style="background:var(--s); color:white; text-align:center;"><div class="container reveal"><h2 style="color:var(--btn-txt) !important; font-size:clamp(2.5rem, 5vw, 3.5rem); margin-bottom:1rem;">Ready to Launch?</h2><p style="margin-bottom:2rem; font-size:1.3rem; opacity:0.9; color:var(--btn-txt) !important;">Join the future of web architecture.</p><a href="contact.html" class="btn" style="background:var(--bg); color:var(--txt-h) !important;">Get Started</a></div></section>'

# ADVANCED CONTACT PAGE
contact_content = f"""
{gen_inner_header("Contact Us")}
<section style="background:var(--bg);">
    <div class="container">
        <div class="contact-grid">
            <div class="card" style="padding: clamp(1.5rem, 5vw, 3rem);">
                <h3 style="margin-bottom:1.5rem; font-size:2rem;">Get In Touch</h3>
                <div style="margin-bottom:1.5rem;">
                    <strong style="color:var(--txt-h); font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Headquarters</strong>
                    <p style="font-size:1.1rem; color:var(--txt); opacity:0.9; margin-top:0.5rem;">{biz_addr}</p>
                </div>
                <div style="margin-bottom:1.5rem;">
                    <strong style="color:var(--txt-h); font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Direct Line</strong>
                    <p style="font-size:1.1rem; margin-top:0.5rem;"><a href="tel:{biz_phone}" style="color:var(--s); text-decoration:none; font-weight:bold;">{biz_phone}</a></p>
                </div>
                <div style="margin-bottom:2.5rem;">
                    <strong style="color:var(--txt-h); font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Email</strong>
                    <p style="font-size:1.1rem; margin-top:0.5rem;"><a href="mailto:{biz_email}" style="color:var(--txt); text-decoration:none; opacity:0.9;">{biz_email}</a></p>
                </div>
                <a href="https://wa.me/{wa_num}" target="_blank" class="btn btn-accent" style="width:100%;">WhatsApp Us Instantly</a>
            </div>
            
            <div class="card" style="padding: clamp(1.5rem, 5vw, 3rem);">
                <h3 style="margin-bottom:1.5rem; font-size:2rem;">Send a Message</h3>
                <form action="https://formsubmit.co/{biz_email}" method="POST" style="display:flex; flex-direction:column; gap:1.5rem;">
                    <div>
                        <label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; color:var(--txt-h); margin-bottom:0.5rem; display:block;">Full Name</label>
                        <input type="text" name="name" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; font-family:inherit; outline:none;">
                    </div>
                    <div>
                        <label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; color:var(--txt-h); margin-bottom:0.5rem; display:block;">Email Address</label>
                        <input type="email" name="email" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; font-family:inherit; outline:none;">
                    </div>
                    <div>
                        <label style="font-weight:600; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px; color:var(--txt-h); margin-bottom:0.5rem; display:block;">Your Message</label>
                        <textarea name="msg" rows="5" required style="width:100%; padding:1.2rem; border:1px solid var(--border); border-radius:8px; background:var(--bg); color:var(--txt); font-size:1rem; font-family:inherit; outline:none; resize:vertical;"></textarea>
                    </div>
                    <button class="btn btn-primary" type="submit" style="height:4rem; font-size:1.1rem; margin-top:1rem;">Send Secure Message</button>
                </form>
            </div>
        </div>
        <div style="border-radius:var(--radius); overflow:hidden; border:1px solid var(--border); margin-top:4rem; box-shadow:0 10px 30px rgba(0,0,0,0.05); height: 450px; position: relative;">
            {map_iframe.replace('<iframe ', '<iframe style="width:100% !important; height:100% !important; position:absolute; top:0; left:0; border:none;" ')}
        </div>
    </div>
</section>
"""

# PRE-GENERATE HTML
html_to_render = ""
if preview_mode == "Home": html_to_render = build_page("Home", home_content)
elif preview_mode == "About": html_to_render = build_page("About", f"{gen_inner_header('About')}<section style='background:var(--bg);'><div class='container' style='color:var(--txt);'>{format_text(about_long)}</div></section>")
elif preview_mode == "Contact": html_to_render = build_page("Contact", contact_content)
elif preview_mode == "Privacy": html_to_render = build_page("Privacy", f"{gen_inner_header('Privacy')}<section style='background:var(--bg);'><div class='container' style='color:var(--txt);'>{format_text(priv_txt)}</div></section>")
elif preview_mode == "Terms": html_to_render = build_page("Terms", f"{gen_inner_header('Terms')}<section style='background:var(--bg);'><div class='container' style='color:var(--txt);'>{format_text(term_txt)}</div></section>")
elif preview_mode == "Blog Index": html_to_render = build_page("Blog", gen_blog_index_html())
elif preview_mode == "Blog Post (Demo)": html_to_render = build_page("Article", gen_blog_post_html())
elif preview_mode == "Product Detail (Demo)":
    st.info("ℹ️ Demo Mode Active: Showing the first available product from your CSV.")
    html_to_render = build_page("Product", gen_product_page_content(is_demo=True))
elif preview_mode == "Booking Page":
    html_to_render = build_page("Book Now", gen_booking_content())

# RENDER
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
    st.success("Architectural Core Synchronized.")
    
    z_b = io.BytesIO()
    with zipfile.ZipFile(z_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("index.html", build_page("Home", home_content))
        zf.writestr("about.html", build_page("About", f"{gen_inner_header('About')}<section style='background:var(--bg);'><div class='container' style='color:var(--txt);'>{format_text(about_long)}</div></section>"))
        zf.writestr("contact.html", build_page("Contact", contact_content))
        zf.writestr("privacy.html", build_page("Privacy", f"{gen_inner_header('Privacy')}<section style='background:var(--bg);'><div class='container' style='color:var(--txt);'>{format_text(priv_txt)}</div></section>"))
        zf.writestr("terms.html", build_page("Terms", f"{gen_inner_header('Terms')}<section style='background:var(--bg);'><div class='container' style='color:var(--txt);'>{format_text(term_txt)}</div></section>"))
        
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
                    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
                    headers = {"Authorization": f"Bearer {pinata_jwt}"}
                    files = {"file": ("titan_site.zip", z_b.getvalue())}
                    res = requests.post(url, headers=headers, files=files)
                    if res.status_code == 200:
                        cid = res.json()['IpfsHash']
                        st.success(f"Deployed! Live forever on IPFS.")
                        st.markdown(f"**Gateway Link:** [ipfs.io/ipfs/{cid}](https://ipfs.io/ipfs/{cid})")
                    else: st.error(f"IPFS Error: {res.text}")
                except Exception as e: st.error(f"Upload failed: {e}")
    else:
        st.download_button("📥 DOWNLOAD APEX PACKAGE", z_b.getvalue(), f"{biz_name.lower().replace(' ','_')}_apex.zip", "application/zip", type="primary")
