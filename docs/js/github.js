// Pulls Sebastian's public repos straight from the GitHub REST API — no
// backend involved. This is the one API call in the whole site that the
// browser makes directly to a third party; see the roadmap's architecture
// notes for why.

const GITHUB_USERNAME = "SyoungCode";
const REPO_GRID_ID = "repo-grid";

async function loadRepos() {
  const grid = document.getElementById(REPO_GRID_ID);
  if (!grid) return;

  try {
    const res = await fetch(
      `https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=100`
    );

    if (!res.ok) {
      // Most likely cause on a fresh account: nothing to do with rate
      // limits, just a 404 because the username has zero repos or a typo.
      throw new Error(`GitHub API responded with ${res.status}`);
    }

    const repos = await res.json();
    const visible = repos.filter((r) => !r.fork); // hide forks, keep original work

    if (visible.length === 0) {
      grid.innerHTML = `
        <div class="empty-state">
          No public repos on <strong>github.com/${GITHUB_USERNAME}</strong> yet —
          once you push your first one, it'll show up here automatically.
        </div>`;
      return;
    }

    grid.innerHTML = visible
      .map(
        (repo) => `
        <div class="card">
          <h3>${escapeHtml(repo.name)}</h3>
          <p>${escapeHtml(repo.description || "No description yet.")}</p>
          <div class="tags">
            ${repo.language ? `<span class="pill">${escapeHtml(repo.language)}</span>` : ""}
            <span class="pill">★ ${repo.stargazers_count}</span>
          </div>
          <p style="margin-top:12px;margin-bottom:0;">
            <a class="card-link" href="${repo.html_url}" target="_blank" rel="noopener">View on GitHub →</a>
          </p>
        </div>`
      )
      .join("");
  } catch (err) {
    grid.innerHTML = `
      <div class="empty-state">
        Couldn't load repos from GitHub right now (${escapeHtml(err.message)}).
        <br>Check <a href="https://github.com/${GITHUB_USERNAME}" target="_blank" rel="noopener">github.com/${GITHUB_USERNAME}</a> directly.
      </div>`;
  }
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

document.addEventListener("DOMContentLoaded", loadRepos);
