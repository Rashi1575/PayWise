const signInForm = document.getElementById("sign-in-form");
const signUpForm = document.getElementById("sign-up-form");
const forgotForm = document.getElementById("forgot-form");

document.getElementById("show-signup").addEventListener("click", () => {
  signInForm.classList.remove("active");
  forgotForm.classList.remove("active");
  signUpForm.classList.add("active");
});

document.getElementById("show-signin").addEventListener("click", () => {
  signUpForm.classList.remove("active");
  forgotForm.classList.remove("active");
  signInForm.classList.add("active");
});

document.getElementById("show-forgot").addEventListener("click", () => {
  signInForm.classList.remove("active");
  signUpForm.classList.remove("active");
  forgotForm.classList.add("active");
});

document.getElementById("back-to-signin").addEventListener("click", () => {
  forgotForm.classList.remove("active");
  signInForm.classList.add("active");
});
    