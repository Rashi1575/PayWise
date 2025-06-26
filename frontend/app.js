// ====== Form Elements ======
const signInForm = document.getElementById("sign-in-form");
const signUpForm = document.getElementById("sign-up-form");
const forgotForm = document.getElementById("forgot-form");

let currentFormType = "";
let forgotEmail = "";

// ====== Modal Creation (if not already present) ======
function createModals() {
  if (!document.getElementById("captchaModal")) {
    const captchaModal = document.createElement('div');
    captchaModal.id = 'captchaModal';
    captchaModal.className = 'modal';
    captchaModal.style.display = 'none';
    captchaModal.innerHTML = `
      <div class="modal-content">
        <h2>Please verify you're human</h2>
        <p id="captcha-question">Loading captcha...</p>
        <input type="text" id="captcha-answer" placeholder="Your answer" />
        <button id="verifyCaptchaBtn">Verify</button>
      </div>
    `;
    document.body.appendChild(captchaModal);
  }

  if (!document.getElementById("otpModal")) {
    const otpModal = document.createElement('div');
    otpModal.id = 'otpModal';
    otpModal.className = 'modal';
    otpModal.style.display = 'none';
    otpModal.innerHTML = `
      <div class="modal-content">
        <h2>Enter OTP sent to your email</h2>
        <input type="text" id="otp-input" placeholder="Enter OTP" />
        <button id="verifyOtpBtn">Verify OTP</button>
      </div>
    `;
    document.body.appendChild(otpModal);
  }
}
createModals();

// ====== Captcha Logic ======
function generateCaptcha() {
  const num1 = Math.floor(Math.random() * 10);
  const num2 = Math.floor(Math.random() * 10);
  document.getElementById("captcha-question").textContent = `What is ${num1} + ${num2}?`;
  return num1 + num2;
}

function showCaptchaModal(formType) {
  currentFormType = formType;
  const answer = generateCaptcha();
  document.getElementById("captchaModal").style.display = "flex";
  document.getElementById("verifyCaptchaBtn").dataset.answer = answer;
}

document.getElementById("verifyCaptchaBtn").addEventListener("click", () => {
  const userAns = parseInt(document.getElementById("captcha-answer").value.trim());
  const correctAns = parseInt(document.getElementById("verifyCaptchaBtn").dataset.answer);
  if (userAns === correctAns) {
    document.getElementById("captchaModal").style.display = "none";
    showOtpModal();
  } else {
    alert("Incorrect captcha. Try again.");
  }
});

// ====== Form Switching ======
function hideAllForms() {
  signInForm.classList.remove("active");
  signUpForm.classList.remove("active");
  forgotForm.classList.remove("active");
}

function switchForm(type) {
  hideAllForms();
  if (type === "signin") signInForm.classList.add("active");
  else if (type === "signup") signUpForm.classList.add("active");
  else if (type === "forgot") forgotForm.classList.add("active");
}

document.querySelectorAll("#show-signin").forEach(el => el.addEventListener("click", () => switchForm("signin")));
document.querySelectorAll("#show-signup").forEach(el => el.addEventListener("click", () => switchForm("signup")));
document.querySelectorAll("#show-forgot").forEach(el => el.addEventListener("click", () => switchForm("forgot")));
document.getElementById("back-to-signin").addEventListener("click", () => switchForm("signin"));

// ====== Form Submission Events ======
signInForm.addEventListener("submit", e => {
  e.preventDefault();
  showCaptchaModal("signin");
});

signUpForm.addEventListener("submit", e => {
  e.preventDefault();
  showCaptchaModal("signup");
});

forgotForm.addEventListener("submit", e => {
  e.preventDefault();
  const newPass = document.getElementById("new-password").value;
  const confirmPass = document.getElementById("confirm-new-password").value;
  if (newPass !== confirmPass) {
    alert("Passwords do not match!");
    return;
  }
  showCaptchaModal("forgot");
});

// ====== OTP Flow ======
async function showOtpModal() {
  let email = "";

  if (currentFormType === "signup") {
    email = document.getElementById("signup-email").value;
  } else if (currentFormType === "forgot") {
    const username = document.getElementById("forgot-username").value;
    const result = await fetch("http://localhost:5000/get-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });
    const res = await result.json();
    if (!res.success) {
      alert("Email not found for this username.");
      return;
    }
    email = res.email;
    forgotEmail = email;
  } else {
    const username = document.getElementById("signin-username").value;
    const result = await fetch("http://localhost:5000/get-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });
    const res = await result.json();
    if (!res.success) {
      alert("Email not found for this username.");
      return;
    }
    email = res.email;
  }

  // Send OTP
  const otpRes = await fetch("http://localhost:5000/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  });
  const otpResult = await otpRes.json();

  if (!otpResult.success) {
    alert("Failed to send OTP. Try again later.");
    return;
  }

  document.getElementById("otpModal").style.display = "flex";
}

// OTP Verify
document.getElementById("verifyOtpBtn").addEventListener("click", async () => {
  const otp = document.getElementById("otp-input").value;

  const email = currentFormType === "forgot" ? forgotEmail : document.getElementById("signup-email").value || (await getEmailForUsername());

  const verifyRes = await fetch("http://localhost:5000/verify-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, otp })
  });
  const verifyResult = await verifyRes.json();

  if (!verifyResult.success) {
    alert("Invalid OTP. Try again.");
    return;
  }

  document.getElementById("otpModal").style.display = "none";

  if (currentFormType === "signup") {
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;
    const confirmPass = document.getElementById("signup-confirm-password").value;

    if (password !== confirmPass) {
      alert("Passwords do not match.");
      return;
    }

    const res = await fetch("http://localhost:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });
    const result = await res.json();
    alert(result.message || "Signup complete!");
    if (result.success) switchForm("signin");

  } else if (currentFormType === "signin") {
    const username = document.getElementById("signin-username").value;
    const password = document.getElementById("signin-password").value;

    const res = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const result = await res.json();

    if (result.success) {
      alert("Login successful!");
      localStorage.setItem("username", username);
      window.location.href = "dashboard.html";
    } else {
      alert(result.message || "Login failed.");
    }

  } else if (currentFormType === "forgot") {
    const username = document.getElementById("forgot-username").value;
    const newPassword = document.getElementById("new-password").value;

    const res = await fetch("http://localhost:5000/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, new_password: newPassword })
    });

    const result = await res.json();
    alert(result.message || "Password reset complete.");
    if (result.success) switchForm("signin");
  }
});

// Helper to get email for login
async function getEmailForUsername() {
  const username = document.getElementById("signin-username").value;
  const result = await fetch("http://localhost:5000/get-email", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });
  const res = await result.json();
  return res.email;
}
