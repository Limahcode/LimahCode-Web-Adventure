// HTML & CSS Adventure for Teenagers - Game Logic and State Management

// Initialize Game State
const DEFAULT_STATE = {
    completedLessons: [],    // IDs of completed lessons: [1, 2, ...]
    completedChallenges: [], // IDs of completed challenges: [1, 2, 3]
    stars: 0,
    badges: []               // Unlocked badge keys: ['html_explorer', 'website_builder', 'junior_web_designer']
};

function getGameState() {
    const stateStr = localStorage.getItem('html_css_adventure_state');
    if (!stateStr) {
        localStorage.setItem('html_css_adventure_state', JSON.stringify(DEFAULT_STATE));
        return DEFAULT_STATE;
    }
    try {
        return JSON.parse(stateStr);
    } catch (e) {
        return DEFAULT_STATE;
    }
}

function saveGameState(state) {
    localStorage.setItem('html_css_adventure_state', JSON.stringify(state));
    // Synchronize to server database if logged in
    syncProgressToServer(state);
}

// Synchronize state and code to the server backend
function syncProgressToServer(state) {
    const editor = document.getElementById('code-editor');
    let savedCodes = {};
    try {
        const storedCodes = localStorage.getItem('adventure_all_saved_codes');
        if (storedCodes) savedCodes = JSON.parse(storedCodes);
    } catch(e) {}
    
    if (editor) {
        savedCodes[window.location.pathname] = editor.value;
        localStorage.setItem('adventure_all_saved_codes', JSON.stringify(savedCodes));
    }

    fetch('/api/save-progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            stars: state.stars,
            badges: state.badges,
            completedLessons: state.completedLessons,
            completedChallenges: state.completedChallenges,
            savedCodes: savedCodes
        })
    }).catch(err => console.log("Offline or guest mode"));
}

// Generate smart, actionable hints based on student code
function generateSmartHints(code, ruleStr) {
    const hints = [];
    const lower = code.toLowerCase();

    if (ruleStr.includes('doctype') && !lower.includes('<!doctype html>')) {
        hints.push("Missing <code>&lt;!DOCTYPE html&gt;</code> at the top of your code.");
    }
    if (ruleStr.includes('<html>') && (!code.includes('<html>') || !code.includes('</html>'))) {
        hints.push("Make sure you wrap your webpage inside <code>&lt;html&gt;</code> and <code>&lt;/html&gt;</code> tags.");
    }
    if (ruleStr.includes('<body>') && (!code.includes('<body>') || !code.includes('</body>'))) {
        hints.push("Make sure your visible page elements are inside <code>&lt;body&gt;</code> and <code>&lt;/body&gt;</code>.");
    }
    if (ruleStr.includes('<h1>') && (!code.includes('<h1>') || !code.includes('</h1>'))) {
        hints.push("You need an <code>&lt;h1&gt;</code> main heading tag.");
    }
    if (ruleStr.includes('<br>') && !code.includes('<br>')) {
        hints.push("Add a <code>&lt;br&gt;</code> line break inside your paragraph.");
    }
    if (ruleStr.includes('<ol>') && (!code.includes('<ol>') || !code.includes('</ol>'))) {
        hints.push("You need an ordered list <code>&lt;ol&gt;...&lt;/ol&gt;</code> for numbered items.");
    }
    if (ruleStr.includes('<span>') && (!code.includes('<span>') || !code.includes('</span>'))) {
        hints.push("Wrap at least one word inside an inline <code>&lt;span&gt;...&lt;/span&gt;</code> tag.");
    }
    if (ruleStr.includes('href') && !code.includes('href=')) {
        hints.push("Links need an <code>href=\"...\"</code> attribute to tell the browser where to go (e.g. <code>&lt;a href=\"https://google.com\"&gt;</code>).");
    }
    if (ruleStr.includes('<img') && !code.includes('<img')) {
        hints.push("Add an image tag <code>&lt;img src=\"...\"&gt;</code>.");
    }
    if (ruleStr.includes('<form>') && (!code.includes('<form>') || !code.includes('</form>'))) {
        hints.push("Build a form container with <code>&lt;form&gt;...&lt;/form&gt;</code>.");
    }
    if (ruleStr.includes('<input') && !code.includes('<input')) {
        hints.push("Add at least one input box with <code>&lt;input type=\"text\"&gt;</code> inside your form.");
    }
    if (ruleStr.includes('<table>') && (!code.includes('<table>') || !code.includes('</table>'))) {
        hints.push("You need a table container: <code>&lt;table&gt;...&lt;/table&gt;</code>.");
    }
    if (ruleStr.includes('<th>') && (code.match(/<th>/g) || []).length < 2) {
        hints.push("Add at least 2 column headers with <code>&lt;th&gt;...&lt;/th&gt;</code> inside your table.");
    }
    if (ruleStr.includes('border-radius') && !code.includes('border-radius')) {
        hints.push("Use the CSS property <code>border-radius: ...;</code> to give your boxes smooth rounded corners.");
    }
    if (ruleStr.includes('class="card"') && !code.includes('class="card"')) {
        hints.push("Give your container the class name <code>class=\"card\"</code>.");
    }

    if (hints.length === 0) {
        hints.push("Check that all your open HTML tags have matching closing tags (e.g. <code>&lt;/p&gt;</code>, <code>&lt;/div&gt;</code>).");
    }
    return hints;
}

// Display smart hints in the UI
function showSmartHint(hints) {
    const box = document.getElementById('smart-hint-box');
    const content = document.getElementById('smart-hint-content');
    if (!box || !content) return;

    let html = `
        <div style="display: flex; align-items: center; gap: 8px; color: #f59e0b; font-weight: 700; margin-bottom: 6px;">
            <span>💡 Smart Mentor Hint:</span>
        </div>
        <ul style="margin: 0; padding-left: 20px; color: #cbd5e1; line-height: 1.6;">
    `;
    hints.forEach(h => {
        html += `<li>${h}</li>`;
    });
    html += `</ul>`;

    content.innerHTML = html;
    box.style.display = 'block';
}

function hideSmartHint() {
    const box = document.getElementById('smart-hint-box');
    if (box) box.style.display = 'none';
}

// Reset Game State
function resetGameState() {
    if (confirm("Are you sure you want to reset your progress back to zero?")) {
        localStorage.setItem('html_css_adventure_state', JSON.stringify(DEFAULT_STATE));
        localStorage.removeItem('adventure_all_saved_codes');
        
        // Also sync empty progress to server if logged in
        fetch('/api/save-progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                stars: 0,
                badges: [],
                completedLessons: [],
                completedChallenges: [],
                savedCodes: {}
            })
        }).finally(() => {
            window.location.reload();
        });
    }
}

// Check if a lesson is unlocked
function isLessonUnlocked(lessonId, state) {
    if (window.TEACHER_UNLOCKED_LESSONS) {
        return window.TEACHER_UNLOCKED_LESSONS.includes(lessonId);
    }
    
    // Fallback: Lesson 1 is always unlocked
    if (lessonId === 1) return true;
    
    // Other lessons require the previous lesson
    return state.completedLessons.includes(lessonId - 1);
}

// Check if a challenge is unlocked
function isChallengeUnlocked(challengeId, state) {
    if (window.TEACHER_UNLOCKED_CHALLENGES) {
        return window.TEACHER_UNLOCKED_CHALLENGES.includes(challengeId);
    }
    return false;
}

// Update Top Navigation Bar Stats
function updateNavbarStats() {
    const state = getGameState();
    const starElement = document.getElementById('navbar-stars');
    const badgeElement = document.getElementById('navbar-badges');
    
    if (starElement) starElement.textContent = state.stars;
    if (badgeElement) badgeElement.textContent = state.badges.length;
}

// Run the current user code in the preview iframe
function runCodePreview() {
    const editor = document.getElementById('code-editor');
    const previewFrame = document.getElementById('preview-frame');
    if (!editor || !previewFrame) return;
    
    const code = editor.value;
    const previewDocument = previewFrame.contentDocument || previewFrame.contentWindow.document;
    
    previewDocument.open();
    // Inject standard CSS or resetting so it looks clean inside the preview box
    let template = code;
    if (!code.includes('<style>') && !code.includes('<body>')) {
        // If they just typed HTML snippets, wrap it nicely
        template = `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: sans-serif; padding: 15px; margin: 0; color: #1e293b; }
                    table { border-collapse: collapse; width: 100%; margin: 10px 0; }
                    th, td { border: 2px solid #cbd5e1; padding: 8px; text-align: left; }
                    th { background-color: #f1f5f9; }
                </style>
            </head>
            <body>
                ${code}
            </body>
            </html>
        `;
    }
    previewDocument.write(template);
    previewDocument.close();
}

// Reset code editor to initial starter template
function resetEditorCode(defaultTemplate) {
    if (confirm("Do you want to reset your code to the starting template?")) {
        const editor = document.getElementById('code-editor');
        if (editor) {
            editor.value = defaultTemplate || '';
            const storageKey = 'adventure_saved_code_' + window.location.pathname;
            localStorage.removeItem(storageKey);
            hideSmartHint();
            runCodePreview();
        }
    }
}

// Check the solution of a lesson
function verifyLesson(lessonId) {
    const editor = document.getElementById('code-editor');
    const checkBtn = document.getElementById('check-answer-btn');
    if (!editor || !checkBtn) return;
    
    const code = editor.value;
    const solutionRule = checkBtn.dataset.solutionCheck;
    
    // Evaluate rule safely in context of code
    let passed = false;
    try {
        // Simple evaluator using the rule string stored in app.py
        const checkFn = new Function('code', `return (${solutionRule});`);
        passed = checkFn(code);
    } catch (e) {
        console.error("Validation error:", e);
    }
    
    if (passed) {
        hideSmartHint();
        const state = getGameState();
        
        // Check if already completed to avoid duplicate stars
        const isNew = !state.completedLessons.includes(lessonId);
        if (isNew) {
            state.completedLessons.push(lessonId);
            state.stars += 10; // Earn 10 stars per lesson
            saveGameState(state);
            updateNavbarStats();
        }
        
        // Trigger Congratulation Popup
        showCelebrationPopup(
            "⭐ Lesson Completed! ⭐",
            `Awesome work! You mastered this lesson and earned 10 Stars. You have ${state.stars} stars now!`,
            false
        );
        
        // Play success audio if supported or just trigger effects
        triggerConfettiShower();
    } else {
        const hints = generateSmartHints(code, solutionRule);
        showSmartHint(hints);
    }
}

// Check the solution of a weekly challenge
function verifyChallenge(challengeId) {
    const editor = document.getElementById('code-editor');
    const checkBtn = document.getElementById('check-challenge-btn');
    if (!editor || !checkBtn) return;
    
    const code = editor.value;
    const solutionRule = checkBtn.dataset.solutionCheck;
    const badgeKey = checkBtn.dataset.badge;
    const badgeName = checkBtn.dataset.badgeName;
    
    let passed = false;
    try {
        const checkFn = new Function('code', `return (${solutionRule});`);
        passed = checkFn(code);
    } catch (e) {
        console.error("Challenge validation error:", e);
    }
    
    if (passed) {
        hideSmartHint();
        const state = getGameState();
        
        const isNew = !state.completedChallenges.includes(challengeId);
        if (isNew) {
            state.completedChallenges.push(challengeId);
            state.stars += 25; // Challenges earn 25 stars!
            if (!state.badges.includes(badgeKey)) {
                state.badges.push(badgeKey);
            }
            saveGameState(state);
            updateNavbarStats();
        }
        
        // Popup badge display
        showCelebrationPopup(
            "🏅 Challenge Conquered! 🏅",
            `Spectacular! You have completed the challenge, earned 25 Stars, and unlocked the official **${badgeName}**!`,
            badgeKey
        );
        
        triggerConfettiShower();
    } else {
        const hints = generateSmartHints(code, solutionRule);
        showSmartHint(hints);
    }
}

// Celebration Confetti effect using raw CSS and elements
function triggerConfettiShower() {
    const container = document.body;
    const colors = ['#6366f1', '#22c55e', '#eab308', '#ef4444', '#a855f7', '#f97316'];
    
    for (let i = 0; i < 60; i++) {
        const confetti = document.createElement('div');
        confetti.classList.add('confetti');
        
        // Random positions and animations
        const left = Math.random() * window.innerWidth;
        const size = Math.random() * 8 + 6;
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        confetti.style.left = left + 'px';
        // Start from random height near top
        confetti.style.top = (window.scrollY - 10) + 'px';
        confetti.style.width = size + 'px';
        confetti.style.height = size + 'px';
        confetti.style.backgroundColor = color;
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0%';
        
        container.appendChild(confetti);
        
        // Animate falling down
        const duration = Math.random() * 2 + 1.5;
        const drift = Math.random() * 150 - 75;
        
        confetti.animate([
            { transform: 'translate3d(0, 0, 0) rotate(0deg)', opacity: 1 },
            { transform: `translate3d(${drift}px, ${window.innerHeight + 100}px, 0) rotate(${Math.random() * 360}deg)`, opacity: 0 }
        ], {
            duration: duration * 1000,
            easing: 'cubic-bezier(0.1, 0.8, 0.3, 1)',
            fill: 'forwards'
        });
        
        // Remove element after animation
        setTimeout(() => {
            confetti.remove();
        }, duration * 1000);
    }
}

// Show the celebration popup modal
function showCelebrationPopup(title, text, badgeKey) {
    const overlay = document.getElementById('celebration-overlay');
    const popupTitle = document.getElementById('popup-title');
    const popupText = document.getElementById('popup-text');
    const popupBadgeImg = document.getElementById('popup-badge-img');
    const popupActionBtn = document.getElementById('popup-action-btn');
    
    if (!overlay) return;
    
    popupTitle.textContent = title;
    popupText.textContent = text;
    
    if (badgeKey) {
        popupBadgeImg.src = `/static/images/badges/${badgeKey}_badge.png`;
        popupBadgeImg.style.display = 'inline-block';
    } else {
        popupBadgeImg.style.display = 'none';
    }
    
    overlay.classList.add('show');
}

function closeCelebrationPopup() {
    const overlay = document.getElementById('celebration-overlay');
    if (overlay) {
        overlay.classList.remove('show');
    }
}

// Render Dashboard status (locks, maps, badges)
function renderDashboard() {
    const state = getGameState();
    
    // 1. Update Progress Bar
    // Calculate based on the student's actual completed lessons and challenges
    const completedCount = state.completedLessons.length + state.completedChallenges.length;
    const progressPercent = Math.min((completedCount / 13) * 100, 100);
    
    const fillEl = document.getElementById('dashboard-progress-fill');
    const textEl = document.getElementById('dashboard-progress-text');
    if (fillEl) fillEl.style.width = `${progressPercent}%`;
    if (textEl) textEl.textContent = `${Math.round(progressPercent)}% Done!`;
    
    // 2. Render Winding Journey Map nodes
    const mapNodes = document.querySelectorAll('.map-node');
    mapNodes.forEach(node => {
        const type = node.dataset.type; // "lesson" or "challenge"
        const id = parseInt(node.dataset.id);
        const nodeBtn = node.querySelector('.node-btn');
        const nodeIcon = node.querySelector('.node-icon');
        
        if (type === 'lesson') {
            const completed = state.completedLessons.includes(id);
            const unlocked = isLessonUnlocked(id, state);
            
            if (completed) {
                nodeBtn.className = 'node-btn completed';
                if (nodeIcon) nodeIcon.innerHTML = '⭐';
                nodeBtn.style.pointerEvents = 'auto';
            } else if (unlocked) {
                nodeBtn.className = 'node-btn active';
                if (nodeIcon) nodeIcon.innerHTML = '⚡';
                nodeBtn.style.pointerEvents = 'auto';
            } else {
                nodeBtn.className = 'node-btn locked';
                if (nodeIcon) nodeIcon.innerHTML = '🔒';
                nodeBtn.style.pointerEvents = 'none';
            }
        } else if (type === 'challenge') {
            const completed = state.completedChallenges.includes(id);
            const unlocked = isChallengeUnlocked(id, state);
            
            if (completed) {
                nodeBtn.className = 'node-btn completed';
                if (nodeIcon) nodeIcon.innerHTML = '🏆';
                nodeBtn.style.pointerEvents = 'auto';
            } else if (unlocked) {
                nodeBtn.className = 'node-btn active';
                if (nodeIcon) nodeIcon.innerHTML = '🔥';
                nodeBtn.style.pointerEvents = 'auto';
            } else {
                nodeBtn.className = 'node-btn locked';
                if (nodeIcon) nodeIcon.innerHTML = '🔒';
                nodeBtn.style.pointerEvents = 'none';
            }
        }
    });
    
    // 3. Render Lesson & Challenge Cards in the Timetable
    const cards = document.querySelectorAll('.timetable-card');
    cards.forEach(card => {
        const type = card.dataset.type || 'lesson';
        const id = parseInt(card.dataset.id);
        
        let completed = false;
        let unlocked = false;
        
        if (type === 'lesson') {
            completed = state.completedLessons.includes(id);
            unlocked = isLessonUnlocked(id, state);
        } else if (type === 'challenge') {
            completed = state.completedChallenges.includes(id);
            unlocked = isChallengeUnlocked(id, state);
        }
        
        // Ensure pointerEvents is reset back to auto when unlocked/completed
        card.style.pointerEvents = 'auto';
        
        if (completed) {
            card.classList.remove('locked');
            const statusLabel = card.querySelector('.status-label');
            if (statusLabel) {
                if (type === 'lesson') {
                    statusLabel.innerHTML = '<span style="color: var(--color-success)">⭐ Completed!</span>';
                } else {
                    statusLabel.innerHTML = '<span style="color: var(--color-success)">🏆 Conquered!</span>';
                }
            }
        } else if (unlocked) {
            card.classList.remove('locked');
            const statusLabel = card.querySelector('.status-label');
            if (statusLabel) {
                if (type === 'lesson') {
                    statusLabel.innerHTML = '<span style="color: var(--color-warning)">⚡ Start Lesson</span>';
                } else {
                    statusLabel.innerHTML = '<span style="color: var(--color-warning)">⚡ Start Challenge</span>';
                }
            }
        } else {
            card.classList.add('locked');
            const statusLabel = card.querySelector('.status-label');
            if (statusLabel) {
                statusLabel.innerHTML = '<span style="color: var(--text-secondary)">🔒 Locked</span>';
            }
            // Disable click
            card.style.pointerEvents = 'none';
        }
    });
    
    // 4. Render Badges list
    const badgeItems = document.querySelectorAll('.badge-item');
    badgeItems.forEach(badge => {
        const key = badge.dataset.badge;
        const unlocked = state.badges.includes(key);
        if (unlocked) {
            badge.classList.remove('locked');
            const badgeStatus = badge.querySelector('.badge-status');
            if (badgeStatus) badgeStatus.innerHTML = '<span style="color: var(--color-success)">Collected!</span>';
        } else {
            badge.classList.add('locked');
            const badgeStatus = badge.querySelector('.badge-status');
            if (badgeStatus) badgeStatus.innerHTML = '<span style="color: var(--text-secondary)">Locked</span>';
        }
    });

    // 5. Check if certificate is unlocked
    const certBtn = document.getElementById('claim-certificate-btn');
    if (certBtn) {
        // Unlocked when challenges are completed OR when teacher unlocks week 3 (challenge 3)
        const teacherHasUnlockedFinal = (window.TEACHER_UNLOCKED_CHALLENGES && window.TEACHER_UNLOCKED_CHALLENGES.includes(3)) || (state.completedChallenges && state.completedChallenges.length >= 2);
        const unlocked = state.completedChallenges.length >= 3 || teacherHasUnlockedFinal;
        if (unlocked) {
            certBtn.classList.remove('btn-locked');
            certBtn.removeAttribute('disabled');
            certBtn.style.opacity = '1';
            certBtn.style.cursor = 'pointer';
        } else {
            certBtn.style.opacity = '0.7';
            certBtn.style.cursor = 'pointer';
            certBtn.removeAttribute('disabled');
        }
    }
}

// Redirect checking when loading lesson or challenge pages directly
function checkPageAccess(type, id) {
    const state = getGameState();
    if (type === 'lesson') {
        if (!isLessonUnlocked(id, state)) {
            alert("This lesson is locked! Complete the previous topics first.");
            window.location.href = '/dashboard';
        }
    } else if (type === 'challenge') {
        if (!isChallengeUnlocked(id, state)) {
            alert("This weekly challenge is locked! Complete all lessons in the week first.");
            window.location.href = '/dashboard';
        }
    }
}

// Handle layout adjustments and code sync in real-time
document.addEventListener('DOMContentLoaded', () => {
    // Attempt to hydrate state from server if logged in
    fetch('/api/user-state')
        .then(r => r.json())
        .then(data => {
            if (data.logged_in) {
                const state = getGameState();
                // Merge server state with local state
                state.stars = Math.max(state.stars, data.stars || 0);
                if (data.badges && data.badges.length) {
                    data.badges.forEach(b => { if (!state.badges.includes(b)) state.badges.push(b); });
                }
                if (data.completedLessons && data.completedLessons.length) {
                    data.completedLessons.forEach(l => { if (!state.completedLessons.includes(l)) state.completedLessons.push(l); });
                }
                if (data.completedChallenges && data.completedChallenges.length) {
                    data.completedChallenges.forEach(c => { if (!state.completedChallenges.includes(c)) state.completedChallenges.push(c); });
                }
                localStorage.setItem('html_css_adventure_state', JSON.stringify(state));
                
                // If student has saved code for this route in DB
                const editor = document.getElementById('code-editor');
                if (editor && data.savedCodes && data.savedCodes[window.location.pathname]) {
                    const storageKey = 'adventure_saved_code_' + window.location.pathname;
                    if (!localStorage.getItem(storageKey)) {
                        editor.value = data.savedCodes[window.location.pathname];
                        localStorage.setItem(storageKey, editor.value);
                        runCodePreview();
                    }
                }
            }
            updateNavbarStats();
            if (document.getElementById('dashboard-progress-fill')) {
                renderDashboard();
            }
        })
        .catch(() => {
            updateNavbarStats();
            if (document.getElementById('dashboard-progress-fill')) {
                renderDashboard();
            }
        });
    
    // Automatic route access check based on path
    const path = window.location.pathname;
    const lessonMatch = path.match(/\/lesson\/(\d+)/);
    if (lessonMatch) {
        checkPageAccess('lesson', parseInt(lessonMatch[1]));
    }
    const challengeMatch = path.match(/\/challenge\/(\d+)/);
    if (challengeMatch) {
        checkPageAccess('challenge', parseInt(challengeMatch[1]));
    }
    
    // Check if on Lesson or Challenge page
    const editor = document.getElementById('code-editor');
    if (editor) {
        // Auto-restore saved code if available for this specific lesson/challenge
        const currentPath = window.location.pathname; // e.g. /lesson/6 or /challenge/2
        const storageKey = 'adventure_saved_code_' + currentPath;
        const savedCode = localStorage.getItem(storageKey);
        
        if (savedCode !== null && savedCode.trim() !== '') {
            editor.value = savedCode;
        }
        
        // Run initial preview
        runCodePreview();
        
        // Listen to code changes: update preview and auto-save
        editor.addEventListener('input', () => {
            runCodePreview();
            localStorage.setItem(storageKey, editor.value);
        });
    }
});
