document.addEventListener('DOMContentLoaded', function() {
    const signInForm = document.getElementById('sign-in-form');
    const signUpForm = document.getElementById('sign-up-form');
    const showSignUpLink = document.getElementById('show-sign-up');
    const showSignInLink = document.getElementById('show-sign-in');

    // Handle showing the Sign Up form
    showSignUpLink.addEventListener('click', function() {
        signInForm.classList.remove('active');
        signUpForm.classList.add('active');
    });

    // Handle showing the Sign In form
    showSignInLink.addEventListener('click', function() {
        signUpForm.classList.remove('active');
        signInForm.classList.add('active');
    });

    // Handle Sign In form submission
    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        // Implement sign-in logic here
        console.log('Sign In:', username, password);
        // You can send credentials to your server or perform other actions
    });

    // Handle Sign Up form submission
    document.getElementById('signup-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('signup-username').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        // Implement sign-up logic here
        console.log('Sign Up:', username, email, password);
        // You can send credentials to your server or perform other actions
    });
});