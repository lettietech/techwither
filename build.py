import os
import json

def build_site():
    print("Building TechWitHer Magazine...")

    # Ensure required directories exist
    os.makedirs("categories", exist_ok=True)
    os.makedirs("posts", exist_ok=True)

    # Load real articles data
    if os.path.exists("articles.json"):
        with open("articles.json", "r", encoding="utf-8") as f:
            articles = json.load(f)
        print(f" Loaded {len(articles)} article(s) from articles.json.")
    else:
        print(" [WARNING] articles.json not found yet. Create it when you're ready to add posts!")
        articles = []

    # 1. Build Homepage Feed (index.html)
    cards_html = ""
    if articles:
        for art in articles:
            cards_html += f"""
        <div class="article-card">
            <div class="thumbnail-wrapper">
                <img src="{art['thumbnail']}" alt="{art['title']}">
            </div>
            <div class="meta">{art['category']} • {art['date']}</div>
            <h2><a href="posts/{art['slug']}.html">{art['title']}</a></h2>
            <p>{art['summary']}</p>
        </div>
        """
    else:
        cards_html = "<p style='color: #666;'>No articles published yet. Add your first post to articles.json!</p>"

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechWitHer - The Digital Tech Magazine</title>
    <link rel="icon" type="image/svg+xml" href="techwither.svg">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="index.html" class="active">Home</a>
                <a href="categories/Artificial Intelligence & Practical Automation.html">AI</a>
                <a href="categories/Consumer Tech & Hardware Reviews.html">Hardware</a>
                <a href="categories/Software, Apps & Digital Tools.html">Software</a>
            </nav>
        </header>

        <main>
            <section class="magazine-grid">
                {cards_html}
            </section>
        </main>

        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Built Clean. Zero Bloat.</p>
        </footer>
    </div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print(" Homepage (index.html) generated successfully.")

    # 2. Build Individual Post Pages
    for art in articles:
        post_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{art['title']} - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="../techwither.svg">
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="../index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="../index.html">Home</a>
            </nav>
        </header>
        
        <main style="max-width: 750px; margin: 0 auto;">
            <article>
                <div class="meta" style="margin-bottom: 1rem;">{art['category']} • {art['date']}</div>
                <h1 style="font-size: 2.5rem; font-weight: 900; line-height: 1.15; margin-bottom: 1.5rem; letter-spacing: -1px;">{art['title']}</h1>
                
                <div class="thumbnail-wrapper" style="margin-bottom: 2rem;">
                    <img src="../{art['thumbnail']}" alt="{art['title']}">
                </div>

                <div class="content" style="font-size: 1.15rem; line-height: 1.8; color: #222222;">
                    {art['content']}
                </div>
            </article>
        </main>

        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Tech Magazine</p>
        </footer>
    </div>
</body>
</html>
"""
        with open(f"posts/{art['slug']}.html", "w", encoding="utf-8") as pf:
            pf.write(post_html)

    if articles:
        print(" All individual article pages generated successfully under /posts/")

    print(" Build process complete!")

if __name__ == "__main__":
    build_site()