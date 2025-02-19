document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('checkSpamButton').addEventListener('click', function () {
        const emailText = document.getElementById('emailInput').value;

        // Check if input is empty
        if (!emailText.trim()) {
            showError("Please enter an email before checking.");
            return;
        }

        fetch('http://127.0.0.1:5000/predict', {  // Make sure backend is running
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: emailText })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            showResult(data.prediction);
        })
        .catch(error => {
            console.error('Error:', error);
            showError("Error connecting to the server. Make sure the backend is running.");
        });
    });
});

// Function to display the result
function showResult(prediction) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `✅ Prediction: <strong>${prediction}</strong>`;
    resultDiv.style.color = 'green';
    resultDiv.style.display = 'block';
}

// Function to display errors
function showError(message) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `❌ ${message}`;
    resultDiv.style.color = 'red';
    resultDiv.style.display = 'block';
}
