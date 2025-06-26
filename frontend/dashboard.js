document.addEventListener("DOMContentLoaded", () => {
  // ──────── SECTION HELPERS ────────
  const showOnly = (...els) => {
    document.querySelectorAll("main section").forEach(sec => sec.style.display = "none");
    els.forEach(el => el && (el.style.display = "block"));
  };

  // ──────── DARK MODE SETUP ────────
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

  // ──────── PIE CHART: Spending ────────
  const pieCanvas = document.getElementById("spendingChart");
  if (pieCanvas) {
    const ctx = pieCanvas.getContext("2d");
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Food', 'Transport', 'Utilities', 'Shopping', 'Others'],
        datasets: [{
          data: [5000, 2000, 1500, 3000, 1000],
          backgroundColor: ['#00bfa5', '#00acc1', '#ffa726', '#ef5350', '#ab47bc'],
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } }
      }
    });
  }

  // ──────── BAR CHART: Budget ────────
  const barCanvas = document.getElementById("budgetChart");
  if (barCanvas) {
    const barCtx = barCanvas.getContext("2d");
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

  // ──────── NAVIGATION SETUP ────────
  const sections = {
    dashboard: [document.getElementById("payment-section"), document.getElementById("insights-section")],
    profile: document.getElementById("profile-section"),
    budget: document.getElementById("budget-section"),
    rewards: document.getElementById("rewards-section"),
    about: document.getElementById("about-section"),
    payments: document.getElementById("payment-history-section")
  };

  document.getElementById("paywiseLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(...sections.dashboard);
  });

  document.getElementById("homeLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(...sections.dashboard);
  });

  document.getElementById("profileLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(sections.profile);
  });

  document.getElementById("budgetLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(sections.budget);
  });

  document.getElementById("aboutLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(sections.about);
  });

  document.getElementById("rewardsLink")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(sections.rewards);

    // Update top category
    const categoryData = { labels: ["Food", "Transport", "Utilities", "Shopping", "Others"], data: [5000, 2000, 1500, 3000, 1000] };
    const maxIndex = categoryData.data.indexOf(Math.max(...categoryData.data));
    document.getElementById("highestCategory").textContent = categoryData.labels[maxIndex];
  });

  // ──────── BUDGET SAVE ────────
  document.getElementById("saveBudget")?.addEventListener("click", () => {
    const total = document.getElementById("totalBudget").value.trim();
    const cat = document.getElementById("category").value;
    const catAmt = document.getElementById("categoryBudget").value.trim();
    if (!total || !catAmt) return alert("Please enter both total and category budget.");
    alert(`Saved:\nTotal Budget: ₹${total}\n${cat}: ₹${catAmt}`);
  });

  // ──────── REFERRAL COPY ────────
  document.querySelector(".referral-code")?.addEventListener("click", () => {
    navigator.clipboard.writeText("PAYWISE123");
    alert("Referral code copied!");
  });

  // ──────── PAYMENT HISTORY ────────
  const payments = [
    { id: "TXN001", date: "2025-06-12", type: "Grocery Shopping", withdrawal: 2000, deposit: 0, category: "Groceries", closing: 8000 },
    { id: "TXN002", date: "2025-05-28", type: "Salary", withdrawal: 0, deposit: 15000, category: "Income", closing: 18000 }
  ];

  const renderTable = (data) => {
    const tbody = document.querySelector("#paymentTable tbody");
    tbody.innerHTML = "";
    data.forEach(txn => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${txn.id}</td>
        <td>${txn.date}</td>
        <td>${txn.type}</td>
        <td>${txn.withdrawal || '-'}</td>
        <td>${txn.deposit || '-'}</td>
        <td>${txn.category}</td>
        <td>${txn.closing}</td>`;
      tbody.appendChild(row);
    });
  };

  document.getElementById("paymentHistoryBtn")?.addEventListener("click", e => {
    e.preventDefault();
    showOnly(sections.payments);
    document.getElementById("monthSelect").value = "all";
    renderTable(payments);
  });

  document.getElementById("monthSelect")?.addEventListener("change", function () {
    const selected = this.value;
    if (selected === "all") renderTable(payments);
    else renderTable(payments.filter(txn => txn.date.startsWith(selected)));
  });

  renderTable(payments); // default load

  // ──────── LIGHT/DARK TOGGLE FOR HISTORY ────────
  document.getElementById("togglePayMode")?.addEventListener("click", () => {
    const section = sections.payments;
    section.classList.toggle("dark-mode");
    section.classList.toggle("light-mode");
  });

  // ──────── LOGOUT + SESSION CHECK ────────
  const username = localStorage.getItem("username");
  const loggedIn = localStorage.getItem("loggedIn");

  if (!loggedIn) {
    alert("Please login first.");
    window.location.href = "index.html";
  }

  document.getElementById("logoutBtn")?.addEventListener("click", e => {
    e.preventDefault();
    localStorage.removeItem("loggedIn");
    localStorage.removeItem("username");
    window.location.href = "index.html";
  });

  // OPTIONAL: show username on dashboard if needed
  const nameTag = document.getElementById("username");
  if (username && nameTag) nameTag.textContent = username;
});

  
