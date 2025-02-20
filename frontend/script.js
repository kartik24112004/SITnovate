document.addEventListener("DOMContentLoaded", function () {
<<<<<<< HEAD
    let checkButton = document.getElementById("checkSpamButton");
    let emailInput = document.getElementById("emailField");

    if (!checkButton || !emailInput) {
        console.error("Button or input field not found!");
        return;
    }

    checkButton.addEventListener("click", function () {
        console.log("Button clicked!");
        let emailText = emailInput.value.trim(); // Get input value

        // Check if input is empty
        if (!emailText) {
=======
    document.getElementById('checkSpamButton').addEventListener('click', function () {
        const emailText = document.getElementById('emailInput').value;

        // Check if input is empty
        if (!emailText.trim()) {
>>>>>>> 7ae3501e94362588c93b4434b2de01389d6f7b5c
            showError("Please enter an email before checking.");
            return;
        }

<<<<<<< HEAD
        fetch("http://127.0.0.1:5000/predict", { // Make sure backend is running
            method: "POST",
            headers: {
                "Content-Type": "application/json"
=======
        fetch('http://127.0.0.1:5000/predict', {  // Make sure backend is running
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
>>>>>>> 7ae3501e94362588c93b4434b2de01389d6f7b5c
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
<<<<<<< HEAD
            console.error("Error:", error);
=======
            console.error('Error:', error);
>>>>>>> 7ae3501e94362588c93b4434b2de01389d6f7b5c
            showError("Error connecting to the server. Make sure the backend is running.");
        });
    });
});

// Function to display the result
function showResult(prediction) {
<<<<<<< HEAD
    const resultDiv = document.getElementById("result");
    if (resultDiv) {
        resultDiv.innerHTML = `Prediction: <strong>${prediction}</strong>`;
        resultDiv.style.color = "green";
        resultDiv.style.display = "block";
    } else {
        console.error("Result div not found!");
    }
=======
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `✅ Prediction: <strong>${prediction}</strong>`;
    resultDiv.style.color = 'green';
    resultDiv.style.display = 'block';
>>>>>>> 7ae3501e94362588c93b4434b2de01389d6f7b5c
}

// Function to display errors
function showError(message) {
<<<<<<< HEAD
    const resultDiv = document.getElementById("result");
    if (resultDiv) {
        resultDiv.innerHTML = `${message}`;
        resultDiv.style.color = "red";
        resultDiv.style.display = "block";
    } else {
        console.error("Result div not found!");
    }
=======
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `❌ ${message}`;
    resultDiv.style.color = 'red';
    resultDiv.style.display = 'block';
>>>>>>> 7ae3501e94362588c93b4434b2de01389d6f7b5c
}
