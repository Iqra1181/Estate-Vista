/* ═══════════════════════════════════════════════════════════════
   main.js — EstateVista Global JavaScript
   
   Features:
   1. 🌙 Dark Mode Toggle (persists across pages via localStorage)
   2. ❤️ Favorite Toggle (works from listing cards)
   3. Navbar scroll effect
═══════════════════════════════════════════════════════════════ */

// ─────────────────────────────────────────────
// 1. DARK MODE TOGGLE
// Saves preference in localStorage so it
// persists when user navigates pages.
// ─────────────────────────────────────────────

const html = document.documentElement;       // <html> element
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

// Apply saved theme on every page load
function applySavedTheme() {
    const saved = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
}

// Update the moon/sun icon based on current theme
function updateThemeIcon(theme) {
    if (!themeIcon) return;
    if (theme === 'dark') {
        themeIcon.className = 'bi bi-sun-fill';       // Show sun when in dark mode
    } else {
        themeIcon.className = 'bi bi-moon-fill';      // Show moon when in light mode
    }
}

// Toggle between light and dark when button clicked
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const current = html.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);         // Remember choice
        updateThemeIcon(next);
    });
}

// Run theme restore immediately (before DOM renders fully)
applySavedTheme();


// ─────────────────────────────────────────────
// 2. FAVORITE TOGGLE (from listing cards)
// Called by the heart buttons on property cards
// in index.html and favorites.html
// ─────────────────────────────────────────────

/**
 * Toggle a property as favorite/unfavorite.
 * @param {number} propertyId - The property's database ID
 * @param {HTMLElement} btn   - The heart button element that was clicked
 */
async function toggleFavorite(propertyId, btn) {
    try {
        const res = await fetch(`/favorite/${propertyId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        // Not logged in → redirect to login page
        if (res.status === 401) {
            window.location.href = '/login';
            return;
        }

        const data = await res.json();
        const icon = btn.querySelector('i');

        if (data.status === 'added') {
            // Property was saved → fill the heart
            btn.classList.add('active');
            icon.className = 'bi bi-heart-fill';

            // Animate: quick scale pulse
            btn.style.transform = 'scale(1.3)';
            setTimeout(() => btn.style.transform = '', 200);

        } else {
            // Property was unsaved → outline heart
            btn.classList.remove('active');
            icon.className = 'bi bi-heart';

            // If on favorites page, fade out and remove the card
            const card = btn.closest('.col-md-4') || btn.closest('.col-md-3');
            if (card && window.location.pathname.includes('/favorites')) {
                card.style.transition = 'opacity 0.3s, transform 0.3s';
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';
                setTimeout(() => card.remove(), 300);
            }
        }

    } catch (err) {
        console.error('Failed to toggle favorite:', err);
        showToast('Something went wrong. Please try again.', 'danger');
    }
}


// ─────────────────────────────────────────────
// 3. NAVBAR SCROLL EFFECT
// Adds a stronger shadow when user scrolls down
// ─────────────────────────────────────────────

const nav = document.getElementById('mainNav');
window.addEventListener('scroll', () => {
    if (!nav) return;
    if (window.scrollY > 40) {
        nav.style.boxShadow = '0 4px 24px rgba(0,0,0,0.12)';
    } else {
        nav.style.boxShadow = 'none';
    }
});


// ─────────────────────────────────────────────
// 4. TOAST NOTIFICATION HELPER
// Shows a small Bootstrap toast message
// ─────────────────────────────────────────────

function showToast(message, type = 'success') {
    // Create toast container if it doesn't exist
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }

    const id = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${id}" class="toast align-items-center text-white bg-${type} border-0 shadow" role="alert">
            <div class="d-flex">
                <div class="toast-body fw-500">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', toastHTML);

    const toastEl = document.getElementById(id);
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();

    // Remove from DOM after hiding
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}


// ─────────────────────────────────────────────
// 5. AUTO-DISMISS FLASH ALERTS
// Flash messages auto-disappear after 5 seconds
// ─────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            // Use Bootstrap's Alert API to dismiss smoothly
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
});
