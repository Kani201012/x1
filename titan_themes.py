# titan_themes.py
# 2050 Titan Architecture Theme Engine - 25 Premium Modern Layouts

THEME_REGISTRY = {
    # --- SAAS & TECH (High Conversion, Clean) ---
    "1. Stripe Cloud (Modern SaaS)": {"bg": "#f8fafc", "txt": "#0f172a", "card": "#ffffff", "p": "#6366f1", "s": "#10b981", "nav": "rgba(255,255,255,0.8)", "shadow": "0 10px 40px -10px rgba(99,102,241,0.15)", "radius": "16px", "border": "1px solid #e2e8f0"},
    "2. Vercel Dark (Developer Core)": {"bg": "#000000", "txt": "#ededed", "card": "#111111", "p": "#ffffff", "s": "#0070f3", "nav": "rgba(0,0,0,0.8)", "shadow": "0 0 0 1px #333", "radius": "8px", "border": "1px solid #333"},
    "3. Apple Minimalist (Pure Clean)": {"bg": "#fbfbfd", "txt": "#1d1d1f", "card": "#ffffff", "p": "#000000", "s": "#0066cc", "nav": "rgba(251,251,253,0.8)", "shadow": "0 4px 24px rgba(0,0,0,0.04)", "radius": "24px", "border": "none"},
    "4. Neo-Brutalist (Gumroad Style)": {"bg": "#f4f4f0", "txt": "#000000", "card": "#ffffff", "p": "#000000", "s": "#ff90e8", "nav": "#f4f4f0", "shadow": "6px 6px 0px #000000", "radius": "0px", "border": "3px solid #000000"},
    "5. Glassmorphism (Translucent)": {"bg": "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)", "txt": "#1e1e24", "card": "rgba(255, 255, 255, 0.25)", "p": "#3a0ca3", "s": "#ff006e", "nav": "rgba(255,255,255,0.1)", "shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.37)", "radius": "20px", "border": "1px solid rgba(255, 255, 255, 0.4)"},

    # --- RETAIL & E-COMMERCE ---
    "6. Luxury Boutique (High-End)": {"bg": "#faf9f6", "txt": "#2c2a29", "card": "#ffffff", "p": "#d4af37", "s": "#1a1a1a", "nav": "rgba(250,249,246,0.9)", "shadow": "0 15px 35px rgba(0,0,0,0.05)", "radius": "0px", "border": "1px solid #eaeaea"},
    "7. Streetwear Edge (Hypebeast)": {"bg": "#121212", "txt": "#f4f4f4", "card": "#1e1e1e", "p": "#ff4500", "s": "#ffffff", "nav": "rgba(18,18,18,0.9)", "shadow": "0 20px 40px rgba(255,69,0,0.15)", "radius": "4px", "border": "1px solid #333"},
    "8. Organic Eco (Sustainable)": {"bg": "#f0f4f0", "txt": "#2c3e2e", "card": "#ffffff", "p": "#4a7c59", "s": "#f39c12", "nav": "rgba(240,244,240,0.9)", "shadow": "0 10px 30px rgba(74,124,89,0.08)", "radius": "30px", "border": "none"},
    "9. Cosmetic Pastel (Beauty)": {"bg": "#fff5f5", "txt": "#5c4a4a", "card": "#ffffff", "p": "#e8b4b8", "s": "#a36b7e", "nav": "rgba(255,245,245,0.9)", "shadow": "0 12px 24px rgba(232,180,184,0.15)", "radius": "20px", "border": "1px solid #ffe3e3"},
    "10. Tech Hardware (Neon Dark)": {"bg": "#0d1117", "txt": "#c9d1d9", "card": "#161b22", "p": "#58a6ff", "s": "#238636", "nav": "rgba(13,17,23,0.9)", "shadow": "0 0 20px rgba(88,166,255,0.1)", "radius": "12px", "border": "1px solid #30363d"},

    # --- HEALTH & CLINICS ---
    "11. Medical Platinum (Trust)": {"bg": "#ffffff", "txt": "#1e293b", "card": "#f8fafc", "p": "#0284c7", "s": "#059669", "nav": "rgba(255,255,255,0.95)", "shadow": "0 4px 6px -1px rgba(0,0,0,0.05)", "radius": "12px", "border": "1px solid #e2e8f0"},
    "12. Dental Aqua (Clean)": {"bg": "#f0fdfa", "txt": "#0f172a", "card": "#ffffff", "p": "#0d9488", "s": "#0284c7", "nav": "rgba(240,253,250,0.9)", "shadow": "0 10px 25px rgba(13,148,136,0.1)", "radius": "16px", "border": "1px solid #ccfbf1"},
    "13. Fitness Aggressive (Gym)": {"bg": "#0a0a0a", "txt": "#ffffff", "card": "#171717", "p": "#e11d48", "s": "#facc15", "nav": "rgba(10,10,10,0.9)", "shadow": "0 10px 30px rgba(225,29,72,0.2)", "radius": "8px", "border": "1px solid #262626"},
    "14. Spa Therapy (Calm)": {"bg": "#faf5f0", "txt": "#4a443c", "card": "#ffffff", "p": "#bfa58a", "s": "#8c735a", "nav": "rgba(250,245,240,0.9)", "shadow": "0 8px 20px rgba(191,165,138,0.1)", "radius": "24px", "border": "1px solid #f0e6da"},
    "15. Yoga Mindfulness": {"bg": "#fdf8f5", "txt": "#333333", "card": "#ffffff", "p": "#d4a373", "s": "#a1c181", "nav": "rgba(253,248,245,0.9)", "shadow": "0 5px 15px rgba(0,0,0,0.03)", "radius": "50px", "border": "none"},

    # --- CORPORATE & REAL ESTATE ---
    "16. Law Firm Heritage": {"bg": "#ffffff", "txt": "#1f2937", "card": "#f9fafb", "p": "#1e3a8a", "s": "#b45309", "nav": "rgba(255,255,255,0.95)", "shadow": "0 4px 6px rgba(0,0,0,0.05)", "radius": "4px", "border": "1px solid #e5e7eb"},
    "17. Real Estate Prime": {"bg": "#111827", "txt": "#f3f4f6", "card": "#1f2937", "p": "#fbbf24", "s": "#f9fafb", "nav": "rgba(17,24,39,0.9)", "shadow": "0 10px 30px rgba(251,191,36,0.1)", "radius": "8px", "border": "1px solid #374151"},
    "18. Construction Industrial": {"bg": "#f5f5f5", "txt": "#1a1a1a", "card": "#ffffff", "p": "#f59e0b", "s": "#000000", "nav": "rgba(245,245,245,0.95)", "shadow": "0 8px 0px #e5e5e5", "radius": "0px", "border": "2px solid #000000"},
    "19. Architecture Grid": {"bg": "#ffffff", "txt": "#000000", "card": "#f4f4f5", "p": "#000000", "s": "#3b82f6", "nav": "#ffffff", "shadow": "none", "radius": "0px", "border": "1px solid #000000"},
    "20. Agency Bold (Creative)": {"bg": "#4f46e5", "txt": "#ffffff", "card": "#4338ca", "p": "#f9a8d4", "s": "#fde047", "nav": "rgba(79,70,229,0.9)", "shadow": "0 20px 40px rgba(0,0,0,0.2)", "radius": "20px", "border": "none"},

    # --- CREATOR & EXOTIC ---
    "21. Cyberpunk 2077": {"bg": "#fcee0a", "txt": "#000000", "card": "#000000", "p": "#00ffff", "s": "#ff003c", "nav": "#fcee0a", "shadow": "8px 8px 0px #00ffff", "radius": "0px", "border": "2px solid #000000"},
    "22. Monochromatic Black/White": {"bg": "#ffffff", "txt": "#000000", "card": "#ffffff", "p": "#000000", "s": "#000000", "nav": "#ffffff", "shadow": "4px 4px 0px #000000", "radius": "0px", "border": "2px solid #000000"},
    "23. Retro Synthwave": {"bg": "#2b213a", "txt": "#e0d6eb", "card": "#181425", "p": "#ff007f", "s": "#00f0ff", "nav": "rgba(43,33,58,0.9)", "shadow": "0 0 15px rgba(255,0,127,0.5)", "radius": "10px", "border": "1px solid #ff007f"},
    "24. Gradient Mesh": {"bg": "linear-gradient(45deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)", "txt": "#333", "card": "rgba(255,255,255,0.6)", "p": "#f77062", "s": "#3f51b5", "nav": "rgba(255,255,255,0.4)", "shadow": "0 8px 32px rgba(0,0,0,0.1)", "radius": "30px", "border": "1px solid rgba(255,255,255,0.5)"},
    "25. Midnight Ocean": {"bg": "#0f2027", "txt": "#d1d5db", "card": "#203a43", "p": "#2c5364", "s": "#38ef7d", "nav": "rgba(15,32,39,0.9)", "shadow": "0 15px 25px rgba(0,0,0,0.3)", "radius": "16px", "border": "1px solid #2c5364"}
}

def generate_modern_css(theme_name, h_font, b_font, hero_align, h_color, b_color, h1_size, p_size, cta_bg, cta_txt):
    # 1. Fetch the base colors from the registry
    t = THEME_REGISTRY.get(theme_name, THEME_REGISTRY["1. Stripe Cloud (Modern SaaS)"])
    
    # 2. Define special effects (Gradient, Hover, Backdrop)
    gradient_text = ""
    if any(x in theme_name for x in ["SaaS", "Dark", "Creative"]):
        gradient_text = f"background: linear-gradient(90deg, {t['p']}, {t['s']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"

    btn_hover = "transform: translateY(-3px) scale(1.02); filter: brightness(1.15); box-shadow: 0 10px 25px -5px var(--p);"
    if any(x in theme_name for x in ["Brutalist", "Cyberpunk", "Monochromatic"]):
        btn_hover = "transform: translate(-4px, -4px); box-shadow: 8px 8px 0px #000;"

    backdrop = "backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);" if any(x in theme_name for x in ["Glass", "Mesh"]) else ""

    h_align = "text-align: center; justify-content: center;"
    if hero_align == "Left":
        h_align = "text-align: left; justify-content: flex-start; align-items: center;"

    # 3. Return exact CSS with Professional Typography & Mobile Fixes
    return f"""
    :root {{
        --p: {t['p']}; --s: {t['s']}; --bg: {t['bg']}; 
        --nav: {t['nav']}; --card: {t['card']};
        --radius: {t['radius']}; --shadow: {t['shadow']}; --border: {t['border']};
        --h-font: '{h_font}', sans-serif; --b-font: '{b_font}', sans-serif;
        
        /* MANUAL OVERRIDES */
        --txt-h: {h_color};
        --txt-b: {b_color};
        --h1-size: {h1_size};
        --p-size: {p_size};
        --cta-bg: {cta_bg};
        --cta-txt: {cta_txt};
    }}
    
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-size: 16px; }}
    
    body {{ 
        background: var(--bg); 
        color: var(--txt-b); 
        font-family: var(--b-font); 
        font-size: var(--p-size); 
        line-height: 1.8; /* Industry standard for high readability */
        letter-spacing: 0.01em; /* Subtle air between characters */
        overflow-x: hidden; 
        width: 100vw; max-width: 100%;
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

    p {{ 
        margin-bottom: 2rem; 
        opacity: 0.9;
        font-weight: 400;
        text-align: justify; /* THIS MAKES THE TEXT ARRANGEMENT STRAIGHT */
        text-justify: inter-word; /* Balances the gaps between words */
        hyphens: auto; /* Prevents awkward gaps on mobile */
        -webkit-hyphens: auto;
    }}
    
    /* 2026 ADVANCED HERO ENGINE */
    .hero {{ position: relative; min-height: 95vh; overflow: hidden; display: flex; {h_align} padding-top: 120px; }}
    .carousel-slide {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s cubic-bezier(0.4, 0, 0.2, 1); z-index: 0; transform: scale(1.05); }}
    .carousel-slide.active {{ opacity: 1; transform: scale(1); }}
    .hero-overlay {{ background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.8) 100%); position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
    .hero-content {{ z-index: 2; position: relative; width: 100%; padding: 0 5%; max-width: 1400px; }}
    .hero h1 {{ color: #ffffff !important; text-shadow: 0 10px 30px rgba(0,0,0,0.5); -webkit-text-fill-color: #fff; background: none; }}
    .hero p {{ color: rgba(255,255,255,0.9) !important; font-size: clamp(1.2rem, 2vw, 1.4rem); max-width: 800px; margin: 0 {'auto' if hero_align == 'Center' else '0'} 2.5rem {'auto' if hero_align == 'Center' else '0'}; font-weight: 400; }}
    
    /* BENTO-STYLE GRID LAYOUTS */
    .container {{ max-width: 1300px; margin: 0 auto; padding: 0 2rem; }}
    main section {{ padding: clamp(2rem, 8vw, 8rem) 0; position: relative; }}
    .section-head {{ text-align: center; margin-bottom: clamp(3rem, 5vw, 5rem); }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2.5rem; }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items: center; }}
    
    /* FIX: Added missing contact-grid */
    .contact-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: stretch; }}
    
    /* 2026 CARD PHYSICS & MICRO-INTERACTIONS */
    .card {{ 
        background: var(--card); 
        border-radius: var(--radius); 
        border: var(--border); 
        box-shadow: var(--shadow);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
        display: flex; 
        flex-direction: column; 
        overflow: hidden; 
        position: relative;
        color: var(--txt-b) !important;
        {backdrop}
    }}

    /* Premium Top-Border Glow */
    .card::before {{ 
        content: ''; 
        position: absolute; 
        top: 0; left: 0; right: 0; 
        height: 4px; 
        background: linear-gradient(90deg, var(--p), var(--s)); 
        opacity: 0; 
        transition: 0.3s; 
        z-index: 5;
    }}

    .card:hover {{ 
        transform: translateY(-10px); 
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.2); 
    }}

    .card:hover::before {{ 
        opacity: 1; 
    }}
    
    /* REFINED PRODUCT TYPOGRAPHY */
    .card h3 {{ 
        font-size: 1.35rem !important;
        font-weight: 800; 
        line-height: 1.2; 
        margin-bottom: 0.4rem; 
        color: var(--txt-h) !important;
        letter-spacing: -0.02em;
    }}

    .card-body {{ 
        padding: 2rem; 
        display: flex; 
        flex-direction: column; 
        flex-grow: 1; 
    }}

    .card-desc {{ 
        font-size: 0.95rem; 
        line-height: 1.6;
        opacity: 0.7; 
        margin-bottom: 1.5rem; 
        display: -webkit-box; 
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; 
        overflow: hidden; 
        color: var(--txt-b);
    }}

    .prod-img {{ 
        width: 100%; 
        height: 260px;
        object-fit: cover; 
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); 
    }}

    .card:hover .prod-img {{ 
        transform: scale(1.08); 
    }}
    
    /* ENTERPRISE BUTTON COMPONENTS */
    .btn {{ 
        display: inline-flex; align-items: center; justify-content: center;
        padding: 1.2rem 2.5rem; border-radius: var(--radius); 
        font-weight: 800; text-decoration: none; transition: all 0.3s ease; 
        text-transform: uppercase; cursor: pointer; border: none; text-align: center;
        font-size: 0.95rem; letter-spacing: 1.5px; position: relative; overflow: hidden;
    }}
    .btn-primary {{ background: var(--p); color: #fff !important; }}
    .btn-accent {{ background: var(--s); color: #fff !important; }}
    .btn:hover {{ {btn_hover} }}
    
    /* GLASSMORPHISM NAVIGATION */
    nav#main-navbar {{ 
        position: fixed; top: 0; width: 100%; z-index: 2000; /* FIXED: Elevated above everything */
        background: var(--nav); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(128,128,128,0.1); padding: 1.2rem 0; transition: top 0.3s, background 0.3s; 
    }}
    .nav-flex {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-links {{ display: flex; align-items: center; gap: 2rem; }}
    .nav-links a {{ text-decoration: none; font-weight: 600; color: var(--txt-h); font-size: 0.95rem; transition: 0.2s; position: relative; }}
    .nav-links a::after {{ content: ''; position: absolute; width: 0; height: 2px; bottom: -4px; left: 0; background-color: var(--p); transition: 0.3s; }}
    .nav-links a:hover::after {{ width: 100%; }}
    .nav-links a:hover {{ color: var(--p); }}
    .mobile-menu {{ display: none; font-size: 1.8rem; cursor: pointer; background:none; border:none; color:var(--txt-h); z-index: 2001; }} /* Ensure hamburger is clickable */
    
    /* PREMIUM ASYMMETRICAL PRODUCT VIEW */
    .detail-view {{ 
        display: grid; 
        grid-template-columns: 0.8fr 1.2fr;
        gap: 6rem; 
        align-items: start; 
        background: var(--card); 
        padding: 5rem; 
        border-radius: 32px; 
        box-shadow: var(--shadow); 
        border: var(--border); 
        position: relative;
    }}

    .product-media-column {{ 
        position: sticky; 
        top: 150px;
    }}

    .product-price-tag {{ 
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(5, 150, 105, 0.1);
        color: #059669; 
        font-size: 2rem; 
        font-weight: 900; 
        border-radius: 50px;
        margin-bottom: 2rem; 
    }}

    .product-info-column h1 {{ 
        font-size: clamp(2.5rem, 4vw, 4.5rem); 
        margin-bottom: 1.5rem; 
        line-height: 1;
    }}

    .product-specs-container {{
        font-size: 1.15rem;
        line-height: 1.8;
        color: var(--txt-b);
        opacity: 0.9;
    }}

    .product-specs-container strong {{
        display: block;
        margin-top: 2rem;
        font-size: 1.3rem;
        color: var(--p);
    }}

    .product-meta-box {{ background: rgba(128,128,128,0.05); padding: 2rem; border-radius: var(--radius); margin-bottom: 2.5rem; border-left: 5px solid var(--p); }}
    .gallery-thumbs {{ display: flex; gap: 15px; margin-top: 20px; overflow-x: auto; padding-bottom:10px; }}
    .thumb {{ width: 80px; height: 80px; border-radius: var(--radius); object-fit: cover; cursor: pointer; border: 2px solid transparent; opacity: 0.6; transition: 0.3s; }}
    .thumb:hover, .thumb.active {{ border-color: var(--p); opacity: 1; transform: translateY(-5px); }}
    
    /* RESPONSIVE PRICING TABLES */
    .pricing-wrapper {{ overflow-x: auto; -webkit-overflow-scrolling: touch; width: 100%; margin: 0 auto; box-shadow: var(--shadow); border-radius: var(--radius); background: var(--card); border: var(--border); }}
    .pricing-table {{ width: 100%; border-collapse: collapse; min-width: 800px; }}
    .pricing-table th {{ background: var(--p); color: white; padding: 2rem; text-align: left; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }}
    .pricing-table td {{ padding: 2rem; border-bottom: 1px solid rgba(128,128,128,0.1); color: var(--txt-b); font-size: 1.1rem; }}
    .pricing-table tr:hover td {{ background: rgba(128,128,128,0.03); }}

    /* MODERN FOOTER */
    footer {{ background: #0f172a; color: #f8fafc; padding: 6rem 0 3rem 0; margin-top: auto; border-top: 4px solid var(--p); }}
    .footer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 4rem; }}
    footer a {{ color: #94a3b8 !important; text-decoration: none; display: block; margin-bottom: 1rem; transition: 0.3s; font-size: 1.05rem; }}
    footer a:hover {{ color: #ffffff !important; transform: translateX(5px); }}
    .social-icon {{ width: 28px; height: 28px; fill: #94a3b8; transition: 0.3s; }}
    .social-icon:hover {{ fill: var(--p); transform: scale(1.2) translateY(-3px); }}

    /* ACCESSIBILITY & UTILS */
    .reveal {{ opacity: 0; transform: translateY(40px); transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94); z-index: 10; position:relative; }}
    .reveal.active {{ opacity: 1; transform: translateY(0); }}
    details {{ background: var(--card); border: var(--border); border-radius: var(--radius); margin-bottom: 1.5rem; padding: 1.5rem; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition:0.3s; }}
    details:hover {{ box-shadow: var(--shadow); transform: translateX(5px); border-left: 4px solid var(--p); }}
    details summary {{ font-weight: 800; font-size: 1.2rem; outline: none; }}

    /* SMART CART PHYSICS & OVERLAYS */
    #cart-float {{ position: fixed; bottom: 100px; right: 30px; background: var(--p); color: #fff; padding: 15px 25px; border-radius: 50px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); cursor: pointer; z-index: 1000; display: flex; align-items: center; gap: 10px; font-weight: 800; transition: 0.3s; border: 2px solid rgba(255,255,255,0.1); }}
    #cart-float:hover {{ transform: scale(1.05) translateY(-5px); }}
    
    #cart-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); z-index: 3000; }}
    
    #cart-modal {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); width: 90%; max-width: 500px; max-height: 90vh; overflow-y: auto; padding: 2.5rem; border-radius: 24px; box-shadow: 0 30px 60px rgba(0,0,0,0.4); z-index: 3001; border: var(--border); color: var(--txt-b); }}
    #cart-modal h3 {{ margin-bottom: 1.5rem; color: var(--p); font-size: 1.8rem; border-bottom: 1px solid rgba(128,128,128,0.1); padding-bottom: 1rem; }}
    
    .cart-item {{ display: flex; justify-content: space-between; border-bottom: 1px solid rgba(128,128,128,0.1); padding: 15px 0; font-size: 1.1rem; }}
    
    .local-vault {{ background: rgba(128,128,128,0.05); padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem; border: 1px solid rgba(128,128,128,0.1); }}
    .local-vault input {{ width: 100%; padding: 1rem; margin-top: 0.5rem; border-radius: 8px; border: var(--border); background: var(--bg); color: var(--txt-b); font-size: 1rem; }}
    
    /* POPUP PHYSICS */
    #lead-popup {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); padding: 3.5rem; text-align: center; border-radius: var(--radius); z-index: 3001; box-shadow: 0 30px 60px rgba(0,0,0,0.5); width: 90%; max-width: 500px; border: var(--border); color: var(--txt-b); }}
    .close-popup {{ position: absolute; top: 15px; right: 20px; cursor: pointer; font-size: 2rem; opacity: 0.5; transition: 0.3s; }}
    .close-popup:hover {{ opacity: 1; color: var(--s); }}

    /* =========================================
       2026 STRUCTURAL LAYOUT UPGRADES 
       ========================================= */
       
    /* 1. ASYMMETRICAL HERO WITH FLOATING GLASS */
    .modern-hero {{ position: relative; min-height: 100vh; display: flex; {h_align} padding-top: 120px; }}
    .modern-hero-bg {{ position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle at 50% 50%, rgba(128,128,128,0.05) 0%, transparent 50%); z-index: -1; animation: rotate 60s linear infinite; }}
    .modern-hero-grid {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 4rem; align-items: center; width: 100%; }}
    
    .hero-badge {{ display: inline-block; padding: 0.5rem 1rem; background: rgba(128,128,128,0.1); border: 1px solid rgba(128,128,128,0.2); border-radius: 50px; font-size: 0.9rem; font-weight: 700; margin-bottom: 1.5rem; color: var(--txt-h); text-transform: uppercase; letter-spacing: 1px; }}
    .hero-btn-group {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
    .btn-outline-light {{ background: transparent; color: var(--txt-h) !important; border: 2px solid var(--txt-h); }}
    .btn-outline-light:hover {{ background: var(--txt-h); color: var(--bg) !important; }}
    
    .modern-hero-visual {{ position: relative; width: 100%; height: 600px; display: flex; align-items: center; justify-content: center; }}
    .visual-frame {{ width: 100%; height: 100%; border-radius: 32px; overflow: hidden; position: relative; z-index: 2; box-shadow: 0 30px 60px rgba(0,0,0,0.15); border: 8px solid var(--card); }}
    .floating-element {{ position: absolute; border-radius: 50%; filter: blur(60px); z-index: 1; opacity: 0.6; }}
    .glow-1 {{ width: 300px; height: 300px; background: var(--p); top: -50px; right: -50px; }}
    .glow-2 {{ width: 250px; height: 250px; background: var(--s); bottom: -50px; left: -50px; }}
    
    /* 2. FLOATING STATS RIBBON */
    .stats-ribbon-container {{ margin-top: -60px; position: relative; z-index: 100; padding: 0 20px; }}
    .stats-ribbon {{ background: var(--card); border-radius: 24px; padding: 3rem; display: flex; justify-content: space-around; align-items: center; box-shadow: var(--shadow); border: var(--border); backdrop-filter: blur(20px); }}
    .stat-block {{ text-align: center; }}
    .stat-block h3 {{ font-size: 3.5rem; color: var(--p); margin-bottom: 0.5rem; line-height: 1; }}
    .stat-block p {{ font-size: 1.1rem; font-weight: 600; color: var(--txt-b); text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; margin: 0; }}
    .stat-divider {{ width: 2px; height: 60px; background: rgba(128,128,128,0.2); }}

    /* 3. BENTO-STYLE FEATURES GRID */
    .section-subtitle {{ font-size: 1.2rem; color: var(--txt-b); opacity: 0.7; margin-top: 1rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }}
    .modern-grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; }}
    .modern-feature-card {{ background: var(--card); padding: 3rem; border-radius: 24px; box-shadow: var(--shadow); border: var(--border); transition: 0.4s; display: flex; flex-direction: column; gap: 1.5rem; }}
    .modern-feature-card:hover {{ transform: translateY(-10px); border-color: var(--p); }}
    .feature-icon-wrapper {{ width: 64px; height: 64px; border-radius: 16px; background: rgba(128,128,128,0.05); display: flex; align-items: center; justify-content: center; color: var(--s); border: 1px solid rgba(128,128,128,0.1); }}
    .feature-content h3 {{ font-size: 1.5rem; margin-bottom: 1rem; color: var(--txt-h); }}
    
    /* 4. PREMIUM ABOUT SECTION */
    .modern-about {{ background: rgba(128,128,128,0.02); overflow: hidden; }}
    .about-visual {{ position: relative; }}
    .about-main-img {{ width: 100%; height: 600px; object-fit: cover; border-radius: 32px; box-shadow: var(--shadow); }}
    .about-experience-badge {{ position: absolute; bottom: -30px; right: -30px; background: var(--p); color: #fff; padding: 2rem; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); display: flex; align-items: center; gap: 1rem; border: 4px solid var(--card); }}
    .about-experience-badge strong {{ font-size: 3rem; line-height: 1; color: #fff; }}
    .about-experience-badge span {{ font-size: 1rem; font-weight: 700; text-transform: uppercase; line-height: 1.2; }}
    .about-lead {{ font-size: 1.25rem; line-height: 1.8; opacity: 0.9; color: var(--txt-b); border-left: 4px solid var(--s); padding-left: 1.5rem; }}
    
    @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    /* LANGUAGE MODAL PHYSICS */
    #lang-overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); z-index: 3000; }}
    #lang-modal {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--card); width: 90%; max-width: 500px; padding: 3rem; border-radius: 24px; box-shadow: 0 30px 60px rgba(0,0,0,0.4); z-index: 3001; border: var(--border); color: var(--txt-b); }}
    #lang-modal h3 {{ margin-bottom: 1.5rem; color: var(--p); font-size: 1.8rem; border-bottom: 1px solid rgba(128,128,128,0.1); padding-bottom: 1rem; text-align:center; }}
    .lang-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
    .lang-opt {{ display: flex; align-items: center; justify-content: center; width: 100%; padding: 1.2rem; border: var(--border); border-radius: 12px; cursor: pointer; font-weight: 700; transition: 0.3s; background: var(--bg); }}
    .lang-opt:hover {{ background: var(--p); color: #fff; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}

    /* TOP PROMO BAR PHYSICS */
    #top-bar {{ position: fixed; top: 0; left: 0; width: 100%; background: var(--s); color: #fff; text-align: center; padding: 12px; z-index: 2005; font-weight: 800; font-size: 0.95rem; letter-spacing: 1px; transition: transform 0.3s; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
    #top-bar a {{ color: #fff !important; text-decoration: none; text-underline-offset: 4px; margin-left: 10px; transition: 0.3s; }}
    #top-bar a:hover {{ opacity: 0.8; }}

    /* DARK MODE TOGGLE PHYSICS */
    #theme-toggle {{ position: fixed; bottom: 30px; left: 30px; width: 50px; height: 50px; background: var(--card); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2); cursor: pointer; z-index: 1000; font-size: 1.5rem; border: var(--border); transition: 0.3s; }}
    #theme-toggle:hover {{ transform: scale(1.1) rotate(15deg); border-color: var(--p); }}

    /* VOICE SEARCH FLOATING PHYSICS */
    #voice-btn {{ 
        position: fixed; 
        bottom: 170px;
        right: 30px; 
        background: var(--p); 
        color: #fff; 
        border-radius: 50%; 
        width: 50px; 
        height: 50px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        font-size: 1.2rem; 
        cursor: pointer; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.2); 
        z-index: 1000; 
        border: 2px solid rgba(255,255,255,0.1);
        transition: 0.3s;
    }}
    #voice-btn:hover {{ transform: scale(1.1); background: var(--s); }}

    /* VOICE LISTENING ANIMATION */
    .listening {{ 
        animation: voice-pulse 1.5s infinite; 
        background: var(--s) !important; 
    }}
    
    @keyframes voice-pulse {{ 
        0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 0, 60, 0.4); }} 
        70% {{ transform: scale(1.2); box-shadow: 0 0 0 20px rgba(255, 0, 60, 0); }} 
        100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 0, 60, 0); }} 
    }}

/* --- SHARE BUTTON & ICON CONSTRAINTS --- */
    .share-row {{ 
        display: flex; 
        gap: 12px; 
        flex-wrap: wrap; 
        align-items: center;
        margin-top: 1.5rem;
    }}

    .share-btn {{ 
        width: 45px !important; 
        height: 45px !important; 
        display: flex !important; 
        align-items: center; 
        justify-content: center; 
        border-radius: 12px; 
        transition: 0.3s;
        text-decoration: none;
    }}

    /* This targets the SVGs specifically to stop them from becoming giant */
    .share-btn svg, .share-row svg {{ 
        width: 22px !important; 
        height: 22px !important; 
        fill: white; 
    }}

    .bg-wa {{ background: #25D366; }}
    .bg-fb {{ background: #1877F2; }}
    .bg-x {{ background: #000000; }}
    .bg-li {{ background: #0A66C2; }}
    .bg-link {{ background: #64748b; }}
    

    /* --- PRODUCT DETAIL SIZE OVERRIDES --- */
    
    /* 1. The Title (The Consultant Pro) */
    .product-info-column h1 {{ 
        font-size: clamp(1.8rem, 3vw, 2.5rem) !important; 
        margin-bottom: 1rem !important;
    }}

    /* 2. The Price ($499) */
    .product-price-tag {{ 
        font-size: 1.4rem !important; 
        padding: 0.4rem 1.2rem !important;
        margin-bottom: 1.5rem !important;
    }}

    /* 3. The Description Text (The Ultimate Industrial...) */
    .product-specs-container, .product-specs-container p {{
        font-size: 1rem !important; 
        line-height: 1.6 !important;
        opacity: 0.8 !important;
    }}
    
    /* Shrink the back button too for balance */
    .back-btn {{
        font-size: 0.75rem !important;
        margin-bottom: 20px !important;
    }}

    /* ==========================================================
       MOBILE OPTIMIZATION (THE FIX)
       ========================================================== */
    @media (max-width: 992px) {{
        /* Nav Menu Collapse Fixed Layering */
        nav#main-navbar .nav-links {{ 
            position: absolute; 
            top: 100%; 
            left: -100%; 
            width: 100vw; 
            height: 100dvh; 
            background: var(--bg); flex-direction: column; padding: 3rem; 
            transition: left 0.4s ease; align-items: center; justify-content: flex-start; 
            gap: 2.5rem; z-index: 1999; overflow-y: auto; 
        }}
        nav#main-navbar .nav-links.active {{ left: 0; }}
        .nav-links a {{ font-size: 1.5rem; }}
        .mobile-menu {{ display: block; }}
        
        /* Grid Breakdowns */
        .about-grid, .detail-view, .grid-3, .modern-grid-3, .contact-grid {{ grid-template-columns: 1fr !important; gap: 3rem; }}
        
        /* Hero Refinements for small screens */
        .modern-hero-grid {{ grid-template-columns: 1fr; text-align: center; }}
        .modern-hero-text {{ text-align: center; align-items: center; justify-content: center; }}
        .hero-btn-group {{ justify-content: center; }}
        .modern-hero-visual {{ height: 400px; }}
        .hero {{ padding-top: 100px; text-align: center; }}
        
        /* Detail View Reset */
        .detail-view {{ padding: 2rem; gap: 2rem; }}
        .product-media-column {{ position: relative; top: 0; margin-bottom: 2rem; }}
        
        /* Stats Ribbon Stacking securely */
        .stats-ribbon {{ flex-direction: column; padding: 2.5rem 1.5rem; gap: 2rem; }}
        .stat-divider {{ width: 100%; height: 2px; }}
        .stats-ribbon-container {{ margin-top: -30px; }}
        
        /* Badges overlapping fixed */
        .about-experience-badge {{ position: relative; bottom: 0; right: 0; margin-top: -30px; margin-left: auto; margin-right: auto; width: fit-content; z-index: 10; }}
        
        .pricing-table th, .pricing-table td {{ padding: 1.2rem 1rem; font-size: 0.95rem; }}
    }}
    
   @media (max-width: 480px) {{
         p {{ 
            text-align: left; /* Optional: We usually switch back to left-align on very narrow screens to prevent 'rivers' of white space */
            hyphens: auto; 
        }}
        /* 1. ELIMINATE THE BLUE GAP & HORIZONTAL GLITCHES */
        html, body {{ 
            width: 100% !important; 
            margin: 0 !important; 
            padding: 0 !important; 
            overflow-x: hidden !important; 
            background: var(--bg); /* Matches background to theme to hide gaps */
        }}

        .container {{ 
            width: 100% !important; 
            max-width: 100% !important; 
            padding: 0 24px !important; /* Proper breathing room for text */
            margin: 0 auto !important;
            box-sizing: border-box !important;
        }}

        /* 2. FOOTER SAFE ZONE (Prevents buttons from covering links) */
        footer {{ 
            padding: 4rem 0 10rem 0 !important; /* Extra bottom padding so you can scroll past the buttons */
        }}
        .footer-grid {{ 
            display: flex !important;
            flex-direction: column !important;
            gap: 3rem !important; 
            text-align: left !important;
        }}

        /* 3. HERO & TEXT SCALING */
        h1, #hero-title, .modern-hero-text h1 {{ 
            font-size: 2.4rem !important; 
            line-height: 1.1 !important; 
            margin-bottom: 1.5rem !important;
        }}
        
        #hero-sub, .modern-hero-text p {{
            font-size: 1.1rem !important; 
            opacity: 0.8;
            margin-bottom: 2.5rem !important;
        }}

        /* 4. BUTTON STACKING */
        .hero-btn-group {{ 
            display: flex; 
            flex-direction: column !important; 
            gap: 12px; 
            width: 100%; 
        }}
        .hero-btn-group .btn {{ width: 100% !important; }}

        /* 5. FLOATING BUTTON TRAFFIC CONTROL (Corner Pinning) */
        /* We move them to 10px from the edge so they don't block the center text */
        #wa-widget {{ 
            bottom: 15px !important; 
            right: 10px !important; 
            scale: 0.8; 
        }}
        #theme-toggle {{ 
            bottom: 15px !important; 
            left: 10px !important; 
            scale: 0.8; 
            background: rgba(255,255,255,0.9); /* Makes toggle stand out on dark footers */
            border: 1px solid rgba(0,0,0,0.1);
        }}
        #cart-float {{ 
            bottom: 80px !important; 
            right: 10px !important; 
            scale: 0.8; 
        }}
        #voice-btn {{ 
            bottom: 140px !important; 
            right: 10px !important; 
            scale: 0.8; 
        }}

        /* 6. COMPONENT FIXES */
        .modern-hero-visual {{ height: 300px !important; margin-top: 2rem !important; }}
        .visual-frame {{ border-width: 4px !important; }}
        .stat-block h3 {{ font-size: 2.8rem !important; }}
        .modern-feature-card {{ padding: 2rem !important; }}
        
        /* Pricing Table Mobile Fix */
        .pricing-table {{ min-width: 100% !important; }}
        .pricing-table th, .pricing-table td {{ padding: 1rem 0.5rem !important; font-size: 0.85rem !important; }}
    }}
    """
