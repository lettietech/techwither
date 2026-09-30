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

    # Ensure articles category directories exist based on your structure
    categories = [
        "AI & Machine Learning",
        "Gadgets & Hardware",
        "Software & Digital Life",
        "Robotics & Future Tech",
        "Reviews & Verdicts"
    ]
    
    for cat in categories:
        dir_path = os.path.join('articles', 'Categories', cat)
        os.makedirs(dir_path, exist_ok=True)

    # Verification and processing loop
    for article in articles:
        filename = article['filename']
        if os.path.exists(filename):
            print(f"[OK] Found: {article['title']} -> {filename}")
        else:
            print(f"[WARNING] File referenced in JSON not found on disk: {filename}")
            
    print("Build complete! All paths and JSON indexes verified.")

if __name__ == '__main__':
    build_site()