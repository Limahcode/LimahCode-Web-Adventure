import json
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

def get_teacher_config():
    config_path = os.path.join(app.root_path, 'teacher_config.json')
    if not os.path.exists(config_path):
        default_config = {"unlocked_lessons": [1], "unlocked_challenges": []}
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {"unlocked_lessons": [1], "unlocked_challenges": []}

@app.context_processor
def inject_teacher_config():
    config = get_teacher_config()
    return {
        "teacher_unlocked_lessons": config.get("unlocked_lessons", [1]),
        "teacher_unlocked_challenges": config.get("unlocked_challenges", [])
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
        "week_title": "Making Websites Beautiful with CSS",
        "title": "Master Review & Final Project Briefing (Lessons 1-8)",
        "day": "Wednesday",
        "description": "Full summary of everything learned from HTML structure to CSS styling, plus full instructions for your 3-page Final Portfolio Project!",
        "points": 25,
        "concept": "You have mastered HTML structure (headings, text, images, links, lists, tables, forms, layout divs) and CSS styling (colors, background-images, fonts, borders, padding, margins)! Now let's connect all 3 pages together: Sign-Up, Login, and Dashboard.",
        "steps": [
            {
                "title": "1. The Complete Master Review (Lessons 1 to 8)",
                "text": "Here is your cheat sheet of superpowers:\n• **HTML Structure**: `<!DOCTYPE html>`, `<html>`, `<head>` (brain/styles), `<body>` (visible content)\n• **Headings & Paragraphs**: `<h1>` to `<h6>`, `<p>`\n• **Visuals & Links**: `<img src=\"...\" alt=\"...\">`, `<a href=\"...\">`\n• **Lists**: `<ul>` & `<li>` (bullet points), `<ol>` & `<li>` (numbered)\n• **Tables**: `<table>`, `<tr>` (row), `<th>` (header), `<td>` (data cell)\n• **Forms & Input**: `<form action=\"page.html\">`, `<label>`, `<input type=\"text|email|password\">`, `<button type=\"submit\">`\n• **CSS Basics**: `<style>` in `<head>`, selectors (`body`, `h1`, `.card`), colors (`color`, `background-color`, `background-image: url(...)`)\n• **Box Model**: `border: 3px solid black;`, `border-radius: 12px;`, `padding: 15px;`, `margin: 10px;`, `font-family: Arial, sans-serif;`"
            },
            {
                "title": "2. 🚀 Your Final Portfolio Project Requirements",
                "text": "Every student will build a **3-Page Linked Website**:\n1. **`signup.html`**: Registration form (Full Name, Email, Password, Favorite Hobby) that submits to `login.html` via `<form action=\"login.html\">`.\n2. **`login.html`**: Login form (Email, Password) with a button that submits to `dashboard.html` via `<form action=\"dashboard.html\">`.\n3. **`dashboard.html`**: Your personal command center! Features your Welcome Banner (`<header>`), About Me (`<p>`), My Hobbies Table (`<table>`), and Favorite Links (`<a>`).\n• **Styling**: Give all 3 pages beautiful CSS backgrounds, rounded borders, padding, and custom fonts!"
            },
            {
                "title": "3. 📅 Important Timeline & Deadlines",
                "text": "• **Wednesday**: Master Review & start coding your 3 pages.\n• **Friday**: Final Project Submission deadline (Submit your project folder or live link in the WhatsApp group).\n• **Saturday**: Live Class Presentation & Project Defense! Each student will present their project in class and explain how they built it!"
            }
        ],
        "example": "<!-- Complete 3-Page Website Structure Example -->\n<!-- 1. SIGNUP PAGE (signup.html) -->\n<style>\n  body { background-color: lightyellow; font-family: Arial, sans-serif; padding: 20px; }\n  .card { border: 3px solid black; border-radius: 12px; padding: 20px; max-width: 400px; margin: 0 auto; background: white; }\n  input { width: 90%; padding: 8px; margin-bottom: 10px; border-radius: 6px; border: 2px solid black; }\n  button { background-color: coral; color: white; border: 2px solid black; border-radius: 8px; padding: 10px 16px; font-weight: bold; cursor: pointer; }\n</style>\n\n<div class=\"card\">\n  <h2>🚀 Create Your Account</h2>\n  <form action=\"login.html\">\n    <label>Full Name:</label><br>\n    <input type=\"text\" placeholder=\"Enter your name\" required><br>\n    <label>Email Address:</label><br>\n    <input type=\"email\" placeholder=\"name@example.com\" required><br>\n    <button type=\"submit\">Register & Go to Login ➡️</button>\n  </form>\n</div>",
        "editor_template": "<!-- 🎯 Lesson 9 Task: Build your SignUp Card that links to login.html! -->\n<!-- 1. In the <style> block, style body with a background color and .card with a border, border-radius, and padding -->\n<!-- 2. Inside the card, create a <form action=\"login.html\"> with an <input> and <button type=\"submit\"> -->\n<style>\n  body {\n    background-color: lightyellow;\n    font-family: Arial, sans-serif;\n  }\n  .card {\n    border: 3px solid black;\n    border-radius: 12px;\n    padding: 20px;\n    background-color: white;\n  }\n</style>\n\n<div class=\"card\">\n  <h2>Sign Up</h2>\n  <form action=\"login.html\">\n    <input type=\"text\" placeholder=\"Your name\">\n    <button type=\"submit\">Submit to Login</button>\n  </form>\n</div>",
        "solution_check": "code.includes('<form') && code.includes('login.html') && code.includes('border-radius') && code.includes('padding')"
    },
    
    10: {
        "id": 10,
        "week": 3,
        "week_title": "Making Websites Beautiful with CSS",
        "title": "Bonus Masterclass: Deploying to Netlify (Going Live!)",
        "day": "Bonus",
        "description": "Turn your 3-page project into a real, live website on the internet with a public link you can share worldwide!",
        "points": 25,
        "concept": "Deploying means hosting your files on a 24/7 web server. With Netlify Drop, you can publish your entire project folder in under 30 seconds for FREE without any command line tools.",
        "steps": [
            {
                "title": "Step 1: Organize Your Project Folder on Your Computer",
                "text": "Before uploading, make sure your folder is properly organized:\n• Folder name: e.g. `my-final-portfolio/`\n• Main entry file **MUST** be named exactly `index.html` (or `signup.html` / `dashboard.html`). If your homepage is `signup.html`, make a copy or rename it to `index.html` so Netlify knows which page to open first!\n• All image files should be inside the same folder or in an `images/` subfolder."
            },
            {
                "title": "Step 2: Open Netlify Drop",
                "text": "1. Open your browser and go to: **https://app.netlify.com/drop**\n2. (Optional & Recommended) Sign up for a free Netlify account so your live website links never expire!\n3. You will see a large box that says **'Drag and drop your site output folder here'**."
            },
            {
                "title": "Step 3: Drag & Drop Your Folder",
                "text": "1. Open your computer's File Explorer (Windows) or Finder (Mac).\n2. Drag your **ENTIRE project folder** and drop it directly onto the Netlify webpage.\n3. Wait 10 to 15 seconds while Netlify uploads and builds your site.\n4. Netlify will display: **'Production: Published'** with your live link (e.g. `https://super-coder-12345.netlify.app`)!"
            },
            {
                "title": "Step 4: Customize Your Link & Share",
                "text": "1. Click **Site configuration** > **Change site name** to make it personalized (e.g. `https://limahcode-alex.netlify.app`).\n2. Open the link on your mobile phone or send it to your parents and WhatsApp group!\n3. Paste your live URL below in the playground to complete the bonus masterclass!"
            }
        ],
        "example": "📁 YOUR PROJECT FOLDER STRUCTURE:\nmy-portfolio/\n├── index.html        (Your Homepage)\n├── login.html        (Your Login Page)\n├── dashboard.html    (Your Dashboard)\n└── images/\n    └── my-photo.jpg\n\n🎉 YOUR NETLIFY LIVE URL WILL LOOK LIKE:\nhttps://alex-webadventure.netlify.app",
        "editor_template": "<!-- 🎯 Lesson 10 Bonus Task: Deploy your website on Netlify! -->\n<!-- 1. Go to https://app.netlify.com/drop -->\n<!-- 2. Drag and drop your project folder -->\n<!-- 3. Copy your live link and paste it below: -->\n\n<!-- My Live Netlify Website: https://my-name.netlify.app -->\n<p>My website is live on the internet! 🚀</p>\n",
        "solution_check": "code.toLowerCase().includes('netlify.app') || code.toLowerCase().includes('vercel.app') || code.toLowerCase().includes('http') || code.toLowerCase().includes('https')"
    }
}

CHALLENGES = {
    1: {
        "id": 1,
        "week": 1,
        "title": "HTML Explorer Challenge",
        "badge": "html_explorer",
        "badge_name": "HTML Explorer Badge",
        "instructions": "Create your first personal webpage! Your page must contain:\n1. A big heading (<h1>)\n2. A paragraph about yourself (<p>)\n3. A bulleted list (<ul> and <li>) with at least two hobbies\n4. A link (<a>) to your favorite website",
        "editor_template": "<!-- Build your first personal webpage here! -->\n<h1>My Webpage</h1>\n",
        "solution_check": "code.includes('<h1>') && code.includes('</h1>') && code.includes('<p>') && code.includes('</p>') && code.includes('<ul>') && code.includes('</ul>') && (code.match(/<li>/g) || []).length >= 2 && code.includes('<a') && code.includes('href')"
    },
    2: {
        "id": 2,
        "week": 2,
        "title": "Website Builder Challenge",
        "badge": "website_builder",
        "badge_name": "Website Builder Badge",
        "instructions": "Build a Registration Page! Your webpage must contain:\n1. A form (<form>)\n2. A text input (<input type=\"text\">) inside the form\n3. A submit button (<button>)\n4. A table (<table>) listing 'Registrant Name' and 'Registration Date' as column headers (<th>)",
        "editor_template": "<!-- Build a simple registration page! -->\n",
        "solution_check": "code.includes('<form>') && code.includes('</form>') && code.includes('<input') && code.includes('<button') && code.includes('<table>') && code.includes('</table>') && (code.match(/<th>/g) || []).length >= 2"
    },
    3: {
        "id": 3,
        "week": 3,
        "title": "Final Portfolio Defense Project",
        "badge": "junior_web_designer",
        "badge_name": "Junior Web Designer Certificate",
        "instructions": "Build your 3-Page Linked Website for Friday Submission and Saturday Live Defense!\nRequirements:\n1. Sign Up Page (signup.html): Form submitting to login.html\n2. Login Page (login.html): Form submitting to dashboard.html\n3. Dashboard Page (dashboard.html): Header, styled cards (<div class=\"card\">), hobbies table (<table>), and custom CSS (background-color, borders, border-radius, padding, fonts)!\n4. Use the playground below to test and submit your combined dashboard prototype!",
        "editor_template": "<!-- 🏆 Final Portfolio Defense Project -->\n<!-- Style your complete Dashboard below with CSS and HTML! -->\n<style>\n  body {\n    background-color: lightyellow;\n    font-family: Arial, sans-serif;\n    padding: 20px;\n  }\n  .card {\n    border: 3px solid black;\n    border-radius: 14px;\n    padding: 20px;\n    margin: 15px 0;\n    background-color: white;\n  }\n  table {\n    border-collapse: collapse;\n    width: 100%;\n  }\n  th, td {\n    border: 2px solid black;\n    padding: 8px;\n  }\n</style>\n\n<header class=\"card\">\n  <h1>🚀 Welcome to My Portfolio Dashboard</h1>\n  <p>Built with HTML & CSS by a Junior Web Designer!</p>\n</header>\n\n<div class=\"card\">\n  <h2>🏆 My Favorite Skills & Hobbies</h2>\n  <table>\n    <tr><th>Skill / Hobby</th><th>Experience Level</th></tr>\n    <tr><td>HTML & CSS Coding</td><td>Master</td></tr>\n    <tr><td>Game Building</td><td>Intermediate</td></tr>\n  </table>\n</div>\n",
        "solution_check": "code.includes('<header') && code.includes('<h1>') && code.includes('class=\"card\"') && code.includes('<table>') && code.includes('border-radius') && code.includes('padding')"
    }
}

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', lessons=LESSONS, challenges=CHALLENGES)

@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
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
    if challenge_id not in CHALLENGES:
        return "Challenge not found!", 404
        
    challenge_data = CHALLENGES[challenge_id]
    return render_template('challenge.html', challenge=challenge_data, lessons=LESSONS)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/mini-dashboard')
def mini_dashboard():
    return render_template('mini_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
