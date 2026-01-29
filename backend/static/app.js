const API_URL = "http://localhost:8000";
let userId = localStorage.getItem("user_id");

if (!userId) {
    userId = "user_" + Math.floor(Math.random() * 10000);
    localStorage.setItem("user_id", userId);
}

document.getElementById("user-id-display").innerText = userId;

// --- API Functions ---

async function fetchContent() {
    try {
        const response = await fetch(`${API_URL}/content`);
        const data = await response.json();
        renderContent(data);
    } catch (error) {
        console.error("Error fetching content:", error);
    }
}

async function fetchRecommendations() {
    const list = document.getElementById("recommendations-list");
    // Visual feedback: Flash/Opactiy change
    list.style.opacity = "0.5";

    try {
        const response = await fetch(`${API_URL}/recommend/${userId}`);
        const data = await response.json();

        // Small artificial delay so the flash is visible (feels more 'computational')
        setTimeout(() => {
            renderRecommendations(data);
            list.style.opacity = "1";

            // Add a flash border effect
            const sidebar = document.querySelector('.sidebar');
            sidebar.style.borderColor = "#0aff00";
            setTimeout(() => sidebar.style.borderColor = "rgba(255, 255, 255, 0.1)", 300);
        }, 300);

        updateDebugProfile();
    } catch (error) {
        console.error("Error fetching recommendations:", error);
        list.style.opacity = "1";
    }
}

async function sendInteraction(contentId) {
    try {
        await fetch(`${API_URL}/interact`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                content_id: contentId,
                interaction_type: "like"
            })
        });

        // Instant feedback loop
        fetchRecommendations();

    } catch (error) {
        console.error("Error sending interaction:", error);
    }
}

async function updateDebugProfile() {
    try {
        const response = await fetch(`${API_URL}/profile/${userId}`);
        const data = await response.json();
        const container = document.getElementById("debug-profile");
        container.innerHTML = `
            <p>Interactions: ${data.interaction_count}</p>
            <p>Preferences: ${JSON.stringify(data.category_preference, null, 2)}</p>
         `;
    } catch (e) { }
}

// --- Render Functions ---

function renderContent(items) {
    const grid = document.getElementById("content-grid");
    grid.innerHTML = items.map(item => {
        let badge = '';
        let btnText = '<i class="far fa-compass"></i> Explore';
        let cardClass = '';

        if (item.content_type === 'video') {
            badge = '<div class="badge badge-video" style="background:#6a00ff; color:white;">VIDEO</div>';
            btnText = '<i class="fas fa-play"></i> Watch';
            cardClass = 'type-video';
        } else if (item.content_type === 'live') {
            badge = '<div class="badge badge-live">● LIVE</div>';
            btnText = '<i class="fas fa-play"></i> Watch';
            cardClass = 'type-live';
        } else if (item.content_type === 'ticket') {
            badge = '<div class="badge badge-ticket"><i class="fas fa-ticket-alt"></i> TICKET</div>';
            btnText = '<i class="fas fa-shopping-cart"></i> Buy';
            cardClass = 'type-ticket';
        } else if (item.content_type === 'merchandise') {
            badge = '<div class="badge badge-merch">SHOP</div>';
            btnText = '<i class="fas fa-shopping-bag"></i> Shop';
        } else if (item.content_type === 'article') {
            badge = '<div class="badge badge-article">READ</div>';
            btnText = '<i class="fas fa-book-open"></i> Read';
        }

        return `
        <div class="card ${cardClass}">
            ${badge}
            <!-- CLICKABLE IMAGE triggers the Action -->
            <img src="${item.image_url}" alt="${item.title}" class="card-img" 
                 onclick="handleAction('${item.content_type}', '${item.action_url}')" 
                 style="cursor: pointer;">
                 
            <div class="card-body">
                <span class="card-category">${item.category}</span>
                <h3 class="card-title">${item.title}</h3>
                <div class="card-tags">
                    ${item.tags.split(',').map(tag => `<span class="tag">#${tag.trim()}</span>`).join('')}
                </div>
                
                <div style="display:flex; gap:10px;">
                    <button class="action-btn" onclick="handleLike(this, ${item.id})" style="flex:1">
                        <i class="far fa-heart"></i>
                    </button>
                    <button class="action-btn" onclick="handleAction('${item.content_type}', '${item.action_url}')" style="flex:3; background:rgba(255,255,255,0.1); border-color:white;">
                        ${btnText}
                    </button>
                </div>
            </div>
        </div>
    `}).join('');
}

function handleAction(type, url) {
    if (!url || url === 'undefined' || url === 'null') {
        alert("This content is a demo placeholder (No URL).");
        return;
    }

    if (type === 'video' || type === 'live') {
        openVideoModal(url);
    } else {
        window.open(url, '_blank');
    }
}

function openVideoModal(url) {
    let embedUrl = url;

    // Robust YouTube ID extraction
    try {
        if (url.includes('youtube.com') || url.includes('youtu.be')) {
            let videoId = '';
            if (url.includes('v=')) {
                videoId = url.split('v=')[1].split('&')[0];
            } else if (url.includes('youtu.be/')) {
                videoId = url.split('youtu.be/')[1].split('?')[0];
            } else if (url.includes('embed/')) {
                videoId = url.split('embed/')[1].split('?')[0];
            }

            if (videoId) {
                embedUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0`;
            }
        }
    } catch (e) {
        console.error("Error parsing video URL", e);
    }

    const modal = document.createElement('div');
    modal.className = 'video-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-btn" onclick="this.parentElement.parentElement.remove()">×</span>
            <iframe src="${embedUrl}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
    `;
    document.body.appendChild(modal);
}

// --- Dynamic Interactions ---
// Scroll Listener Removed to allow CSS Animation to take over color cycling.
// window.addEventListener('scroll', () => { ... });

window.addEventListener('click', (e) => {
    // Add a ripple or glitch effect on click?
    // For now, let's just do a tiny jump
    if (e.target.tagName !== 'BUTTON') {
        // Maybe play a sound sound later?
    }
});

function renderRecommendations(items) {
    const list = document.getElementById("recommendations-list");
    if (items.length === 0) {
        list.innerHTML = '<p style="padding:10px; opacity:0.7">Interact with content to see recommendations.</p>';
        return;
    }

    list.innerHTML = items.map(item => `
        <div class="rec-item">
            <img src="${item.image_url}" class="rec-img">
            <div class="rec-info">
                <h4>${item.title}</h4>
                <span class="rec-category">${item.category}</span>
            </div>
        </div>
    `).join('');
}

// --- Event Handlers ---

function handleLike(btn, contentId) {
    if (btn.classList.contains('liked')) return;

    btn.classList.add('liked');
    btn.innerHTML = '<i class="fas fa-heart"></i> Liked';

    // Tiny animation effect
    btn.style.transform = "scale(1.1)";
    setTimeout(() => btn.style.transform = "scale(1)", 200);

    sendInteraction(contentId);

    // Dynamic Injection Logic
    injectDynamicContent();
}

async function injectDynamicContent() {
    try {
        const response = await fetch(`${API_URL}/recommend/${userId}`);
        const data = await response.json();

        // Take top 2 recommendations
        const newItems = data.slice(0, 2);

        if (newItems.length > 0) {
            const grid = document.getElementById("content-grid");

            // Create a separator
            const separator = document.createElement('div');
            separator.style.gridColumn = "1 / -1";
            separator.style.margin = "20px 0";
            separator.style.borderTop = "1px dashed var(--neon-pink)";
            separator.style.textAlign = "center";
            separator.innerHTML = `<span style="background:black; padding:0 10px; color:var(--neon-pink); font-size:0.8rem; letter-spacing: 2px;">BECAUSE YOU LIKED THIS</span>`;

            grid.appendChild(separator);

            newItems.forEach(item => {
                const card = createCardElement(item);
                card.style.borderColor = "var(--neon-pink)";
                card.classList.add('fade-in');
                grid.appendChild(card);
            });

            // Auto scroll slightly to show new content
            setTimeout(() => {
                separator.scrollIntoView({ behavior: "smooth", block: "center" });
            }, 500);
        }
    } catch (e) {
        console.error("Error injecting content", e);
    }
}

function createCardElement(item) {
    const div = document.createElement('div');
    // Re-use logic from renderContent but for single element
    let badge = '';
    let btnText = '<i class="far fa-heart"></i> Like';
    let cardClass = '';

    // FIX: Handle 'video' explicitly so it shows WATCH instead of LIKE
    if (item.content_type === 'video') {
        badge = '<div class="badge badge-video" style="background:#6a00ff; color:white;">VIDEO</div>';
        btnText = '<i class="fas fa-play"></i> Watch';
        cardClass = 'type-video';
    } else if (item.content_type === 'live') {
        badge = '<div class="badge badge-live">● LIVE</div>';
        btnText = '<i class="fas fa-play"></i> Watch';
        cardClass = 'type-live';
    } else if (item.content_type === 'ticket') {
        badge = '<div class="badge badge-ticket"><i class="fas fa-ticket-alt"></i> TICKET</div>';
        btnText = '<i class="fas fa-shopping-cart"></i> Buy';
        cardClass = 'type-ticket';
    } else if (item.content_type === 'merchandise') {
        badge = '<div class="badge badge-merch">SHOP</div>';
        btnText = '<i class="fas fa-shopping-bag"></i> Shop';
    } else if (item.content_type === 'article') {
        badge = '<div class="badge badge-article">READ</div>';
        btnText = '<i class="fas fa-book-open"></i> Read';
    }

    div.className = `card ${cardClass}`;
    div.innerHTML = `
        ${badge}
        <img src="${item.image_url}" alt="${item.title}" class="card-img">
        <div class="card-body">
            <span class="card-category">${item.category}</span>
            <h3 class="card-title">${item.title}</h3>
            <div class="card-tags">
                ${item.tags.split(',').map(tag => `<span class="tag">#${tag.trim()}</span>`).join('')}
            </div>
            
            <div style="display:flex; gap:10px;">
                <button class="action-btn" onclick="handleLike(this, ${item.id})" style="flex:1">
                    <i class="far fa-heart"></i>
                </button>
                <button class="action-btn" onclick="handleAction('${item.content_type}', '${item.action_url}')" style="flex:3; background:rgba(255,255,255,0.1); border-color:white;">
                    ${btnText}
                </button>
            </div>
        </div>
    `;
    return div;
}

// --- Init ---
fetchContent();
fetchRecommendations();
updateDebugProfile();
