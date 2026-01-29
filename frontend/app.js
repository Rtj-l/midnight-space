const API_URL = "http://localhost:8001";
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
        let btnText = '<i class="far fa-heart"></i> Like';
        let cardClass = '';

        if (item.content_type === 'live') {
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
            <img src="${item.image_url}" alt="${item.title}" class="card-img">
            <div class="card-body">
                <span class="card-category">${item.category}</span>
                <h3 class="card-title">${item.title}</h3>
                <div class="card-tags">
                    ${item.tags.split(',').map(tag => `<span class="tag">#${tag.trim()}</span>`).join('')}
                </div>
                <button class="action-btn" onclick="handleLike(this, ${item.id})">
                    ${btnText}
                </button>
            </div>
        </div>
    `}).join('');
}

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
}

// --- Init ---
fetchContent();
fetchRecommendations();
updateDebugProfile();
