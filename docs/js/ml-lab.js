// Wires the wine-quality form to the live /api/ml/wine-quality endpoint.
// Field names here match WineInput in api/main.py exactly.

const WINE_DEFAULTS = {
  fixed_acidity: 7.4, volatile_acidity: 0.7, citric_acid: 0.0,
  residual_sugar: 1.9, chlorides: 0.076, free_sulfur_dioxide: 11,
  total_sulfur_dioxide: 34, density: 0.9978, pH: 3.51,
  sulphates: 0.56, alcohol: 9.4,
};

function initWineForm() {
  const form = document.getElementById("wine-form");
  const result = document.getElementById("wine-result");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = {};
    for (const key of Object.keys(WINE_DEFAULTS)) {
      payload[key] = parseFloat(formData.get(key));
    }

    result.className = "predict-result";
    result.style.display = "block";
    result.textContent = "Predicting…";

    try {
      const res = await fetch(`${API_BASE}/api/ml/wine-quality`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || `status ${res.status}`);

      result.textContent = `Predicted quality: ${data.predicted_quality} / 10`;
    } catch (err) {
      result.className = "predict-result error";
      result.textContent = `Couldn't get a prediction — ${err.message}`;
    }
  });
}

document.addEventListener("DOMContentLoaded", initWineForm);
