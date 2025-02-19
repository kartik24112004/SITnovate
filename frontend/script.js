// Wait for the DOM to load before running the script
document.addEventListener("DOMContentLoaded", function () {
    // Get elements by ID
    const emailText = document.getElementById("emailText");
    const submitBtn = document.getElementById("submitBtn");
    const resultDiv = document.getElementById("result");

    // Add event listener to the button
    submitBtn.addEventListener("click", function () {
        let text = emailText.value.trim(); // Get the input text and trim spaces

        if (text === "") {
            resultDiv.innerHTML = "<p style='color: red;'>Please enter an email text!</p>";
            return;
        }

        // Dummy spam words list (for frontend testing only)
        let spamWords = ["win", "prize", "free", "money", "offer", "click", "subscribe"];

        // Check if input contains spam words
        let isSpam = spamWords.some(word => text.toLowerCase().includes(word));

        if (isSpam) {
            resultDiv.innerHTML = "<p style='color: red; font-weight: bold;'>🚨 This email looks like spam!</p>";
        } else {
            resultDiv.innerHTML = "<p style='color: green; font-weight: bold;'>✅ This email seems safe.</p>";
        }
    });
});
