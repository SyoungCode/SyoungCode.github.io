// Fetches the four KPIs from the backend and fills in the stat tiles.
// If the database isn't connected yet (Phase 4 setup not done — see
// database/README.md), the API returns a clear "not connected" error
// instead of crashing, and this just shows that message honestly.

const KPI_FIELDS = [
  { id: "kpi-orders", key: "total_orders", format: (v) => v.toLocaleString() },
  { id: "kpi-revenue", key: "total_revenue_brl", format: (v) => `R$${v.toLocaleString(undefined, { maximumFractionDigits: 0 })}` },
  { id: "kpi-review", key: "avg_review_score", format: (v) => `${v.toFixed(2)} / 5` },
  { id: "kpi-delivery", key: "avg_delivery_days", format: (v) => `${v.toFixed(1)} days` },
];

async function loadDashboard() {
  const grid = document.getElementById("kpi-grid");
  const note = document.getElementById("dashboard-note");
  if (!grid) return;

  try {
    const res = await fetch(`${API_BASE}/api/olist/kpis`);
    const data = await res.json();

    if (!res.ok) {
      // The API's own message (e.g. "Database not connected yet...") is
      // more useful here than a generic error.
      throw new Error(data.detail || `status ${res.status}`);
    }

    KPI_FIELDS.forEach(({ id, key, format }) => {
      const el = document.getElementById(id);
      if (el) el.textContent = format(data[key]);
    });
    if (note) note.style.display = "none";
    grid.style.display = "grid";
  } catch (err) {
    const detail = document.getElementById("dashboard-note-detail");
    if (detail) detail.textContent = err.message;
    if (note) note.style.display = "block";
    grid.style.display = "none";
  }
}

document.addEventListener("DOMContentLoaded", loadDashboard);
