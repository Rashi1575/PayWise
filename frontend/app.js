// Get Form Elements
const signInForm = document.getElementById("sign-in-form");
const signUpForm = document.getElementById("sign-up-form");
const forgotForm = document.getElementById("forgot-form");
let forgotEmail = "";  // Store email used in forgot flow

let currentFormType = "";

// Dynamically create modals on page load
function createModals() {
  const captchaModal = document.createElement('div');
  captchaModal.id = 'captchaModal';
  captchaModal.className = 'modal';
  captchaModal.style.display = 'none';
  captchaModal.innerHTML = `
    <div class="modal-content">
      <h3>Please verify you're human</h3>
      <p id="captcha-question">Loading captcha...</p>
      <input type="text" id="captcha-answer" placeholder="Your answer" />
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
      <h3>Enter OTP sent to your email</h3>
      <input type="text" id="otpInput" placeholder="Enter OTP" />
      <div class="modal-buttons">
        <button id="verifyOtpBtn">Verify OTP</button>
      </div>
    </div>`;

  document.body.appendChild(captchaModal);
  document.body.appendChild(otpModal);
}

function generateCaptcha() {
  const num1 = Math.floor(Math.random() * 100) + 1;
  const num2 = Math.floor(Math.random() * 100) + 1;
  const operators = ["+", "-"];
  const operator = operators[Math.floor(Math.random() * operators.length)];

  let question;
  let answer;

  switch (operator) {
    case "+":
      answer = num1 + num2;
      question = `What is ${num1} + ${num2}?`;
      break;
    case "-":
      answer = num1 - num2;
      question = `What is ${num1} - ${num2}?`;
      break;
  }

  document.getElementById("captcha-question").textContent = question;
  return answer;
}



function showCaptchaModal(formType) {
  currentFormType = formType;
  const answer = generateCaptcha();
  document.getElementById("captchaModal").style.display = 'flex';
  document.getElementById("verifyCaptchaBtn").dataset.answer = answer;
}



function hideAllForms() {
  signInForm.classList.remove("active");
  signUpForm.classList.remove("active");
  forgotForm.classList.remove("active");
}

// Form Switching
function switchForm(form) {
  hideAllForms();
  if (form === 'signin') signInForm.classList.add("active");
  if (form === 'signup') signUpForm.classList.add("active");
  if (form === 'forgot') forgotForm.classList.add("active");
}

document.querySelectorAll("#show-signup").forEach(el => el.addEventListener("click", () => switchForm('signup')));
document.querySelectorAll("#show-signin").forEach(el => el.addEventListener("click", () => switchForm('signin')));
document.querySelectorAll("#show-forgot").forEach(el => el.addEventListener("click", () => switchForm('forgot')));
document.getElementById("back-to-signin").addEventListener("click", () => switchForm('signin'));

// Form Submissions
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
    alert("Passwords don't match!");
    return;
  }
  showCaptchaModal("forgot");
});

async function sendOtp() {
  let email = "";

  if (currentFormType === "signup") {
    email = document.getElementById("signup-email").value;
  } else if (currentFormType === "forgot") {
    email = prompt("Enter the email where OTP was sent:");
  }

  if (!email) {
    alert("Email is missing.");
    return;
  }

  const response = await fetch("http://localhost:5000/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  const data = await response.json();
  if (data.success) {
    document.getElementById("otpModal").style.display = 'flex';
    document.getElementById("otpInput").value = "";
  } else {
    alert("Failed to send OTP: " + data.message);
  }
}



async function sendSignupRequest() {
  const username = document.getElementById("signup-username").value;
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;
  const confirm_password = document.getElementById("signup-confirm-password").value;

  const response = await fetch("http://localhost:5000/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password, confirm_password }),
  });

  const data = await response.json();
  if (data.success) {
    alert("Signup successful! ");
    switchForm("signin"); // Move to login form
  } else {
    alert("Signup failed: " + data.error);
  }
}

async function handleLogin() {
  const username = document.getElementById("signin-username").value;
  const password = document.getElementById("signin-password").value;

  const response = await fetch("http://localhost:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();
  if (data.success) {
    alert("Login successful!");
    window.location.href = "dashb.html";  // ✅ redirect to dashboard
  } else {
    alert("Login failed: " + data.error);
  }
}

async function sendForgotPasswordRequest(otp) {
  const username = document.getElementById("forgot-username").value;
  const new_password = document.getElementById("new-password").value;
  const confirm_password = document.getElementById("confirm-new-password").value;

  const response = await fetch("http://localhost:5000/forgot-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, new_password, confirm_password, otp }), // ✅ include OTP here
  });

  const data = await response.json();
  if (data.success) {
    alert("Password reset successful!");
    switchForm("signin");
  } else {
    alert("Reset failed: " + data.error);
  }
}



async function showOtpModal() {
  let email = "";

  if (currentFormType === "signup") {
    email = document.getElementById("signup-email").value;
  } else if (currentFormType === "forgot") {
    const username = document.getElementById("forgot-username").value;

    // 🔥 Fetch email from backend using username
    const res = await fetch("http://localhost:5000/get-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    });

    const result = await res.json();
    if (!result.success) {
      alert("Email not found for this username.");
      return;
    }

    email = result.email;
    forgotEmail = email;  // ✅ Save it globally for OTP verification
  }

  const response = await fetch("http://localhost:5000/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  const data = await response.json();
  if (data.success) {
    document.getElementById("otpModal").style.display = 'flex';
    document.getElementById("otpInput").value = "";
    console.log("📬 OTP sent to:", email); // ✅ for debugging
  } else {
    alert("Failed to send OTP: " + data.message);
  }
}




// Captcha Verification
function verifyCaptcha() {
  const userAnswer = parseInt(document.getElementById("captcha-answer").value);
  const correctAnswer = parseInt(document.getElementById("verifyCaptchaBtn").dataset.answer);

  if (userAnswer === correctAnswer) {
    document.getElementById("captchaModal").style.display = 'none';

    if (currentFormType === "signin") {
      handleLogin();  // Sign in directly
    } else {
      sendOtp();  // 🔥 Only send OTP once, then open modal
    }
  } else {
    alert("Incorrect captcha. Try again.");
    generateCaptcha();
  }
}


async function verifyOtp() {
  const otp = document.getElementById("otpInput").value;
  let email = "";

  if (currentFormType === "signup") {
    email = document.getElementById("signup-email").value;
  } else if (currentFormType === "forgot") {
    email = forgotEmail; // 🔥 Comes from showOtpModal() when OTP was sent
  }

  console.log("📤 VERIFY OTP FOR:", email, "OTP:", otp);

  const response = await fetch("http://localhost:5000/verify-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, otp }),
  });

  const data = await response.json();
  if (data.success) {
    document.getElementById("otpModal").style.display = 'none';

    if (currentFormType === "signup") {
      await sendSignupRequest();
      window.location.href = "dashb.html";  // ✅ redirect after signup
    } else if (currentFormType === "forgot") {
      await sendForgotPasswordRequest(otp);
    }
  } else {
    alert("❌ Invalid OTP. Try again.");
  }
}



// Call once when the page loads
createModals();
document.addEventListener("click", (e) => {
  if (e.target.id === "verifyCaptchaBtn") verifyCaptcha();
  if (e.target.id === "verifyOtpBtn") verifyOtp();
});

switchForm('signin'); // Show signin form by default


