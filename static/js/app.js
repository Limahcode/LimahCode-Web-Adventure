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
}

// Reset Game State
function resetGameState() {
    localStorage.setItem('html_css_adventure_state', JSON.stringify(DEFAULT_STATE));
    window.location.reload();
}

// Check if a lesson is unlocked
function isLessonUnlocked(lessonId, state) {
    // If teacher explicitly unlocked it in config, it is unlocked for all students!
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
        alert("Oops! Your code doesn't match the challenge requirements yet. Read the instructions and try again! Double check tags and matching braces.");
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
        alert("Not quite right yet! Ensure you have included all the required HTML tags and CSS properties listed in the instructions.");
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
    updateNavbarStats();
    
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
    
    // Check if on Dashboard page
    if (document.getElementById('dashboard-progress-fill')) {
        renderDashboard();
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
