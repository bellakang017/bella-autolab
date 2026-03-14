"""
Build the strategy deck — 3-second rule: big type, big photos, click for detail.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "figures")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "ghost-deck")

def img_b64(name):
    path = os.path.join(FIGURES_DIR, f"{name}.png")
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

C = {k: img_b64(k) for k in [
    "grouped_bar_dvs", "forest_plot", "violin_trust",
    "mediation_diagram", "regression_scatter", "cluster_scatter", "radar_profile"
]}

VI = {
    "miquela": "https://cdn.prod.website-files.com/5d7e8885cad5174a2fcb98d7/64933f9c0c7c9d517168b331_5eddd9f5af2fbd3c05bffc66_virtual-influencer-lil-miquela.jpeg",
    "noonoouri": "https://cdn.prod.website-files.com/5d7e8885cad5174a2fcb98d7/64933f9d5ac24012720d4bea_5eddda6b255e446d17a740f1_virtual-influencer-noonoouri.jpeg",
    "aitana": "https://cdn.prod.website-files.com/5d7e8885cad5174a2fcb98d7/69940c79ea2ff186542d6610_626287245_17966024253009555_2573877171271977039_n.jpeg",
    "bmw": "https://www.brandinginasia.com/wp-content/uploads/2023/10/BMW-and-Lil-Miquela.jpg",
}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Virtual Influencer Strategy</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
    --ink:#1a1a1a;--ink2:#444;--ink3:#888;
    --bg:#fff;--warm:#f7f5f2;--cream:#ede9e3;
    --blue:#1a3a5c;--red:#8b2500;--green:#1a5c3a;
    --rule:#e0e0e0;
    --serif:'Playfair Display',Georgia,serif;
    --sans:'DM Sans',system-ui,sans-serif;
    --mono:'JetBrains Mono',monospace;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-snap-type:y mandatory;scroll-behavior:smooth;}}
body{{font-family:var(--sans);color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased;}}
img{{max-width:100%;height:auto;display:block;}}

/* ─── SLIDE ─── */
.sl{{min-height:100vh;scroll-snap-align:start;position:relative;overflow:hidden;}}
.pg{{position:absolute;bottom:20px;right:32px;font-family:var(--mono);font-size:11px;color:#ccc;}}
.src{{position:absolute;bottom:20px;left:48px;font-family:var(--mono);font-size:9px;color:#bbb;}}

/* ─── 3-SECOND TYPOGRAPHY ─── */
.headline {{
    font-family:var(--serif);
    font-size:clamp(2.2rem,4vw,3.2rem);
    font-weight:500;
    line-height:1.15;
    letter-spacing:-0.02em;
    color:var(--blue);
}}
.headline em {{ font-style:italic; color:var(--red); }}
.subline {{
    font-size:clamp(1rem,1.8vw,1.2rem);
    color:var(--ink2);
    line-height:1.6;
    margin-top:16px;
    max-width:560px;
}}
.label {{
    font-family:var(--mono);
    font-size:11px;
    letter-spacing:0.18em;
    text-transform:uppercase;
    color:var(--blue);
    margin-bottom:16px;
    opacity:0.6;
}}

/* ─── BIG NUMBER ─── */
.bignum {{
    font-family:var(--serif);
    font-weight:600;
    line-height:1;
}}
.bignum--hero {{ font-size:clamp(4rem,8vw,7rem); }}
.bignum--lg {{ font-size:clamp(2.4rem,4vw,3.6rem); }}
.bignum--green {{ color:var(--green); }}
.bignum--red {{ color:var(--red); }}
.bignum-label {{
    font-size:clamp(0.85rem,1.2vw,1rem);
    color:var(--ink3);
    margin-top:4px;
}}

/* ─── SPLIT LAYOUT ─── */
.split {{
    display:grid;
    grid-template-columns:1fr 1fr;
    min-height:100vh;
}}
.split__img {{
    overflow:hidden;
    position:relative;
}}
.split__img img {{
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center center;
}}
.split__text {{
    display:flex;
    flex-direction:column;
    justify-content:center;
    padding:clamp(40px,6vw,80px);
}}

/* ─── FULL-PAD ─── */
.pad {{
    padding:clamp(48px,6vw,80px);
    min-height:100vh;
    display:flex;
    flex-direction:column;
    justify-content:center;
}}

/* ─── TABLE — readable ─── */
.tbl {{
    width:100%;
    border-collapse:collapse;
    margin-top:24px;
}}
.tbl th {{
    font-size:clamp(0.7rem,1vw,0.8rem);
    font-weight:600;
    letter-spacing:0.08em;
    text-transform:uppercase;
    text-align:left;
    padding:14px 20px;
    color:var(--ink3);
    border-bottom:2px solid var(--ink);
}}
.tbl td {{
    padding:16px 20px;
    border-bottom:1px solid var(--rule);
    font-size:clamp(0.9rem,1.2vw,1rem);
    color:var(--ink2);
    vertical-align:middle;
}}
.tbl td:first-child {{ font-weight:500; color:var(--ink); }}
.tag {{
    display:inline-block;
    font-size:clamp(0.7rem,0.9vw,0.8rem);
    font-weight:600;
    padding:4px 14px;
    border-radius:2px;
}}
.tag-y {{ background:#e8f5e9; color:var(--green); }}
.tag-n {{ background:#fbe9e7; color:var(--red); }}
.tag-m {{ background:#fff8e1; color:#8d6e00; }}

/* ─── DO / DON'T ─── */
.verdict {{
    padding:24px 28px;
    border-radius:4px;
    margin-bottom:16px;
}}
.verdict--do {{ background:#f0f7f3; border-left:4px solid var(--green); }}
.verdict--dont {{ background:#fdf2ef; border-left:4px solid var(--red); }}
.verdict h4 {{
    font-size:clamp(0.8rem,1vw,0.9rem);
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:0.1em;
    margin-bottom:10px;
}}
.verdict--do h4 {{ color:var(--green); }}
.verdict--dont h4 {{ color:var(--red); }}
.verdict li {{
    font-size:clamp(0.9rem,1.2vw,1.05rem);
    color:var(--ink2);
    line-height:1.6;
    margin-left:18px;
    margin-bottom:4px;
}}

/* ─── CASE PHOTOS — full height, clickable ─── */
.cases {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    min-height:100vh;
}}
.case {{
    position:relative;
    overflow:hidden;
    cursor:pointer;
}}
.case img {{
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center center;
    transition:transform 0.4s ease;
}}
.case:hover img {{ transform:scale(1.03); }}
.case__overlay {{
    position:absolute;
    bottom:0;
    left:0;
    right:0;
    padding:28px;
    background:linear-gradient(transparent 0%, rgba(0,0,0,0.75) 100%);
    color:#fff;
}}
.case__tag {{
    display:inline-block;
    font-size:0.7rem;
    font-weight:600;
    padding:3px 10px;
    border-radius:2px;
    margin-bottom:8px;
}}
.case__tag--s {{ background:rgba(26,92,58,0.9); }}
.case__tag--f {{ background:rgba(139,37,0,0.9); }}
.case__name {{
    font-family:var(--serif);
    font-size:clamp(1.1rem,1.8vw,1.4rem);
    font-weight:500;
    margin-bottom:4px;
}}
.case__stat {{
    font-size:clamp(0.8rem,1vw,0.95rem);
    opacity:0.8;
}}
/* BMW case — text only, big number */
.case--text {{
    background:var(--cream);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    padding:32px;
}}
.case--text .bignum {{ color:var(--red); }}

/* ─── MODAL ─── */
.modal-bg {{
    display:none;
    position:fixed;
    inset:0;
    background:rgba(0,0,0,0.6);
    z-index:1000;
    align-items:center;
    justify-content:center;
    backdrop-filter:blur(4px);
}}
.modal-bg.open {{ display:flex; }}
.modal {{
    background:#fff;
    max-width:640px;
    width:90%;
    border-radius:6px;
    overflow:hidden;
    box-shadow:0 24px 80px rgba(0,0,0,0.3);
    max-height:90vh;
    overflow-y:auto;
}}
.modal__img {{
    width:100%;
    height:auto;
    max-height:420px;
    object-fit:contain;
    object-position:center center;
    background:var(--warm);
}}
.modal__body {{
    padding:32px;
}}
.modal__body h3 {{
    font-family:var(--serif);
    font-size:1.5rem;
    font-weight:500;
    color:var(--blue);
    margin-bottom:12px;
}}
.modal__body p {{
    font-size:1rem;
    color:var(--ink2);
    line-height:1.7;
    margin-bottom:12px;
}}
.modal__body .meta {{
    font-family:var(--mono);
    font-size:0.75rem;
    color:var(--ink3);
    padding-top:12px;
    border-top:1px solid var(--rule);
}}
.modal__close {{
    position:absolute;
    top:16px;
    right:16px;
    width:36px;
    height:36px;
    background:rgba(0,0,0,0.5);
    color:#fff;
    border:none;
    border-radius:50%;
    font-size:18px;
    cursor:pointer;
    display:flex;
    align-items:center;
    justify-content:center;
}}

/* ─── FUNNEL — visual ─── */
.funnel {{
    display:flex;
    flex-direction:column;
    gap:3px;
    margin-top:32px;
}}
.funnel__row {{
    display:grid;
    grid-template-columns:140px 1fr;
    align-items:center;
    gap:24px;
    padding:24px 32px;
    border-radius:4px;
}}
.funnel__row:nth-child(1) {{ background:#eef2f7; }}
.funnel__row:nth-child(2) {{ background:var(--warm); }}
.funnel__row:nth-child(3) {{ background:#f5efeb; }}
.funnel__stage {{
    font-family:var(--mono);
    font-size:clamp(0.65rem,0.9vw,0.75rem);
    letter-spacing:0.12em;
    text-transform:uppercase;
    color:var(--ink3);
}}
.funnel__content {{
    font-size:clamp(1rem,1.5vw,1.15rem);
    color:var(--ink);
    line-height:1.5;
}}
.funnel__content strong {{ color:var(--blue); }}

/* ─── SEGMENTS ─── */
.segs {{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:16px;
    margin-top:28px;
}}
.seg {{
    border:1px solid var(--rule);
    border-radius:4px;
    padding:28px;
    border-top:4px solid var(--rule);
}}
.seg--1 {{ border-top-color:var(--green); }}
.seg--2 {{ border-top-color:var(--blue); }}
.seg--3 {{ border-top-color:#b8860b; }}
.seg--4 {{ border-top-color:#aaa; }}
.seg h4 {{
    font-family:var(--serif);
    font-size:clamp(1.1rem,1.5vw,1.3rem);
    font-weight:500;
    margin-bottom:8px;
}}
.seg p {{
    font-size:clamp(0.85rem,1.1vw,1rem);
    color:var(--ink3);
    line-height:1.55;
}}

/* ─── TOOLS — visual cards, not table ─── */
.tools {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:16px;
    margin-top:32px;
}}
.tool {{
    border:1px solid var(--rule);
    border-radius:4px;
    padding:24px;
    text-align:center;
    transition:transform 0.2s;
}}
.tool:hover {{ transform:translateY(-2px); box-shadow:0 4px 16px rgba(0,0,0,0.06); }}
.tool__name {{
    font-family:var(--sans);
    font-size:clamp(1rem,1.3vw,1.15rem);
    font-weight:600;
    color:var(--ink);
    margin-bottom:4px;
}}
.tool__what {{
    font-size:clamp(0.8rem,1vw,0.9rem);
    color:var(--ink3);
    margin-bottom:12px;
    line-height:1.4;
}}
.tool__price {{
    font-family:var(--mono);
    font-size:clamp(0.9rem,1.2vw,1.05rem);
    font-weight:500;
    color:var(--blue);
}}

/* ─── HERO CTA ─── */
.hero-cta {{
    display:flex;
    align-items:center;
    gap:16px;
    margin-top:32px;
    padding:16px 20px;
    background:var(--warm);
    border:1px solid var(--rule);
    border-radius:6px;
    text-decoration:none;
    color:var(--ink);
    transition:transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    max-width:480px;
}}
.hero-cta:hover {{
    transform:translateY(-2px);
    box-shadow:0 8px 24px rgba(0,0,0,0.08);
    border-color:var(--blue);
}}
.hero-cta__left {{
    flex:1;
    min-width:0;
}}
.hero-cta__label {{
    display:block;
    font-family:var(--sans);
    font-size:clamp(0.9rem,1.2vw,1.05rem);
    font-weight:600;
    color:var(--blue);
    margin-bottom:2px;
}}
.hero-cta__desc {{
    display:block;
    font-size:clamp(0.7rem,0.9vw,0.8rem);
    color:var(--ink3);
}}
.hero-cta__preview {{
    display:flex;
    gap:4px;
    flex-shrink:0;
}}
.hero-cta__preview img {{
    width:56px;
    height:40px;
    object-fit:cover;
    border-radius:3px;
    border:1px solid var(--rule);
}}
.hero-cta__arrow {{
    flex-shrink:0;
    color:var(--blue);
    opacity:0.5;
    transition:opacity 0.2s, transform 0.2s;
}}
.hero-cta:hover .hero-cta__arrow {{
    opacity:1;
    transform:translateX(4px);
}}

/* ─── CHART FRAME ─── */
.chart {{ border:1px solid var(--rule); border-radius:4px; overflow:hidden; }}
.chart img {{ width:100%; }}

/* ─── CLOSE ─── */
.close {{ background:var(--blue); color:#fff; }}
.close .headline {{ color:#fff; font-size:clamp(1.8rem,3.5vw,2.8rem); }}
.close-nums {{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:16px;
    margin-top:48px;
}}
.close-n {{
    text-align:center;
    padding:24px 16px;
    background:rgba(255,255,255,0.07);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:4px;
}}
.close-n .n {{
    font-family:var(--serif);
    font-size:clamp(2rem,3vw,2.8rem);
    font-weight:600;
    color:rgba(255,255,255,0.85);
}}
.close-n p {{
    font-size:clamp(0.8rem,1vw,0.9rem);
    color:rgba(255,255,255,0.5);
    margin-top:4px;
    line-height:1.4;
}}

/* ─── RESPONSIVE ─── */
@media(max-width:1024px) {{
    .split {{ grid-template-columns:1fr; }}
    .split__img {{ height:45vh; }}
    .cases {{ grid-template-columns:1fr 1fr; }}
    .tools {{ grid-template-columns:1fr 1fr; }}
    .close-nums {{ grid-template-columns:1fr 1fr; }}
    .segs {{ grid-template-columns:1fr; }}
    .pad {{ padding:32px 24px; }}
}}
@media(max-width:600px) {{
    .cases {{ grid-template-columns:1fr; }}
    .tools {{ grid-template-columns:1fr; }}
    .close-nums {{ grid-template-columns:1fr; }}
}}
</style>
</head>
<body>

<!-- ═══ 01 COVER ═══ -->
<section class="sl" id="s1">
    <div class="split">
        <div class="split__img">
            <img src="{VI['miquela']}" alt="Lil Miquela">
        </div>
        <div class="split__text">
            <p class="label">Strategic Recommendation</p>
            <h1 class="headline">When should a brand use a <em>virtual influencer</em>?</h1>
            <p class="subline">A data-driven playbook from a controlled experiment (N=83) and analysis of the $6B virtual influencer market.</p>

            <!-- CTA + Portfolio Preview -->
            <a href="../portfolio/index.html" target="_blank" class="hero-cta">
                <div class="hero-cta__left">
                    <span class="hero-cta__label">Full Research Portfolio</span>
                    <span class="hero-cta__desc">24 analyses &middot; 12 findings &middot; 11 charts &middot; Complete data</span>
                </div>
                <div class="hero-cta__preview">
                    <img src="{C['grouped_bar_dvs']}" alt="Preview">
                    <img src="{C['forest_plot']}" alt="Preview">
                    <img src="{C['mediation_diagram']}" alt="Preview">
                </div>
                <svg class="hero-cta__arrow" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>

            <div style="margin-top:32px;display:flex;gap:40px;">
                <div><p style="font-family:var(--mono);font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:var(--ink3);margin-bottom:2px;">Prepared by</p><p style="font-size:1rem;">Bella Kang</p></div>
                <div><p style="font-family:var(--mono);font-size:10px;letter-spacing:0.15em;text-transform:uppercase;color:var(--ink3);margin-bottom:2px;">Date</p><p style="font-size:1rem;">March 2026</p></div>
            </div>
        </div>
    </div>
    <span class="pg">1</span>
</section>

<!-- ═══ 02 THE PARADOX — big numbers ═══ -->
<section class="sl" id="s2">
    <div class="split">
        <div class="split__text">
            <p class="label">The Paradox</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;">
                <div>
                    <div class="bignum bignum--hero bignum--green">&minus;30%</div>
                    <div class="bignum-label">Cost savings vs human influencer</div>
                </div>
                <div>
                    <div class="bignum bignum--hero bignum--red">&minus;0.39</div>
                    <div class="bignum-label">Trust penalty (5-point scale)</div>
                </div>
            </div>
            <p class="subline" style="margin-top:32px;">VIs are cheaper and drive 3&times; organic engagement &mdash; but sponsored content underperforms because consumers don't trust them the same way.</p>
        </div>
        <div class="split__img" style="background:var(--warm);display:flex;align-items:center;justify-content:center;padding:40px;">
            <div class="chart"><img src="{C['forest_plot']}" alt="Effect Sizes"></div>
        </div>
    </div>
    <span class="src">ADV382 experiment N=83; Gartner; HypeAuditor; Storyclash</span>
    <span class="pg">2</span>
</section>

<!-- ═══ 03 WHERE TO USE ═══ -->
<section class="sl" id="s3">
    <div class="pad">
        <p class="label">Recommendation 1</p>
        <h2 class="headline">Use VIs where attitude drives purchase.<br>Avoid where trust is required.</h2>
        <table class="tbl" style="margin-top:32px;">
            <thead><tr><th>Category</th><th>Fit</th><th>Why</th><th>Action</th></tr></thead>
            <tbody>
                <tr><td>Fashion / Streetwear</td><td><span class="tag tag-y">Deploy</span></td><td>Aesthetic appeal &gt; credibility</td><td>VI as primary endorser</td></tr>
                <tr><td>Gaming / Tech</td><td><span class="tag tag-y">Deploy</span></td><td>Digital-native audience</td><td>VI-first. Samsung model: 126M views</td></tr>
                <tr><td>Beauty / Skincare</td><td><span class="tag tag-m">Hybrid</span></td><td>"Real skin" proof needed</td><td>VI for brand, human for demo</td></tr>
                <tr><td>Food / Beverage</td><td><span class="tag tag-m">Hybrid</span></td><td>Can't demonstrate taste</td><td>VI for awareness only</td></tr>
                <tr><td>Health / Wellness</td><td><span class="tag tag-n">Avoid</span></td><td>Trust mediates purchase (p=.027)</td><td>Human only</td></tr>
                <tr><td>Finance / Insurance</td><td><span class="tag tag-n">Avoid</span></td><td>Maximum trust sensitivity</td><td>Human only</td></tr>
            </tbody>
        </table>
    </div>
    <span class="pg">3</span>
</section>

<!-- ═══ 04 EMOTION > CREDIBILITY ═══ -->
<section class="sl" id="s4">
    <div class="split">
        <div class="split__img" style="background:var(--warm);display:flex;align-items:center;justify-content:center;padding:40px;">
            <div class="chart"><img src="{C['regression_scatter']}" alt="Trust vs PI"></div>
        </div>
        <div class="split__text">
            <p class="label">Recommendation 2</p>
            <h2 class="headline">Lead with <em>feeling</em>, not credibility.</h2>
            <p class="subline">Attitude predicts purchase intent 46% more strongly than trust.</p>
            <div style="margin-top:28px;">
                <div class="verdict verdict--do">
                    <h4>Do</h4>
                    <ul>
                        <li>Entertain first. Make it shareable.</li>
                        <li>Embrace the virtual identity as the hook.</li>
                        <li>Optimize for likeability, not trustworthiness.</li>
                    </ul>
                </div>
                <div class="verdict verdict--dont">
                    <h4>Don't</h4>
                    <ul>
                        <li>"Honest review" or testimonial formats.</li>
                        <li>Making the VI appear human.</li>
                        <li>Copying human influencer templates.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <span class="pg">4</span>
</section>

<!-- ═══ 05 FUNNEL ═══ -->
<section class="sl" id="s5">
    <div class="split">
        <div class="split__text">
            <p class="label">Recommendation 3</p>
            <h2 class="headline">VI for reach. Human for conversion.</h2>
            <div class="funnel">
                <div class="funnel__row">
                    <div class="funnel__stage">Awareness</div>
                    <div class="funnel__content"><strong>Virtual Influencer.</strong> 3&times; engagement. Novelty drives discovery. 30% lower cost.</div>
                </div>
                <div class="funnel__row">
                    <div class="funnel__stage">Consideration</div>
                    <div class="funnel__content"><strong>VI + Human collab.</strong> Human vouches for product. Credibility transfer.</div>
                </div>
                <div class="funnel__row">
                    <div class="funnel__stage">Conversion</div>
                    <div class="funnel__content"><strong>Human influencer.</strong> Reviews, demos, testimonials. Trust required.</div>
                </div>
            </div>
        </div>
        <div class="split__img" style="background:var(--warm);display:flex;flex-direction:column;gap:16px;align-items:center;justify-content:center;padding:32px;">
            <div class="chart"><img src="{C['mediation_diagram']}" alt="Mediation"></div>
            <div class="chart"><img src="{C['grouped_bar_dvs']}" alt="Group Comparison"></div>
        </div>
    </div>
    <span class="pg">5</span>
</section>

<!-- ═══ 06 SEGMENTS ═══ -->
<section class="sl" id="s6">
    <div class="split">
        <div class="split__text">
            <p class="label">Recommendation 4</p>
            <h2 class="headline">4 audiences. 4 strategies.</h2>
            <div class="segs">
                <div class="seg seg--1"><h4 style="color:var(--green);">Believers</h4><p>High trust &amp; PI. Serve aspirational content. Convert directly. Don't over-explain.</p></div>
                <div class="seg seg--2"><h4 style="color:var(--blue);">Curious Skeptics</h4><p>Low trust, high attitude. Highest-value target. Transparency + entertainment = conversion.</p></div>
                <div class="seg seg--3"><h4 style="color:#8d6e00;">Pragmatists</h4><p>Moderate everything. Need proof. Pair VI with human co-sign.</p></div>
                <div class="seg seg--4"><h4 style="color:#aaa;">Resistors</h4><p>Low across the board. Don't waste VI budget here. Human influencers only.</p></div>
            </div>
        </div>
        <div class="split__img" style="background:var(--warm);display:flex;align-items:center;justify-content:center;padding:40px;">
            <div class="chart"><img src="{C['cluster_scatter']}" alt="Segments"></div>
        </div>
    </div>
    <span class="pg">6</span>
</section>

<!-- ═══ 07 CASES — full-bleed photos, click for modal ═══ -->
<section class="sl" id="s7">
    <div class="cases">
        <div class="case" onclick="openModal('m1')">
            <img src="{VI['miquela']}" alt="Lil Miquela Samsung">
            <div class="case__overlay">
                <span class="case__tag case__tag--s">Success</span>
                <div class="case__name">Miquela &times; Samsung</div>
                <div class="case__stat">126M organic views</div>
            </div>
        </div>
        <div class="case" onclick="openModal('m2')">
            <img src="{VI['noonoouri']}" alt="Noonoouri Dior">
            <div class="case__overlay">
                <span class="case__tag case__tag--s">Success</span>
                <div class="case__name">Noonoouri &times; Dior</div>
                <div class="case__stat">130+ luxury collabs</div>
            </div>
        </div>
        <div class="case" onclick="openModal('m3')">
            <img src="{VI['aitana']}" alt="Aitana Lopez">
            <div class="case__overlay">
                <span class="case__tag case__tag--s">Success</span>
                <div class="case__name">Aitana Lopez</div>
                <div class="case__stat">$30K/month revenue</div>
            </div>
        </div>
        <div class="case" onclick="openModal('m4')">
            <img src="{VI['bmw']}" alt="BMW iX2 Lil Miquela">
            <div class="case__overlay">
                <span class="case__tag case__tag--f">Failure</span>
                <div class="case__name">Miquela &times; BMW iX2</div>
                <div class="case__stat">0.6% vs 3.6% engagement</div>
            </div>
        </div>
    </div>
    <span class="pg" style="color:rgba(255,255,255,0.5);">7</span>
</section>

<!-- ═══ 08 TOOLS — visual cards ═══ -->
<section class="sl" id="s8">
    <div class="pad">
        <p class="label">Recommendation 5</p>
        <h2 class="headline">Disclose, and use these tools.</h2>
        <p class="subline">CA AI Transparency Act (Jan 2026). FTC enforcement up 340%. Make "powered by AI" a feature, not a disclaimer.</p>
        <div class="tools">
            <div class="tool">
                <div class="tool__name">Synthesia</div>
                <div class="tool__what">Create VI content</div>
                <div class="tool__price">$29/mo+</div>
            </div>
            <div class="tool">
                <div class="tool__name">HypeAuditor</div>
                <div class="tool__what">Verify engagement</div>
                <div class="tool__price">$299/mo</div>
            </div>
            <div class="tool">
                <div class="tool__name">Optimizely</div>
                <div class="tool__what">A/B test creative</div>
                <div class="tool__price">Enterprise</div>
            </div>
            <div class="tool">
                <div class="tool__name">Brandwatch</div>
                <div class="tool__what">Monitor sentiment</div>
                <div class="tool__price">$800+/mo</div>
            </div>
            <div class="tool">
                <div class="tool__name">CreatorIQ</div>
                <div class="tool__what">FTC compliance</div>
                <div class="tool__price">$2K+/mo</div>
            </div>
            <div class="tool">
                <div class="tool__name">C2PA</div>
                <div class="tool__what">Content labeling</div>
                <div class="tool__price">Free</div>
            </div>
            <div class="tool">
                <div class="tool__name">Dynamic Yield</div>
                <div class="tool__what">Segment targeting</div>
                <div class="tool__price">$35K/yr</div>
            </div>
            <div class="tool" style="background:var(--warm);border-color:var(--blue);">
                <div class="tool__name" style="color:var(--blue);">Total Stack</div>
                <div class="tool__what">Mid-market brand</div>
                <div class="tool__price" style="font-size:clamp(1.1rem,1.5vw,1.3rem);">~$5&ndash;8K/mo</div>
            </div>
        </div>
    </div>
    <span class="pg">8</span>
</section>

<!-- ═══ 09 CLOSE ═══ -->
<section class="sl close" id="s9">
    <div class="pad" style="text-align:center;align-items:center;">
        <p class="label" style="color:rgba(255,255,255,0.35);">The Bottom Line</p>
        <h2 style="font-family:var(--serif);font-size:clamp(2.2rem,4.5vw,3.4rem);font-weight:500;color:#fff;line-height:1.15;max-width:900px;letter-spacing:-0.02em;">
            Virtual influencers save you <span style="color:#5ce6b0;">30% on cost</span>.<br>
            But deploy them wrong and you lose <span style="color:#ff6b4a;">83% of engagement</span>.
        </h2>
        <p style="font-size:clamp(1rem,1.5vw,1.2rem);color:rgba(255,255,255,0.55);margin-top:20px;max-width:600px;">
            Our experiment proved exactly where VIs work and where they don't. These five rules are the difference.
        </p>

        <div class="close-nums" style="margin-top:40px;max-width:900px;">
            <div class="close-n"><div class="n">1</div><p>Right category &mdash; attitude, not trust</p></div>
            <div class="close-n"><div class="n">2</div><p>Emotion first &mdash; likeability over credibility</p></div>
            <div class="close-n"><div class="n">3</div><p>Right funnel &mdash; VI for reach, human for close</p></div>
            <div class="close-n"><div class="n">4</div><p>Right audience &mdash; 4 segments, 4 strategies</p></div>
            <div class="close-n"><div class="n">5</div><p>Own it &mdash; disclosure as brand feature</p></div>
        </div>

        <div style="margin-top:48px;">
            <a href="../portfolio/index.html" target="_blank" style="display:inline-flex;align-items:center;gap:12px;padding:18px 40px;background:#fff;color:var(--blue);font-family:var(--sans);font-size:clamp(1rem,1.3vw,1.15rem);font-weight:600;border-radius:4px;text-decoration:none;transition:transform 0.2s,box-shadow 0.2s;letter-spacing:0.01em;">
                Full research portfolio &amp; data
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
            <p style="font-size:clamp(0.75rem,1vw,0.85rem);color:rgba(255,255,255,0.3);margin-top:16px;">
                24 analyses, 12 findings, 11 visualizations, full methodology transparency, interdisciplinary implications.
            </p>
        </div>

        <div style="margin-top:56px;padding-top:24px;border-top:1px solid rgba(255,255,255,0.1);display:flex;justify-content:space-between;align-items:flex-end;width:100%;max-width:900px;">
            <div style="text-align:left;">
                <p style="font-family:var(--serif);font-size:1.15rem;color:rgba(255,255,255,0.85);">Bella Kang</p>
                <p style="font-size:0.85rem;color:rgba(255,255,255,0.35);margin-top:2px;">ADV 382 &middot; The University of Texas at Austin</p>
            </div>
            <p style="font-size:0.75rem;color:rgba(255,255,255,0.2);font-family:var(--mono);text-align:right;">Controlled experiment N=83<br>24 automated analyses &middot; 12 significant findings<br>March 2026</p>
        </div>
    </div>
    <span class="pg" style="color:rgba(255,255,255,0.2);">9</span>
</section>

<!-- ═══ MODALS — consulting-grade case studies ═══ -->

<!-- MODAL 1: Samsung -->
<div class="modal-bg" id="m1" onclick="closeModal(this)">
    <div class="modal" onclick="event.stopPropagation()" style="max-width:820px;">
        <button class="modal__close" onclick="closeModal(document.getElementById('m1'))">&times;</button>
        <img class="modal__img" src="{VI['miquela']}" alt="Lil Miquela">
        <div class="modal__body">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
                <div>
                    <span class="tag tag-y" style="margin-bottom:8px;">Success</span>
                    <h3>Lil Miquela &times; Samsung Galaxy</h3>
                </div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--ink3);">#TeamGalaxy Campaign</span>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:24px;">
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--green);">126M</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Organic Views</div>
                </div>
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--green);">24M</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Engagements</div>
                </div>
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--blue);">~$10M/yr</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Creator Revenue</div>
                </div>
            </div>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;">Campaign Overview</h4>
            <p>Samsung's #TeamGalaxy campaign paired Lil Miquela with real creators Steve Aoki, Millie Bobby Brown, and Ninja. The strategy positioned Miquela as a peer among human talent &mdash; not a replacement, but a collaborator. The content was entertainment-first: music, lifestyle, and culture, with Samsung Galaxy as the enabling technology.</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;margin-top:20px;">Why It Worked &mdash; Connected to Our Data</h4>
            <p>Tech/entertainment is an <strong>attitude-driven category</strong> (our Recommendation 1). Samsung didn't ask consumers to trust Miquela's product review &mdash; they asked consumers to enjoy the content. This maps directly to our regression finding: attitude (&beta;=0.293) predicts purchase intent more strongly than trust (&beta;=0.200). Samsung optimized the right variable.</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;margin-top:20px;">Strategic Takeaway</h4>
            <p>VIs work when the brand treats them as <strong>entertainment IP</strong>, not as endorsers. Samsung used Miquela at the top of the funnel (awareness) where our data shows VIs excel (3&times; organic engagement), then relied on human creators and retail channels for conversion.</p>

            <div style="margin-top:24px;padding-top:16px;border-top:1px solid var(--rule);">
                <table style="width:100%;font-size:13px;border-collapse:collapse;">
                    <tr><td style="padding:6px 0;color:var(--ink3);width:130px;">Creator</td><td style="padding:6px 0;">Brud / Dapper Labs (acq. 2021, $144.5M valuation)</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Audience</td><td style="padding:6px 0;">2.5M Instagram &middot; 3.4M TikTok &middot; 91 brand collabs in 12 months</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Category</td><td style="padding:6px 0;">Consumer Electronics / Entertainment</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Funnel Stage</td><td style="padding:6px 0;">Top-of-funnel (Awareness)</td></tr>
                </table>
            </div>
            <div style="margin-top:16px;display:flex;gap:12px;">
                <a href="https://shortyawards.com/12th/samsung-teamgalaxy" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Shorty Awards</a>
                <a href="https://www.virtualhumans.org/human/miquela-sousa" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">VirtualHumans.org</a>
                <a href="https://www.marketingdive.com/news/virtual-influencers-gain-traction/728150/" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Marketing Dive</a>
            </div>
        </div>
    </div>
</div>

<!-- MODAL 2: Noonoouri -->
<div class="modal-bg" id="m2" onclick="closeModal(this)">
    <div class="modal" onclick="event.stopPropagation()" style="max-width:820px;">
        <button class="modal__close" onclick="closeModal(document.getElementById('m2'))">&times;</button>
        <img class="modal__img" src="{VI['noonoouri']}" alt="Noonoouri">
        <div class="modal__body">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
                <div>
                    <span class="tag tag-y" style="margin-bottom:8px;">Success</span>
                    <h3>Noonoouri &times; Dior, Balenciaga, Valentino</h3>
                </div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--ink3);">Luxury Fashion</span>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:24px;">
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--green);">130+</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Brand Collaborations</div>
                </div>
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--green);">EUR 771K</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Est. Media Value</div>
                </div>
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--blue);">Warner</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Record Deal (2023)</div>
                </div>
            </div>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;">Campaign Overview</h4>
            <p>Created by German graphic designer Joerg Zuber in 2018, Noonoouri has become the most successful VI in luxury fashion. She recreated Natalie Portman's Dior Rouge campaign, walked virtual fashion weeks, and collaborated with Dior, Balenciaga, Valentino, Versace, and Bulgari. In 2023, she signed with Warner Music &mdash; the first VI to land a major label deal.</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;margin-top:20px;">Why It Worked &mdash; Connected to Our Data</h4>
            <p>Noonoouri's <strong>cartoon aesthetic is the key</strong>. Unlike hyper-realistic VIs (Miquela, Aitana), she can't be mistaken for a real person. This eliminates the "deception" backlash entirely. In our framework: she bypasses the trust question altogether. Luxury fashion is the purest attitude-driven category &mdash; consumers buy aspiration, not endorser credibility. Our data shows attitude (&beta;=0.293) is the stronger driver of purchase intent.</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;margin-top:20px;">Strategic Takeaway</h4>
            <p>The more obviously artificial the VI, the less the trust gap matters. Brands in aspirational categories should consider <strong>stylized, non-photorealistic VIs</strong> &mdash; they get the cost and creative control advantages without triggering consumer distrust. This is the "own it" approach from our Recommendation 5.</p>

            <div style="margin-top:24px;padding-top:16px;border-top:1px solid var(--rule);">
                <table style="width:100%;font-size:13px;border-collapse:collapse;">
                    <tr><td style="padding:6px 0;color:var(--ink3);width:130px;">Creator</td><td style="padding:6px 0;">Joerg Zuber (Germany), independent creator</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Audience</td><td style="padding:6px 0;">400K+ Instagram &middot; Global luxury fashion audience</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Category</td><td style="padding:6px 0;">Luxury Fashion / Music / Entertainment</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Key Insight</td><td style="padding:6px 0;">Non-photorealistic design eliminates trust concerns entirely</td></tr>
                </table>
            </div>
            <div style="margin-top:16px;display:flex;gap:12px;">
                <a href="https://www.virtualhumans.org/human/noonoouri" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">VirtualHumans.org</a>
                <a href="https://www.luxurydaily.com/dior-hopes-to-reach-new-audiences-with-noonouri-tribute/" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Luxury Daily</a>
                <a href="https://www.storyclash.com/blog/en/virtual-influencers/" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Storyclash</a>
            </div>
        </div>
    </div>
</div>

<!-- MODAL 3: Aitana Lopez -->
<div class="modal-bg" id="m3" onclick="closeModal(this)">
    <div class="modal" onclick="event.stopPropagation()" style="max-width:820px;">
        <button class="modal__close" onclick="closeModal(document.getElementById('m3'))">&times;</button>
        <img class="modal__img" src="{VI['aitana']}" alt="Aitana Lopez">
        <div class="modal__body">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
                <div>
                    <span class="tag tag-y" style="margin-bottom:8px;">Success</span>
                    <h3>Aitana Lopez &times; Victoria's Secret, Olaplex</h3>
                </div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--ink3);">Brand-Owned VI Model</span>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:24px;">
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--green);">$30K</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Monthly Revenue</div>
                </div>
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--green);">300K+</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Instagram Followers</div>
                </div>
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--blue);">$0</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">PR Crisis Cost</div>
                </div>
            </div>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;">Campaign Overview</h4>
            <p>Aitana Lopez was created by Spanish agency The Clueless in 2023, explicitly because the founders were "tired of unreliable human influencers." She is a hyper-realistic 25-year-old fitness enthusiast from Barcelona, with brand deals with Victoria's Secret, Olaplex, Intimissimi, Amazon, and Razer. Total estimated revenue: $800K&ndash;$1M. She also serves as Fanvue ambassador, expanding into creator-platform revenue.</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;margin-top:20px;">Why It Worked &mdash; Connected to Our Data</h4>
            <p>Aitana operates in <strong>visual-first, attitude-driven categories</strong>: fashion, fitness, lifestyle. No consumer expects her to have "tried the product." Her value proposition to brands is pure creative control: the agency owns the IP, controls every image, and eliminates the scandal risk entirely. This is the <strong>brand-owned VI model</strong> &mdash; the agency doesn't hire influencers, they build them. Our cost data supports this: brand-owned VIs reduce campaign costs by 30% (Gartner) while eliminating hidden costs (travel, personal management, contract disputes).</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--blue);margin-bottom:8px;margin-top:20px;">Strategic Takeaway</h4>
            <p>The brand-owned model works when: (1) the category is attitude-driven, (2) the brand wants full IP ownership, and (3) the primary risk being mitigated is <strong>human unpredictability</strong>, not consumer trust. Aitana's success proves that "replacing" human influencers is viable &mdash; but only in categories where our data shows trust isn't the purchase driver.</p>

            <div style="margin-top:24px;padding-top:16px;border-top:1px solid var(--rule);">
                <table style="width:100%;font-size:13px;border-collapse:collapse;">
                    <tr><td style="padding:6px 0;color:var(--ink3);width:130px;">Creator</td><td style="padding:6px 0;">The Clueless (Barcelona, Spain)</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Business Model</td><td style="padding:6px 0;">Brand deals + Fanvue subscription + licensing</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Category</td><td style="padding:6px 0;">Fashion / Fitness / Lifestyle</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Key Insight</td><td style="padding:6px 0;">Brand-owned VIs eliminate human unpredictability in attitude-driven categories</td></tr>
                </table>
            </div>
            <div style="margin-top:16px;display:flex;gap:12px;">
                <a href="https://www.virtualhumans.org/human/aitana-lopez" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">VirtualHumans.org</a>
                <a href="https://www.euronews.com/next/2024/12/27/meet-the-first-spanish-ai-model-earning-up-to-10000-per-month" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Euronews</a>
                <a href="https://en.wikipedia.org/wiki/Aitana_L%C3%B3pez" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Wikipedia</a>
            </div>
        </div>
    </div>
</div>

<!-- MODAL 4: BMW (Failure) -->
<div class="modal-bg" id="m4" onclick="closeModal(this)">
    <div class="modal" onclick="event.stopPropagation()" style="max-width:820px;">
        <button class="modal__close" onclick="closeModal(document.getElementById('m4'))">&times;</button>
        <img class="modal__img" src="{VI['bmw']}" alt="BMW iX2 Lil Miquela">
        <div class="modal__body">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
                <div>
                    <span class="tag tag-n" style="margin-bottom:8px;">Failure</span>
                    <h3>Lil Miquela &times; BMW iX2</h3>
                </div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--ink3);">"Make It Real" Campaign</span>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:24px;">
                <div style="background:#fdf2ef;padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--red);">0.6%</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">VI Engagement Rate</div>
                </div>
                <div style="background:var(--warm);padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--green);">3.6%</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Human Engagement</div>
                </div>
                <div style="background:#fdf2ef;padding:16px;border-radius:4px;text-align:center;">
                    <div style="font-family:var(--serif);font-size:1.6rem;font-weight:600;color:var(--red);">&minus;83%</div>
                    <div style="font-size:12px;color:var(--ink3);margin-top:2px;">Performance Gap</div>
                </div>
            </div>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--red);margin-bottom:8px;">Campaign Overview</h4>
            <p>BMW's "Make It Real" campaign for the iX2 electric SUV was produced by creative agency Media.Monks, directed by Stefanie Soho. The film used AI face replacement technology to show Lil Miquela "breaking into the real world" and falling in love with human experiences while driving the iX2. The campaign launched globally across EMEA, APAC, and the US.</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--red);margin-bottom:8px;margin-top:20px;">Why It Failed &mdash; Connected to Our Data</h4>
            <p>Automotive is a <strong>high-ticket, trust-dependent purchase</strong>. The iX2 starts at ~$48,000 &mdash; consumers need to believe the endorser has actually driven the car, felt the steering, experienced the range anxiety. A virtual influencer structurally cannot provide this credibility.</p>
            <p style="margin-top:8px;">Our mediation analysis (Sobel z=&minus;2.21, p=.027) proves that <strong>trust is the causal mechanism</strong> between influencer type and purchase intent. BMW deployed Miquela at the <strong>bottom of the funnel</strong> (conversion-stage content) where our data shows VIs are weakest. The campaign was well-produced &mdash; the failure was strategic, not creative.</p>

            <h4 style="font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--red);margin-bottom:8px;margin-top:20px;">What Should Have Been Done</h4>
            <p>Per our hybrid funnel model (Recommendation 3): use Miquela at <strong>top-of-funnel only</strong> (awareness, brand perception) and transition to human automotive journalists and real owners for product reviews and test drive content. The creative concept was strong &mdash; it just needed to feed into a conversion funnel staffed by humans.</p>

            <div style="margin-top:24px;padding-top:16px;border-top:1px solid var(--rule);">
                <table style="width:100%;font-size:13px;border-collapse:collapse;">
                    <tr><td style="padding:6px 0;color:var(--ink3);width:130px;">Brand</td><td style="padding:6px 0;">BMW Group &middot; iX2 Electric SUV (~$48K MSRP)</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Agency</td><td style="padding:6px 0;">Media.Monks (now Monks) &middot; Director: Stefanie Soho</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Category</td><td style="padding:6px 0;">Automotive (High-ticket, trust-dependent)</td></tr>
                    <tr><td style="padding:6px 0;color:var(--ink3);">Root Cause</td><td style="padding:6px 0;">Wrong funnel stage &times; wrong category = trust gap kills conversion</td></tr>
                </table>
            </div>
            <div style="margin-top:16px;display:flex;gap:12px;">
                <a href="https://www.storyclash.com/blog/en/virtual-influencers/" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Storyclash Analysis</a>
                <a href="https://musebyclios.com/advertising/lil-miquela-gets-a-human-experience-in-the-world-straddling-bmw-ix2/" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Muse by Clio</a>
                <a href="https://www.monks.com/case-studies/bmw-lil-miquela-make-it-real-ai-influencers" target="_blank" style="font-size:12px;color:var(--blue);font-family:var(--mono);">Monks Case Study</a>
            </div>
        </div>
    </div>
</div>

<script>
function openModal(id){{document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}}
function closeModal(el){{el.classList.remove('open');document.body.style.overflow='';}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape')document.querySelectorAll('.modal-bg.open').forEach(m=>closeModal(m));}});
const S=document.querySelectorAll('.sl');
document.addEventListener('keydown',e=>{{
    if(document.querySelector('.modal-bg.open'))return;
    const c=[...S].findIndex(s=>{{const r=s.getBoundingClientRect();return r.top>=-100&&r.top<innerHeight/2;}});
    if(e.key==='ArrowDown'||e.key===' '){{e.preventDefault();if(c<S.length-1)S[c+1].scrollIntoView({{behavior:'smooth'}})}}
    if(e.key==='ArrowUp'){{e.preventDefault();if(c>0)S[c-1].scrollIntoView({{behavior:'smooth'}})}}
}});
</script>
</body>
</html>"""

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
    f.write(html)
print("Done. 9 slides, 4 modals, big type, full-bleed photos.")
