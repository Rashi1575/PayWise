document.addEventListener("DOMContentLoaded", () => {
  // Form Elements
  const signInForm = document.getElementById("sign-in-form");
  const signUpForm = document.getElementById("sign-up-form");
  const forgotForm = document.getElementById("forgot-form");
  let currentFormType = "";
  let forgotEmail = "";

  // Create CAPTCHA & OTP modals
  function createModals() {
    const captchaModal = document.createElement('div');
    captchaModal.id = 'captchaModal';
    captchaModal.className = 'modal';
    captchaModal.style.display = 'none';
    captchaModal.innerHTML = `
      <div class="modal-content">
        <h3>Verify you're human</h3>
        <p id="captcha-question">Loading...</p>
        <input type="text" id="captcha-answer" placeholder="Answer" />
        <div class="modal-buttons">
          <button id="verifyCaptchaBtn">Verify</button>
        </div>
      </div>`;

    const otpModal = document.createElement('div');
    otpModal.id = 'otpModal';
    otpModal.className = 'modal';
    otpModal.style.display = 'none';
    otpModal.innerHTML = `
      <div class="modal-content">
        <h3>Enter OTP</h3>
        <input type="text" id="otpInput" placeholder="Enter OTP" />
        <div class="modal-buttons">
          <button id="verifyOtpBtn">Verify OTP</button>
        </div>
      </div>`;

    document.body.appendChild(captchaModal);
    document.body.appendChild(otpModal);
  }

  function generateCaptcha() {
    const num1 = Math.floor(Math.random() * 50) + 1;
    const num2 = Math.floor(Math.random() * 50) + 1;
    const operator = Math.random() > 0.5 ? '+' : '-';
    const answer = operator === '+' ? num1 + num2 : num1 - num2;
    const question = `What is ${num1} ${operator} ${num2}?`;
    document.getElementById("captcha-question").textContent = question;
    return answer;
  }

  function showCaptchaModal(formType) {
    currentFormType = formType;
    const answer = generateCaptcha();
    document.getElementById("captchaModal").style.display = "flex";
    document.getElementById("verifyCaptchaBtn").dataset.answer = answer;
  }

  function verifyCaptcha() {
    const userAnswer = parseInt(document.getElementById("captcha-answer").value);
    const correctAnswer = parseInt(document.getElementById("verifyCaptchaBtn").dataset.answer);
    if (userAnswer === correctAnswer) {
      document.getElementById("captchaModal").style.display = "none";
      if (currentFormType === "signin") {
        handleLogin();
      } else {
        sendOtp();
      }
    } else {
      alert("❌ Incorrect captcha. Try again.");
      generateCaptcha();
    }
  }

  function switchForm(form) {
    signInForm.classList.remove("active");
    signUpForm.classList.remove("active");
    forgotForm.classList.remove("active");
    if (form === 'signin') signInForm.classList.add("active");
    if (form === 'signup') signUpForm.classList.add("active");
    if (form === 'forgot') forgotForm.classList.add("active");
  }

  async function sendOtp() {
    let email = "";

    if (currentFormType === "signup") {
      email = document.getElementById("signup-email").value;
    } else if (currentFormType === "forgot") {
      const username = document.getElementById("forgot-username").value;

      // Get email from backend
      const res = await fetch("http://localhost:5000/get-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username }),
      });

      const result = await res.json();
      if (!result.success) return alert("Email not found for this username.");
      email = result.email;
      forgotEmail = email;
    }

    const response = await fetch("http://localhost:5000/send-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    const data = await response.json();
    if (data.success) {
      document.getElementById("otpModal").style.display = 'flex';
      document.getElementById("otpInput").value = '';
    } else {
      alert("Failed to send OTP: " + data.message);
    }
  }

  async function verifyOtp() {
    const otp = document.getElementById("otpInput").value;
    let email = currentFormType === "signup"
      ? document.getElementById("signup-email").value
      : forgotEmail;

    if (!email) {
      alert("Email missing. Try again.");
      return;
    }

    const response = await fetch("http://localhost:5000/verify-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, otp }),
    });

    const data = await response.json();
    if (data.success) {
      document.getElementById("otpModal").style.display = "none";

      if (currentFormType === "signup") {
        sendSignupRequest();
      } else if (currentFormType === "forgot") {
        sendForgotPasswordRequest(otp);
      }
    } else {
      alert("Invalid OTP. Try again.");
    }
  }

  async function sendSignupRequest() {
    const username = document.getElementById("signup-username").value;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;
    const confirm = document.getElementById("signup-confirm-password").value;

    const res = await fetch("http://localhost:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, confirm_password: confirm }),
    });

    const data = await res.json();
    if (data.success) {
      alert("Signup successful!");
      switchForm("signin");
    } else {
      alert("Signup failed: " + data.error);
    }
  }

  async function sendForgotPasswordRequest(otp) {
    const username = document.getElementById("forgot-username").value;
    const newPass = document.getElementById("new-password").value;
    const confirmPass = document.getElementById("confirm-new-password").value;

    const res = await fetch("http://localhost:5000/forgot-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        new_password: newPass,
        confirm_password: confirmPass,
        otp
      }),
    });

    const data = await res.json();
    if (data.success) {
      alert("Password reset successful!");
      switchForm("signin");
    } else {
      alert("Reset failed: " + data.error);
    }
  }

  async function handleLogin() {
    const username = document.getElementById("signin-username").value;
    const password = document.getElementById("signin-password").value;

    const res = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    if (data.success) {
      alert("Login successful!");
      localStorage.setItem("loggedIn", true);
      localStorage.setItem("username", username);
      window.location.href = "dashb.html";
    } else {
      alert("Login failed: " + data.error);
    }
  }

  // Initial setup
  createModals();
  switchForm("signin");

  // Event bindings
  document.querySelectorAll("#show-signup").forEach(el => el.addEventListener("click", () => switchForm("signup")));
  document.querySelectorAll("#show-signin").forEach(el => el.addEventListener("click", () => switchForm("signin")));
  document.querySelectorAll("#show-forgot").forEach(el => el.addEventListener("click", () => switchForm("forgot")));
  document.getElementById("back-to-signin").addEventListener("click", () => switchForm("signin"));

  signInForm.addEventListener("submit", e => { e.preventDefault(); showCaptchaModal("signin"); });
  signUpForm.addEventListener("submit", e => { e.preventDefault(); showCaptchaModal("signup"); });
  forgotForm.addEventListener("submit", e => {
    e.preventDefault();
    const pass = document.getElementById("new-password").value;
    const confirm = document.getElementById("confirm-new-password").value;
    if (pass !== confirm) return alert("Passwords don't match.");
    showCaptchaModal("forgot");
  });

  document.addEventListener("click", e => {
    if (e.target.id === "verifyCaptchaBtn") verifyCaptcha();
    if (e.target.id === "verifyOtpBtn") verifyOtp();
  });
});



