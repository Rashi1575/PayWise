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

function renderTable(data) {
  const tbody = document.querySelector("#paymentTable tbody");
  tbody.innerHTML = "";

  data.forEach(txn => {
    const row = document.createElement("tr");

    const date = new Date(txn.date).toLocaleDateString("en-IN");
    const withdrawal = txn.withdrawal != null ? `₹${txn.withdrawal}` : "-";
    const deposit = txn.deposit != null ? `₹${txn.deposit}` : "-";
    const closing = txn.closing_balance != null ? `₹${txn.closing_balance}` : "-";

    row.innerHTML = `
      <td>${txn.transaction_id || "-"}</td>
      <td>${date}</td>
      <td>${txn.description || "-"}</td>
      <td>${withdrawal}</td>
      <td>${deposit}</td>
      <td>${txn.category}</td>
      <td>${closing}</td>
    `;

    tbody.appendChild(row);
  });
}

function getSuggestions(category) {
  const map = {
    "Food and Grocery": "Dining, Fast Food",
    "Transportation": "Cabs, Fuel",
    "Shopping": "Clothes, Online Orders",
    "Housing and Bills": "Electricity, Rent",
    "Healthcare": "Medicine, Tests",
    "Entertainment": "Movies, OTT",
    "Education": "Tuition, Courses",
    "Others": "Review all expenses"
  };
  return map[category] || "Review all expenses";
}

async function loadSpendingInsights() {
  const username = localStorage.getItem("username");
  if (!username) return;

  const res = await fetch("http://localhost:5000/spending-insights", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });

  const data = await res.json();
  if (!data.success) return alert("❌ Error fetching insights");

  const { total_spent, category_totals, highest_category } = data;

  // Update insight cards
  document.querySelector(".card:nth-child(1)").textContent = `Total Monthly Spending: ₹${total_spent}`;
  document.querySelector(".card:nth-child(2)").textContent = `Highest Spending Category: ${highest_category}`;
  document.querySelector(".card:nth-child(3)").textContent = `Suggested Savings: ${getSuggestions(highest_category)}`;

  // Update chart
  const labels = Object.keys(category_totals);
  const values = Object.values(category_totals);
  const colors = ['#00bfa5','#00acc1','#ffa726','#ef5350','#ab47bc','#42a5f5','#66bb6a','#ff7043'];

  if (spendingChart) spendingChart.destroy();

  const ctx = document.getElementById('spendingChart').getContext('2d');
  spendingChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, labels.length)
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  });
}

let spendingChart; // holds the pie chart instance

document.addEventListener("DOMContentLoaded", () => {


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


  // Make Payment link
  const makePaymentLink = document.getElementById("makePaymentLink");
  makePaymentLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelectorAll("main section").forEach(sec => sec.style.display = "none");
    paymentSection.style.display = "block";
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
    insightsSection.style.display = "block";
  });

  /*-------------Profile Section ---------- */
  const profileLink = document.getElementById("profileLink");
  const profileSection = document.getElementById("profile-section");

  if (profileLink && profileSection) {
    profileLink.addEventListener("click", (e) => {
      e.preventDefault();
      showOnly(profileSection);  // reuse your own helper
      loadProfile();             // fetch from backend
      loadProfile();  // Now it runs when you open the section
    });
  }

  const rewardsLink = document.getElementById("rewardsLink");
  const rewardsSection = document.getElementById("rewards-section");

  if (rewardsLink && rewardsSection) {
    rewardsLink.addEventListener("click", (e) => {
      e.preventDefault();
      showOnly(rewardsSection);
      loadRewards();

      const categoryData = {
        labels: ["Food", "Transport", "Utilities", "Shopping", "Others"],
        data: [5000, 2000, 1500, 3000, 1000]
      };

      const maxIndex = categoryData.data.indexOf(Math.max(...categoryData.data));
      const topCategory = categoryData.labels[maxIndex];
      document.getElementById("highestCategory").textContent = topCategory;
    });
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
  
  document.getElementById("paywiseLink")?.addEventListener("click", e => {
    e.preventDefault();
    document.querySelectorAll("main section").forEach(sec => sec.style.display = "none");
    document.getElementById("insights-section").style.display = "block";
    loadSpendingInsights(); 
  });


  const aboutLink = document.getElementById("aboutLink");
  const aboutSection = document.getElementById("about-section");

  aboutLink.addEventListener("click", (e) => {
    e.preventDefault();
    const allSections = document.querySelectorAll("main section");
    allSections.forEach(sec => sec.style.display = "none");
    aboutSection.style.display = "block";
  });

  document.getElementById("monthSelect").addEventListener("change", async function () {
  const selected = this.value;
  const username = localStorage.getItem("username");

  const res = await fetch("http://localhost:5000/get-payments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });

  const data = await res.json();
  if (!data.success) return alert("❌ Error loading payments");

  let filtered = data.payments;

  if (selected !== "all") {
    // Rashi
    filtered = data.payments.filter(txn => {
      if (!txn.date) return false;
      const parts = txn.date.split("-");
      if (parts.length !== 3) return false;
      const year = parts[2];
      const month = parts[1].padStart(2, '0');
      return `${year}-${month}` === selected;
    });

  }

  renderTable(filtered);

  if (filtered.length === 0) {
    document.querySelector("#paymentTable tbody").innerHTML = `
      <tr><td colspan="7" style="text-align:center;">No transactions for selected month</td></tr>`;
  }

});

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
    // renderTable(payments);
  });

  document.getElementById("togglePayMode").addEventListener("click", () => {
  const section = document.getElementById("payment-history-section");
  section.classList.toggle("dark-mode");
  section.classList.toggle("light-mode");
  });

  // ───────────────────── LOGOUT ─────────────────────
  document.getElementById("logoutLink")?.addEventListener("click", (e) => {
    e.preventDefault();
    console.log("Logging out...");
    localStorage.removeItem("username");
    localStorage.removeItem("dark-mode");
    window.location.href = "index.html";  // or "login.html" if separate
  });

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

// Rashi
document.getElementById("paymentHistoryBtn").addEventListener("click", async (e) => {
  e.preventDefault();
  document.querySelectorAll("main section").forEach(sec => sec.style.display = "none");
  const section = document.getElementById("payment-history-section");
  section.style.display = "block";
  try {
    await loadPayments();            // fetch data from backend
    // renderTable(data.payments);     
  } catch (err) {
    console.error("Failed to load payments:", err);
  }
});

/* ───────────────────── REWARDS ───────────────────── */
// Get logged-in username from either localStorage or sessionStorage
const username = localStorage.getItem("username") || sessionStorage.getItem("username");

// Only proceed if username is present
if (username) {
  // Fetch active rewards
  function loadRewards() {
    const username = localStorage.getItem("username");
    if (!username) return;
    fetch("http://localhost:5000/get-rewards", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const list = document.getElementById("reward-list");
          list.innerHTML = "";

          if (data.rewards.length === 0) {
            list.innerHTML = `<li>No active rewards found.</li>`;
            return;
        }
        data.rewards.forEach(reward => {
            const [name, category, expiry] = reward;
            const li = document.createElement("li");
            li.innerHTML = `🎁 <strong>${name}</strong> — ${category} (expires on ${expiry})`;
            list.appendChild(li);
        });
      }   else {
          console.error(data.error);
      }
    });
}

// Add a new reward dynamically (example only!)
  fetch("/add-reward", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      reward_name: "₹50 Cashback",
      category: "Food",
      expiry_date: "2025-12-31",
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("✅ Reward Added:", data);
    });
// Suggest rewards for the user
  fetch("/suggest-rewards", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        console.log("💡 Suggestions:", data.suggestions);
      } else {
        console.error("❌ Suggestion error:", data.error);
      }
    });

// Auto-generate a reward dynamically
  fetch("/auto-generate-reward", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      category: "Food",
      trigger_type: "spend",
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("🎫 Auto-Generated Reward:", data);
    });
} else {
  console.error("⚠️ No logged-in user found. Cannot load rewards.");
}

/* ─────────────── TARGET TRACKER HANDLING ─────────────── */
  const editBtn = document.getElementById("edit-target-btn");
  const deleteBtn = document.getElementById("delete-target-btn");
  const saveBtn = document.getElementById("save-target-btn");
  const form = document.getElementById("edit-target-form");

  // Elements for UI rendering
  const titleEl = document.getElementById("target-title");
  const amountEl = document.getElementById("target-amount");
  const savedEl = document.getElementById("target-saved");
  const deadlineEl = document.getElementById("target-deadline");
  const progressFill = document.getElementById("savings-progress-fill");
  const progressText = document.getElementById("savings-progress-text");

  // Deadline alert
  const alertBox = document.getElementById("deadline-alert");
  const alertTitle = document.getElementById("alert-title");
  const alertDays = document.getElementById("alert-days");

  // Edit Target → Show Form
  editBtn.addEventListener("click", () => {
    form.style.display = form.style.display === "none" ? "block" : "none";

    // Pre-fill form with current values
    document.getElementById("edit-title").value = titleEl.textContent;
    document.getElementById("edit-amount").value = amountEl.textContent;
    document.getElementById("edit-saved").value = savedEl.textContent;
    
    // Convert "10 Oct 2025" to YYYY-MM-DD
    const parsedDate = new Date(deadlineEl.textContent);
    document.getElementById("edit-deadline").value = parsedDate.toISOString().split("T")[0];
  });

  // Save Target → Update UI
  saveBtn.addEventListener("click", () => {
    const newTitle = document.getElementById("edit-title").value;
    const newAmount = parseFloat(document.getElementById("edit-amount").value);
    const newSaved = parseFloat(document.getElementById("edit-saved").value);
    const newDeadline = document.getElementById("edit-deadline").value;

    if (!newTitle || isNaN(newAmount) || isNaN(newSaved) || !newDeadline) {
      alert("❌ Please fill all fields correctly.");
      return;
    }

    // Update UI
    titleEl.textContent = newTitle;
    amountEl.textContent = newAmount.toLocaleString();
    savedEl.textContent = newSaved.toLocaleString();
    deadlineEl.textContent = new Date(newDeadline).toLocaleDateString("en-IN", {
      day: "2-digit", month: "short", year: "numeric"
    });

    // Update progress bar
    const pct = Math.min(100, (newSaved / newAmount) * 100).toFixed(0);
    progressFill.style.width = `${pct}%`;
    progressText.textContent = `${pct}% completed`;

    // Update deadline alert
    const dueDate = new Date(newDeadline);
    const daysLeft = Math.ceil((dueDate - new Date()) / (1000 * 60 * 60 * 24));
    if (daysLeft <= 5 && daysLeft >= 0) {
      alertTitle.textContent = newTitle;
      alertDays.textContent = daysLeft;
      alertBox.style.display = "block";
    } else {
      alertBox.style.display = "none";
    }

    form.style.display = "none";
    // Rashi
    // Save to backend
    fetch("http://localhost:5000/targets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: localStorage.getItem("username"),
        title: newTitle,
        target_amount: newAmount,
        due_date: newDeadline,
        savings: newSaved
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("🎯 Target saved to backend!");
      } else {
        alert("❌ Failed to save target: " + data.error);
      }
    });

  });

  // Delete Target (stub)
  deleteBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to delete this target?")) {
      alert("🚧 Delete functionality coming soon.");
    }
  });

  // Rashi
  document.getElementById("submitPayment").addEventListener("click", () => {
    const sender = localStorage.getItem("username");
    const receiver = document.getElementById("receiverUsername").value;
    const amount = parseFloat(document.getElementById("payAmount").value);
    const description = document.getElementById("payDesc").value;
    const method = document.getElementById("payMethod").value;

    if (!sender || !receiver || !amount || !description) {
      document.getElementById("payStatus").textContent = "Please fill all fields.";
      return;
    }

    document.getElementById("paymentLoader").style.display = "block";

    fetch("http://localhost:5000/make-payment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sender,
        receiver,
        amount,
        description,
        method
      })
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("paymentLoader").style.display = "none";
      if (data.success) {
        document.getElementById("payStatus").textContent = "✅ Payment successful!";
      } else {
        document.getElementById("payStatus").textContent = "❌ Failed: " + data.message;
      }
    })
    .catch((err) => {
      document.getElementById("paymentLoader").style.display = "none";
      document.getElementById("payStatus").textContent = "⚠ Error processing payment.";
      console.error(err);
    });
  });

  document.getElementById("saveBudget").addEventListener("click", () => {
    const username = localStorage.getItem("username");
    const category = document.getElementById("category").value;
    const amount = parseFloat(document.getElementById("categoryBudget").value);

    if (!username || !category || isNaN(amount)) {
      alert("Please fill category and amount.");
      return;
    }

    fetch("http://localhost:5000/budgets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        category,
        budget_amount: amount
      })
    })

    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("Budget saved successfully.");
      } else {
        alert("Failed to save budget.");
      }
    });
  });
  // Rashi
  loadProfile();
  // loadPayments();
  loadSpendingInsights();
  loadTargets(); 
  
})
// DOM ends
// OUTSIDE the DOMContentLoaded block
// Rashi
async function loadTargets() {
  const username = localStorage.getItem("username");
  const res = await fetch("http://localhost:5000/targets?username=" + username);
  const data = await res.json();
  if (!data.success) return;

  const t = data.data[0];
  if (!t) return;

  document.getElementById("target-title").textContent = t.title;
  document.getElementById("target-amount").textContent = t.target_amount;
  document.getElementById("target-saved").textContent = t.savings;
  document.getElementById("target-deadline").textContent = new Date(t.due_date).toLocaleDateString("en-IN");

  const pct = Math.min(100, (t.savings / t.target_amount) * 100).toFixed(0);
  document.getElementById("savings-progress-fill").style.width = `${pct}%`;
  document.getElementById("savings-progress-text").textContent = `${pct}% completed`;

  const dueDate = new Date(t.due_date);
  const daysLeft = Math.ceil((dueDate - new Date()) / (1000 * 60 * 60 * 24));
  if (daysLeft <= 5 && daysLeft >= 0) {
    document.getElementById("alert-title").textContent = t.title;
    document.getElementById("alert-days").textContent = daysLeft;
    document.getElementById("deadline-alert").style.display = "block";
  }
}
