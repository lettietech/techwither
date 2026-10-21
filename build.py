import os
import json
from datetime import datetime
import shutil

def build_site():
    # 1. Load articles from articles.json
    try:
        with open('articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("articles.json not found. Creating a blank list.")
        articles = []

    # Map category names to their respective folders and filenames
    category_config = {
        "Artificial Intelligence & Practical Automation": {
            "folder": "AI",
            "filename": "Artificial Intelligence & Practical Automation.html",
            "nav_title": "AI"
        },
        "Consumer Tech & Hardware Reviews": {
            "folder": "Hardware",
            "filename": "Consumer Tech & Hardware Reviews.html",
            "nav_title": "Hardware"
        },
        "Software, Apps & Digital Tools": {
            "folder": "Software",
            "filename": "Software, Apps & Digital Tools.html",
            "nav_title": "Software"
        }
    }

    # If articles.json is empty, clean out old category folders to start fresh
    if not articles:
        if os.path.exists("categories"):
            shutil.rmtree("categories")
        print("articles.json is empty. Cleared old category files for a fresh start.")

    # 2. Sort articles chronologically (Newest to Oldest based on 'date') if any exist
    if articles:
        articles.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)

    # Helper function to generate clean, text-first article cards (no image dependency)
    def generate_cards(article_list):
        cards = ""
        for article in article_list:
            cat_name = article['category']
            folder = category_config.get(cat_name, {"folder": "AI"})["folder"]
            post_link = f"/categories/{folder}/{article['slug']}.html"

            cards += f'''
                <article class="article-card">
                    <div class="meta">{cat_name} &bull; {article['date']}</div>
                    <h2><a href="{post_link}">{article['title']}</a></h2>
                    <p>{article['excerpt']}</p>
                </article>'''
        return cards

    # 3. Build Homepage (index.html)
    home_cards = generate_cards(articles)
    
    index_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechWitHer - The Digital Tech Magazine</title>
    <link rel="icon" type="image/svg+xml" href="techwither.svg">
    <link rel="stylesheet" href="style.css">

    <!-- Google AdSense Code -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <!-- Magazine Header -->
        <header>
            <a href="/index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="/index.html" class="active">Home</a>
                <a href="/categories/AI/Artificial Intelligence & Practical Automation.html">AI</a>
                <a href="/categories/Hardware/Consumer Tech & Hardware Reviews.html">Hardware</a>
                <a href="/categories/Software/Software, Apps & Digital Tools.html">Software</a>
            </nav>
        </header>

        <!-- Main Content Feed -->
        <main>
            <section class="magazine-grid">
{home_cards if home_cards else '<p style="color: #666; font-size: 1.1rem; padding: 2rem 0;">No articles published yet. Check back soon for deep-dive technical insights.</p>'}
            </section>
        </main>

        <!-- Footer -->
        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Searched By Her</p>
        </footer>
    </div>
</body>
</html>
'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)

    # 4. Build Individual Article Pages & Category Archives (Only if articles exist)
    if articles:
        for article in articles:
            cat_name = article['category']
            config = category_config.get(cat_name, category_config["Artificial Intelligence & Practical Automation"])
            folder = config["folder"]
            
            article_content_html = article.get('content', f"<p>{article['excerpt']}</p>")
            
            post_page_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="../../techwither.svg">
    <link rel="stylesheet" href="../../style.css">

    <!-- Google AdSense Code -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <!-- Magazine Header -->
        <header>
            <a href="/index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="/index.html">Home</a>
                <a href="/categories/AI/Artificial Intelligence & Practical Automation.html" class="{'active' if folder=='AI' else ''}">AI</a>
                <a href="/categories/Hardware/Consumer Tech & Hardware Reviews.html" class="{'active' if folder=='Hardware' else ''}">Hardware</a>
                <a href="/categories/Software/Software, Apps & Digital Tools.html" class="{'active' if folder=='Software' else ''}">Software</a>
            </nav>
        </header>

        <!-- Main Article Content -->
        <main>
            <article class="post-content">
                <h1>{article['title']}</h1>
                <p class="post-meta">{article['category']} &bull; {article['date']}</p>
                
                <!-- Top AdSense Unit -->
                <div class="adsense-unit" style="margin: 1.5rem 0; text-align: center;">
                    <ins class="adsbygoogle"
                         style="display:block"
                         data-ad-client="ca-pub-3209789109672774"
                         data-ad-slot="1234567890"
                         data-ad-format="auto"
                         data-full-width-responsive="true"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                </div>

                {article_content_html}
            </article>
        </main>

        <!-- Footer -->
        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Searched By Her</p>
        </footer>
    </div>
</body>
</html>
'''
            os.makedirs(f"categories/{folder}", exist_ok=True)
            with open(f"categories/{folder}/{article['slug']}.html", 'w', encoding='utf-8') as f:
                f.write(post_page_content)

        # 5. Build Category Archive Pages Automatically
        for cat_name, config in category_config.items():
            folder = config["folder"]
            filename = config["filename"]
            
            cat_articles = [a for a in articles if a['category'] == cat_name]
            cat_cards = generate_cards(cat_articles)

            cat_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_name} - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="../../techwither.svg">
    <link rel="stylesheet" href="../../style.css">

    <!-- Google AdSense Code -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <!-- Magazine Header -->
        <header>
            <a href="/index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="/index.html">Home</a>
                <a href="/categories/AI/Artificial Intelligence & Practical Automation.html" class="{'active' if folder=='AI' else ''}">AI</a>
                <a href="/categories/Hardware/Consumer Tech & Hardware Reviews.html" class="{'active' if folder=='Hardware' else ''}">Hardware</a>
                <a href="/categories/Software/Software, Apps & Digital Tools.html" class="{'active' if folder=='Software' else ''}">Software</a>
            </nav>
        </header>

        <!-- Main Content Feed -->
        <main>
            <h1 style="margin-bottom: 2rem; font-size: 1.8rem; border-bottom: 2px solid #000; padding-bottom: 0.5rem;">{cat_name}</h1>
            <section class="magazine-grid">
{cat_cards if cat_cards else '<p style="color: #666; font-size: 1rem;">No articles in this category yet.</p>'}
            </section>
        </main>

        <!-- Footer -->
        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Searched By Her</p>
        </footer>
    </div>
</body>
</html>
'''
            os.makedirs(f"categories/{folder}", exist_ok=True)
            with open(f"categories/{folder}/{filename}", 'w', encoding='utf-8') as f:
                f.write(cat_content)

    print("Successfully built site! Slate is completely clean and ready for your first article.")

if __name__ == '__main__':
    build_site()