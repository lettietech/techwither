import os
import json
from datetime import datetime

def build_site():
    # 1. Load articles from articles.json
    try:
        with open('articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("articles.json not found. Creating a blank list.")
        articles = []

    # 2. Sort articles chronologically (Newest to Oldest based on 'date')
    articles.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)

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

    # Helper function to generate card HTML
    def generate_cards(article_list, base_path_prefix=""):
        cards = ""
        for article in article_list:
            cat_name = article['category']
            folder = category_config.get(cat_name, {"folder": "AI"})["folder"]
            # Adjust path depending on whether we are in root or inside a category subfolder
            post_link = f"{base_path_prefix}categories/{folder}/{article['slug']}.html"
            thumb_link = f"{base_path_prefix}{article['thumbnail']}" if not article['thumbnail'].startswith("http") else article['thumbnail']

            cards += f'''
                <article class="article-card">
                    <div class="thumbnail-wrapper">
                        <img src="{thumb_link}" alt="Article Thumbnail">
                    </div>
                    <div class="meta">{cat_name} &bull; {article['date']}</div>
                    <h2><a href="{post_link}">{article['title']}</a></h2>
                    <p>{article['excerpt']}</p>
                </article>'''
        return cards

    # 3. Build Homepage (index.html)
    home_cards = generate_cards(articles, base_path_prefix="")
    
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
            <a href="index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="index.html" class="active">Home</a>
                <a href="categories/AI/Artificial Intelligence & Practical Automation.html">AI</a>
                <a href="categories/Hardware/Consumer Tech & Hardware Reviews.html">Hardware</a>
                <a href="categories/Software/Software, Apps & Digital Tools.html">Software</a>
            </nav>
        </header>

        <!-- Main Content Feed -->
        <main>
            <section class="magazine-grid">
{home_cards}
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

    # 4. Build Category Archive Pages Automatically
    for cat_name, config in category_config.items():
        folder = config["folder"]
        filename = config["filename"]
        
        # Filter articles belonging only to this category
        cat_articles = [a for a in articles if a['category'] == cat_name]
        cat_cards = generate_cards(cat_articles, base_path_prefix="../../")

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
            <a href="../../index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="../../index.html">Home</a>
                <a href="Artificial Intelligence & Practical Automation.html" class="{'active' if folder=='AI' else ''}">AI</a>
                <a href="../Hardware/Consumer Tech & Hardware Reviews.html" class="{'active' if folder=='Hardware' else ''}">Hardware</a>
                <a href="../Software/Software, Apps & Digital Tools.html" class="{'active' if folder=='Software' else ''}">Software</a>
            </nav>
        </header>

        <!-- Main Content Feed -->
        <main>
            <h1 style="margin-bottom: 2rem; font-size: 1.8rem; border-bottom: 2px solid #000; padding-bottom: 0.5rem;">{cat_name}</h1>
            <section class="magazine-grid">
{cat_cards}
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
        # Ensure directory exists and write file
        os.makedirs(f"categories/{folder}", exist_ok=True)
        with open(f"categories/{folder}/{filename}", 'w', encoding='utf-8') as f:
            f.write(cat_content)

    print("Successfully built homepage and all category archive pages automatically!")

if __name__ == '__main__':
    build_site()