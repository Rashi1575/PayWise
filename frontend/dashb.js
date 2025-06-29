document.addEventListener("DOMContentLoaded", () => {
  /* ───────────────── HELPERS ───────────────── */
  const sections = Array.from(document.querySelectorAll("main section"));
  const showOnly = (...els) => {
    sections.forEach(sec => sec.style.display = "none");
    els.forEach(el => el && (el.style.display = "block"));
  };

  const ctx = document.getElementById('spendingChart').getContext('2d');
  const spendingChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Food', 'Transport', 'Utilities', 'Shopping', 'Others'],
      datasets: [{
        label: 'Spending',
        data: [5000, 2000, 1500, 3000, 1000],
        backgroundColor: ['#00bfa5', '#00acc1', '#ffa726', '#ef5350', '#ab47bc'],
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false // Because you’re using a custom legend
        }
      }
    }
  });


  /* ───────────────── DARK MODE ───────────────── */
  const darkToggle = document.getElementById("dark-mode-toggle");
  if (darkToggle) {
    if (localStorage.getItem("dark-mode") === "enabled") {
      document.body.classList.add("dark-mode");
      darkToggle.checked = true;
    }
    darkToggle.addEventListener("change", () => {
      const enabled = darkToggle.checked;
      document.body.classList.toggle("dark-mode", enabled);
      localStorage.setItem("dark-mode", enabled ? "enabled" : "disabled");
    });
  }

  /* ───────────────── BUDGET PAGE NAV ───────────────── */
  const budgetLink = document.getElementById("budgetLink");
  const budgetSect = document.getElementById("budget-section");
  if (budgetLink && budgetSect) {
    budgetLink.addEventListener("click", e => {
      e.preventDefault();
      showOnly(budgetSect);
    });
  }

  /* ───────────────── SAVE BUDGET BUTTON ───────────────── */
  document.getElementById("saveBudget")?.addEventListener("click", () => {
    const total  = document.getElementById("totalBudget").value.trim();
    const cat    = document.getElementById("category").value;
    const catAmt = document.getElementById("categoryBudget").value.trim();

    if (!total || !catAmt) {
      alert("Please enter both total budget and category budget.");
      return;
    }
    alert(`Saved:\nTotal Budget: ₹${total}\n${cat}: ₹${catAmt}`);
  });

  const paywiseLink = document.getElementById("paywiseLink");
  const paymentSection = document.getElementById("payment-section");
  const insightsSection = document.getElementById("insights-section");

  paywiseLink.addEventListener("click", (e) => {
    e.preventDefault();

    // Hide all sections
    const allSections = document.querySelectorAll("main section");
    allSections.forEach(sec => sec.style.display = "none");

    // Show dashboard sections
    paymentSection.style.display = "block";
    insightsSection.style.display = "block";
  });

  /*-------------Profile Section ---------- */
  const profileLink = document.getElementById("profileLink");
  const profileSection = document.getElementById("profile-section");

  profileLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelectorAll("main section").forEach(sec => sec.style.display = "none");
    profileSection.style.display = "block";
  });

  const rewardsLink = document.getElementById("rewardsLink");
  const rewardsSection = document.getElementById("rewards-section");
  const highestCategoryEl = document.getElementById("highestCategory");

  rewardsLink.addEventListener("click", (e) => {
    e.preventDefault();
    sections.forEach(sec => sec.style.display = "none");
    rewardsSection.style.display = "block";

    // ⬇️ Replace with actual highest category if needed
    const categoryData = {
      labels: ["Food", "Transport", "Utilities", "Shopping", "Others"],
      data: [5000, 2000, 1500, 3000, 1000]
    };

    const maxIndex = categoryData.data.indexOf(Math.max(...categoryData.data));
    const topCategory = categoryData.labels[maxIndex];
    highestCategoryEl.textContent = topCategory;

    // Optionally: you can change offers dynamically here as well!
  });

  function copyReferral() {
  navigator.clipboard.writeText("PAYWISE123");
  alert("Referral code copied!");
  }

  /* ───────────────── CHART #2 (Bar) ───────────────── */
  const barCtx = document.getElementById("budgetChart")?.getContext("2d");
  if (barCtx) {
    new Chart(barCtx, {
      type: "bar",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
          label: "Monthly Budget (₹)",
          data: [18000, 20000, 19500, 21000, 19000, 20500],
          backgroundColor: "#00c9a7"
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });
  }

  /* ───────────────── DASHBOARD (HOME & LOGO) NAV ───────────────── */
  const paymentSect  = document.querySelector(".payment-section");
  const insightsSect = document.querySelector(".insights-section");

  // Home link
  document.getElementById("homeLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(paymentSect, insightsSect);
  });

  // PayWise logo link
  document.getElementById("paywiseLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(paymentSect, insightsSect);
  });

  const aboutLink = document.getElementById("aboutLink");
  const aboutSection = document.getElementById("about-section");

  aboutLink.addEventListener("click", (e) => {
    e.preventDefault();
    const allSections = document.querySelectorAll("main section");
    allSections.forEach(sec => sec.style.display = "none");
    aboutSection.style.display = "block";
  });

  // ───────────────────── LOGOUT ─────────────────────
  const payments = [
  {
    id: "TXN001",
    date: "2025-06-12",
    type: "Grocery Shopping",
    withdrawal: 2000,
    deposit: 0,
    category: "Groceries",
    closing: 8000
  },
  {
    id: "TXN002",
    date: "2025-05-28",
    type: "Salary",
    withdrawal: 0,
    deposit: 15000,
    category: "Income",
    closing: 18000
  },
  // Add more dummy records
    ];

    function renderTable(data) {
      const tbody = document.querySelector("#paymentTable tbody");
      tbody.innerHTML = ""; // Clear previous rows

      data.forEach(txn => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${txn.id}</td>
          <td>${txn.date}</td>
          <td>${txn.type}</td>
          <td>${txn.withdrawal || '-'}</td>
          <td>${txn.deposit || '-'}</td>
          <td>${txn.category}</td>
          <td>${txn.closing}</td>
        `;
        tbody.appendChild(row);
      });
    }

    document.getElementById("monthSelect").addEventListener("change", function () {
      const selected = this.value;
      if (selected === "all") {
        renderTable(payments);
      } else {
        const filtered = payments.filter(txn => txn.date.startsWith(selected));
        renderTable(filtered);
      }
    });

    // Load default table
    renderTable(payments);

    document.getElementById("paymentHistoryBtn").addEventListener("click", function (e) {
    e.preventDefault();

    // Optional: Hide all other sections
    const allSections = document.querySelectorAll("main section");
    allSections.forEach(sec => sec.style.display = "none");

    // Show payment history section
    const paymentSection = document.getElementById("payment-history-section");
    if (paymentSection) paymentSection.style.display = "block";

    // Optional: Reset month filter and render table again
    document.getElementById("monthSelect").value = "all";
    renderTable(payments);
  });

  document.getElementById("togglePayMode").addEventListener("click", () => {
  const section = document.getElementById("payment-history-section");
  section.classList.toggle("dark-mode");
  section.classList.toggle("light-mode");
  });

  // ───────────────────── LOGOUT ─────────────────────
  document.getElementById("logoutLink")?.addEventListener("click", (e) => {
    e.preventDefault();

    // Optional: clear any saved session data
    localStorage.removeItem("dark-mode"); // or any user info you stored

    // Redirect to login page
    window.location.href = "index.html";
  });

});
