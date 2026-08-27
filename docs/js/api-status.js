// Pings the backend API and updates the "Backend API" line in the Home
// page's status strip — a small, honest proof that the frontend and
// backend actually talk to each other, not just a claim in prose.

const API_BASE = "https://syoungcode-github-io.onrender.com";

async function checkBackendStatus() {
  const dot = document.getElementById("backend-status-dot");
  const text = document.getElementById("backend-status-text");
  if (!dot || !text) return;

  if (API_BASE.includes("YOUR-RENDER-URL")) {
    // Not deployed yet — leave the "planned" state as-is, no network call.
    return;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);

  try {
    const res = await fetch(`${API_BASE}/api/ping`, { signal: controller.signal });
    clearTimeout(timeout);
    if (!res.ok) throw new Error(`status ${res.status}`);
    dot.className = "dot live";
    text.textContent = "Backend API — live";
  } catch (err) {
    clearTimeout(timeout);
    // Render's free tier sleeps after ~15 min idle — a timeout here usually
    // just means it's waking up, not that anything is broken.
    dot.className = "dot progress";
    text.textContent = "Backend API — waking up (free tier), try refreshing in a moment";
  }
}

document.addEventListener("DOMContentLoaded", checkBackendStatus);
