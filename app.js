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

// Handle Signup Submission
document.getElementById("sign-up-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const inputs = e.target.querySelectorAll("input");
  const data = {
    username: inputs[0].value,
    email: inputs[1].value,
    password: inputs[2].value,
    confirm_password: inputs[2].value  // for now, assuming confirm = password
  };

  try {
    const response = await fetch("http://localhost:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    alert(result.message);
  } catch (err) {
    alert("Error during signup");
  }
});

// Handle Login Submission
document.getElementById("sign-in-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const inputs = e.target.querySelectorAll("input");
  const data = {
    username: inputs[0].value,
    password: inputs[1].value
  };

  try {
    const response = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    alert(result.message);
  } catch (err) {
    alert("Error during login");
  }
});
  