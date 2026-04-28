/**
 * SugarSense — main.js
 * Handles: mobile nav, table search, form validation UX
 */

// ── Mobile Nav Toggle ──────────────────────────────────────────────
const hamburger = document.getElementById("hamburger");
const navLinks  = document.querySelector(".nav-links");

if (hamburger && navLinks) {
  hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });

  // Close nav when a link is clicked
  navLinks.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => navLinks.classList.remove("open"));
  });
}

// ── Live Table Search ──────────────────────────────────────────────
const searchInput = document.getElementById("tableSearch");
const table       = document.getElementById("recordsTable");

if (searchInput && table) {
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    const rows  = table.querySelectorAll("tbody tr");

    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(query) ? "" : "none";
    });
  });
}

// ── Form Validation UX ─────────────────────────────────────────────
const form = document.getElementById("farm-form");

if (form) {
  // Set max date to today for planting date
  const dateInput = document.getElementById("date_of_planting");
  if (dateInput) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.setAttribute("max", today);
  }

  form.addEventListener("submit", (e) => {
    const landArea           = parseFloat(document.getElementById("land_area")?.value);
    const irrigationInterval = parseInt(document.getElementById("irrigation_interval")?.value);
    const fertCost           = parseFloat(document.getElementById("fertilizer_cost")?.value);

    if (landArea <= 0 || isNaN(landArea)) {
      alert("Land area must be a positive number.");
      e.preventDefault();
      return;
    }
    if (irrigationInterval < 1 || isNaN(irrigationInterval)) {
      alert("Irrigation interval must be at least 1 day.");
      e.preventDefault();
      return;
    }
    if (fertCost < 0 || isNaN(fertCost)) {
      alert("Fertilizer cost cannot be negative.");
      e.preventDefault();
      return;
    }
  });
}

// ── Auto-dismiss flash messages ────────────────────────────────────
document.querySelectorAll(".flash").forEach(flash => {
  setTimeout(() => {
    flash.style.transition = "opacity .5s";
    flash.style.opacity    = "0";
    setTimeout(() => flash.remove(), 500);
  }, 4000);
});

// ── Animate metric cards on result page ──────────────────────────
document.querySelectorAll(".metric-card").forEach((card, i) => {
  card.style.opacity   = "0";
  card.style.transform = "translateY(16px)";
  card.style.transition = `opacity .4s ease ${i * 0.08}s, transform .4s ease ${i * 0.08}s`;

  // Trigger after paint
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      card.style.opacity   = "1";
      card.style.transform = "translateY(0)";
    });
  });
});
