import json
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, make_response
import database

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'limahcode_super_adventure_secret_2026')

# Initialize SQLite database
database.init_db()

def get_teacher_config():
    config_path = os.path.join(app.root_path, 'teacher_config.json')
    if not os.path.exists(config_path):
        default_config = {"unlocked_lessons": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "unlocked_challenges": [1, 2, 3]}
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {"unlocked_lessons": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "unlocked_challenges": [1, 2, 3]}

@app.context_processor
def inject_global_context():
    config = get_teacher_config()
    current_user = None
    if 'user_id' in session:
        current_user = database.get_user_by_id(session['user_id'])
    try:
        site_theme = database.get_site_theme()
    except Exception:
        site_theme = getattr(database, 'DEFAULT_THEME', {})
    return {
        "teacher_unlocked_lessons": config.get("unlocked_lessons", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        "teacher_unlocked_challenges": config.get("unlocked_challenges", [1, 2, 3]),
        "current_user": current_user,
        "theme": site_theme
    }


# Lesson and Challenge data structure for the 3-week HTML & CSS Adventure
LESSONS = {
    1: {
        "id": 1,
        "week": 1,
        "week_title": "Discovering HTML (Building the Structure)",
        "title": "What is a Website? & Tech Giants Page",
        "day": "Saturday",
        "description": "Learn standard HTML (<!DOCTYPE html>, <html>, <body>) and build a fun Tech Giants page using <h1>, <p>, and <br>!",
        "points": 10,
        "concept": "HTML is the skeleton of the web! We use <h1>-<h6> for titles (like company names), <p> for descriptions, and <br> for line breaks!",
        "steps": [
            {"title": "What is a Website?", "text": "Every webpage (Google, YouTube, TikTok) is written in HTML. Your browser reads the HTML document and draws it on screen."},
            {"title": "The HTML Skeleton", "text": "Start with `<!DOCTYPE html>`. Wrap everything in `<html>`. Put hidden info in `<head>` and everything visible inside `<body>`."},
            {"title": "Headings (<h1>-<h6>) & Paragraphs (<p>)", "text": "Use `<h1>` for big titles (like **Google** or **Meta**) and `<p>` for descriptions of what they built."},
            {"title": "Line Breaks (<br>)", "text": "Use `<br>` inside a paragraph to start a new line without making a whole new paragraph block!"}
        ],
        "example": "<!DOCTYPE html>\n<html>\n<head>\n  <title>Tech Giants</title>\n</head>\n<body>\n  <h1>Google</h1>\n  <p>Founded by Larry Page & Sergey Brin.<br>Products: Search, YouTube, and Android!</p>\n  \n  <h2>Meta</h2>\n  <p>Founded by Mark Zuckerberg.<br>Products: Facebook, Instagram, and WhatsApp!</p>\n</body>\n</html>",
        "editor_template": "<!-- 🎯 Lesson 1 Task: Build your Tech Giants page! -->\n<!-- 1. Add <!DOCTYPE html>, <html>, and <body> tags -->\n<!-- 2. Inside <body>, add an <h1> heading with a company name -->\n<!-- 3. Add a <p> with a <br> line break describing what they built -->\n\n",
        "solution_check": "code.toLowerCase().includes('<!doctype html>') && code.includes('<html>') && code.includes('<body>') && code.includes('<h1>') && code.includes('<br>')"
    },
    2: {
        "id": 2,
        "week": 1,
        "week_title": "Discovering HTML (Building the Structure)",
        "title": "Lists (UL vs OL) & Inline Spans (<span>)",
        "day": "Sunday",
        "description": "Learn how to build Bulleted (<ul>) and Numbered (<ol>) lists, and use <span> to group specific words!",
        "points": 10,
        "concept": "Use <ul> for bulleted lists, <ol> for numbered rankings, and <span> to target specific inline text for styling!",
        "steps": [
            {"title": "Bulleted Lists (<ul>)", "text": "Use `<ul>` (Unordered List) for bullet points. Each item gets an `<li>` tag (e.g., list of tech products)."},
            {"title": "Numbered Lists (<ol>)", "text": "Use `<ol>` (Ordered List) when order matters (1, 2, 3)! Example: Top 3 Most Downloaded Apps."},
            {"title": "Inline Spans (<span>)", "text": "Use `<span>` to wrap specific words inside a sentence so you can target them later for colors or styles!"}
        ],
        "example": "<h2>Top Tech Companies</h2>\n<ul>\n  <li><span>Google</span> (Search Engine)</li>\n  <li><span>Apple</span> (Smartphones)</li>\n</ul>\n\n<h2>Top 3 Apps</h2>\n<ol>\n  <li>TikTok</li>\n  <li>WhatsApp</li>\n  <li>Instagram</li>\n</ol>",
        "editor_template": "<!-- 🎯 Lesson 2 Task: Lists and Spans -->\n<!-- 1. Create an ordered list (<ol>) with at least 2 items (<li>) -->\n<!-- 2. Wrap at least one word inside a <span> tag! -->\n\n",
        "solution_check": "code.includes('<ol>') && code.includes('</ol>') && code.includes('<span>') && (code.match(/<li>/g) || []).length >= 2"
    },
    3: {
        "id": 3,
        "week": 1,
        "week_title": "Discovering HTML (Building the Structure)",
        "title": "Links, Images & Interactive Webpages!",
        "day": "Wednesday",
        "description": "Bring your website to life with clickable links (<a>) and awesome images (<img>)!",
        "points": 10,
        "concept": "Attributes give HTML tags superpower powers! We use 'href' for links to tell the browser where to go, and 'src', 'alt', and 'width' for images.",
        "steps": [
            {"title": "Clickable Links (<a> tag & href)", "text": "We use the `<a>` (anchor) tag to create links. The `href=\"...\"` attribute tells the browser where to take the user when clicked! Example: `<a href=\"https://google.com\">Search Google</a>`."},
            {"title": "Adding Pictures (<img> tag & src)", "text": "We use the `<img>` tag to show images. Unlike `<h1>` or `<p>`, `<img>` is **self-closing** (no `</img>` needed!). It uses `src=\"...\"` (source) to point to the image location."},
            {"title": "Image Attributes (alt, width, & height)", "text": "Control your images with attributes inside `<img ...>`:\n• **`alt=\"description\"`**: Text that displays if the image fails to load (great for screen readers!).\n• **`width=\"200\"`** & **`height=\"200\"`**: Controls how big or small the picture appears on screen in pixels (px)!"}
        ],
        "example": "<!-- Clickable Link with href -->\n<a href=\"https://google.com\">Search Google</a>\n\n<!-- Image with src, alt, width, and height -->\n<img src=\"https://picsum.photos/300/200\" alt=\"Random Picture\" width=\"250\" height=\"180\">",
        "editor_template": "<!-- 🎯 Lesson 3 Task: Images & Links -->\n<!-- 1. Add an <img> tag with src and alt attributes -->\n<!-- 2. Add an <a> link tag with an href attribute -->\n\n",
        "solution_check": "code.includes('<a') && code.includes('href') && code.includes('<img') && code.includes('src')"
    },
    4: {
        "id": 4,
        "week": 2,
        "week_title": "Becoming an HTML Creator",
        "title": "Forms, Input Fields & Page Navigation!",
        "day": "Saturday",
        "description": "Learn how <form action=\"dashboard.html\"> redirects users to another HTML page when they click Register!",
        "points": 15,
        "concept": "Forms (<form action=\"dashboard.html\">) direct users to another file in your folder! Use <label> for field names, <input> for typing, and <button type=\"submit\"> to submit!",
        "steps": [
            {"title": "1. The Form Action Attribute (<form action=\"...\">)", "text": "To make a form send users to another page in your folder (like `dashboard.html` or `login.html`) when they click Register/Submit, we add `action=\"dashboard.html\"` inside `<form>`!"},
            {"title": "2. Labels & Input Types (<label> & <input>)", "text": "Use `<label>` for field titles. Use `<input>` for user typing: `type=\"text\"` for names, `type=\"email\"` for emails, and `type=\"password\"` to hide passwords!"},
            {"title": "3. Submit Button (<button type=\"submit\">)", "text": "Clicking `<button type=\"submit\">` activates the form's `action=\"dashboard.html\"` and takes the user straight to their dashboard.html file!"},
            {"title": "4. Combining Everything!", "text": "Combine your form with an `<h1>` heading, `<p>` description, `<img>` banner, `<ul>` feature list, and `<a>` link!"}
        ],
        "example": "<!-- Form that redirects to dashboard.html in your folder on submit -->\n<h1>🚀 Join LimahCode Club</h1>\n<p>Fill out the form below to enter your dashboard!</p>\n\n<img src=\"https://picsum.photos/300/150\" alt=\"LimahCode Banner\" width=\"250\" height=\"120\">\n\n<!-- action=\"dashboard.html\" directs the user to dashboard.html when they click Submit! -->\n<form action=\"dashboard.html\">\n  <label>Full Name:</label><br>\n  <input type=\"text\" placeholder=\"Enter your name\"><br><br>\n  \n  <label>Email Address:</label><br>\n  <input type=\"email\" placeholder=\"name@example.com\"><br><br>\n  \n  <button type=\"submit\">Register & Go to Dashboard 🚀</button>\n</form>",
        "editor_template": "<!-- 🎯 Lesson 4 Task: Build a Form with Action -->\n<!-- 1. Create a <form action=\"dashboard.html\"> tag -->\n<!-- 2. Inside the form, add an <input> tag and a <button type=\"submit\"> -->\n\n",
        "solution_check": "code.includes('<form') && code.includes('action') && code.includes('</form>') && code.includes('<input') && code.includes('<button')"
    },
    5: {
        "id": 5,
        "week": 2,
        "week_title": "Becoming an HTML Creator",
        "title": "HTML Tables & Organizing Info",
        "day": "Sunday",
        "description": "Learn how to structure information in grids using rows, headers, and columns.",
        "points": 15,
        "concept": "Tables (<table>) organize data into rows (<tr>), headers (<th>), and standard cells (<td>).",
        "steps": [
            {"title": "Table Structure", "text": "Every table starts with `<table>` and ends with `</table>`."},
            {"title": "Rows and Headers", "text": "We create a new row using `<tr>` (Table Row). Inside a row, we use `<th>` (Table Header) for titles. These are bold and centered by default."},
            {"title": "Table Data Cells", "text": "Inside regular rows, we use `<td>` (Table Data) for the actual information cells. For example:\n`<tr>`\n`  <td>Iron Man</td>`\n`  <td>Flying Suit</td>`\n`</tr>`"}
        ],
        "example": "<table>\n  <tr>\n    <th>Superhero</th>\n    <th>Superpower</th>\n  </tr>\n  <tr>\n    <td>Spider-Man</td>\n    <td>Web-slinging</td>\n  </tr>\n</table>",
        "editor_template": "<!-- 🎯 Lesson 5 Task: Build a Table -->\n<!-- 1. Create a <table> with at least 1 row (<tr>) -->\n<!-- 2. Add at least 2 data cells (<td>) inside the row -->\n\n",
        "solution_check": "code.includes('<table>') && code.includes('</table>') && code.includes('<tr>') && code.includes('</tr>') && (code.match(/<td>/g) || []).length >= 2"
    },
    6: {
        "id": 6,
        "week": 2,
        "week_title": "Becoming an HTML Creator",
        "title": "Combining Everything to Build a Full Webpage!",
        "day": "Wednesday",
        "description": "Combine header, main, footer, divs, forms, tables, lists, and images to create a real multi-section website!",
        "points": 15,
        "concept": "Real websites use layout boxes! We use <header> for the top banner, <main> for content sections (grouped with <div>), and <footer> for the bottom.",
        "steps": [
            {"title": "1. Layout Structure (<header>, <main>, <footer>)", "text": "Organize your page like a pro: `<header>` for your title and logo, `<main>` for your primary content, and `<footer>` for your copyright/contact info."},
            {"title": "2. Grouping Content with <div>", "text": "Use `<div>` (divider container) boxes to separate your page into distinct sections—like a Game Leaderboard box and a Sign-Up Form box!"},
            {"title": "3. The Big Showcase", "text": "Put everything together: Headings, Paragraphs, Images, Lists, Tables, and Forms all inside one complete webpage!"}
        ],
        "example": "<!-- Complete Multi-Section Webpage -->\n<header>\n  <h1>🚀 LimahCode Game Zone</h1>\n  <p>Play, compete, and learn code!</p>\n</header>\n\n<main>\n  <div>\n    <h2>🏆 High Scores</h2>\n    <table border=\"1\">\n      <tr><th>Player</th><th>Score</th></tr>\n      <tr><td>Alex</td><td>9500</td></tr>\n    </table>\n  </div>\n  \n  <br>\n  \n  <div>\n    <h2>📩 Player Registration</h2>\n    <form action=\"dashboard.html\">\n      <label>Gamertag:</label><br>\n      <input type=\"text\" placeholder=\"Enter gamertag\"><br><br>\n      <button type=\"submit\">Register</button>\n    </form>\n  </div>\n</main>\n\n<footer>\n  <p>© 2026 LimahCode Academy | <a href=\"https://google.com\">Privacy</a></p>\n</footer>",
        "editor_template": "<!-- 🎯 Lesson 6 Task: Multi-Section Layout -->\n<!-- 1. Use <div> container tags to group your content -->\n<!-- 2. Write your full webpage structure below: -->\n\n",
        "solution_check": "code.toLowerCase().includes('<div>') && code.toLowerCase().includes('</div>')"
    },
    7: {
        "id": 7,
        "week": 3,
        "week_title": "Making Websites Beautiful with CSS",
        "title": "Intro to CSS, Colors & Backgrounds",
        "day": "Saturday",
        "description": "Style your HTML using CSS selectors, changing background colors and text properties.",
        "points": 20,
        "concept": "CSS (Cascading Style Sheets) adds style to structure. You target elements by their name (like 'h1' or 'body') and change their properties.",
        "steps": [
            {"title": "What is CSS?", "text": "CSS describes how HTML elements look. While HTML creates the content, CSS paints the colors, sizes the text, and designs the layout."},
            {"title": "The CSS Rule Structure", "text": "A CSS rule looks like this:\n`h1 {`\n`  color: blue;`\n`  font-size: 24px;`\n`}`\nHere, `h1` is the **selector** (who we style), `color` is the **property**, and `blue` is the **value**."},
            {"title": "Backgrounds", "text": "You can change background colors using `background-color: coral;` or background images using `background-image`."}
        ],
        "example": "<style>\n  body {\n    background-color: #f0fdf4;\n  }\n  h1 {\n    color: #15803d;\n  }\n  p {\n    color: #374151;\n  }\n</style>\n<h1>Green Vibes</h1>\n<p>This page is custom styled using CSS colors!</p>",
        "editor_template": "<!-- Add a CSS rule in the <style> tag to make the <p> tag text color 'purple'! -->\n<style>\n  p {\n    \n  }\n</style>\n<p>Make me purple!</p>",
        "solution_check": "code.includes('color') && code.includes('purple')"
    },
    8: {
        "id": 8,
        "week": 3,
        "week_title": "Making Websites Beautiful with CSS",
        "title": "Fonts, Borders, Margins, & Padding",
        "day": "Sunday",
        "description": "Understand the Box Model: margins, borders, padding, and custom fonts.",
        "points": 20,
        "concept": "Every element on a webpage is a box. Padding is space inside the box; margin is space outside the box; border is the outline.",
        "steps": [
            {"title": "The Box Model", "text": "Elements have width and height, plus three outer rings: **Padding** (clears an area around the content), **Border** (goes around padding), and **Margin** (clears an area outside the border)."},
            {"title": "Styling Text and Borders", "text": "We can change text looks with `font-family: Arial;`, `font-weight: bold;`, and align it using `text-align: center;`."},
            {"title": "Borders", "text": "Add borders like this: `border: 4px solid black;`. You can round the corners with `border-radius: 12px;`!"}
        ],
        "example": "<style>\n  .card {\n    border: 3px solid red;\n    border-radius: 16px;\n    padding: 20px;\n    margin: 10px;\n    background-color: lightyellow;\n    font-family: Arial, sans-serif;\n  }\n</style>\n<div class=\"card\">\n  <h3>A Beautiful Box</h3>\n  <p>Check out my round borders and padding!</p>\n</div>",
        "editor_template": "<!-- In the style tag, give the .box class a border-radius of '15px' and a padding of '20px'! -->\n<style>\n  .box {\n    border: 2px solid blue;\n    \n    \n  }\n</style>\n<div class=\"box\">\n  Styling Boxes!\n</div>",
        "solution_check": "code.includes('border-radius') && code.includes('padding') && code.includes('15px') && code.includes('20px')"
    },
    9: {
        "id": 9,
        "week": 3,
        "month": 3,
        "week_title": "Month 3: JavaScript Programming (The Brain & Interactivity)",
        "title": "What is JavaScript? Variables & Data Types",
        "day": "Wednesday",
        "description": "Give your websites a brain! Learn how JavaScript makes pages interactive with variables (let, const) and numbers/text.",
        "points": 25,
        "concept": "HTML is the skeleton, CSS is the style, and JavaScript is the brain! We use variables like 'let' to remember player names, scores, and lives.",
        "steps": [
            {"title": "The Power of JavaScript", "text": "JavaScript allows websites to calculate scores, play sounds, react to clicks, and change content dynamically without refreshing the page."},
            {"title": "Variables: `let` and `const`", "text": "Use `let score = 0;` to store values that can change. Use `const gameName = 'CyberGame';` for values that stay constant."},
            {"title": "Running JavaScript in HTML", "text": "Wrap your JS code inside `<script> ... </script>` tags at the bottom of your HTML body!"}
        ],
        "example": "<!DOCTYPE html>\n<html>\n<body>\n  <h1 id=\"player-tag\">Player Profile</h1>\n  <p id=\"score-text\"></p>\n\n  <script>\n    let playerName = \"Alex\";\n    let score = 100;\n    document.getElementById(\"score-text\").textContent = playerName + \" has \" + score + \" points!\";\n  </script>\n</body>\n</html>",
        "editor_template": "<!-- 🎯 Lesson 9: Your First JavaScript Variable! -->\n<h1>Player Scoreboard</h1>\n<p id=\"status\"></p>\n\n<script>\n  // 1. Declare a variable called 'playerName' with your name\n  // 2. Declare a variable called 'level' with number 1\n  \n  \n</script>",
        "solution_check": "code.includes('<script>') && code.includes('</script>') && code.includes('playerName') && (code.includes('let ') || code.includes('const ') || code.includes('var '))"
    },
    10: {
        "id": 10,
        "week": 3,
        "month": 3,
        "week_title": "Month 3: JavaScript Programming (The Brain & Interactivity)",
        "title": "DOM Manipulation: Button Clicks & Live Actions",
        "day": "Friday",
        "description": "Connect HTML buttons to JavaScript using onclick and document.getElementById() to change webpage content in real time!",
        "points": 25,
        "concept": "The DOM (Document Object Model) lets JavaScript reach into the HTML page and change colors, text, or hide/show elements when a user clicks a button!",
        "steps": [
            {"title": "Selecting Elements: `document.getElementById()`", "text": "Give an HTML element an `id=\"my-box\"`. In JS, grab it with `document.getElementById('my-box')`."},
            {"title": "Button Click Events (`onclick`)", "text": "Add `onclick=\"myFunction()\"` to any button to run JavaScript code the moment a user clicks!"},
            {"title": "Changing Content dynamically", "text": "Use `.textContent = 'New text!'` or `.style.backgroundColor = 'coral'` to change page elements in real time."}
        ],
        "example": "<body>\n  <h2 id=\"headline\">Click the button to change me!</h2>\n  <button onclick=\"changeHeadline()\">Magic Button ✨</button>\n\n  <script>\n    function changeHeadline() {\n      document.getElementById('headline').textContent = '🎉 You Clicked Me!';\n      document.getElementById('headline').style.color = 'green';\n    }\n  </script>\n</body>",
        "editor_template": "<!-- 🎯 Lesson 10: Interactive Click Button! -->\n<h2 id=\"greeting\">Hello World</h2>\n<button onclick=\"sayHello()\">Click Me</button>\n\n<script>\n  function sayHello() {\n    // Change greeting text to 'Welcome to LimahCode!'\n    \n  }\n</script>",
        "solution_check": "code.includes('document.getElementById') && code.includes('onclick') && code.includes('function sayHello')"
    },
    11: {
        "id": 11,
        "week": 3,
        "month": 3,
        "week_title": "Month 3: JavaScript Programming (The Brain & Interactivity)",
        "title": "Conditionals (If/Else) & Building a Clicker Counter",
        "day": "Saturday",
        "description": "Learn programming logic with if/else statements and build a live Click Counter game!",
        "points": 30,
        "concept": "Conditionals let computers make decisions! If score >= 10, display 'Winner!'; else, display 'Keep clicking!'.",
        "steps": [
            {"title": "Making Decisions: `if` and `else`", "text": "Use `if (condition) { ... } else { ... }` to execute code depending on user actions."},
            {"title": "Click Counter Math", "text": "Increment numbers with `count = count + 1` or `count++` every time a button is clicked!"},
            {"title": "Live Score Feedback", "text": "Display win messages dynamically when reaching target milestones."}
        ],
        "example": "<body>\n  <h2>Cookie Counter: <span id=\"score\">0</span></h2>\n  <button onclick=\"tapCookie()\">🍪 Tap Cookie</button>\n  <p id=\"message\"></p>\n\n  <script>\n    let clicks = 0;\n    function tapCookie() {\n      clicks++;\n      document.getElementById('score').textContent = clicks;\n      if (clicks >= 5) {\n        document.getElementById('message').textContent = '🏆 Cookie Master Level!';\n      }\n    }\n  </script>\n</body>",
        "editor_template": "<!-- 🎯 Lesson 11: Build a Click Counter with if/else! -->\n<h2>Clicks: <span id=\"count\">0</span></h2>\n<button onclick=\"addPoint()\">+1 Point</button>\n<p id=\"feedback\"></p>\n\n<script>\n  let count = 0;\n  function addPoint() {\n    count++;\n    document.getElementById('count').textContent = count;\n    // If count >= 3, set feedback text to 'Great Job!'\n    \n  }\n</script>",
        "solution_check": "code.includes('count++') || code.includes('count = count + 1') && code.includes('if') && code.includes('document.getElementById')"
    },
    12: {
        "id": 12,
        "week": 3,
        "month": 3,
        "week_title": "Month 3: JavaScript Programming (The Brain & Interactivity)",
        "title": "Grand Graduation: Netlify Deployment & Live App Showcase",
        "day": "Bonus",
        "description": "Deploy your complete interactive HTML + CSS + JavaScript web app live on Netlify and prepare for class defense!",
        "points": 30,
        "concept": "Turn your code into a real, live web app accessible anywhere in the world on Netlify Drop with custom domain names!",
        "steps": [
            {"title": "Organizing your 3-Month Project", "text": "Bundle your `index.html`, styled CSS, and interactive JavaScript files into one neat project folder."},
            {"title": "Drag and Drop to Netlify", "text": "Drop your folder on **app.netlify.com/drop** to launch your live URL in 15 seconds!"},
            {"title": "Claim your Diploma", "text": "Present your live project in class to receive your official Junior Full-Stack Web Creator Diploma."}
        ],
        "example": "<!-- Live Project Deployed to Netlify -->\n<p>My Live Interactive App: <a href=\"https://limahcode-games.netlify.app\">limahcode-games.netlify.app</a></p>",
        "editor_template": "<!-- 🎯 Lesson 12: Paste your live Netlify or project URL below! -->\n<h1>My Grand Graduation Web App</h1>\n<p>Visit my live website: <a href=\"https://my-app.netlify.app\">Click Here</a></p>\n",
        "solution_check": "code.toLowerCase().includes('netlify.app') || code.toLowerCase().includes('vercel.app') || code.toLowerCase().includes('http') || code.toLowerCase().includes('https')"
    }
}

CHALLENGES = {
    1: {
        "id": 1,
        "week": 1,
        "month": 1,
        "title": "Month 1: HTML Explorer Capstone",
        "badge": "html_explorer",
        "badge_name": "Certified HTML Specialist",
        "instructions": "Create your first personal webpage! Your page must contain:\n1. A big heading (<h1>)\n2. A paragraph about yourself (<p>)\n3. A bulleted list (<ul> and <li>) with at least two hobbies\n4. A link (<a>) to your favorite website",
        "editor_template": "<!-- Build your first personal webpage here! -->\n<h1>My Webpage</h1>\n",
        "solution_check": "code.includes('<h1>') && code.includes('</h1>') && code.includes('<p>') && code.includes('</p>') && code.includes('<ul>') && code.includes('</ul>') && (code.match(/<li>/g) || []).length >= 2 && code.includes('<a') && code.includes('href')"
    },
    2: {
        "id": 2,
        "week": 2,
        "month": 2,
        "title": "Month 2: CSS Designer Showcase",
        "badge": "website_builder",
        "badge_name": "Certified CSS Stylist",
        "instructions": "Build a styled registration card! Your webpage must contain:\n1. A form container (<form>)\n2. Text inputs (<input type=\"text\">)\n3. A submit button (<button>)\n4. CSS rounded borders (border-radius) and padding!",
        "editor_template": "<!-- Build a styled registration card! -->\n",
        "solution_check": "code.includes('<form>') && code.includes('</form>') && code.includes('<input') && code.includes('<button') && (code.includes('border-radius') || code.includes('padding'))"
    },
    3: {
        "id": 3,
        "week": 3,
        "month": 3,
        "title": "Month 3: Full-Stack JavaScript Capstone",
        "badge": "junior_web_designer",
        "badge_name": "Junior Full-Stack Web Creator Diploma",
        "instructions": "Build your Final Graduation Interactive Web App!\nRequirements:\n1. Header and styled cards (<div class=\"card\">)\n2. Interactive button with an onclick event\n3. Dynamic JavaScript logic (variables and DOM updates)\n4. Beautiful CSS styling with rounded borders and padding!",
        "editor_template": "<!-- 🏆 Final Graduation Interactive Web App -->\n<style>\n  body {\n    background-color: lightyellow;\n    font-family: Arial, sans-serif;\n    padding: 20px;\n  }\n  .card {\n    border: 3px solid black;\n    border-radius: 14px;\n    padding: 20px;\n    background-color: white;\n    max-width: 500px;\n    margin: 20px auto;\n  }\n  button {\n    background-color: coral;\n    color: white;\n    padding: 10px 16px;\n    border-radius: 8px;\n    border: 2px solid black;\n    font-size: 16px;\n    cursor: pointer;\n  }\n</style>\n\n<div class=\"card\">\n  <h1>🚀 Interactive Game Counter</h1>\n  <p>Clicks: <span id=\"score-display\">0</span></p>\n  <button onclick=\"addClick()\">Tap Me!</button>\n</div>\n\n<script>\n  let score = 0;\n  function addClick() {\n    score++;\n    document.getElementById('score-display').textContent = score;\n  }\n</script>\n",
        "solution_check": "code.includes('class=\"card\"') && code.includes('<button') && code.includes('onclick') && code.includes('<script>') && code.includes('document.getElementById')"
    }
}

def get_client_device(client_hint=''):
    if client_hint and client_hint.strip() == 'Mobile':
        return 'Mobile'
    ua = request.headers.get('User-Agent', '').lower()
    mobile_agents = [
        'mobile', 'android', 'iphone', 'ipad', 'ipod', 
        'webos', 'blackberry', 'opera mini', 'iemobile', 
        'windows phone', 'huawei', 'xiaomi', 'redmi', 
        'samsungbrowser', 'silk', 'fennec', 'tablet', 'kindle'
    ]
    if any(m in ua for m in mobile_agents) or request.headers.get('Sec-CH-UA-Mobile') == '?1':
        return 'Mobile'
    if client_hint and client_hint.strip():
        return client_hint.strip()
    return 'Desktop'

@app.before_request
def track_portal_visitor():
    if request.method == 'GET':
        path = request.path
        if not path.startswith('/static') and not path.startswith('/api') and not path.startswith('/admin'):
            try:
                page_name = path if path != '/' else 'portal_home'
                device = get_client_device()
                referrer = request.referrer or ''
                database.record_analytics_event('portal_view', page_name, device, referrer)
            except Exception:
                pass

@app.route('/')
def welcome():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in with your registered student account to access the classroom.", "info")
        return redirect(url_for('login'))
    return render_template('dashboard.html', lessons=LESSONS, challenges=CHALLENGES)

@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    if 'user_id' not in session:
        flash("Please log in to access your coding lessons.", "info")
        return redirect(url_for('login'))
        
    if lesson_id not in LESSONS:
        return "Lesson not found!", 404
        
    config = get_teacher_config()
    unlocked = config.get("unlocked_lessons", [1])
    if lesson_id not in unlocked:
        return render_template('dashboard.html', lessons=LESSONS, challenges=CHALLENGES, locked_notice=True)
        
    lesson_data = LESSONS[lesson_id]
    
    # Identify associated challenge
    week_challenge = None
    for cid, chal in CHALLENGES.items():
        if chal["week"] == lesson_data["week"]:
            week_challenge = chal
            break
            
    return render_template('lesson.html', lesson=lesson_data, challenge=week_challenge, lessons=LESSONS)

@app.route('/challenge/<int:challenge_id>')
def challenge(challenge_id):
    if 'user_id' not in session:
        flash("Please log in to access this milestone capstone challenge.", "info")
        return redirect(url_for('login'))
        
    if challenge_id not in CHALLENGES:
        return "Challenge not found!", 404
        
    challenge_data = CHALLENGES[challenge_id]
    return render_template('challenge.html', challenge=challenge_data, lessons=LESSONS)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    preselected_track = request.args.get('track', 'junior')
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        track = request.form.get('track', 'junior')
        
        if not fullname or not email or not password:
            flash("All fields are required!", "error")
            return render_template('signup.html', selected_track=track)
            
        user_id, error = database.create_user(fullname, email, password, role='student', track=track)
        if error:
            flash(error, "error")
            return render_template('signup.html', selected_track=track)
            
        session['user_id'] = user_id
        session['user_role'] = 'student'
        session['user_track'] = track
        
        try:
            device = get_client_device()
            database.record_analytics_event('signup', '/signup', device, '')
        except Exception:
            pass

        cohort_name = "Adult Career Track" if track == 'adult' else "Junior & Teen Adventure"
        flash(f"Welcome to LIM Innovations {cohort_name}, {fullname}! 🚀", "success")
        return redirect(url_for('dashboard'))
        
    return render_template('signup.html', selected_track=preselected_track)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user = database.authenticate_user(email, password)
        if not user:
            flash("Invalid email or password. Please try again.", "error")
            return render_template('login.html')
            
        session['user_id'] = user['id']
        session['user_role'] = user['role']
        
        try:
            device = get_client_device()
            database.record_analytics_event('login', '/login', device, '')
        except Exception:
            pass

        flash(f"Welcome back, {user['fullname']}! 🌟", "success")
        
        if user['role'] == 'teacher':
            return redirect(url_for('admin_panel'))
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have logged out. Keep up the great coding! 👋", "info")
    return redirect(url_for('welcome'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        # If not logged in as teacher, prompt for teacher credentials
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            user = database.authenticate_user(email, password)
            if user and user['role'] == 'teacher':
                session['user_id'] = user['id']
                session['user_role'] = 'teacher'
                return redirect(url_for('admin_panel'))
            else:
                flash("Unauthorized. Teacher credentials required.", "error")
        return render_template('admin_login.html')
        
    students = database.get_all_students()
    reservations = database.get_all_reservations()
    analytics = database.get_analytics_summary()
    reviews = database.get_all_reviews()
    config = get_teacher_config()
    return render_template('admin.html', students=students, reservations=reservations, analytics=analytics, reviews=reviews, config=config, lessons=LESSONS, challenges=CHALLENGES)

@app.route('/api/reviews', methods=['GET'])
def api_get_reviews():
    revs = database.get_approved_reviews()
    res = jsonify({"success": True, "reviews": revs})
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@app.route('/api/submit-review', methods=['POST', 'OPTIONS'])
def api_submit_review():
    if request.method == 'OPTIONS':
        res = make_response()
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Headers"] = "*"
        res.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return res
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    name = (data.get('name') or '').strip()
    role = (data.get('role') or 'Student / Parent').strip()
    rating = int(data.get('rating') or 5)
    comment = (data.get('comment') or '').strip()
    if not name or not comment:
        res = jsonify({"success": False, "error": "Name and review comment are required."})
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res, 400
    database.create_review(name, role, rating, comment)
    res = jsonify({"success": True, "message": "Thank you! Your review has been submitted for instructor verification."})
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@app.route('/admin/approve-review/<int:review_id>', methods=['POST'])
def admin_approve_review(review_id):
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    database.approve_review(review_id)
    flash("Review approved and published live!", "success")
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete-review/<int:review_id>', methods=['POST'])
def admin_delete_review(review_id):
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    database.delete_review(review_id)
    flash("Review deleted.", "info")
    return redirect(url_for('admin_panel'))

@app.route('/api/theme', methods=['GET', 'OPTIONS'])
def api_theme():
    if request.method == 'OPTIONS':
        res = make_response()
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Headers"] = "*"
        res.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        return res
    theme = database.get_site_theme()
    res = jsonify({"success": True, "theme": theme})
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@app.route('/admin/update-theme', methods=['POST'])
def admin_update_theme():
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('admin_login'))
    
    primary_color = request.form.get('primary_color', '').strip()
    primary_dark = request.form.get('primary_dark', '').strip()
    secondary_color = request.form.get('secondary_color', '').strip()
    accent_gold = request.form.get('accent_gold', '').strip()
    bg_main = request.form.get('bg_main', '').strip()
    text_primary = request.form.get('text_primary', '').strip()
    
    theme_data = {
        'primary_color': primary_color,
        'primary_dark': primary_dark,
        'secondary_color': secondary_color,
        'accent_gold': accent_gold,
        'bg_main': bg_main,
        'text_primary': text_primary
    }
    database.update_site_theme(theme_data)
    flash("🎨 Brand colors updated successfully across the entire platform!", "success")
    return redirect(url_for('admin_panel'))

@app.route('/admin/reset-theme', methods=['POST'])
def admin_reset_theme():
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('admin_login'))
    database.reset_site_theme()
    flash("Brand colors reset to official LIM Innovations Emerald & Gold!", "info")
    return redirect(url_for('admin_panel'))

@app.route('/api/track', methods=['POST', 'OPTIONS'])
def api_track():
    if request.method == 'OPTIONS':
        res = make_response()
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Headers"] = "*"
        res.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return res
        
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    event_type = data.get('event_type') or 'pageview'
    page = data.get('page') or 'index.html'
    client_device = data.get('device') or ''
    device = get_client_device(client_device)
    referrer = data.get('referrer') or ''
    database.record_analytics_event(event_type, page, device, referrer)
    res = jsonify({"success": True})
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@app.route('/flyer')
def flyer_designer():
    return render_template('flyer_designer.html')

@app.route('/admin/add-lead', methods=['POST'])
def admin_add_lead():
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    fullname = request.form.get('fullname', '').strip()
    track = request.form.get('track', 'Teens (9-17)').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    experience = request.form.get('experience', '').strip()
    if not fullname or not phone:
        flash("Name and phone number are required.", "error")
        return redirect(url_for('admin_panel'))
    database.create_reservation(fullname, track, phone, email, experience)
    flash(f"Lead for {fullname} successfully added!", "success")
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete-lead/<int:lead_id>', methods=['POST'])
def admin_delete_lead(lead_id):
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    database.delete_reservation(lead_id)
    flash("Lead removed successfully.", "info")
    return redirect(url_for('admin_panel'))


@app.route('/api/admissions', methods=['POST', 'OPTIONS'])
def api_admissions():
    if request.method == 'OPTIONS':
        res = make_response()
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Headers"] = "*"
        res.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return res
        
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    fullname = data.get('fullname') or data.get('name') or ''
    track = data.get('track') or ''
    phone = data.get('phone') or ''
    email = data.get('email') or ''
    experience = data.get('experience') or ''
    
    if not fullname or not phone:
        res = jsonify({"success": False, "error": "Name and phone number are required"})
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res, 400
        
    success, error = database.create_reservation(fullname, track, phone, email, experience)
    if not success:
        res = jsonify({"success": False, "error": error})
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res, 500
        
    res = jsonify({
        "success": True, 
        "message": f"Reservation successfully saved for {fullname} ({track})! Admissions team will message on WhatsApp."
    })
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@app.route('/flyer')
def flyer():
    return render_template('flyer_designer.html')

@app.route('/admin/update-locks', methods=['POST'])
def admin_update_locks():
    if 'user_id' not in session or session.get('user_role') != 'teacher':
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.get_json() or {}
    unlocked_lessons = data.get('unlocked_lessons', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    unlocked_challenges = data.get('unlocked_challenges', [1, 2, 3])
    
    config_path = os.path.join(app.root_path, 'teacher_config.json')
    new_config = {
        "unlocked_lessons": unlocked_lessons,
        "unlocked_challenges": unlocked_challenges
    }
    with open(config_path, 'w') as f:
        json.dump(new_config, f, indent=4)
        
    return jsonify({"success": True, "config": new_config})

@app.route('/api/user-state', methods=['GET'])
def get_user_state():
    if 'user_id' in session:
        user = database.get_user_by_id(session['user_id'])
        if user:
            return jsonify({
                "logged_in": True,
                "fullname": user['fullname'],
                "email": user['email'],
                "role": user['role'],
                "stars": user['stars'],
                "badges": json.loads(user['badges']) if user['badges'] else [],
                "completedLessons": json.loads(user['completed_lessons']) if user['completed_lessons'] else [],
                "completedChallenges": json.loads(user['completed_challenges']) if user['completed_challenges'] else [],
                "savedCodes": json.loads(user['saved_codes']) if user['saved_codes'] else {}
            })
    return jsonify({"logged_in": False})

@app.route('/api/save-progress', methods=['POST'])
def save_user_progress():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Guest mode - saved to localStorage only"}), 200
        
    data = request.get_json() or {}
    stars = data.get('stars')
    badges = data.get('badges')
    completed_lessons = data.get('completedLessons')
    completed_challenges = data.get('completedChallenges')
    saved_codes = data.get('savedCodes')
    
    database.update_user_progress(
        session['user_id'],
        stars=stars,
        badges=badges,
        completed_lessons=completed_lessons,
        completed_challenges=completed_challenges,
        saved_codes=saved_codes
    )
    return jsonify({"success": True})

@app.route('/mini-dashboard')
def mini_dashboard():
    student_data = None
    if 'user_id' in session:
        student_data = database.get_user_by_id(session['user_id'])
        if student_data:
            student_data['badges'] = json.loads(student_data['badges']) if student_data['badges'] else []
            student_data['completed_lessons'] = json.loads(student_data['completed_lessons']) if student_data['completed_lessons'] else []
            student_data['completed_challenges'] = json.loads(student_data['completed_challenges']) if student_data['completed_challenges'] else []
    return render_template('mini_dashboard.html', student=student_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
