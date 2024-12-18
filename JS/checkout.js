document.getElementById('checkout-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    // Collect form data
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try { //Tries to catch data from database
        const response = await fetch('http://localhost:3000/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (response.ok) { //If response is okay, then order sucessful
            alert('Order submitted successfully!');
        } else { //Prints out error otherwise
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) { //Catches error 
        console.error('Error submitting form:', error);
        alert('Failed to submit the order. Please try again later.');
    }
});
