ocument.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim(); // Trim whitespace
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    try {
        // Send login data to Flask backend
        const response = await fetch('/login', { // Update URL if hosted
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                // Redirect to fleeb on successful login
                window.location.href = '/fleeb'; 
            } else {
                // Show error message from server
                errorMessage.textContent = result.message || 'Invalid username or password.';
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
