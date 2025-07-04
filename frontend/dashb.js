document.addEventListener("DOMContentLoaded", () => {
  //new Kpish
  const payMethodSelect = document.getElementById("payMethod");
  const extraDiv = document.getElementById("paymentDetailsExtra");

  payMethodSelect.addEventListener("change", () => {
    const method = payMethodSelect.value;
    if (method === "UPI") {
      extraDiv.innerHTML = `
        <input type="text" id="extraField1" placeholder="Enter UPI ID (e.g., name@upi)" />
      `;
    } else if (method === "Net Banking") {
      extraDiv.innerHTML = `
        <select id="extraField1">
          <option selected disabled>Select Bank</option>
          <option>HDFC</option>
          <option>ICICI</option>
          <option>SBI</option>
          <option>Axis</option>
        </select>
        <input type="text" id="extraField2" placeholder="Enter IFSC Code" />
      `;
    } else {
      extraDiv.innerHTML = "";
    }
  });

// Load initial field
payMethodSelect.dispatchEvent(new Event("change"));


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
  //new kpish
  profileLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelectorAll("main section").forEach(sec => sec.style.display = "none");
    profileSection.style.display = "block";
    loadProfile();  // ✅ Load profile data from Supabase
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


  function loadProfile() {
    const username = localStorage.getItem("username");
    if (!username) return;

    fetch(`http://localhost:5000/profile/${username}`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const profile = data.data;
          document.getElementById("username").textContent = username;
          document.getElementById("fullName").value = profile.full_name || "";
          document.getElementById("email").value = profile.email || "";
          document.getElementById("phone").value = profile.phone || "";
          document.getElementById("gender").value = profile.gender || "";
          document.getElementById("nationality").value = profile.nationality || "";
          document.getElementById("address").value = profile.address || "";
        }
      });
  }


  function saveProfileData() {
    const username = localStorage.getItem("username");
    if (!username) return alert("No user logged in.");

    const full_name   = document.getElementById("fullName").value;
    const email       = document.getElementById("email").value;
    const phone       = document.getElementById("phone").value;
    const gender      = document.getElementById("gender").value;
    const nationality = document.getElementById("nationality").value;
    const address     = document.getElementById("address").value;

    fetch("http://localhost:5000/update-profile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        full_name,
        email,
        phone,
        gender,
        nationality,
        address
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) alert("✅ Profile saved!");
      else alert("❌ Error saving profile: " + data.error);
    })
    .catch(err => alert("❌ Server error: " + err));
  }

  document.getElementById("saveProfileBtn")?.addEventListener("click", saveProfileData);

});
  //new Kpish
  document.getElementById("submitPayment")?.addEventListener("click", async () => {
    const receiver = document.getElementById("receiverUsername").value;
    const amount = document.getElementById("payAmount").value.trim();
    const desc = document.getElementById("payDesc").value;
    const method = document.getElementById("payMethod").value;
    const sender = localStorage.getItem("username");

    const payStatus = document.getElementById("payStatus");
    const loader = document.getElementById("paymentLoader");

    // Validate inputs
    if (!receiver || !amount || !desc || isNaN(amount) || amount <= 0) {
      alert("Please fill all fields correctly.");
      return;
    }

    // Show loader
    payStatus.textContent = "";
    loader.style.display = "block";

    // Simulate fake processing delay
    setTimeout(async () => {
      try {
        const res = await fetch("http://localhost:5000/make-payment", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sender,
            receiver,
            amount: parseFloat(amount),
            description: desc,
            payment_method: method
          })
        });

        const data = await res.json();
        loader.style.display = "none";

        if (data.success) {
          payStatus.textContent = "✅ Transaction successful!";
          document.getElementById("receiverUsername").value = "";
          document.getElementById("payAmount").value = "";
          document.getElementById("payDesc").value = "";
          document.getElementById("paymentDetailsExtra").innerHTML = "";
        } else {
          payStatus.textContent = `❌ Error: ${data.error}`;
        }
      } catch (err) {
        loader.style.display = "none";
        payStatus.textContent = "❌ Server error: " + err.message;
      }
    }, 2000);
  });


  async function loadPayments() {
  const username = localStorage.getItem("username");
  const res = await fetch("http://localhost:5000/get-payments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });

  const data = await res.json();
  if (data.success) renderTable(data.payments);
}

document.getElementById("paymentHistoryBtn").addEventListener("click", async (e) => {
  e.preventDefault();
  document.querySelectorAll("main section").forEach(sec => sec.style.display = "none");
  const section = document.getElementById("payment-history-section");
  section.style.display = "block";
  await loadPayments();
  //new kpish
  loadProfile();

});
