import json
import os
from datetime import datetime

def build_site():
    print("Building TechWitHer site...")

    # 1. Load articles data
    if not os.path.exists("articles.json"):
        print("Error: articles.json not found!")
        return

    with open("articles.json", "r", encoding="utf-8") as f:
        all_articles = json.load(f)

    # 2. Filter articles based on schedule (only show articles whose date <= today)
    today = datetime.now().strftime("%Y-%m-%d")
    published_articles = [
        art for art in all_articles if art["date"] <= today
    ]

    # Sort by date descending (newest first)
    published_articles.sort(key=lambda x: x["date"], reverse=True)

    if not published_articles:
        print("No published articles found for today.")
        return

    # Split into Latest Drop (first item) and Recent Lineup (the rest)
    latest_drop = published_articles[0]
    recent_lineup = published_articles[1:4] # Up to 3 recent items
    trending_stories = published_articles[:3] # Top 3 for sidebar

    # 3. Generate index.html
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FX6490W6T7"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-FX6490W6T7');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechWitHer | Modern Tech, Science & Culture</title>
    <link rel="icon" type="image/svg+xml" href="techwither.svg">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="site-wrapper">
        <div class="top-ticker">
            <span>TECHWITHER JOURNAL</span>
            <div>LIVE ANALYTICS ACTIVE &bull; <span>EST. 2026</span></div>
        </div>

        <header class="site-header">
            <a href="index.html" class="brand-box">TECHWITHER<span>.</span></a>
            <p class="subtitle">The unapologetic digital journal on tech, science, and how it actually messes with our lives.</p>
            
            <nav class="categories">
                <a href="index.html" class="category-tag">Home</a>
                <a href="archive.html" class="category-tag">Full Archive</a>
                <a href="archive.html#ai" class="category-tag">AI & Machine Learning</a>
                <a href="archive.html#gadgets" class="category-tag">Gadgets & Hardware</a>
                <a href="archive.html#software" class="category-tag">Software & Digital Life</a>
                <a href="archive.html#robotics" class="category-tag">Robotics & Future Tech</a>
                <a href="archive.html#reviews" class="category-tag">Reviews & Verdicts</a>
            </nav>
        </header>

        <main class="main-grid">
            <section class="latest-section">
                <div class="drop-header">
                    <span class="live-dot"></span>
                    <h2>Latest Drop</h2>
                </div>

                <!-- Latest Article -->
                <article class="featured-card" style="padding: 1.5rem; margin-bottom: 2.5rem; box-shadow: 5px 5px 0px var(--dark); display: flex; gap: 1.5rem; align-items: center;">
                    <img src="{latest_drop['thumbnail']}" alt="{latest_drop['title']}" style="width: 140px; height: 100px; object-fit: cover; border: 1px solid var(--dark); flex-shrink: 0;" onerror="this.style.display='none'">
                    <div>
                        <div class="card-meta">
                            <span class="highlight">{latest_drop['category']}</span> &bull; {latest_drop['date']}
                        </div>
                        <h2 style="font-size: 1.4rem; font-weight: 900; margin-bottom: 0.4rem;">
                            <a href="{latest_drop['filename']}" style="color: var(--dark); text-decoration: none;">{latest_drop['title']}</a>
                        </h2>
                        <p class="card-snippet" style="font-size: 0.95rem; margin-bottom: 0.8rem; line-height: 1.4;">
                            {latest_drop['snippet']}
                        </p>
                        <a href="{latest_drop['filename']}" class="read-more-btn" style="padding: 0.4rem 1rem; font-size: 0.75rem;">Read Full Article &rarr;</a>
                    </div>
                </article>

                <!-- Recent Lineup -->
                <div class="drop-header" style="margin-top: 1rem;">
                    <h2>Recent Lineup</h2>
                </div>
"""

    for art in recent_lineup:
        index_html += f"""
                <div class="featured-card" style="padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 3px 3px 0px var(--dark); display: flex; gap: 1.5rem; align-items: center;">
                    <img src="{art['thumbnail']}" alt="{art['title']}" style="width: 120px; height: 80px; object-fit: cover; border: 1px solid var(--dark); flex-shrink: 0;" onerror="this.style.display='none'">
                    <div>
                        <div class="card-meta">
                            <span class="highlight">{art['category']}</span> &bull; <span class="date">{art['date']}</span>
                        </div>
                        <h3 style="font-size: 1.3rem; font-weight: 900; margin-bottom: 0.4rem;">
                            <a href="{art['filename']}" style="color: var(--dark); text-decoration: none;">{art['title']}</a>
                        </h3>
                        <p class="card-snippet" style="font-size: 0.9rem; margin-bottom: 0.8rem; line-height: 1.4;">{art['snippet']}</p>
                        <a href="{art['filename']}" class="read-more-btn" style="padding: 0.3rem 0.8rem; font-size: 0.7rem;">Read Article &rarr;</a>
                    </div>
                </div>
"""

    index_html += """
            </section>

            <!-- Sidebar -->
            <aside class="sidebar">
                <div class="drop-header">
                    <h2>Trending Stories</h2>
                </div>
"""
    for art in trending_stories:
        index_html += f"""
                <div class="sidebar-card">
                    <span class="sidebar-tag">{art['category']}</span>
                    <h3><a href="{art['filename']}" style="color: var(--dark); text-decoration: none;">{art['title']}</a></h3>
                </div>
"""

    index_html += """
            </aside>
        </main>

        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Independent Tech Journalism</p>
        </footer>
    </div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("index.html generated successfully.")

    # 4. Generate archive.html (Structured by category pillars)
    archive_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FX6490W6T7"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-FX6490W6T7');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Full Archive | TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="techwither.svg">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="site-wrapper">
        <div class="top-ticker">
            <span>TECHWITHER JOURNAL</span>
            <div>LIVE ANALYTICS ACTIVE &bull; <span>EST. 2026</span></div>
        </div>

        <header class="site-header">
            <a href="index.html" class="brand-box">TECHWITHER<span>.</span></a>
            <p class="subtitle">The unapologetic digital journal on tech, science, and how it actually messes with our lives.</p>
            
            <nav class="categories">
                <a href="index.html" class="category-tag">&larr; Back to Home</a>
                <a href="archive.html" class="category-tag" style="color: var(--accent);">Full Archive</a>
            </nav>
        </header>

        <main class="main-grid" style="grid-template-columns: 1fr;">
            <section class="latest-section">
                <div class="drop-header">
                    <span class="live-dot"></span>
                    <h2>Complete Article Archive & Categorized Repository</h2>
                </div>
"""

    # Group articles by category pillars
    pillars = [
        "AI & Machine Learning",
        "Gadgets & Hardware",
        "Software & Digital Life",
        "Robotics & Future Tech",
        "Reviews & Verdicts"
    ]

    for pillar in pillars:
        pillar_slug = pillar.lower().replace(" & ", "-").replace(" ", "-")
        pillar_articles = [art for art in published_articles if art.get('category') == pillar]
        
        archive_html += f"""
                <div id="{pillar_slug}" class="featured-card" style="padding: 2rem; margin-bottom: 2rem;">
                    <h3 style="font-size: 1.4rem; font-weight: 900; border-bottom: 2px solid var(--dark); padding-bottom: 0.5rem; margin-bottom: 1rem; color: var(--dark);">{pillar}</h3>
"""
        if pillar_articles:
            archive_html += '<ul style="list-style-type: none; padding: 0; line-height: 2.2;">'
            for art in pillar_articles:
                archive_html += f"""
                        <li style="border-bottom: 1px solid #eee; padding-bottom: 0.75rem; margin-bottom: 0.75rem;">
                            <span class="date" style="font-weight: 700; color: #666; margin-right: 1rem;">{art['date']}</span> 
                            <a href="{art['filename']}" style="color: var(--dark); font-weight: 800; text-decoration: none;">{art['title']}</a>
                        </li>
"""
            archive_html += '</ul>'
        else:
            archive_html += '<p style="color: #666; font-style: italic;">No articles published in this category yet. Stay tuned.</p>'

        archive_html += '</div>'

    archive_html += """
            </section>
        </main>

        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Independent Tech Journalism</p>
        </footer>
    </div>
</body>
</html>
"""

    with open("archive.html", "w", encoding="utf-8") as f:
        f.write(archive_html)
    print("archive.html generated successfully with strict pillar sections.")

if __name__ == "__main__":
    build_site()