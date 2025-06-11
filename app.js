const signInForm = document.getElementById("sign-in-form");
const signUpForm = document.getElementById("sign-up-form");
const forgotForm = document.getElementById("forgot-form");

// Handle all "Sign Up" links
document.querySelectorAll("#show-signup").forEach(el =>
  el.addEventListener("click", () => {
    signInForm.classList.remove("active");
    forgotForm.classList.remove("active");
    signUpForm.classList.add("active");
  })
);

// Handle all "Sign In" links
document.querySelectorAll("#show-signin").forEach(el =>
  el.addEventListener("click", () => {
    signUpForm.classList.remove("active");
    forgotForm.classList.remove("active");
    signInForm.classList.add("active");
  })
);

// Handle all "Forgot Password" links
document.querySelectorAll("#show-forgot").forEach(el =>
  el.addEventListener("click", () => {
    signInForm.classList.remove("active");
    signUpForm.classList.remove("active");
    forgotForm.classList.add("active");
  })
);

// Back to Sign In (only one ID)
document.getElementById("back-to-signin").addEventListener("click", () => {
  forgotForm.classList.remove("active");
  signInForm.classList.add("active");
});

    
