document.getElementById('feedback-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        feedback: document.getElementById('feedback').value
    };

    try {
        const response = await fetch('/submit-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);
            document.getElementById('feedback-form').reset(); // Clear form fields
        } else {
            const errorData = await response.json();
            alert('Error submitting feedback: ' + errorData.message);
        }
    } catch (error) {
        console.error('Error connecting to the server:', error);
        alert('Error connecting to the server.');
    }
});
