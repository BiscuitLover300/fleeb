document.getElementById('signupForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim(); // Trim whitespace
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const errorMessage = document.getElementById('error-message');

    // Ensure passwords match
    if (password !== confirmPassword) {
        errorMessage.textContent = 'Passwords do not match. Please try again.';
        return;
    }

    try {
        // Send signup data to Flask backend
        const response = await fetch('http://127.0.0.1:5000/signup', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                // Redirect to login page on success
                window.location.href = '/login';
            } else {
                // Show error message from server
                errorMessage.textContent = result.message;
            }
        } else {
            // Generic server error message
            errorMessage.textContent = 'Server error. Please try again later.';
        }
    } catch (error) {
        // Handle network or unexpected errors
        errorMessage.textContent = 'An error occurred. Please check your connection.';
        console.error('Error:', error);
    }
});
