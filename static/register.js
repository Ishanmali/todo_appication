document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("Registration");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("password2");
  const errorMessage = document.getElementById("error-message");

  form.addEventListener("submit", function (e) {
      if (password.value !== confirmPassword.value) {
          e.preventDefault();
          errorMessage.style.display = "block";
      } else {
          errorMessage.style.display = "none";
      }

      if (password.value.length < 5) {
          e.preventDefault();
          alert('Password must be at least 5 characters long');
      }
  });
});





