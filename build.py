import json
import os

# Load articles metadata
with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Sort articles by date descending (newest first)
articles.sort(key=lambda x: x["date"], reverse=True)

# Define the 5 Locked Pillars
CATEGORIES = [
    "AI & Machine Learning",
    "Gadgets & Hardware",
    "Software & Digital Life",
    "Robotics & Future Tech",
    "Reviews & Verdicts"
]

def get_nav_html(active_cat="Home"):
    nav_html = f'<a href="index.html" class="{"active" if active_cat == "Home" else ""}">Home</a>\n'
    for cat in CATEGORIES:
        prefix = "../../" if active_cat != "Home" else ""
        cat_path = f"{prefix}articles/Categories/{cat}/index.html"
        is_active = 'class="active" style="color: var(--tw-red);"' if active_cat == cat else ''
        nav_html += f'        <a href="{cat_path}" {is_active}>{cat}</a>\n'
    return nav_html

# 1. BUILD CATEGORY LANDING PAGES
for cat in CATEGORIES:
    cat_dir = os.path.join("articles", "Categories", cat)
    os.makedirs(cat_dir, exist_ok=True)
    
    cat_articles = [a for a in articles if a["category"] == cat]
    
    articles_html = ""
    for art in cat_articles:
        snippet_text = art.get('snippet', 'Explore the full article on TechWitHer.')
        articles_html += f"""
        <div class="article-card">
            <div class="flex-with-thumb">
                <div class="thumb-small"><img src="../../../{art['thumbnail']}" alt="{art['title']}"></div>
                <div>
                    <span class="tag-meta">{art['category']} &bull; {art['date']}</span>
                    <h3><a href="../../../{art['filename']}">{art['title']}</a></h3>
                    <p class="snippet">{snippet_text}</p>
                </div>
            </div>
        </div>
        """
    
    if not cat_articles:
        articles_html = "<p>No articles published in this category yet. Check back soon!</p>"

    cat_page_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat} | TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="../../../techwither.svg">
    <link rel="stylesheet" href="../../../style.css">
    <style>
        :root {{ --tw-red: #e60000; --tw-black: #000000; --tw-gray: #757575; --tw-border: #111111; }}
        body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: var(--tw-black); background: #fff; line-height: 1.5; }}
        .top-ticker {{ background: var(--tw-black); color: #fff; font-size: 0.75rem; font-weight: 700; padding: 6px 20px; display: flex; justify-content: space-between; text-transform: uppercase; }}
        .top-ticker span {{ color: var(--tw-red); }}
        .site-header {{ border-bottom: 3px solid var(--tw-border); padding: 1.2rem 2rem 0.8rem 2rem; }}
        .brand-logo {{ font-size: 2.8rem; font-weight: 900; letter-spacing: -1.5px; text-decoration: none; color: var(--tw-black); font-family: monospace; }}
        .brand-logo span {{ color: var(--tw-red); }}
        .nav-bar {{ border-bottom: 1px solid var(--tw-border); background: #fff; padding: 0 2rem; }}
        .nav-container {{ max-width: 1400px; margin: 0 auto; display: flex; gap: 2rem; overflow-x: auto; white-space: nowrap; padding: 0.7rem 0; }}
        .nav-container a {{ text-decoration: none; color: var(--tw-black); font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; }}
        .nav-container a:hover, .nav-container a.active {{ color: var(--tw-red); }}
        .container {{ max-width: 1000px; margin: 2rem auto; padding: 0 2rem; }}
        .section-header-bar {{ background: var(--tw-black); color: #fff; font-size: 0.75rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.2px; padding: 6px 12px; display: inline-block; margin-bottom: 1.5rem; }}
        .article-card {{ margin-bottom: 1.8rem; padding-bottom: 1.8rem; border-bottom: 1px solid #eaeaea; }}
        .tag-meta {{ font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; color: var(--tw-red); display: block; margin-bottom: 0.3rem; }}
        h3 a {{ color: var(--tw-black); text-decoration: none; font-weight: 900; }}
        h3 a:hover {{ color: var(--tw-red); }}
        .snippet {{ font-size: 0.95rem; color: #333; margin-top: 0.4rem; }}
        .thumb-small {{ width: 110px; height: 80px; background: #111; flex-shrink: 0; overflow: hidden; }}
        .thumb-small img {{ width: 100%; height: 100%; object-fit: cover; }}
        .flex-with-thumb {{ display: flex; gap: 1rem; align-items: flex-start; }}
        footer {{ background: var(--tw-black); color: #fff; padding: 3rem 2rem; margin-top: 4rem; text-align: center; font-size: 0.85rem; }}
        footer p {{ margin: 0.4rem 0; color: #aaa; }}
    </style>
</head>
<body>
    <div class="top-ticker"><div>TECHWITHER REPOSITORY &bull; <span>CATEGORY ARCHIVE</span></div><div>EST. 2026</div></div>
    <header class="site-header"><div style="max-width: 1400px; margin: 0 auto;"><a href="../../../index.html" class="brand-logo">TECHWITHER<span>.</span></a></div></header>
    <nav class="nav-bar"><div class="nav-container">{get_nav_html(cat)}</div></nav>
    <main class="container">
        <div class="section-header-bar">Category: {cat}</div>
        {articles_html}
    </main>
    <footer>
        <div style="font-family: monospace; font-size: 1.2rem; font-weight: 900; margin-bottom: 0.5rem;">TECHWITHER<span>.</span></div>
        <p>&copy; 2026 TechWitHer. All rights reserved.</p>
    </footer>
</body>
</html>
"""
    with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(cat_page_content)

# 2. BUILD MAIN INDEX.HTML
lead_article = next((a for a in articles if a.get("lead_feature")), articles[0])
latest_articles = [a for a in articles if a != lead_article][:2]
grid_articles = articles[3:6] if len(articles) > 3 else articles[:3]

def render_article_card_small(art):
    return f"""
    <div class="article-card">
        <div class="flex-with-thumb">
            <div class="thumb-small"><img src="{art['thumbnail']}" alt="{art['title']}"></div>
            <div>
                <a href="articles/Categories/{art['category']}/index.html" class="tag-meta">{art['category']} <span>&bull; {art['date']}</span></a>
                <h3 style="font-size: 1rem; line-height: 1.2;"><a href="{art['filename']}">{art['title']}</a></h3>
            </div>
        </div>
    </div>
    """

latest_drops_html = "".join([render_article_card_small(a) for a in latest_articles])

lead_snippet = lead_article.get('snippet', 'Explore the full feature on TechWitHer.')

index_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FX6490W6T7"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-FX6490W6T7');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechWitHer | The Digital Repository on Tech & Future Engineering</title>
    <link rel="icon" type="image/svg+xml" href="techwither.svg">
    <link rel="stylesheet" href="style.css">
    <style>
        :root {{ --tw-red: #e60000; --tw-black: #000000; --tw-gray: #757575; --tw-border: #111111; }}
        body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: var(--tw-black); background: #ffffff; line-height: 1.5; }}
        .top-ticker {{ background: var(--tw-black); color: #fff; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; padding: 6px 20px; display: flex; justify-content: space-between; text-transform: uppercase; }}
        .top-ticker span {{ color: var(--tw-red); }}
        .site-header {{ border-bottom: 3px solid var(--tw-border); padding: 1.2rem 2rem 0.8rem 2rem; background: #fff; }}
        .header-container {{ max-width: 1400px; margin: 0 auto; display: flex; align-items: baseline; justify-content: space-between; }}
        .brand-logo {{ font-size: 2.8rem; font-weight: 900; letter-spacing: -1.5px; text-decoration: none; color: var(--tw-black); font-family: monospace; }}
        .brand-logo span {{ color: var(--tw-red); }}
        .nav-bar {{ border-bottom: 1px solid var(--tw-border); background: #fff; padding: 0 2rem; }}
        .nav-container {{ max-width: 1400px; margin: 0 auto; display: flex; gap: 2rem; overflow-x: auto; white-space: nowrap; padding: 0.7rem 0; }}
        .nav-container a {{ text-decoration: none; color: var(--tw-black); font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; transition: color 0.1s ease; }}
        .nav-container a:hover, .nav-container a.active {{ color: var(--tw-red); }}
        .container {{ max-width: 1400px; margin: 2rem auto; padding: 0 2rem; }}
        .wire-grid-lead {{ display: grid; grid-template-columns: 2fr 1fr; gap: 2.5rem; padding-bottom: 2.5rem; border-bottom: 1px solid var(--tw-border); }}
        @media (max-width: 900px) {{ .wire-grid-lead {{ grid-template-columns: 1fr; }} }}
        .article-card {{ margin-bottom: 1.8rem; padding-bottom: 1.8rem; border-bottom: 1px solid #eaeaea; }}
        .article-card:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .tag-meta {{ font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; color: var(--tw-red); text-decoration: none; margin-bottom: 0.3rem; display: inline-block; }}
        .tag-meta span {{ color: var(--tw-gray); font-weight: 600; }}
        .article-card h2, .article-card h3 {{ margin: 0.3rem 0 0.5rem 0; font-weight: 900; letter-spacing: -0.5px; }}
        .article-card h2 a, .article-card h3 a {{ color: var(--tw-black); text-decoration: none; }}
        .article-card h2 a:hover, .article-card h3 a:hover {{ color: var(--tw-red); }}
        .lead-headline {{ font-size: 2.3rem; line-height: 1.1; }}
        .sub-headline {{ font-size: 1.2rem; line-height: 1.25; }}
        .snippet {{ font-size: 0.95rem; color: #333; margin-bottom: 0.6rem; line-height: 1.4; }}
        .thumb-container {{ width: 100%; height: 220px; background: #111; margin-bottom: 1rem; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
        .thumb-container img {{ width: 100%; height: 100%; object-fit: cover; }}
        .thumb-small {{ width: 90px; height: 70px; background: #111; flex-shrink: 0; overflow: hidden; }}
        .thumb-small img {{ width: 100%; height: 100%; object-fit: cover; }}
        .flex-with-thumb {{ display: flex; gap: 1rem; align-items: flex-start; }}
        .section-header-bar {{ background: var(--tw-black); color: #fff; font-size: 0.75rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1.2px; padding: 6px 12px; display: inline-block; margin-bottom: 1.5rem; }}
        .three-col-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 2px solid var(--tw-border); }}
        @media (max-width: 1000px) {{ .three-col-grid {{ grid-template-columns: 1fr; }} }}
        footer {{ background: var(--tw-black); color: #fff; padding: 3rem 2rem; margin-top: 4rem; text-align: center; font-size: 0.85rem; }}
        footer p {{ margin: 0.4rem 0; color: #aaa; }}
    </style>
</head>
<body>
    <div class="top-ticker"><div>TECHWITHER REPOSITORY &bull; <span>LIVE EDITORIAL</span></div><div>EST. 2026</div></div>
    <header class="site-header">
        <div class="header-container">
            <a href="index.html" class="brand-logo">TECHWITHER<span>.</span></a>
            <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; display: none; @media(min-width: 768px){display: block;}">
                The Uncompromising Digital Repository on Tech & Future Engineering
            </div>
        </div>
    </header>
    <nav class="nav-bar"><div class="nav-container">{get_nav_html("Home")}</div></nav>
    <main class="container">
        <div class="wire-grid-lead">
            <div>
                <div class="section-header-bar">Lead Feature</div>
                <div class="article-card" style="border: none; padding: 0; margin: 0;">
                    <div class="thumb-container"><img src="{lead_article['thumbnail']}" alt="{lead_article['title']}"></div>
                    <a href="articles/Categories/{lead_article['category']}/index.html" class="tag-meta">{lead_article['category']} <span>&bull; {lead_article['date']}</span></a>
                    <h2 class="lead-headline"><a href="{lead_article['filename']}">{lead_article['title']}</a></h2>
                    <p class="snippet" style="font-size: 1.05rem; margin-top: 0.8rem;">{lead_snippet}</p>
                    <a href="{lead_article['filename']}" style="font-size: 0.8rem; font-weight: 900; text-transform: uppercase; color: var(--tw-black); text-decoration: none; letter-spacing: 0.5px;">Read Full Feature &rarr;</a>
                </div>
            </div>
            <div>
                <div class="section-header-bar">Latest Drop</div>
                {latest_drops_html}
            </div>
        </div>
        <div class="three-col-grid">
"""

for art in grid_articles[:3]:
    grid_snippet = art.get('snippet', 'Read the full article on TechWitHer.')
    index_html_content += f"""
            <div>
                <div class="section-header-bar">{art['category']}</div>
                <div class="article-card">
                    <div class="thumb-container" style="height: 140px;"><img src="{art['thumbnail']}" alt="{art['title']}"></div>
                    <a href="articles/Categories/{art['category']}/index.html" class="tag-meta">{art['category']} <span>&bull; {art['date']}</span></a>
                    <h3 class="sub-headline"><a href="{art['filename']}">{art['title']}</a></h3>
                    <p class="snippet">{grid_snippet}</p>
                    <a href="{art['filename']}" style="font-size: 0.75rem; font-weight: 900; text-transform: uppercase; color: var(--tw-red); text-decoration: none;">Read Article &rarr;</a>
                </div>
            </div>
    """

index_html_content += f"""
        </div>
    </main>
    <footer>
        <div style="font-family: monospace; font-size: 1.2rem; font-weight: 900; margin-bottom: 0.5rem;">TECHWITHER<span>.</span></div>
        <p>The uncompromising repository on technology, intelligence, and future engineering.</p>
        <p style="margin-top: 1.5rem; color: #666; font-size: 0.75rem;">&copy; 2026 TechWitHer. All rights reserved.</p>
    </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html_content)

print("Static site build complete! Your JSON files were read successfully.")