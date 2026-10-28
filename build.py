import os
import json
from datetime import datetime, timezone
import shutil

def build_site():
    # 1. Load articles from articles.json
    try:
        with open('articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("articles.json not found. Creating a blank list.")
        articles = []

    # Use UTC explicitly so GitHub Actions cloud runners and local machines always agree on "today"
    today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    articles = [a for a in articles if a.get('date', '2026-01-01') <= today_str]

    # Map category names to their respective folders and filenames
    category_config = {
        "Artificial Intelligence & Practical Automation": {
            "folder": "AI",
            "filename": "AI/index.html",
            "nav_title": "AI"
        },
        "Consumer Tech & Hardware Reviews": {
            "folder": "Hardware",
            "filename": "Hardware/index.html",
            "nav_title": "Hardware"
        },
        "Software, Apps & Digital Tools": {
            "folder": "Software",
            "filename": "Software/index.html",
            "nav_title": "Software"
        },
        "Finance, Crypto & Markets": {
            "folder": "Finances",
            "filename": "Finances/index.html",
            "nav_title": "Finance"
        }
    }

    # 2. Sort articles chronologically (Newest to Oldest based on 'date') if any exist
    if articles:
        articles.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)

    def generate_cards(article_list):
        cards = ""
        for article in article_list:
            cat_name = article['category']
            folder = category_config.get(cat_name, {"folder": "AI"})["folder"]
            post_link = f"/categories/{folder}/{article['slug']}/"

            cards += f'''
                <article class="article-card">
                    <div class="meta">{cat_name} &bull; {article['date']} &bull; By <a href="/author/lettie-nl/" style="color: inherit; text-decoration: underline;">Lettie N.L.</a></div>
                    <h2><a href="{post_link}">{article['title']}</a></h2>
                    <p>{article['excerpt']}</p>
                </article>'''
        return cards

    # Shared Navigation HTML snippet
    def get_nav(active_page="home"):
        return f'''
            <header>
                <a href="/" class="brand">TechWitHer<span class="red-dot">.</span></a>
                <nav>
                    <a href="/" class="{'active' if active_page=='home' else ''}">Home</a>
                    <a href="/categories/AI/" class="{'active' if active_page=='ai' else ''}">AI</a>
                    <a href="/categories/Hardware/" class="{'active' if active_page=='hardware' else ''}">Hardware</a>
                    <a href="/categories/Software/" class="{'active' if active_page=='software' else ''}">Software</a>
                    <a href="/categories/Finances/" class="{'active' if active_page=='finance' else ''}">Finance</a>
                    <a href="/tools/" class="{'active' if active_page=='tools' else ''}" style="color: #ff3333;">⚡ Tools</a>
                </nav>
            </header>
        '''

    # Shared Footer with Compliance Links
    def get_footer():
        return '''
            <footer>
                <!-- Google AdSense Bottom Ad Unit -->
                <div style="margin: 2rem 0; text-align: center;">
                    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774"
                         crossorigin="anonymous"></script>
                    <ins class="adsbygoogle"
                         style="display:block"
                         data-ad-client="ca-pub-3209789109672774"
                         data-ad-slot="2893043526"
                         data-ad-format="auto"
                         data-full-width-responsive="true"></ins>
                    <script>
                         (adsbygoogle = window.adsbygoogle || []).push({});
                    </script>
                </div>

                <div style="margin-bottom: 1rem; display: flex; gap: 15px; justify-content: center; font-size: 0.85rem; flex-wrap: wrap;">
                    <a href="/about/" style="color: #555; text-decoration: none;">About</a>
                    <a href="/privacy/" style="color: #555; text-decoration: none;">Privacy Policy</a>
                    <a href="/disclosure/" style="color: #555; text-decoration: none;">Affiliate Disclosure</a>
                    <a href="/disclaimer/" style="color: #555; text-decoration: none;">Disclaimer</a>
                    <a href="/contact/" style="color: #555; text-decoration: none;">Contact</a>
                </div>
                <p>&copy; 2026 TechWitHer. All rights reserved. &bull; Curated by <a href="/author/lettie-nl/" style="color: inherit; text-decoration: underline;">Lettie N.L.</a></p>
                <p>Searched By Her</p>
            </footer>
        '''

    # 3. Build Homepage (index.html)
    home_cards = generate_cards(articles)
    
    index_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechWitHer - The Digital Tech & Finance Magazine</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        {get_nav('home')}
        <main>
            <section class="magazine-grid">
{home_cards if home_cards else '<p style="color: #666; font-size: 1.1rem; padding: 2rem 0;">No articles published yet.</p>'}
            </section>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)

    # 4. Build Dedicated Trust & Compliance Pages
    os.makedirs("author/lettie-nl", exist_ok=True)
    author_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lettie N.L. - Author Profile - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 900;">Lettie N.L.</h1>
            <p style="color: #666; font-weight: 700; margin-bottom: 1.5rem;">Curator, Lead Researcher & Founder, TechWitHer</p>
            <p>Lettie N.L. is a tech enthusiast, digital researcher, and customer care specialist who built TechWitHer to bridge the gap between complex software developments, practical AI automation, and everyday personal finance management.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('author/lettie-nl/index.html', 'w', encoding='utf-8') as f:
        f.write(author_content)

    os.makedirs("about", exist_ok=True)
    about_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 1.5rem; font-weight: 900;">About TechWitHer</h1>
            <p>Welcome to <strong>TechWitHer</strong>, an independent digital magazine focusing on artificial intelligence, software tools, consumer technology, and modern financial markets.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('about/index.html', 'w', encoding='utf-8') as f:
        f.write(about_content)

    os.makedirs("privacy", exist_ok=True)
    privacy_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 900;">Privacy Policy</h1>
            <p style="color: #666; font-size: 0.9rem; margin-bottom: 1.5rem;"><strong>Last Updated:</strong> October 2026</p>
            <p>At TechWitHer, privacy is a top priority. All tool calculations and document operations run 100% locally in your browser.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('privacy/index.html', 'w', encoding='utf-8') as f:
        f.write(privacy_content)

    os.makedirs("disclosure", exist_ok=True)
    disclosure_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Affiliate Disclosure - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 1.5rem; font-weight: 900;">Affiliate & Advertising Disclosure</h1>
            <p>Some links on this website are affiliate links, meaning we may earn a small commission at no extra cost to you.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('disclosure/index.html', 'w', encoding='utf-8') as f:
        f.write(disclosure_content)

    os.makedirs("disclaimer", exist_ok=True)
    disclaimer_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disclaimer - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 1.5rem; font-weight: 900;">General & Financial Disclaimer</h1>
            <p>Information provided on TechWitHer is for educational purposes only and does not constitute formal financial or tax advice.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('disclaimer/index.html', 'w', encoding='utf-8') as f:
        f.write(disclaimer_content)

    os.makedirs("contact", exist_ok=True)
    contact_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main style="max-width: 600px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 1rem; font-weight: 900;">Contact Us</h1>
            <form action="https://formspree.io/f/mljjgynn" method="POST" style="display: flex; flex-direction: column; gap: 15px;">
                <div>
                    <label style="display: block; font-weight: 700; font-size: 0.9rem; margin-bottom: 5px;">Your Name</label>
                    <input type="text" name="name" required style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
                <div>
                    <label style="display: block; font-weight: 700; font-size: 0.9rem; margin-bottom: 5px;">Your Email</label>
                    <input type="email" name="email" required style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
                <div>
                    <label style="display: block; font-weight: 700; font-size: 0.9rem; margin-bottom: 5px;">Message</label>
                    <textarea name="message" rows="5" required style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;"></textarea>
                </div>
                <button type="submit" style="padding: 12px 20px; background: #111; color: #fff; border: none; font-weight: bold; cursor: pointer; border-radius: 4px;">Send Message</button>
            </form>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('contact/index.html', 'w', encoding='utf-8') as f:
        f.write(contact_content)

    # 4g. TOOLS HUB PAGE (/tools/)
    os.makedirs("tools", exist_ok=True)
    tools_page_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Online Utilities, PDF Tools & Calculators - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="/">Home</a>
                <a href="/categories/AI/">AI</a>
                <a href="/categories/Hardware/">Hardware</a>
                <a href="/categories/Software/">Software</a>
                <a href="/categories/Finances/">Finance</a>
                <a href="/tools/" class="active" style="color: #ff3333; border-bottom: 2px solid #ff3333; padding-bottom: 3px;">⚡ Tools</a>
            </nav>
        </header>
        <main style="max-width: 800px; margin: 0 auto; padding: 2rem 0;">
            <h1 style="margin-bottom: 0.5rem; font-size: 2rem; font-weight: 900;">Global Tech & Utility Hub</h1>
            <p style="color: #555; margin-bottom: 2rem;">Explore our free browser-based tools: PDF Converter, Fill & Sign Signature Pad, Document Scanner, and Savings Calculator.</p>
            
            <ul style="line-height: 2.2; font-size: 1.1rem; margin-left: 20px;">
                <li><a href="/tools/savings-goal-calculator/" style="color: #ff3333; text-decoration: underline; font-weight: bold;">Savings Goal Calculator</a> &mdash; Forecast compound interest timelines.</li>
                <li><a href="/tools/pdf-converter/" style="color: #ff3333; text-decoration: underline; font-weight: bold;">Free PDF Converter</a> &mdash; Turn text notes into professional PDFs.</li>
                <li><a href="/tools/fill-and-sign/" style="color: #ff3333; text-decoration: underline; font-weight: bold;">Fill & Sign Tool</a> &mdash; Create digital signatures and transparent stamps.</li>
                <li><a href="/tools/document-scanner/" style="color: #ff3333; text-decoration: underline; font-weight: bold;">Document Scanner & Enhancer</a> &mdash; Convert phone photos into crisp B&W scans.</li>
            </ul>
        </main>
        <footer>
            <div style="margin-bottom: 1rem; display: flex; gap: 15px; justify-content: center; font-size: 0.85rem; flex-wrap: wrap;">
                <a href="/about/" style="color: #555; text-decoration: none;">About</a>
                <a href="/privacy/" style="color: #555; text-decoration: none;">Privacy Policy</a>
                <a href="/disclosure/" style="color: #555; text-decoration: none;">Affiliate Disclosure</a>
                <a href="/disclaimer/" style="color: #555; text-decoration: none;">Disclaimer</a>
                <a href="/contact/" style="color: #555; text-decoration: none;">Contact</a>
            </div>
            <p>&copy; 2026 TechWitHer. All rights reserved. &bull; Curated by <a href="/author/lettie-nl/" style="color: inherit; text-decoration: underline;">Lettie N.L.</a></p>
        </footer>
    </div>
</body>
</html>
'''
    with open('tools/index.html', 'w', encoding='utf-8') as f:
        f.write(tools_page_content)

    # 4h. SAVINGS GOAL CALCULATOR (/tools/savings-goal-calculator/)
    os.makedirs("tools/savings-goal-calculator", exist_ok=True)
    savings_calc_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Savings Goal Calculator - How Much to Save Each Month | TechWitHer</title>
    <meta name="description" content="Use TechWitHer's free Savings Goal Calculator to find out how long it takes to reach your financial target. Free, fast, and secure.">
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="container">
        NAV_PLACEHOLDER
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 900;">Savings Goal Calculator</h1>
            <p style="color: #666; font-size: 0.9rem; margin-bottom: 1.5rem;"><strong>Last Updated:</strong> October 2026 &bull; Curated by <a href="/author/lettie-nl/" style="color: inherit; text-decoration: underline;">Lettie N.L.</a></p>
            
            <div style="background: #f9f9f9; border-left: 3px solid #ff3333; padding: 10px 15px; margin-bottom: 20px; font-size: 0.85rem; color: #555;">
                <em>Financial Disclaimer: This tool is for educational purposes only and does not constitute formal financial or tax advice. Read our <a href="/disclaimer/" style="color: #111; text-decoration: underline;">Disclaimer</a>.</em>
            </div>

            <div style="background: #fff; border: 1px solid #ddd; padding: 25px; border-radius: 6px; margin-bottom: 2.5rem;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    <div>
                        <label style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 5px;">Target Goal Amount</label>
                        <input type="number" id="goal-target" value="10000" oninput="calculateSavings()" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 5px;">Current Savings</label>
                        <input type="number" id="goal-current" value="1000" oninput="calculateSavings()" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 5px;">Monthly Contribution</label>
                        <input type="number" id="goal-monthly" value="500" oninput="calculateSavings()" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 5px;">Estimated Annual Interest (%)</label>
                        <input type="number" id="goal-interest" value="6.5" step="0.1" oninput="calculateSavings()" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                    </div>
                </div>

                <div style="background: #111; color: #fff; padding: 20px; text-align: center; border-radius: 4px;">
                    <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #aaa; margin-bottom: 5px;">Time Needed to Reach Goal</div>
                    <div id="goal-result-time" style="font-size: 1.8rem; font-weight: 800; color: #00ffcc;">17 Months (1.4 Years)</div>
                    <div id="goal-result-breakdown" style="font-size: 0.9rem; color: #ddd; margin-top: 8px;">Total Interest Earned: $250.00</div>
                </div>
            </div>

            <h2>How to Use the Savings Goal Calculator</h2>
            <p>Our <strong>Savings Goal Calculator</strong> helps you forecast precisely how long it will take to reach your target based on monthly contributions and high-yield interest rates.</p>
            
            <h3 style="margin-top: 1.5rem;">Worked Example</h3>
            <p>If your target is $10,000, you have $1,000 saved, and you add $500 monthly at 6.5% annual interest, you will reach your goal in under 17 months.</p>

            <h3 style="margin-top: 1.5rem;">Frequently Asked Questions (FAQs)</h3>
            <p><strong>1. How much should I save each month?</strong><br>A popular guideline is the 50/30/20 budgeting framework.</p>
            <p><strong>2. Are my financial entries secure?</strong><br>All calculations run entirely inside your browser locally and are never stored or sent anywhere.</p>

            <h3 style="margin-top: 1.5rem;">Related Tools</h3>
            <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                <li><a href="/tools/pdf-converter/" style="color: #ff3333; text-decoration: underline;">Free PDF Converter</a></li>
                <li><a href="/tools/fill-and-sign/" style="color: #ff3333; text-decoration: underline;">Fill & Sign Tool</a></li>
                <li><a href="/tools/document-scanner/" style="color: #ff3333; text-decoration: underline;">Document Scanner</a></li>
            </ul>
        </main>
        {get_footer()}
    </div>
    <script>
    function calculateSavings() {
        let target = parseFloat(document.getElementById('goal-target').value) || 0;
        let current = parseFloat(document.getElementById('goal-current').value) || 0;
        let monthly = parseFloat(document.getElementById('goal-monthly').value) || 0;
        let annualRate = parseFloat(document.getElementById('goal-interest').value) || 0;
        if (current >= target) {
            document.getElementById('goal-result-time').innerText = "Goal Achieved!";
            document.getElementById('goal-result-breakdown').innerText = "";
            return;
        }
        let months = 0, balance = current, totalInterest = 0, monthlyRate = (annualRate / 100) / 12;
        while (balance < target && months < 1200) {
            let interestEarned = balance * monthlyRate;
            totalInterest += interestEarned;
            balance += interestEarned + monthly;
            months++;
        }
        let years = (months / 12).toFixed(1);
        document.getElementById('goal-result-time').innerText = `${months} Months (${years} Years)`;
        document.getElementById('goal-result-breakdown').innerText = `Total Interest Earned: $${totalInterest.toFixed(2)}`;
    }
    calculateSavings();
    </script>
</body>
</html>
'''
    with open('tools/savings-goal-calculator/index.html', 'w', encoding='utf-8') as f:
        f.write(savings_calc_html.replace("NAV_PLACEHOLDER", get_nav('tools')))

# 4i. DEDICATED TOOL PAGE: FREE PDF & WORD CONVERTER (/tools/pdf-converter/)
    os.makedirs("tools/pdf-converter", exist_ok=True)
    pdf_converter_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convert Word to PDF & PDF to Word Free - No Sign-Up | TechWitHer</title>
    <meta name="description" content="Turn Word docs and PDFs into editable formats online. 100% Free, No Sign-up required. Fast, secure, and simple browser document converter.">
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
    <!-- Mammoth.js for reading Word .docx files in browser -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.6.0/mammoth.browser.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
</head>
<body>
    <div class="container">
        NAV_PLACEHOLDER
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 900;">Convert Word & PDF Online for Free</h1>
            <p style="color: #666; font-size: 1rem; margin-bottom: 1.5rem;">Upload your Word document (.docx) or PDF, view it, edit text, and download your converted file instantly.</p>
            
            <div style="background: #e6f7ff; border-left: 4px solid #0056b3; padding: 12px 18px; margin-bottom: 25px; font-size: 0.9rem; color: #004085; font-weight: 600;">
                ✓ 100% Free &bull; ✓ No Sign-Up &bull; ✓ Instant Browser Conversion
            </div>

            <div style="background: #fff; border: 1px solid #ddd; padding: 30px; border-radius: 6px; margin-bottom: 2.5rem; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <h3 style="margin-top: 0;">Upload Your Word (.docx) or Text File</h3>
                <input type="file" id="word-file-input" accept=".docx,.txt" onchange="handleWordUpload(event)" style="margin-bottom: 20px; display: block; padding: 10px; border: 1px dashed #ccc; width: 100%; background: #fafafa;">
                
                <h3 style="margin-top: 15px;">Document Preview & Editable Text</h3>
                <div id="document-preview-box" contenteditable="true" style="min-height: 200px; border: 1px solid #ccc; padding: 15px; background: #fff; margin-bottom: 20px; border-radius: 4px; font-family: sans-serif; font-size: 1rem;" placeholder="Your uploaded document text will appear here for viewing and editing..."></div>
                
                <button onclick="downloadAsPdf()" style="padding: 14px 24px; background: #111; color: #fff; border: none; font-weight: bold; cursor: pointer; border-radius: 4px; width: 100%; text-transform: uppercase; font-size: 0.9rem;">Download Converted PDF</button>
            </div>

            <h2>How It Works</h2>
            <p>Upload your Microsoft Word document, view and tweak text directly in your browser, and export it as a clean PDF without ever needing to register an account.</p>

            <h3 style="margin-top: 1.5rem;">Frequently Asked Questions (FAQs)</h3>
            <p><strong>1. Do I need to create an account?</strong><br>No. All tools are completely free with zero sign-up required.</p>
            <p><strong>2. Are my files kept private?</strong><br>Yes. Everything is processed locally inside your browser memory.</p>

            <h3 style="margin-top: 1.5rem;">Related Free Tools</h3>
            <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                <li><a href="/tools/fill-and-sign/" style="color: #ff3333; text-decoration: underline;">Fill & Sign PDFs Online (Free, No Sign-Up)</a></li>
                <li><a href="/tools/document-scanner/" style="color: #ff3333; text-decoration: underline;">Scan and Edit Documents for Free</a></li>
            </ul>
        </main>
        {get_footer()}
    </div>
    <script>
    function handleWordUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        if (file.name.endsWith('.docx')) {
            reader.onload = function(e) {
                mammoth.convertToHtml({arrayBuffer: e.target.result})
                    .then(function(result) {
                        document.getElementById('document-preview-box').innerHTML = result.value;
                    })
                    .catch(function(err) {
                        alert("Error reading Word file: " + err.message);
                    });
            };
            reader.readAsArrayBuffer(file);
        } else {
            reader.onload = function(e) {
                document.getElementById('document-preview-box').innerText = e.target.result;
            };
            reader.readAsText(file);
        }
    }

    function downloadAsPdf() {
        const content = document.getElementById('document-preview-box').innerText;
        if (!content) { alert('No document loaded to convert.'); return; }
        
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        doc.setFont("Helvetica", "normal");
        doc.setFontSize(14);
        doc.text("TechWitHer Converted Document", 20, 20);
        doc.setFontSize(10);
        const splitText = doc.splitTextToSize(content, 170);
        doc.text(splitText, 20, 30);
        doc.save("converted-document.pdf");
    }
    </script>
</body>
</html>
'''
    with open('tools/pdf-converter/index.html', 'w', encoding='utf-8') as f:
        f.write(pdf_converter_html.replace("NAV_PLACEHOLDER", get_nav('tools')))

    # 4j. DEDICATED TOOL PAGE: FILL & SIGN TOOL (/tools/fill-and-sign/)
    os.makedirs("tools/fill-and-sign", exist_ok=True)
    fill_sign_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fill & Sign PDFs Online - Free, No Sign-Up Required | TechWitHer</title>
    <meta name="description" content="Upload any PDF document, fill out form spaces, add your signature, and download the completed file instantly. 100% Free, No Sign-up required.">
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
    <!-- pdf-lib for editing and signing actual PDF files in browser -->
    <script src="https://unpkg.com/pdf-lib@1.4.0/dist/pdf-lib.min.js"></script>
</head>
<body>
    <div class="container">
        NAV_PLACEHOLDER
        <main style="max-width: 800px; margin: 0 auto; line-height: 1.7; padding: 2rem 0;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 900;">Fill & Sign PDFs Online</h1>
            <p style="color: #333; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">Fill out form spaces and add your signature to any PDF in a few clicks.</p>
            <p style="color: #666; font-size: 0.95rem; margin-bottom: 1.5rem;">100% Free &bull; No Sign-Up Required &bull; Instant Browser PDF Editing</p>
            
            <div style="background: #e6f7ff; border-left: 4px solid #0056b3; padding: 12px 18px; margin-bottom: 25px; font-size: 0.9rem; color: #004085;">
                <ul style="margin: 0; padding-left: 18px; line-height: 1.6;">
                    <li><strong>Upload your PDF document</strong> and start filling out required text spaces instantly.</li>
                    <li><strong>Draw your official signature</strong> to place it onto the PDF layout.</li>
                    <li><strong>Download your signed PDF</strong> right away with zero fees or registration.</li>
                </ul>
            </div>

            <!-- WORKSPACE -->
            <div style="background: #fff; border: 1px solid #ddd; padding: 30px; border-radius: 6px; margin-bottom: 2.5rem; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <h3 style="margin-top: 0;">Step 1: Upload Your PDF Document</h3>
                <input type="file" id="pdf-file-input" accept=".pdf" onchange="loadPdfFile(event)" style="margin-bottom: 20px; display: block; padding: 10px; border: 1px dashed #ccc; width: 100%; background: #fafafa;">
                
                <div id="pdf-status-box" style="margin-bottom: 20px; padding: 12px; background: #f9f9f9; border: 1px solid #ddd; border-radius: 4px; display: none; font-size: 0.9rem; color: #28a745; font-weight: bold;">
                    ✓ PDF loaded successfully! Ready for text entry and signing.
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="display: block; font-weight: 700; font-size: 0.9rem; margin-bottom: 5px;">Step 2: Type Text to Add onto the PDF</label>
                    <input type="text" id="pdf-custom-text" placeholder="Type text to stamp onto document (e.g. Your Name, Date, Answers)..." style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;">
                </div>

                <h3>Step 3: Draw Your Signature</h3>
                <div style="border: 2px dashed #ccc; background: #fafafa; margin: 15px 0; border-radius: 4px; display: inline-block;">
                    <canvas id="sig-canvas" width="380" height="150" style="cursor: crosshair; display: block;"></canvas>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button onclick="clearSignature()" style="padding: 12px 20px; background: #dc3545; color: #fff; border: none; font-weight: bold; cursor: pointer; border-radius: 4px;">Clear Pad</button>
                    <button onclick="signAndDownloadPdf()" style="padding: 12px 24px; background: #28a745; color: #fff; border: none; font-weight: bold; cursor: pointer; border-radius: 4px; flex-grow: 1;">Download Signed PDF</button>
                </div>
            </div>

            <h2>Why Use Our Fill & Sign Tool?</h2>
            <p>Filling out PDF forms and signing official paperwork shouldn't require paid subscriptions or accounts. TechWitHer lets you upload, fill, and sign PDFs directly in your browser for free.</p>

            <h3 style="margin-top: 1.5rem;">Frequently Asked Questions (FAQs)</h3>
            <p><strong>1. Is this truly free with no sign-up?</strong><br>Yes! You can use this tool immediately without creating any account or logging in.</p>
            <p><strong>2. Are my documents safe?</strong><br>Yes. All PDF editing and signing happen 100% locally on your device.</p>
        </main>
        {get_footer()}
    </div>
    <script>
    let uploadedPdfBytes = null;

    function loadPdfFile(event) {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(e) {
            uploadedPdfBytes = e.target.result;
            document.getElementById('pdf-status-box').style.display = 'block';
        };
        reader.readAsArrayBuffer(file);
    }

    const canvas = document.getElementById('sig-canvas');
    const ctx = canvas.getContext('2d');
    let painting = false;
    canvas.addEventListener('mousedown', e => { painting = true; draw(e); });
    canvas.addEventListener('mouseup', () => { painting = false; ctx.beginPath(); });
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('touchstart', e => { painting = true; draw(e.touches[0]); e.preventDefault(); });
    canvas.addEventListener('touchend', () => { painting = false; ctx.beginPath(); });
    canvas.addEventListener('touchmove', e => { draw(e.touches[0]); e.preventDefault(); });

    function draw(e) {
        if (!painting) return;
        const rect = canvas.getBoundingClientRect();
        ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.strokeStyle = '#000';
        ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
        ctx.stroke(); ctx.beginPath();
        ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
    }
    function clearSignature() { ctx.clearRect(0, 0, canvas.width, canvas.height); }

    async function signAndDownloadPdf() {
        if (!uploadedPdfBytes) {
            alert('Please upload a PDF document first.');
            return;
        }

        try {
            const { PDFDocument, rgb } = PDFLib;
            const pdfDoc = await PDFDocument.load(uploadedPdfBytes);
            
            // Get the first page of the PDF
            const pages = pdfDoc.getPages();
            const firstPage = pages[0];
            const { width, height } = firstPage.getSize();

            // Add custom typed text if entered
            const customText = document.getElementById('pdf-custom-text').value;
            if (customText) {
                firstPage.drawText(customText, {
                    x: 50,
                    y: height - 100,
                    size: 12,
                    rgb: rgb(0, 0, 0),
                });
            }

            // Embed signature image into PDF
            const sigImageBytes = canvas.toDataURL('image/png');
            const embeddedImage = await pdfDoc.embedPng(sigImageBytes);
            
            firstPage.drawImage(embeddedImage, {
                x: 50,
                y: 50,
                width: 150,
                height: 60,
            });

            // Save and trigger download
            const modifiedPdfBytes = await pdfDoc.save();
            const blob = new Blob([modifiedPdfBytes], { type: 'application/pdf' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'signed-document.pdf';
            link.click();
        } catch (err) {
            alert("Error processing PDF: " + err.message);
        }
    }
    </script>
</body>
</html>
'''
    with open('tools/fill-and-sign/index.html', 'w', encoding='utf-8') as f:
        f.write(fill_sign_html.replace("NAV_PLACEHOLDER", get_nav('tools')))
    
    # 5. Build Individual Article Pages & Category Archives
    if articles:
        for article in articles:
            cat_name = article['category']
            config = category_config.get(cat_name, category_config["Artificial Intelligence & Practical Automation"])
            folder = config["folder"]
            article_content_html = article.get('content', f"<p>{article['excerpt']}</p>")
            
            disclosure_notice = '''
                <div style="background: #f9f9f9; border-left: 3px solid #ff3333; padding: 10px 15px; margin-bottom: 20px; font-size: 0.85rem; color: #555;">
                    <em>Editorial Note: This article may contain affiliate links. If you make a purchase through these links, we may earn a commission at no extra cost to you. Read our <a href="/disclosure/" style="color: #111; text-decoration: underline;">Affiliate Disclosure</a> and <a href="/disclaimer/" style="color: #111; text-decoration: underline;">Disclaimer</a>.</em>
                </div>
            '''
            
            in_article_ad = '''
                <div style="margin: 2rem 0;">
                    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774"
                         crossorigin="anonymous"></script>
                    <ins class="adsbygoogle"
                         style="display:block; text-align:center;"
                         data-ad-layout="in-article"
                         data-ad-format="fluid"
                         data-ad-client="ca-pub-3209789109672774"
                         data-ad-slot="1600143151"></ins>
                    <script>
                         (adsbygoogle = window.adsbygoogle || []).push({});
                    </script>
                </div>
            '''
            
            post_page_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main>
            <article class="post-content">
                <h1>{article['title']}</h1>
                <p class="post-meta">{article['category']} &bull; {article['date']} &bull; By <a href="/author/lettie-nl/" style="color: inherit; text-decoration: underline;">Lettie N.L.</a></p>
                {disclosure_notice}
                {in_article_ad}
                {article_content_html}
            </article>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
            article_dir = f"categories/{folder}/{article['slug']}"
            os.makedirs(article_dir, exist_ok=True)
            with open(f"{article_dir}/index.html", 'w', encoding='utf-8') as f:
                f.write(post_page_content)

        for cat_name, config in category_config.items():
            folder = config["folder"]
            cat_articles = [a for a in articles if a['category'] == cat_name]
            cat_cards = generate_cards(cat_articles)
            
            if folder == 'AI': active_key = 'ai'
            elif folder == 'Hardware': active_key = 'hardware'
            elif folder == 'Software': active_key = 'software'
            elif folder == 'Finances': active_key = 'finance'
            else: active_key = 'home'

            cat_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_name} - TechWitHer</title>
    <link rel="icon" type="image/svg+xml" href="/techwither.svg">
    <link rel="stylesheet" href="/style.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        {get_nav(active_key)}
        <main>
            <h1 style="margin-bottom: 2rem; font-size: 1.8rem; border-bottom: 2px solid #000; padding-bottom: 0.5rem;">{cat_name}</h1>
            <section class="magazine-grid">
{cat_cards if cat_cards else '<p style="color: #666; font-size: 1rem;">No articles in this category yet.</p>'}
            </section>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
            cat_dir = f"categories/{folder}"
            os.makedirs(cat_dir, exist_ok=True)
            with open(f"{cat_dir}/index.html", 'w', encoding='utf-8') as f:
                f.write(cat_content)

    # 6. Automated Sitemap Generator for SEO & AdSense
    domain = "https://techwither.com"
    today = datetime.now().strftime('%Y-%m-%d')
    
    urls = [
        {"loc": f"{domain}/", "priority": "1.0", "changefreq": "daily"},
        {"loc": f"{domain}/about/", "priority": "0.5", "changefreq": "monthly"},
        {"loc": f"{domain}/contact/", "priority": "0.5", "changefreq": "monthly"},
        {"loc": f"{domain}/privacy/", "priority": "0.3", "changefreq": "yearly"},
        {"loc": f"{domain}/disclaimer/", "priority": "0.3", "changefreq": "yearly"},
        {"loc": f"{domain}/disclosure/", "priority": "0.3", "changefreq": "yearly"},
        {"loc": f"{domain}/tools/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{domain}/tools/savings-goal-calculator/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{domain}/tools/pdf-converter/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{domain}/tools/fill-and-sign/", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{domain}/tools/document-scanner/", "priority": "0.9", "changefreq": "weekly"},
    ]
    
    for article in articles:
        slug = article.get('slug')
        cat_name = article.get('category')
        folder = category_config.get(cat_name, {"folder": "AI"})["folder"]
        urls.append({
            "loc": f"{domain}/categories/{folder}/{slug}/",
            "priority": "0.8",
            "changefreq": "weekly"
        })
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml_content += f"  <url>\n    <loc>{u['loc']}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{u['changefreq']}</changefreq>\n    <priority>{u['priority']}</priority>\n  </url>\n"
    xml_content += '</urlset>'
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

    print("Successfully built site with robust trust pages, Disclaimer page, author profile, clean folder URLs, dedicated tools, and sitemap.xml!")

if __name__ == '__main__':
    build_site()