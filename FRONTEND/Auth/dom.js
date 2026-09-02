const form = document.querySelector('.form');
const username= document.querySelector('#username');
const email = document.querySelector('#email');
const password = document.querySelector('#password');
const confirmPassword = document.querySelector('#passwordTwo');

form.addEventListener("submit", (event)=>{
   event.preventDefault();
   checkInputsSubmitted();
});
   
function checkInputsSubmitted (){
   const usernameValue = username.value.trim()
   const emailValue = email.value.trim();
   const passwordValue = password.value;
   const password2Value = confirmPassword.value;

   let isValid = true;

   if(usernameValue === "") {
      setError(username, "Username is required");
      isValid = false;
   }else if(usernameValue.length < 5){
      setError(username, "The minimum username length is 5");
      isValid = false;
   }else {
      setSuccess(username);
   }

   if (emailValue === "") {
      setError(email, "Email is required");
      isValid = false;
   } else if(!emailValue.includes("@")) {
      setError(email, "Enter a valid email address")
      isValid = false;
   } else{
      setSuccess(email)
   }

   if (passwordValue === "") {
      setError(password, "Password is required")
      isValid = false;
   } else if(passwordValue.length < 6){
      setError(password, "The minimum password length is 6")
      isValid = false;
   } else if(passwordValue === "password") {
      setError(password, 'The word "password" cannot be used')
      isValid = false;
   } else {
      setSuccess(password)
   }

   if (password2Value === "") {
      setError(confirmPassword, "Confirm Password is required");
      isValid = false;
   } else if (passwordValue !== password2Value) {
      setError(confirmPassword, "Password and Confirm Password must be equal")
      isValid = false;
   } else{
      setSuccess(confirmPassword)
   }
   // return isValid;

  if (isValid) {
    submitForm({ usernameValue, emailValue, passwordValue, password2Value  });
  }
}

function setError(input, errorMessage) {
   const formControl = input.parentElement;
   const small = formControl.querySelector('small');
   formControl.className = "form-control error";
   small.textContent = errorMessage;
}
function setSuccess(input) {
   const formControl = input.parentElement;
   formControl.className = "form-control success";  
}
function submitForm(data) {
  console.log('✅ All fields valid, submitting form...');
      alert("Account created successfully!");
     form.reset();
}
   
   


   
   
   
   
