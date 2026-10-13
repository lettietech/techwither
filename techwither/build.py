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

    # 3. Generate HTML cards dynamically
    cards_html = ""
    for article in articles:
        cards_html += f'''
                <article class="article-card">
                    <div class="thumbnail-wrapper">
                        <img src="{article['thumbnail']}" alt="Article Thumbnail">
                    </div>
                    <div class="meta">{article['category']}</div>
                    <h2><a href="posts/{article['slug']}.html">{article['title']}</a></h2>
                    <p>{article['excerpt']}</p>
                </article>'''

    # 4. Construct the full index.html layout with Google AdSense code included
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
                <a href="categories/Artificial Intelligence & Practical Automation.html">AI</a>
                <a href="categories/Consumer Tech & Hardware Reviews.html">Hardware</a>
                <a href="categories/Software, Apps & Digital Tools.html">Software</a>
            </nav>
        </header>

        <!-- Main Content Feed -->
        <main>
            <section class="magazine-grid">
{cards_html}
            </section>
        </main>

        <!-- Footer -->
        <footer>
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Built Clean. Zero Bloat.</p>
        </footer>
    </div>
</body>
</html>
'''

    # 5. Write out the final index.html file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"Successfully generated index.html with AdSense integration!")

if __name__ == '__main__':
    build_site()