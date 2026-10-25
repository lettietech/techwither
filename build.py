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
            # Clean URL ending with a trailing slash (no .html)
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

    # Shared Footer with Compliance Links (Clean URLs, including Disclaimer)
    def get_footer():
        return '''
            <footer>
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

    # 4. Build Dedicated Trust & Compliance Pages (Clean Folders)
    
    # 4a. AUTHOR BIO PAGE (/author/lettie-nl/)
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
            
            <h3 style="margin-top: 2rem;">Why I Cover These Topics</h3>
            <p>We live in a fast-evolving digital era where technology and personal finance intersect daily. From understanding AI utility to safeguarding your digital assets, TechWitHer was created to cut through confusing jargon and provide clear, grounded, and independent insights.</p>
            
            <h3 style="margin-top: 2rem;">Rigorous Standards & Editorial Independence</h3>
            <p>Every piece of content published under this byline adheres to strict verification protocols. We do not take shortcuts; we evaluate primary sources, test digital workflows, and review financial frameworks objectively to protect reader trust.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('author/lettie-nl/index.html', 'w', encoding='utf-8') as f:
        f.write(author_content)

    # 4b. ABOUT PAGE (/about/)
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
            
            <h3 style="margin-top: 2rem;">Who We Are</h3>
            <p>Founded and curated by <a href="/author/lettie-nl/" style="color: inherit; text-decoration: underline;">Lettie N.L.</a>, TechWitHer was built out of a passion for cutting-edge technology, practical automation, and clear financial insights. Read more on our <a href="/author/lettie-nl/" style="color: inherit; text-decoration: underline;">Author Profile</a>.</p>
            
            <h3 style="margin-top: 2rem;">Why We Cover These Topics</h3>
            <p>Our modern world relies heavily on software performance and smart financial decisions. We cover these niche intersections to equip everyday professionals, creators, and tech enthusiasts with reliable blueprints for navigating the digital economy.</p>

            <h3 style="margin-top: 2rem;">Price & Source Verification Methods</h3>
            <p>We cross-reference pricing tiers, software release notes, and financial data directly from official developer documentations, primary earnings reports, and live platform benchmarks before publication.</p>

            <h3 style="margin-top: 2rem;">Our Scoring & Evaluation Framework</h3>
            <p>When we review products, software platforms, or financial products, our content passes a strict multi-point assessment:</p>
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li><strong>Utility & Practicality:</strong> Does the tool solve a genuine workflow problem?</li>
                <li><strong>Transparency & Cost:</strong> Are subscription tiers, hidden fees, or affiliate relationships clear?</li>
                <li><strong>Security & Privacy:</strong> Does the platform respect user data and privacy laws?</li>
                <li><strong>Reliability:</strong> Is the underlying technology stable, active, and well-supported?</li>
            </ul>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('about/index.html', 'w', encoding='utf-8') as f:
        f.write(about_content)

    # 4c. PRIVACY POLICY PAGE (/privacy/)
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
            
            <p>At TechWitHer, accessible from techwither.com, privacy is a top priority. This Privacy Policy document outlines the types of information collected and recorded by our website and how we use it.</p>
            
            <h3 style="margin-top: 1.5rem;">Information We Collect & Analytics Tool</h3>
            <p>We use web analytics tools (such as Google Analytics) to monitor site traffic and performance. This data helps us understand reader engagement and improve our digital magazine layout.</p>
            
            <h3 style="margin-top: 1.5rem;">Cookies and Third-Party Advertising (Google AdSense)</h3>
            <p>Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to <strong>our website</strong> or other websites. Google's use of advertising cookies enables it and its partners to serve ads to <strong>our users</strong> based on their visit to our site and/or other sites on the Internet.</p>
            <p>Users may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" style="color: #ff3333;">Ads Settings</a>. You can also opt out of third-party vendor cookies across multiple networks by visiting <a href="https://www.aboutads.info" target="_blank" style="color: #ff3333;">aboutads.info</a>.</p>

            <h3 style="margin-top: 1.5rem;">Contact Forms & Data Storage</h3>
            <p>Data submitted through our contact form (such as your name, email address, and message contents) is securely processed and stored via our form service provider to enable direct communication. We never sell or distribute reader correspondence.</p>

            <h3 style="margin-top: 1.5rem;">Global Privacy Rights (GDPR, CCPA & POPIA)</h3>
            <p>Depending on your geographic region (including the European Union under GDPR, California under CCPA, or South Africa under POPIA), readers maintain specific rights regarding their personal data, including the right to access, correct, or request deletion of personal information submitted via forms or cookies. To exercise these rights, contact us directly.</p>

            <h3 style="margin-top: 1.5rem;">Privacy Questions & Contact Email</h3>
            <p>If you have any questions or concerns regarding our privacy practices, you can reach out via our <a href="/contact/" style="color: #ff3333; text-decoration: underline;">Contact Page</a>.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('privacy/index.html', 'w', encoding='utf-8') as f:
        f.write(privacy_content)

    # 4d. AFFILIATE DISCLOSURE PAGE (/disclosure/)
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
            <p>TechWitHer believes in complete transparency with our readers. In compliance with <strong>FTC guidelines</strong> and standard industry disclosures, please note our monetization model:</p>
            
            <h3 style="margin-top: 1.5rem;">Plain-Language Commission Notice</h3>
            <p>Some of the links on this website are affiliate links. This means that if you click on the link and purchase an item or software service, TechWitHer may receive a small commission <strong>at absolutely no extra cost to you</strong>.</p>
            
            <h3 style="margin-top: 1.5rem;">Display Ads & Revenue</h3>
            <p>In addition to affiliate links, we may also earn revenue from programmatic display advertising networks (such as Google AdSense) placed throughout our articles and tool hubs.</p>

            <h3 style="margin-top: 1.5rem;">Editorial Integrity</h3>
            <p>Our reviews, recommendations, and guides are rooted in strict editorial independence. Affiliate partnerships do not influence our content rankings or evaluations; we only endorse products, tools, and platforms that add genuine value to our readers.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('disclosure/index.html', 'w', encoding='utf-8') as f:
        f.write(disclosure_content)

    # 4e. DISCLAIMER PAGE (/disclaimer/)
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
            <p>The information provided on TechWitHer (techwither.com) is for general informational, educational, and entertainment purposes only.</p>
            
            <h3 style="margin-top: 1.5rem;">Financial & Investment Content Disclaimer</h3>
            <p>Articles covering finance, crypto, markets, investments, monetization strategies, and software tools do not constitute formal financial, tax, or legal advice. Markets are volatile, and past performance does not guarantee future results. Always conduct your own independent research or consult with a certified professional before making significant financial commitments.</p>
            
            <h3 style="margin-top: 1.5rem;">External Links</h3>
            <p>TechWitHer contains links to external websites, third-party tools, and affiliate merchants. We assume no responsibility or liability for the content, privacy practices, or service terms of any third-party websites.</p>
        </main>
        {get_footer()}
    </div>
</body>
</html>
'''
    with open('disclaimer/index.html', 'w', encoding='utf-8') as f:
        f.write(disclaimer_content)

    # 4f. SECURE CONTACT PAGE (/contact/)
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
            <p style="color: #555; margin-bottom: 2rem;">Have a question, privacy inquiry, feedback, or a partnership proposal? Send a secure dispatch using the form below. Reader correspondence is handled confidentially.</p>
            
            <!-- Replace the action URL with your free Formspree endpoint -->
            <form action="https://formspree.io/f/your_form_id" method="POST" style="display: flex; flex-direction: column; gap: 15px;">
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
                <button type="submit" style="padding: 12px 20px; background: #111; color: #fff; border: none; font-weight: bold; cursor: pointer; border-radius: 4px; text-transform: uppercase; font-size: 0.9rem;">Send Message</button>
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
    <title>Free Online Calculator, HIIT Workout Timer, World Clock & Currency Converter - TechWitHer</title>
    <meta name="description" content="Use TechWitHer's free online everyday utilities: instant math calculator, customizable HIIT exercise timer with audio beeps, live world clocks, and multi-currency converter.">
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
        <main>
            <h1 style="margin-bottom: 0.5rem; font-size: 2rem; font-weight: 900;">Global Tech & Utility Hub</h1>
            <p style="color: #555; margin-bottom: 2rem;">Your everyday browser toolkit: instant calculations, HIIT workout intervals with audio cues, global time zones, and multi-currency conversion.</p>
            
            <div class="utility-hub-card" style="border: 1px solid #e0e0e0; padding: 2rem; background: #fdfdfd; border-radius: 4px;">
                <div style="display: flex; gap: 8px; margin-bottom: 25px; flex-wrap: wrap;">
                    <button onclick="switchTab('calc')" id="btn-calc" style="padding: 10px 16px; background: #111; color: #fff; border: none; cursor: pointer; font-weight: 700; text-transform: uppercase; font-size: 0.8rem;">Calculator</button>
                    <button onclick="switchTab('timer')" id="btn-timer" style="padding: 10px 16px; background: #eee; color: #111; border: none; cursor: pointer; font-weight: 700; text-transform: uppercase; font-size: 0.8rem;">Workout Timer</button>
                    <button onclick="switchTab('time')" id="btn-time" style="padding: 10px 16px; background: #eee; color: #111; border: none; cursor: pointer; font-weight: 700; text-transform: uppercase; font-size: 0.8rem;">World Clocks</button>
                    <button onclick="switchTab('currency')" id="btn-currency" style="padding: 10px 16px; background: #eee; color: #111; border: none; cursor: pointer; font-weight: 700; text-transform: uppercase; font-size: 0.8rem;">Currency Converter</button>
                </div>

                <!-- TAB 1: CALCULATOR -->
                <div id="tab-calc" class="utility-tab">
                    <div style="max-width: 300px; background: #f4f4f4; padding: 15px; border-radius: 6px; border: 1px solid #ddd;">
                        <input type="text" id="calc-screen" readonly style="width: 100%; height: 45px; font-size: 1.5rem; text-align: right; margin-bottom: 12px; padding: 5px; background: #fff; border: 1px solid #ccc;" value="0">
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">
                            <button onclick="calcClear()" style="padding: 12px; font-weight: bold; background: #ff3333; color: #fff; border: none; cursor: pointer;">C</button>
                            <button onclick="calcAppend('/')" style="padding: 12px; font-weight: bold; background: #ddd; border: none; cursor: pointer;">÷</button>
                            <button onclick="calcAppend('*')" style="padding: 12px; font-weight: bold; background: #ddd; border: none; cursor: pointer;">×</button>
                            <button onclick="calcAppend('-')" style="padding: 12px; font-weight: bold; background: #ddd; border: none; cursor: pointer;">-</button>
                            
                            <button onclick="calcAppend('7')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">7</button>
                            <button onclick="calcAppend('8')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">8</button>
                            <button onclick="calcAppend('9')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">9</button>
                            <button onclick="calcAppend('+')" style="padding: 12px; font-weight: bold; background: #ddd; border: none; cursor: pointer;">+</button>
                            
                            <button onclick="calcAppend('4')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">4</button>
                            <button onclick="calcAppend('5')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">5</button>
                            <button onclick="calcAppend('6')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">6</button>
                            <button onclick="calcCalculate()" style="padding: 12px; font-weight: bold; background: #111; color: #fff; border: none; cursor: pointer; grid-row: span 2;">=</button>
                            
                            <button onclick="calcAppend('1')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">1</button>
                            <button onclick="calcAppend('2')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">2</button>
                            <button onclick="calcAppend('3')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">3</button>
                            
                            <button onclick="calcAppend('0')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer; grid-column: span 2;">0</button>
                            <button onclick="calcAppend('.')" style="padding: 12px; font-weight: bold; background: #fff; border: 1px solid #ccc; cursor: pointer;">.</button>
                        </div>
                    </div>
                </div>

                <!-- TAB 2: EXERCISE INTERVAL TIMER -->
                <div id="tab-timer" class="utility-tab" style="display: none;">
                    <div style="background: #f4f4f4; padding: 20px; border-radius: 6px; border: 1px solid #ddd; max-width: 360px;">
                        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                            <div>
                                <label style="font-size: 0.8rem; font-weight: 700; display: block;">Work (sec)</label>
                                <input type="number" id="timer-work" value="45" style="width: 80px; padding: 8px;">
                            </div>
                            <div>
                                <label style="font-size: 0.8rem; font-weight: 700; display: block;">Rest (sec)</label>
                                <input type="number" id="timer-rest" value="15" style="width: 80px; padding: 8px;">
                            </div>
                            <div>
                                <label style="font-size: 0.8rem; font-weight: 700; display: block;">Rounds</label>
                                <input type="number" id="timer-rounds" value="5" style="width: 70px; padding: 8px;">
                            </div>
                        </div>
                        <div id="timer-display-box" style="background: #111; color: #00ffcc; font-size: 2.2rem; font-family: monospace; text-align: center; padding: 20px; margin-bottom: 15px; border-radius: 4px;">
                            READY
                        </div>
                        <div style="display: flex; gap: 10px;">
                            <button onclick="startWorkoutTimer()" style="flex: 2; padding: 10px; background: #28a745; color: #fff; border: none; font-weight: bold; cursor: pointer;">Start</button>
                            <button onclick="pauseWorkoutTimer()" style="flex: 1; padding: 10px; background: #ffc107; color: #111; border: none; font-weight: bold; cursor: pointer;">Pause</button>
                            <button onclick="resetWorkoutTimer()" style="flex: 1; padding: 10px; background: #dc3545; color: #fff; border: none; font-weight: bold; cursor: pointer;">Reset</button>
                        </div>
                    </div>
                </div>

                <!-- TAB 3: WORLD TIME -->
                <div id="tab-time" class="utility-tab" style="display: none;">
                    <p style="font-size: 0.85rem; color: #555; margin-bottom: 15px;">Live time across major international business, tech, and financial capitals.</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        <div style="background: #fff; padding: 15px; border: 1px solid #ddd; text-align: center;">
                            <strong style="font-size: 0.9rem;">South Africa (SAST)</strong>
                            <div id="time-sast" style="font-size: 1.2rem; font-weight: 800; color: #ff3333; margin-top: 6px;">--:--:--</div>
                        </div>
                        <div style="background: #fff; padding: 15px; border: 1px solid #ddd; text-align: center;">
                            <strong style="font-size: 0.9rem;">New York (EST/EDT)</strong>
                            <div id="time-ny" style="font-size: 1.2rem; font-weight: 800; color: #111; margin-top: 6px;">--:--:--</div>
                        </div>
                        <div style="background: #fff; padding: 15px; border: 1px solid #ddd; text-align: center;">
                            <strong style="font-size: 0.9rem;">London (GMT/BST)</strong>
                            <div id="time-london" style="font-size: 1.2rem; font-weight: 800; color: #111; margin-top: 6px;">--:--:--</div>
                        </div>
                        <div style="background: #fff; padding: 15px; border: 1px solid #ddd; text-align: center;">
                            <strong style="font-size: 0.9rem;">Paris / France (CET)</strong>
                            <div id="time-paris" style="font-size: 1.2rem; font-weight: 800; color: #111; margin-top: 6px;">--:--:--</div>
                        </div>
                        <div style="background: #fff; padding: 15px; border: 1px solid #ddd; text-align: center;">
                            <strong style="font-size: 0.9rem;">Tokyo (JST)</strong>
                            <div id="time-tokyo" style="font-size: 1.2rem; font-weight: 800; color: #111; margin-top: 6px;">--:--:--</div>
                        </div>
                        <div style="background: #fff; padding: 15px; border: 1px solid #ddd; text-align: center;">
                            <strong style="font-size: 0.9rem;">Sydney (AEST/AEDT)</strong>
                            <div id="time-sydney" style="font-size: 1.2rem; font-weight: 800; color: #111; margin-top: 6px;">--:--:--</div>
                        </div>
                    </div>
                </div>

                <!-- TAB 4: CURRENCY CONVERTER -->
                <div id="tab-currency" class="utility-tab" style="display: none;">
                    <div style="background: #fff; padding: 20px; border: 1px solid #ddd; max-width: 450px;">
                        <p style="font-size: 0.85rem; color: #555; margin-bottom: 15px;">Convert across the world's leading global currencies.</p>
                        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 12px; flex-wrap: wrap;">
                            <input type="number" id="curr-amount" value="100" oninput="convertCurrency()" style="padding: 8px; font-size: 1rem; width: 90px; border: 1px solid #ccc;">
                            <select id="curr-from" onchange="convertCurrency()" style="padding: 8px; font-size: 0.95rem; border: 1px solid #ccc;">
                                <option value="USD">USD ($)</option>
                                <option value="EUR">EUR (€)</option>
                                <option value="GBP">GBP (£)</option>
                                <option value="ZAR" selected>ZAR (R)</option>
                                <option value="JPY">JPY (¥)</option>
                                <option value="AUD">AUD ($)</option>
                                <option value="CAD">CAD ($)</option>
                                <option value="CHF">CHF (Fr)</option>
                                <option value="CNY">CNY (¥)</option>
                                <option value="INR">INR (₹)</option>
                            </select>
                            <span style="font-weight: bold;">to</span>
                            <select id="curr-to" onchange="convertCurrency()" style="padding: 8px; font-size: 0.95rem; border: 1px solid #ccc;">
                                <option value="USD" selected>USD ($)</option>
                                <option value="EUR">EUR (€)</option>
                                <option value="GBP">GBP (£)</option>
                                <option value="ZAR">ZAR (R)</option>
                                <option value="JPY">JPY (¥)</option>
                                <option value="AUD">AUD ($)</option>
                                <option value="CAD">CAD ($)</option>
                                <option value="CHF">CHF (Fr)</option>
                                <option value="CNY">CNY (¥)</option>
                                <option value="INR">INR (₹)</option>
                            </select>
                        </div>
                        <div style="background: #f4f4f4; padding: 12px; font-size: 1.2rem; font-weight: 800; text-align: center; border: 1px solid #ccc;" id="curr-result">
                            $ 5.48
                        </div>
                    </div>
                </div>
            </div>
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
            <p>Searched By Her</p>
        </footer>
    </div>

    <!-- AUDIO BEEP GENERATOR USING STANDARD HTML5 AUDIO -->
    <audio id="timer-beep" src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" preload="auto"></audio>

    <script>
    function switchTab(tabName) {
        document.querySelectorAll('.utility-tab').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[id^="btn-"]').forEach(el => { el.style.background = '#eee'; el.style.color = '#111'; });
        document.getElementById('tab-' + tabName).style.display = 'block';
        document.getElementById('btn-' + tabName).style.background = '#111';
        document.getElementById('btn-' + tabName).style.color = '#fff';
    }

    function calcAppend(val) {
        let screen = document.getElementById('calc-screen');
        if (screen.value === '0' || screen.value === 'Error') screen.value = '';
        screen.value += val;
    }
    function calcClear() { document.getElementById('calc-screen').value = '0'; }
    function calcCalculate() {
        let screen = document.getElementById('calc-screen');
        try { screen.value = eval(screen.value); } catch { screen.value = 'Error'; }
    }

    // --- RELIABLE AUDIO BEEP PLAYER ---
    function playBeepSound() {
        const beep = document.getElementById('timer-beep');
        if (beep) {
            beep.currentTime = 0;
            beep.play().catch(e => console.log("Audio waiting for user gesture"));
        }
    }

    let timerInterval = null, currentTime = 0, currentPhase = 'READY', currentRound = 1;
    function startWorkoutTimer() {
        if (timerInterval) return;
        
        playBeepSound();

        let workTime = parseInt(document.getElementById('timer-work').value) || 45;
        let restTime = parseInt(document.getElementById('timer-rest').value) || 15;
        let totalRounds = parseInt(document.getElementById('timer-rounds').value) || 5;
        
        if (currentPhase === 'READY') { 
            currentPhase = 'WORK'; 
            currentTime = workTime; 
        }
        
        timerInterval = setInterval(() => {
            if (currentTime > 1) {
                currentTime--;
                document.getElementById('timer-display-box').innerText = `${currentPhase}: ${currentTime}s (Rd ${currentRound})`;
                if (currentTime <= 3) {
                    playBeepSound();
                }
            } else if (currentTime === 1) {
                currentTime--;
                document.getElementById('timer-display-box').innerText = `${currentPhase}: ${currentTime}s (Rd ${currentRound})`;
                playBeepSound();
            } else {
                playBeepSound();
                if (currentPhase === 'WORK') { 
                    currentPhase = 'REST'; 
                    currentTime = restTime; 
                } else {
                    currentRound++;
                    if (currentRound > totalRounds) {
                        clearInterval(timerInterval); timerInterval = null;
                        currentPhase = 'DONE';
                        document.getElementById('timer-display-box').innerText = 'WORKOUT COMPLETE!';
                        playBeepSound();
                        return;
                    }
                    currentPhase = 'WORK'; 
                    currentTime = workTime;
                }
            }
        }, 1000);
    }
    function pauseWorkoutTimer() { 
        clearInterval(timerInterval); 
        timerInterval = null; 
        playBeepSound();
    }
    function resetWorkoutTimer() {
        pauseWorkoutTimer(); 
        currentPhase = 'READY'; 
        currentRound = 1;
        document.getElementById('timer-display-box').innerText = 'READY';
        playBeepSound();
    }

    function updateClocks() {
        const now = new Date();
        if(document.getElementById('time-sast')) {
            document.getElementById('time-sast').innerText = now.toLocaleTimeString('en-US', { timeZone: 'Africa/Johannesburg' });
            document.getElementById('time-ny').innerText = now.toLocaleTimeString('en-US', { timeZone: 'America/New_York' });
            document.getElementById('time-london').innerText = now.toLocaleTimeString('en-US', { timeZone: 'Europe/London' });
            document.getElementById('time-paris').innerText = now.toLocaleTimeString('en-US', { timeZone: 'Europe/Paris' });
            document.getElementById('time-tokyo').innerText = now.toLocaleTimeString('en-US', { timeZone: 'Asia/Tokyo' });
            document.getElementById('time-sydney').innerText = now.toLocaleTimeString('en-US', { timeZone: 'Australia/Sydney' });
        }
    }
    setInterval(updateClocks, 1000);
    updateClocks();

    const rates = { 
        USD: 1.0, EUR: 0.92, GBP: 0.79, ZAR: 18.25, 
        JPY: 152.50, AUD: 1.52, CAD: 1.38, CHF: 0.89, 
        CNY: 7.12, INR: 83.20 
    };
    
    function convertCurrency() {
        const amount = parseFloat(document.getElementById('curr-amount').value) || 0;
        const from = document.getElementById('curr-from').value;
        const to = document.getElementById('curr-to').value;
        const inUSD = amount / rates[from];
        const converted = inUSD * rates[to];
        const symbols = { 
            USD: '$', EUR: '€', GBP: '£', ZAR: 'R ', 
            JPY: '¥', AUD: 'A$', CAD: 'C$', CHF: 'Fr ', 
            CNY: '¥', INR: '₹ ' 
        };
        document.getElementById('curr-result').innerText = symbols[to] + converted.toFixed(2);
    }
    if(document.getElementById('curr-amount')) convertCurrency();
    </script>
</body>
</html>
'''
    with open('tools/index.html', 'w', encoding='utf-8') as f:
        f.write(tools_page_content)

    # 5. Build Individual Article Pages & Category Archives (Clean Folder URLs)
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

    print("Successfully built site with robust trust pages, Disclaimer page, author profile, and clean folder URLs!")

if __name__ == '__main__':
    build_site()