// Form Elements
const signInForm = document.getElementById("sign-in-form");
const signUpForm = document.getElementById("sign-up-form");
const forgotForm = document.getElementById("forgot-form");

// Track current form type
let currentFormType = "";

// Create modals dynamically (won't affect your CSS)
function createModals() {
  // Captcha Modal
  const captchaModal = document.createElement('div');
  captchaModal.id = 'captchaModal';
  captchaModal.className = 'modal';
  captchaModal.innerHTML = `
    <div class="modal-content">
      <h3>Please verify you're human</h3>
      <p id="captcha-question">Loading captcha...</p>
      <input type="text" id="captcha-answer" placeholder="Your answer" />
      <div class="modal-buttons">
        <button id="verifyCaptchaBtn">Verify</button>
      </div>
    </div>
  `;
  
  // OTP Modal
  const otpModal = document.createElement('div');
  otpModal.id = 'otpModal';
  otpModal.className = 'modal';
  otpModal.innerHTML = `
    <div class="modal-content">
      <h3>Enter OTP sent to your email</h3>
      <input type="text" id="otpInput" placeholder="Enter OTP" />
      <div class="modal-buttons">
        <button id="verifyOtpBtn">Verify OTP</button>
      </div>
    </div>
  `;
  
  document.body.appendChild(captchaModal);
  document.body.appendChild(otpModal);
}

// Generate simple math captcha
function generateCaptcha() {
  const num1 = Math.floor(Math.random() * 10);
  const num2 = Math.floor(Math.random() * 10);
  document.getElementById("captcha-question").textContent = `What is ${num1} + ${num2}?`;
  return num1 + num2;
}

// Show captcha modal
function showCaptchaModal(formType) {
  currentFormType = formType;
  const correctAnswer = generateCaptcha();
  document.getElementById("captchaModal").style.display = 'flex';
  document.getElementById("verifyCaptchaBtn").dataset.answer = correctAnswer;
}

// Show OTP modal
function showOtpModal() {
  document.getElementById("captchaModal").style.display = 'none';
  document.getElementById("otpModal").style.display = 'flex';
}

// Form switching (your existing code)
document.querySelectorAll("#show-signup").forEach(el =>
  el.addEventListener("click", (e) => {
    e.preventDefault();
    signInForm.classList.remove("active");
    forgotForm.classList.remove("active");
    signUpForm.classList.add("active");
  })
);

document.querySelectorAll("#show-signin").forEach(el =>
  el.addEventListener("click", (e) => {
    e.preventDefault();
    signUpForm.classList.remove("active");
    forgotForm.classList.remove("active");
    signInForm.classList.add("active");
  })
);

document.querySelectorAll("#show-forgot").forEach(el =>
  el.addEventListener("click", (e) => {
    e.preventDefault();
    signInForm.classList.remove("active");
    signUpForm.classList.remove("active");
    forgotForm.classList.add("active");
  })
);

document.getElementById("back-to-signin").addEventListener("click", (e) => {
  e.preventDefault();
  forgotForm.classList.remove("active");
  signInForm.classList.add("active");
});

// Form submissions with captcha
signInForm.addEventListener("submit", (e) => {
  e.preventDefault();
  showCaptchaModal("signin");
});

signUpForm.addEventListener("submit", (e) => {
  e.preventDefault();
  showCaptchaModal("signup");
});

forgotForm.addEventListener("submit", (e) => {
  e.preventDefault();
  showCaptchaModal("forgot");
});

// Captcha verification
document.addEventListener('click', (e) => {
  if (e.target.id === 'verifyCaptchaBtn') {
    const userAnswer = parseInt(document.getElementById("captcha-answer").value);
    const correctAnswer = parseInt(e.target.dataset.answer);
    
    if (userAnswer === correctAnswer) {
      if (currentFormType === "signin") {
        alert("Login successful!");
        document.getElementById("captchaModal").style.display = 'none';
      } else {
        showOtpModal();
      }
    } else {
      alert("Incorrect captcha. Try again.");
      generateCaptcha();
    }
  }
  
  if (e.target.id === 'verifyOtpBtn') {
    const otp = document.getElementById("otpInput").value;
    // Mock verification - in real app you'd check with server
    if (otp === "123456") {
      document.getElementById("otpModal").style.display = 'none';
      alert(currentFormType === "signup" ? "Signup successful!" : "Password reset email sent!");
      signInForm.classList.add("active");
      signUpForm.classList.remove("active");
      forgotForm.classList.remove("active");
    } else {
      alert("Invalid OTP. Try again.");
    }
  }
});
// ... (keep all existing form switching code)

// Forgot Password Submission
document.getElementById("forgot-form").addEventListener("submit", function(e) {
  e.preventDefault();
  
  // Validate passwords match
  const newPass = document.getElementById("new-password").value;
  const confirmPass = document.getElementById("confirm-new-password").value;
  
  if (newPass !== confirmPass) {
    alert("Passwords don't match!");
    return;
  }
  
  // Show captcha first
  currentFormType = "forgot";
  showCaptchaModal();
});

// Modified Captcha Verification
function verifyCaptcha() {
  const userAnswer = parseInt(document.getElementById("captcha-answer").value);
  const correctAnswer = parseInt(document.getElementById("verifyCaptchaBtn").dataset.answer);
  
  if (userAnswer === correctAnswer) {
    document.getElementById("captchaModal").style.display = 'none';
    
    if (currentFormType === "forgot") {
      // For forgot password, show OTP after captcha
      showOtpModal();
    } else if (currentFormType === "signin") {
      handleLogin();
    }
  } else {
    alert("Incorrect captcha. Try again.");
    generateCaptcha();
  }
}

// Modified OTP Verification
function verifyOtp() {
  const otp = document.getElementById("otpInput").value;
  
  // Mock verification - in real app you'd check with server
  if (otp === "123456") {
    document.getElementById("otpModal").style.display = 'none';
    
    if (currentFormType === "forgot") {
      // Get form values
      const username = document.getElementById("forgot-username").value;
      const newPassword = document.getElementById("new-password").value;
      
      // In real app, you would send this to your server
      console.log("Password reset for:", username, "New password:", newPassword);
      
      alert("Password reset successful!");
      signInForm.classList.add("active");
      forgotForm.classList.remove("active");
    }
  } else {
    alert("Invalid OTP. Try again.");
  }
}

// Update event listeners
document.getElementById("verifyCaptchaBtn").addEventListener("click", verifyCaptcha);
document.getElementById("verifyOtpBtn").addEventListener("click", verifyOtp);

// Helper function to show OTP modal
function showOtpModal() {
  // In real app, you would send OTP to email here
  console.log("Sending OTP to email...");
  document.getElementById("captchaModal").style.display = 'none';
  document.getElementById("otpModal").style.display = 'flex';
  document.getElementById("otpInput").value = ""; // Clear previous input
}
// Initialize modals when page loads
createModals();
