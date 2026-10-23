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
        },
        "Finance, Crypto & Markets": {
            "folder": "Finances",
            "filename": "Finance, Crypto & Markets.html",
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
            post_link = f"/categories/{folder}/{article['slug']}.html"

            cards += f'''
                <article class="article-card">
                    <div class="meta">{cat_name} &bull; {article['date']}</div>
                    <h2><a href="{post_link}">{article['title']}</a></h2>
                    <p>{article['excerpt']}</p>
                </article>'''
        return cards

    # Shared Navigation HTML snippet (Including Finance)
    def get_nav(active_page="home"):
        return f'''
            <header>
                <a href="/index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
                <nav>
                    <a href="/index.html" class="{'active' if active_page=='home' else ''}">Home</a>
                    <a href="/categories/AI/Artificial Intelligence & Practical Automation.html" class="{'active' if active_page=='ai' else ''}">AI</a>
                    <a href="/categories/Hardware/Consumer Tech & Hardware Reviews.html" class="{'active' if active_page=='hardware' else ''}">Hardware</a>
                    <a href="/categories/Software/Software, Apps & Digital Tools.html" class="{'active' if active_page=='software' else ''}">Software</a>
                    <a href="/categories/Finances/Finance, Crypto & Markets.html" class="{'active' if active_page=='finance' else ''}">Finance</a>
                    <a href="/tools.html" class="{'active' if active_page=='tools' else ''}" style="color: #ff3333;">⚡ Tools</a>
                </nav>
            </header>
        '''

    # 3. Build Homepage (index.html)
    home_cards = generate_cards(articles)
    
    index_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechWitHer - The Digital Tech & Finance Magazine</title>
    <link rel="icon" type="image/svg+xml" href="techwither.svg">
    <link rel="stylesheet" href="style.css">
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

    # 4. Build Dedicated Tools Page (tools.html)
    tools_page_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Online Calculator, HIIT Workout Timer, World Clock & Currency Converter - TechWitHer</title>
    <meta name="description" content="Use TechWitHer's free online everyday utilities: instant math calculator, customizable HIIT exercise timer with audio beeps, live world clocks, and multi-currency converter.">
    <link rel="icon" type="image/svg+xml" href="techwither.svg">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <a href="/index.html" class="brand">TechWitHer<span class="red-dot">.</span></a>
            <nav>
                <a href="/index.html">Home</a>
                <a href="/categories/AI/Artificial Intelligence & Practical Automation.html">AI</a>
                <a href="/categories/Hardware/Consumer Tech & Hardware Reviews.html">Hardware</a>
                <a href="/categories/Software/Software, Apps & Digital Tools.html">Software</a>
                <a href="/categories/Finances/Finance, Crypto & Markets.html">Finance</a>
                <a href="/tools.html" class="active" style="color: #ff3333; border-bottom: 2px solid #ff3333; padding-bottom: 3px;">⚡ Tools</a>
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

                <!-- TAB 2: EXERCISE INTERVAL TIMER WITH AUDIO -->
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
            <p>&copy; 2026 TechWitHer. All rights reserved.</p>
            <p>Searched By Her</p>
        </footer>
    </div>

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

    // --- AUDIO BEEPS FOR WORKOUT TIMER ---
    function playAudioTone(frequency, duration) {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.value = frequency;
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
            osc.stop(ctx.currentTime + duration);
        } catch (e) {
            console.log("Audio not supported or blocked by browser policy");
        }
    }

    let timerInterval = null, currentTime = 0, currentPhase = 'READY', currentRound = 1;
    function startWorkoutTimer() {
        if (timerInterval) return;
        let workTime = parseInt(document.getElementById('timer-work').value) || 45;
        let restTime = parseInt(document.getElementById('timer-rest').value) || 15;
        let totalRounds = parseInt(document.getElementById('timer-rounds').value) || 5;
        
        if (currentPhase === 'READY') { 
            currentPhase = 'WORK'; 
            currentTime = workTime; 
            playAudioTone(880, 0.4); // High start beep
        }
        
        timerInterval = setInterval(() => {
            if (currentTime > 1) {
                currentTime--;
                document.getElementById('timer-display-box').innerText = `${currentPhase}: ${currentTime}s (Rd ${currentRound})`;
                if (currentTime <= 3) {
                    playAudioTone(440, 0.15); // Countdown tick beeps
                }
            } else if (currentTime === 1) {
                currentTime--;
                document.getElementById('timer-display-box').innerText = `${currentPhase}: ${currentTime}s (Rd ${currentRound})`;
                playAudioTone(440, 0.15);
            } else {
                if (currentPhase === 'WORK') { 
                    currentPhase = 'REST'; 
                    currentTime = restTime; 
                    playAudioTone(300, 0.5); // Lower rest beep
                } else {
                    currentRound++;
                    if (currentRound > totalRounds) {
                        clearInterval(timerInterval); timerInterval = null;
                        currentPhase = 'DONE';
                        document.getElementById('timer-display-box').innerText = 'WORKOUT COMPLETE!';
                        playAudioTone(600, 0.8); // Completion fanfare beep
                        return;
                    }
                    currentPhase = 'WORK'; 
                    currentTime = workTime;
                    playAudioTone(880, 0.4); // Next work round beep
                }
            }
        }, 1000);
    }
    function pauseWorkoutTimer() { clearInterval(timerInterval); timerInterval = null; }
    function resetWorkoutTimer() {
        pauseWorkoutTimer(); currentPhase = 'READY'; currentRound = 1;
        document.getElementById('timer-display-box').innerText = 'READY';
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

    # 5. Build Individual Article Pages & Category Archives (If articles exist)
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
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3209789109672774" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        {get_nav('none')}
        <main>
            <article class="post-content">
                <h1>{article['title']}</h1>
                <p class="post-meta">{article['category']} &bull; {article['date']}</p>
                {article_content_html}
            </article>
        </main>
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

        for cat_name, config in category_config.items():
            folder = config["folder"]
            filename = config["filename"]
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
    <link rel="icon" type="image/svg+xml" href="../../techwither.svg">
    <link rel="stylesheet" href="../../style.css">
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

    print("Successfully built site with Finance category and updated navigation!")

if __name__ == '__main__':
    build_site()