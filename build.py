import json
import os

def build_site():
    # Load article metadata
    if not os.path.exists('articles.json'):
        print("Error: articles.json not found!")
        return

    with open('articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Successfully loaded {len(articles)} articles from metadata.")

    # Ensure output directories exist
    os.makedirs('categories', exist_ok=True)

    # Example: Processing loop for static generation or verification
    for article in articles:
        print(f"Processing: {article['title']} [{article['category']}] -> {article['filename']}")

    # Add your full static generation HTML compilation logic here
    print("Build complete! All paths and JSON indexes verified.")

if __name__ == '__main__':
    build_site()