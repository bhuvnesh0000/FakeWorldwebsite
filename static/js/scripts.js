document.getElementById('upload-form').onsubmit = async function(event) {
    event.preventDefault();

    // Show the loading message
    document.getElementById('message').innerText = 'Processing your file...';

    // Prepare form data and send the file to the Flask backend
    const formData = new FormData(this);
    const response = await fetch('/generate', {
        method: 'POST',
        body: formData
    });

    // Handle the response from Flask
    if (response.ok) {
        const jsonResponse = await response.json();
        // Display the download link for the synthetic data CSV
        document.getElementById('message').innerHTML = `
            Synthetic data generated! 
            <a href="${jsonResponse.url}" class="btn btn-success" download>Download CSV</a>
        `;
    } else {
        document.getElementById('message').innerText = 'Error generating synthetic data. Please try again.';
    }
};

const text = "Data Is The Need Of Upcoming Future...";
const typewriterDiv = document.getElementById("typewriter");

let i = 0;
function typeWriter() {
    if (i < text.length) {
        typewriterDiv.innerHTML += text.charAt(i);
        i++;
        setTimeout(typeWriter, 200); 
    }
}

typeWriter(); 
